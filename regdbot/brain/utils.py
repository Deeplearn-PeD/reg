import re

def extract_code_from_markdown(markdown_text: str) -> str:
    """
    Extracts code from markdown text.
    :param markdown_text: Markdown text to extract code from.
    :return: Extracted code as a string.
    """
    # Regular expression pattern to match code blocks
    pattern = r'```.*?\n+(.*?)```.*?'

    # Find all matches of the pattern in the markdown text
    matches = re.findall(pattern, markdown_text, re.DOTALL)

    # Join all matches into a single string, separated by newlines
    code = '\n'.join([m.strip() for m in matches])

    # Remove leading and trailing whitespace
    code = code.strip()

    return code