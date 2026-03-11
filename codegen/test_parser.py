import json
from Parser import detect_format, extract_endpoints, Format

from Prompts import generate_code


def _make_dummy_vectorstore(context_text=""):
    # simple stand-in with minimal retriever behavior
    class DummyDoc:
        def __init__(self, content):
            self.page_content = content

    class DummyRetriever:
        def __init__(self, docs):
            self.docs = docs
        def get_relevant_documents(self, query):
            return self.docs

    class DummyVS:
        def __init__(self, docs):
            self._docs = docs
        def as_retriever(self, search_kwargs=None):
            return DummyRetriever(self._docs)

    return DummyVS([DummyDoc(context_text)])


def test_openapi_parsing():
    spec = {
        "openapi": "3.0.0",
        "paths": {
            "/foo": {"get": {"responses": {"200": {"description": "ok"}}}}
        },
    }
    fmt = detect_format(spec)
    assert fmt == Format.OPENAPI
    endpoints = extract_endpoints(spec)
    assert len(endpoints) == 1
    ep = endpoints[0]
    assert ep["path"] == "/foo"
    assert ep["method"] == "GET"


def test_detect_format_rejects_non_openapi(tmp_path):
    # anything missing the expected keys should raise
    path = tmp_path / "notapispec.json"
    path.write_text(json.dumps({"foo": "bar"}))
    try:
        detect_format(str(path))
        assert False, "Expected ValueError"
    except ValueError as e:
        assert "OpenAPI" in str(e)


def test_generate_code_prompt_and_return(monkeypatch):
    # ensure prompt includes key parts and returns whatever call_llm yields
    endpoint = {"path": "/foo", "method": "POST", "requestBody": {"x": 1}, "responses": {"200": {}}}
    dummy_vs = _make_dummy_vectorstore("some guidelines")

    captured = {}

    def fake_call_llm(prompt):
        captured['prompt'] = prompt
        return "<generated code>"

    monkeypatch.setattr("LLM_Integration.call_llm", fake_call_llm)

    output = generate_code(endpoint, dummy_vs, language="python")
    assert output == "<generated code>"
    assert "Path: /foo" in captured['prompt']
    assert "Method: POST" in captured['prompt']
    assert "Target: FastAPI" in captured['prompt']
