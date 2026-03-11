# Agentic-API-Integration

This repository generates client/server code for a simple API definition. By default it
reads a JSON spec located at `input/api.json`, but you can also point it at any
URL that returns a compatible JSON payload (e.g. another service exposing its
OpenAPI spec).

## Requirements

- Python 3.8+
- `requests` (only needed if specifying an HTTP URL as the spec source)


## Usage

Run the generator from the `codegen` directory:

```bash
python main.py
```

You'll be prompted for the path or URL of the API spec. Leave blank to use
`input/api.json`.

The tool now focuses exclusively on **OpenAPI/Swagger** documents.  It
will reject any other format early with an error message, and the parsing
pipeline has been simplified accordingly.  Provide a JSON or YAML spec containing
at least a `paths` map (or `openapi`/`swagger` key) and the generator will
produce code based on the endpoints found.

Future formats could be reintroduced by extending `Parser.detect_format` and
adding new parser classes, but the current scope is intentionally limited to
OpenAPI for consistency and reduced maintenance.

Examples:

```text
Path or URL of API spec [input/api.json]: https://api.example.com/openapi.json
Choose language for codegen ('java' or 'python') [java]:
```

---