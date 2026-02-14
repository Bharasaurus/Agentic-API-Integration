from LLM_Integration import call_llm


def generate_code(endpoint, vectorstore, language: str = "java"):

    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    query = f"""
    Generate backend code for:
    Path: {endpoint['path']}
    Method: {endpoint['method']}
    """

    # retrieve contextual docs
    docs = retriever.get_relevant_documents(query)
    context = "\n\n".join([doc.page_content for doc in docs])

    # language-specific instructions
    if language.lower() == "python":
        lang_block = """
Target: FastAPI (Python 3.11+)
- Produce Pydantic models for requests/responses.
- Produce async route functions using APIRouter.
- Use `httpx` for HTTP clients and dependency injection for the client.
- Include `# File: <path>` markers before each file OR fenced ```python``` code blocks.
- Provide a `requirements.txt` and a minimal `app.py` startup snippet.
"""
    else:
        lang_block = """
Target: Spring Boot (Java 17)
- Produce Controllers, DTOs, Service and WebClient configuration as before.
- Include `// File: <path>` markers before each file OR fenced ```java``` blocks.
"""

    prompt = f"""{lang_block}
Use the following coding standards and templates:
{context}

Now generate production-ready code for this endpoint.

Endpoint:
Path: {endpoint['path']}
Method: {endpoint['method']}
RequestBody: {endpoint['requestBody']}
Responses: {endpoint['responses']}

Requirements:
- Proper validation and type hints
- Error handling and sensible HTTP status mapping
- Clear filenames (use `# File:` or `// File:` markers) or fenced code blocks
"""

    return call_llm(prompt)
