import unittest
from regdbot import brain


class MyTestCase(unittest.TestCase):
    def test_parse_response(self):
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


if __name__ == '__main__':
    unittest.main()
