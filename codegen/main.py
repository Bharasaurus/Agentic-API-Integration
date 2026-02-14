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
    endpoints = extract_endpoints("input/api.json")

    language = choose_language()

    for endpoint in endpoints:
        code = generate_code(endpoint, vectorstore, language=language)
        write_java_files(code, language=language)
        print(f"Wrote generated files for {endpoint.get('path')} ({language})")
        print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    main()
