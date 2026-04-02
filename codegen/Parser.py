import json
from enum import Enum
from dataclasses import dataclass, asdict

try:
    import requests
except ImportError:
    requests = None

# NEW: SOAP library
try:
    from zeep import Client
except ImportError:
    Client = None


class Format(Enum):
    OPENAPI = "openapi"
    SOAP = "soap"


@dataclass
class UniversalEndpoint:
    path: str
    method: str
    requestBody: object = None
    responses: object = None

    def to_dict(self) -> dict:
        return asdict(self)


# ---------------- SOURCE LOADER ----------------

def _load_source(source):

    if isinstance(source, dict):
        return source

    if isinstance(source, str) and source.lower().startswith("http"):
        if requests is None:
            raise RuntimeError("requests package is required")

        resp = requests.get(source)
        resp.raise_for_status()

        text = resp.text
        try:
            return resp.json()
        except ValueError:
            return text

    with open(source, "r", encoding="utf-8") as f:
        text = f.read()

    try:
        return json.loads(text)
    except ValueError:
        return text


# ---------------- FORMAT DETECTION ----------------

def detect_format(source):

    spec = _load_source(source)

    # Detect OpenAPI
    if isinstance(spec, dict):
        if "paths" in spec or "openapi" in spec or "swagger" in spec:
            return Format.OPENAPI

    # Detect WSDL (SOAP)
    if isinstance(source, str) and source.endswith(".wsdl"):
        return Format.SOAP

    if isinstance(spec, str) and "<definitions" in spec:
        return Format.SOAP

    raise ValueError("Unsupported API specification format")


# ---------------- OPENAPI PARSER ----------------

class OpenAPIParser:

    @staticmethod
    def parse(source):

        spec = _load_source(source)

        if isinstance(spec, str):
            spec = json.loads(spec)

        endpoints = []

        for path, methods in spec.get("paths", {}).items():

            for method, details in methods.items():

                endpoints.append(
                    UniversalEndpoint(
                        path=path,
                        method=method.upper(),
                        requestBody=details.get("requestBody"),
                        responses=details.get("responses"),
                    )
                )

        return endpoints


# ---------------- SOAP PARSER ----------------

class SOAPParser:

    @staticmethod
    def parse(wsdl_path):

        if Client is None:
            raise RuntimeError("zeep library required for SOAP parsing")

        client = Client(wsdl_path)

        endpoints = []

        for service in client.wsdl.services.values():

            for port in service.ports.values():

                operations = port.binding._operations.values()

                for op in operations:

                    endpoints.append(
                        UniversalEndpoint(
                            path=op.name,
                            method="SOAP",
                            requestBody={},
                            responses={}
                        )
                    )

        return endpoints

# ---------------- VALIDATION ----------------

def validate(endpoints):

    for ep in endpoints:

        if not ep.path:
            raise ValueError(f"Invalid path: {ep}")

        if not ep.method:
            raise ValueError(f"Invalid method: {ep}")

        ep.method = ep.method.upper()

    return endpoints


# ---------------- ENRICHMENT ----------------

def enrich(endpoints):

    for ep in endpoints:

        if ep.requestBody is None:
            ep.requestBody = {}

        if ep.responses is None:
            ep.responses = {}

    return endpoints


# ---------------- MAIN ENTRYPOINT ----------------

def extract_endpoints(source):

    fmt = detect_format(source)

    if fmt == Format.OPENAPI:
        eps = OpenAPIParser.parse(source)

    elif fmt == Format.SOAP:
        eps = SOAPParser.parse(source)

    else:
        raise ValueError(f"Unhandled format {fmt}")

    eps = validate(eps)
    eps = enrich(eps)

    return [ep.to_dict() for ep in eps]