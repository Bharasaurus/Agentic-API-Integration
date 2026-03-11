import json
import os
from enum import Enum
from dataclasses import dataclass, asdict

try:
    # requests is only required when fetching a spec from a URL
    import requests
except ImportError:  # pragma: no cover - requests may not be installed by default
    requests = None



class Format(Enum):
    OPENAPI = "openapi"


@dataclass
class UniversalEndpoint:
    path: str
    method: str
    requestBody: object = None
    responses: object = None

    def to_dict(self) -> dict:
        return asdict(self)


# helper loaders ------------------------------------------------------------

def _load_source(source):
    """Return either a dict (parsed JSON) or a raw string.

    The caller can pass a dict, a filesystem path, or an http(s) URL.  If the
    content is JSON it will be parsed; otherwise the raw text is returned.  An
    exception is raised when the underlying fetch fails.
    """

    if isinstance(source, dict):
        return source

    # fetch remote if necessary
    if isinstance(source, str) and source.lower().startswith("http"):
        if requests is None:
            raise RuntimeError("requests package is required to fetch a spec from a URL")
        resp = requests.get(source)
        resp.raise_for_status()
        text = resp.text
        try:
            return resp.json()
        except ValueError:
            return text

    # otherwise treat as file path
    with open(source, "r", encoding="utf-8") as f:
        text = f.read()
    try:
        return json.loads(text)
    except ValueError:  # not JSON, return raw
        return text


# format detection ---------------------------------------------------------

def detect_format(source) -> Format:
    """Determine if the provided spec is OpenAPI.

    We no longer support custom or WSDL formats – anything that does not
    look like OpenAPI is considered invalid and will trigger an error early.
    """

    spec = _load_source(source)

    # dict-based heuristic
    if isinstance(spec, dict):
        if "paths" in spec or "openapi" in spec or "swagger" in spec:
            return Format.OPENAPI
    # try parsing string as JSON in case we were given raw text
    if isinstance(spec, str):
        try:
            j = json.loads(spec)
            if "paths" in j or "openapi" in j or "swagger" in j:
                return Format.OPENAPI
        except ValueError:
            pass

    raise ValueError("Only OpenAPI/Swagger specs are supported")


# parsers ------------------------------------------------------------------

class OpenAPIParser:
    @staticmethod
    def parse(source) -> list[UniversalEndpoint]:
        """Parse an OpenAPI / Swagger document into a list of endpoints."""

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


# validation & enrichment --------------------------------------------------

def validate(endpoints: list[UniversalEndpoint]) -> list[UniversalEndpoint]:
    """Catch missing or malformed fields early in the process."""

    for ep in endpoints:
        if not ep.path or not isinstance(ep.path, str):
            raise ValueError(f"Endpoint has invalid path: {ep}")
        if not ep.method or not isinstance(ep.method, str):
            raise ValueError(f"Endpoint has invalid method: {ep}")
        ep.method = ep.method.upper()
    return endpoints


def enrich(endpoints: list[UniversalEndpoint]) -> list[UniversalEndpoint]:
    """Infer sensible defaults and normalise the IR before handing it off.

    Currently this simply ensures that ``requestBody`` and ``responses`` are
    never ``None``; other conventions could be added here (e.g. filling in
    common HTTP status codes or parameter names).
    """

    for ep in endpoints:
        if ep.requestBody is None:
            ep.requestBody = {}
        if ep.responses is None:
            ep.responses = {}
    return endpoints


# public entrypoint --------------------------------------------------------

def extract_endpoints(source):
    """Load a spec from a path/URL/dict and return normalized endpoint dicts.

    The function dispatches to the appropriate parser based on a simple
    format detection step, then validates and enriches the resulting
    intermediate representation (IR).  The output is a list of plain dicts so
    existing callers (such as ``main.py``) continue to work unchanged.
    """

    fmt = detect_format(source)
    if fmt == Format.OPENAPI:
        eps = OpenAPIParser.parse(source)
    else:  # defensive – should not happen
        raise ValueError(f"Unhandled format {fmt}")

    eps = validate(eps)
    eps = enrich(eps)
    # convert to plain dictionaries for backwards compatibility
    return [ep.to_dict() for ep in eps]
