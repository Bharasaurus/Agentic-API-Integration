import json


def extract_endpoints(path):
    with open(path, "r") as f:
        spec = json.load(f)

    endpoints = []

    # Support OpenAPI-style specs with "paths"
    if "paths" in spec:
        for p, methods in spec["paths"].items():
            for method, details in methods.items():
                endpoints.append({
                    "path": p,
                    "method": method.upper(),
                    "requestBody": details.get("requestBody"),
                    "responses": details.get("responses")
                })
        return endpoints

    # Support project-specific simple format with an "endpoints" list
    if "endpoints" in spec:
        for ep in spec["endpoints"]:
            endpoints.append({
                "path": ep.get("path"),
                "method": ep.get("method", "GET").upper(),
                "requestBody": ep.get("requestBody"),
                "responses": ep.get("responses") or ep.get("response")
            })
        return endpoints

    raise ValueError("Unrecognized API spec format: expected 'paths' or 'endpoints'")
