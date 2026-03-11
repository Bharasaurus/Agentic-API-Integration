import re
import hashlib
from pathlib import Path

EXPECTED_FILES = {
    "WebClientConfig.java",
    "UserServiceClient.java",
    "UserServiceDto.java",
}


def _strip_markdown_fences(content: str, language: str) -> str:
    """Remove markdown code fences (triple backticks) and language markers.
    
    Handles formats like:
    - ```python\ncode\n```
    - ```java\ncode\n```
    - ```\ncode\n```
    """
    # Remove opening fence with optional language tag
    content = re.sub(r'^```(?:python|java|py|js)?\s*\n?', '', content, flags=re.MULTILINE)
    # Remove closing fence
    content = re.sub(r'\n?```\s*$', '', content, flags=re.MULTILINE)
    return content.strip()


def write_java_files(llm_output: str, language: str = "java"):
    output_dir = Path("output/generated")
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1) Prefer explicit markers: support both Java and Python comment styles
    files = re.findall(
        r"(?:\/\/ File:|# File:)\s*(.+?)\n(.*?)(?=(?:\/\/ File:|# File:)|\Z)",
        llm_output,
        re.DOTALL,
    )

    generated = []

    if files:
        for filename, content in files:
            filename = filename.strip()
            # extract just the filename part (before any space or special char that looks like explanation)
            filename = filename.split()[0]  # take only the first token
            # sanitize: remove angle brackets, backticks, parentheses, and other invalid chars
            filename = re.sub(r'[<>:"|?*\(\)`]', '', filename).strip()
            
            if not filename:
                continue  # skip if filename became empty after sanitization
            
            # skip files with wrong extensions (e.g., .java files when generating python)
            if language.lower() == "python":
                if filename.lower().endswith(".java"):
                    continue  # skip Java files in Python mode
                if not filename.lower().endswith(".py"):
                    filename = filename + ".py"
            elif language.lower() == "java":
                if filename.lower().endswith(".py"):
                    # strip .py and add .java if it ends with .java.py
                    if filename.lower().endswith(".java.py"):
                        filename = filename[:-3]  # remove .py, keep .java
                    elif not filename.lower().endswith(".java"):
                        filename = filename + ".java"
                elif not filename.lower().endswith(".java"):
                    filename = filename + ".java"

            # strip markdown code fences if present
            content = _strip_markdown_fences(content, language)
            
            target = output_dir / filename
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content.strip(), encoding="utf-8")
            generated.append(str(target))

    else:
        # 2) Try to extract fenced code blocks and nearby filenames (language-aware)
        code_block_re = re.compile(r"```(?:java|python)?\n(.*?)\n```", re.DOTALL | re.IGNORECASE)
        matches = list(code_block_re.finditer(llm_output))

        for i, m in enumerate(matches):
            code = m.group(1).strip()
            # Remove any stray markdown fences that might be in the captured group
            code = _strip_markdown_fences(code, language)
            
            # Search backwards from the code block for a filename in backticks or plain path
            prefix = llm_output[max(0, m.start() - 300): m.start()]
            if language.lower() == "python":
                name_match = re.search(r"`([^`]+\.py)`", prefix)
                if not name_match:
                    name_match = re.search(r"([A-Za-z0-9_./\\-]+\.py)", prefix)
            else:
                name_match = re.search(r"`([^`]+\.java)`", prefix)
                if not name_match:
                    name_match = re.search(r"([A-Za-z0-9_./\\-]+\.java)", prefix)

            if name_match:
                filename = name_match.group(1).strip()
            else:
                # Try to infer a sensible filename from the code
                if language.lower() == "java":
                    class_match = re.search(r"public\s+class\s+([A-Za-z_][A-Za-z0-9_]*)", code)
                    if not class_match:
                        class_match = re.search(r"class\s+([A-Za-z_][A-Za-z0-9_]*)", code)
                    if class_match:
                        filename = f"{class_match.group(1)}.java"
                    else:
                        filename = f"Unlabeled/CodeBlock_{i+1}.java"
                else:
                    # python: look for first class or function
                    class_match = re.search(r"class\s+([A-Za-z_][A-Za-z0-9_]*)", code)
                    if class_match:
                        filename = f"{class_match.group(1)}.py"
                    else:
                        func_match = re.search(r"def\s+([A-Za-z_][A-Za-z0-9_]*)", code)
                        if func_match:
                            filename = f"{func_match.group(1)}.py"
                        else:
                            filename = f"Unlabeled/Python/CodeBlock_{i+1}.py"

            target = output_dir / filename
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(code, encoding="utf-8")
            generated.append(str(target))

    # If nothing was generated, write a fallback file containing the LLM output
    if not generated:
        short = hashlib.sha1(llm_output.encode()).hexdigest()[:8]
        if language.lower() == "python":
            fallback_name = f"LLM_output_{short}.py"
            content = "# " + "\n# ".join(llm_output.strip().splitlines())
        else:
            fallback_name = f"LLM_output_{short}.java"
            content = "/*\n" + llm_output.strip() + "\n*/"

        (output_dir / fallback_name).write_text(content, encoding="utf-8")
        print(f"No code blocks found — wrote full output to {output_dir / fallback_name}")
        return

    print("Generated files:")
    for p in sorted(generated):
        print(" -", p)
