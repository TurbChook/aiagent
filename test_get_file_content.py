from functions.get_file_content import get_file_content
from config import MAX_CHARS

def main():
    lorem_result = get_file_content("calculator", "lorem.txt")
    print("Length of lorem.txt result:", len(lorem_result))
    print(
        "Ends with truncation marker?:",
        lorem_result.endswith(
            f'[...File "lorem.txt" truncated at {MAX_CHARS} characters]'
        ),
    )

    print("Result for main.py:")
    print(get_file_content("calculator", "main.py"))

    print("Result for pkg/calculator.py:")
    print(get_file_content("calculator", "pkg/calculator.py"))

    print("Result for /bin/cat:")
    print(get_file_content("calculator", "/bin/cat"))

    print("Result for pkg/does_not_exist.py:")
    print(get_file_content("calculator", "pkg/does_not_exist.py"))
    

if __name__ == "__main__":
    main()