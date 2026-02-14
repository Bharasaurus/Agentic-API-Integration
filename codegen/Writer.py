import re
import hashlib
from pathlib import Path

EXPECTED_FILES = {
    "WebClientConfig.java",
    "UserServiceClient.java",
    "UserServiceDto.java",
}

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
            # ensure extension matches language
            if language.lower() == "python" and not filename.lower().endswith(".py"):
                filename = filename + ".py"
            if language.lower() == "java" and not filename.lower().endswith(".java"):
                filename = filename + ".java"

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
