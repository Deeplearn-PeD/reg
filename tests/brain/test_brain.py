import unittest
from regdbot import brain


class MyTestCase(unittest.TestCase):
    def test_parse_response_no_code(self):
        rdb = brain.RegDBot()
        response = """Hello! I'm Reggie D. Bot, your friendly AI assistant for data querying and analysis. It looks like you have a dataset with several text columns. Let's explore the possibilities!
    
    Which column would you like to start with? Do you have any specific questions or goals in mind?
    
    Some possible tasks we could accomplish together:
    
    1. **Data cleaning**: Remove unnecessary spaces, convert text to lowercase, or handle missing values.
    2. **Text analysis**: Count word frequencies, identify common phrases, or perform sentiment analysis.
    3. **Filtering and grouping**: Extract specific data points based on conditions, group by categories, or create summaries.
    4. **Visualization**: Create charts, plots, or heatmaps to visualize the data and gain insights.
    
    Let me know how I can assist you with your dataset!"""
        result = rdb._parse_response(response)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], response, 'Preamble should be the same as the response')
        self.assertEqual(result[1], '', 'Query should be empty')
        self.assertEqual(result[2], '', 'Explanation should be empty')


    def test_parse_response_single_code_block_3quotes(self):
        rdb = brain.RegDBot()
        response = "Here is some SQL code:\n\n ```sql\nSELECT * FROM table_name;```"
        result = rdb._parse_response(response)
        self.assertEqual(result[0],'Here is some SQL code:\n\n ', 'Preamble should be the text before the code block')
        self.assertEqual(result[1],'SELECT * FROM table_name;','Query should be the code block')
        self.assertEqual(result[2],'','Explanation should be empty')

    def test_parse_response_single_backtick_code(self):
        rdb = brain.RegDBot()
        response = "Here is some Python code:\n\n `print('Hello, World!')` Did you know that this code will print 'Hello, World!'?"
        result = rdb._parse_response(response)
        self.assertEqual(result[0],'Here is some Python code:\n\n ', 'Preamble should be the text before the code block')
        self.assertEqual(result[1],'print(\'Hello, World!\')','Query should be the code block')
        self.assertEqual(result[2]," Did you know that this code will print 'Hello, World!'?",'Explanation should be the text after the code block')
if __name__ == '__main__':
    unittest.main()
