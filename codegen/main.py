from Vector_Store import build_vectorstore
from Parser import extract_endpoints
from Prompts import generate_code
from Writer import write_java_files


def choose_language():
    choice = input("Choose language for codegen ('java' or 'python') [java]: ").strip().lower()
    if choice == "" or choice not in ("java", "python"):
        return "java"
    return choice

def main():
    vectorstore = build_vectorstore()

    # allow the user to specify either a local file or an HTTP endpoint
    spec_source = input("Path or URL of API spec [input/api.json]: ").strip()
    if not spec_source:
        spec_source = "input/api.json"

    endpoints = extract_endpoints(spec_source)

    language = choose_language()

    for endpoint in endpoints:
        code = generate_code(endpoint, vectorstore, language=language)
        write_java_files(code, language=language)
        print(f"Wrote generated files for {endpoint.get('path')} ({language})")
        print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    main()
