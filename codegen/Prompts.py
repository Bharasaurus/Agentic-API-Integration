from LLM_Integration import call_llm


def generate_code(endpoint, vectorstore, language: str = "java"):

    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    query = f"""
    Generate backend code for:
    Path: {endpoint['path']}
    Method: {endpoint['method']}
    Language: {language.upper()}
    """

    # retrieve contextual docs
    docs = retriever.get_relevant_documents(query)
    context = "\n\n".join([doc.page_content for doc in docs])

    # language-specific instructions
    if language.lower() == "python":
        lang_block = """**IMPORTANT: GENERATE PYTHON CODE ONLY. DO NOT GENERATE JAVA CODE.**

Target: FastAPI (Python 3.11+)
- Produce Pydantic models for requests/responses.
- Produce async route functions using APIRouter.
- Use `httpx` for HTTP clients and dependency injection for the client.
- Include `# File: <path>` markers before each file OR fenced ```python``` code blocks.
- Provide a `requirements.txt` and a minimal `app.py` startup snippet.
"""
    else:
        lang_block = """**IMPORTANT: GENERATE JAVA CODE ONLY. DO NOT GENERATE PYTHON CODE.**

Target: Spring Boot (Java 17)
- Produce Controllers, DTOs, Service and WebClient configuration.
- Include `// File: <path>` markers before each file OR fenced ```java``` blocks.
"""

    prompt = f"""{lang_block}
Use the following coding standards and templates:
{context}

Now generate production-ready {language.upper()} code for this endpoint ONLY.
Do NOT include code in any other language.

Endpoint:
Path: {endpoint['path']}
Method: {endpoint['method']}
RequestBody: {endpoint['requestBody']}
Responses: {endpoint['responses']}

Requirements:
- Proper validation and type hints
- Error handling and sensible HTTP status mapping
- Clear filenames (use `# File:` or `// File:` markers)
- {language.upper()} code ONLY
"""

    return call_llm(prompt)
