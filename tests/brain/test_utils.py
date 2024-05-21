import unittest
from regdbot.brain.utils import extract_code_from_markdown

class TestExtractCodeFromMarkdown(unittest.TestCase):
    def test_extract_code_from_single_block(self):
        markdown_text = "```python\nprint('Hello, World!')\n```"
        expected_code = "print('Hello, World!')"
        self.assertEqual(expected_code, extract_code_from_markdown(markdown_text))

    def test_extract_code_from_multiple_blocks(self):
        markdown_text = "```python\nprint('Hello, World!')\n```\n```python\nprint('Goodbye, World!')\n```"
        expected_code = "print('Hello, World!')\nprint('Goodbye, World!')"
        self.assertEqual(expected_code, extract_code_from_markdown(markdown_text))

    def test_extract_code_with_no_code_blocks(self):
        markdown_text = "This is a markdown text with no code blocks."
        expected_code = ""
        self.assertEqual(extract_code_from_markdown(markdown_text), expected_code)

    def test_extract_code_with_empty_code_blocks(self):
        markdown_text = "```\n\n```"
        expected_code = ""
        self.assertEqual(expected_code, extract_code_from_markdown(markdown_text))

    def test_extract_code_with_nested_code_blocks(self):
        markdown_text = "```python\nprint('```Hello, World!```')\n```"
        expected_code = "print('```Hello, World!```')"
        self.assertEqual(expected_code,extract_code_from_markdown(markdown_text))

if __name__ == '__main__':
    unittest.main()
