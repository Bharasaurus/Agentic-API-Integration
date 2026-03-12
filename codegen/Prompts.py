from LLM_Integration import call_llm


def generate_code(endpoint, vectorstore, language: str = "python"):

    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    query = f"""
    Generate backend code for:
    Path: {endpoint['path']}
    Method: {endpoint['method']}
    Language: {language.upper()}
    """

    docs = retriever.get_relevant_documents(query)

    context = "\n\n".join([doc.page_content for doc in docs])

    # Detect SOAP endpoint
    is_soap = endpoint["method"] == "SOAP"

    if language.lower() == "python":

        lang_block = """IMPORTANT: GENERATE PYTHON CODE ONLY.

Target: FastAPI (Python 3.11+)

- Use layered architecture
- routers/
- services/
- clients/
- schemas/

Use Pydantic models
Use async FastAPI routes
"""

    else:

        lang_block = """IMPORTANT: GENERATE JAVA CODE ONLY.

Target: Spring Boot
Generate controllers, services and DTOs.
"""

    # SOAP specific instructions
    protocol_block = ""

    if is_soap:

        protocol_block = """
SOAP INTEGRATION REQUIREMENTS:

- Use Zeep library
- Create SOAP client in clients/soap_client.py
- Initialize client using WSDL
- Call SOAP operation using client.service.<operation>
- Wrap SOAP call inside service layer
- Expose REST endpoint that internally calls SOAP service
"""

    prompt = f"""
{lang_block}

{protocol_block}

Use the following coding standards:
{context}

Generate production-ready backend code.

Endpoint Information:

Path: {endpoint['path']}
Method: {endpoint['method']}
RequestBody: {endpoint['requestBody']}
Responses: {endpoint['responses']}

Requirements:

- Clean layered architecture
- Proper validation
- Error handling
- File structure with markers:

# File: routers/...
# File: services/...
# File: clients/...

Generate only {language.upper()} code.
"""

    return call_llm(prompt)