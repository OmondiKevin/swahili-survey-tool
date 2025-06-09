"""
Tests for the ResponseParser module.
"""

import json
import os
import tempfile
import unittest
from unittest.mock import patch, mock_open

from app.response_parser import ResponseParser


class TestResponseParser(unittest.TestCase):
    """Test cases for the ResponseParser class."""

    def setUp(self):
        """Set up test fixtures."""
        # Sample responses for testing
        self.sample_responses = [
            {
                'question_id': 'q1',
                'response': 'q1_opt1',
                'valid': True,
                'error': None,
                'question_type': 'multiple_choice'
            },
            {
                'question_id': 'q1',
                'response': 'q1_opt2',
                'valid': True,
                'error': None,
                'question_type': 'multiple_choice'
            },
            {
                'question_id': 'q1',
                'response': 'q1_opt1',
                'valid': True,
                'error': None,
                'question_type': 'multiple_choice'
            },
            {
                'question_id': 'q2',
                'response': 'yes',
                'valid': True,
                'error': None,
                'question_type': 'yes_no'
            },
            {
                'question_id': 'q2',
                'response': 'no',
                'valid': True,
                'error': None,
                'question_type': 'yes_no'
            },
            {
                'question_id': 'q2',
                'response': 'ndio',
                'valid': True,
                'error': None,
                'question_type': 'yes_no'
            },
            {
                'question_id': 'q3',
                'response': 'I think the service is good but could be improved.',
                'valid': True,
                'error': None,
                'question_type': 'open_ended'
            },
            {
                'question_id': 'q3',
                'response': 'The service needs improvement in several areas.',
                'valid': True,
                'error': None,
                'question_type': 'open_ended'
            },
            {
                'question_id': 'q3',
                'response': 'Overall good service but slow response times.',
                'valid': True,
                'error': None,
                'question_type': 'open_ended'
            }
        ]

        # Create a parser with the sample responses
        self.parser = ResponseParser()
        for response in self.sample_responses:
            self.parser.add_response(response)

    def test_init(self):
        """Test initialization of the ResponseParser class."""
        parser = ResponseParser()
        self.assertEqual(parser.responses, [])
        # The model might be None or a SentenceTransformer object depending on whether
        # the sentence-transformers library is available and the model can be loaded
        # Just check that the model_name is set correctly
        self.assertEqual(parser.model_name, 'paraphrase-multilingual-MiniLM-L12-v2')

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='[{"question_id": "q1", "response": "test"}]')
    def test_load_responses(self, mock_file, mock_exists):
        """Test loading responses from a file."""
        parser = ResponseParser()
        result = parser.load_responses('test.json')
        self.assertEqual(result, [{"question_id": "q1", "response": "test"}])
        self.assertEqual(parser.responses, [{"question_id": "q1", "response": "test"}])

    @patch('os.path.exists', return_value=False)
    def test_load_responses_file_not_found(self, mock_exists):
        """Test loading responses from a non-existent file."""
        parser = ResponseParser()
        with self.assertRaises(FileNotFoundError):
            parser.load_responses('nonexistent.json')

    def test_add_response(self):
        """Test adding a response."""
        parser = ResponseParser()
        parser.add_response({"question_id": "q1", "response": "test"})
        self.assertEqual(parser.responses, [{"question_id": "q1", "response": "test"}])

    def test_get_responses_for_question(self):
        """Test getting responses for a specific question."""
        # Get responses for q1
        responses = self.parser.get_responses_for_question('q1')
        self.assertEqual(len(responses), 3)
        self.assertEqual(responses.count('q1_opt1'), 2)
        self.assertEqual(responses.count('q1_opt2'), 1)

        # Get responses for q2
        responses = self.parser.get_responses_for_question('q2')
        self.assertEqual(len(responses), 3)
        self.assertEqual(responses.count('yes'), 1)
        self.assertEqual(responses.count('no'), 1)
        self.assertEqual(responses.count('ndio'), 1)

        # Get responses for q3
        responses = self.parser.get_responses_for_question('q3')
        self.assertEqual(len(responses), 3)

        # Get responses for a non-existent question
        responses = self.parser.get_responses_for_question('nonexistent')
        self.assertEqual(len(responses), 0)

    def test_count_multiple_choice_responses(self):
        """Test counting multiple choice responses."""
        counts = self.parser.count_multiple_choice_responses('q1')
        self.assertEqual(counts, {'q1_opt1': 2, 'q1_opt2': 1})

        # Test with a non-existent question
        counts = self.parser.count_multiple_choice_responses('nonexistent')
        self.assertEqual(counts, {})

    def test_count_yes_no_responses(self):
        """Test counting yes/no responses."""
        counts = self.parser.count_yes_no_responses('q2')
        self.assertEqual(counts, {'yes': 2, 'no': 1})  # 'ndio' is normalized to 'yes'

        # Test with a non-existent question
        counts = self.parser.count_yes_no_responses('nonexistent')
        self.assertEqual(counts, {})

    def test_extract_keywords(self):
        """Test extracting keywords from text."""
        text = "The service is good but could be improved. The response time is slow."
        keywords = self.parser.extract_keywords(text, 3)

        # Check that we got 3 keywords
        self.assertEqual(len(keywords), 3)

        # Check that each keyword is a tuple of (word, count)
        for keyword in keywords:
            self.assertIsInstance(keyword, tuple)
            self.assertEqual(len(keyword), 2)
            self.assertIsInstance(keyword[0], str)
            self.assertIsInstance(keyword[1], int)

        # Check that common stop words are excluded
        for keyword in keywords:
            self.assertNotIn(keyword[0], ['the', 'is', 'but', 'and', 'or'])

    def test_analyze_open_ended_responses(self):
        """Test analyzing open-ended responses."""
        analysis = self.parser.analyze_open_ended_responses('q3')

        # Check that we got keywords and a response count
        self.assertIn('keywords', analysis)
        self.assertIn('response_count', analysis)
        self.assertEqual(analysis['response_count'], 3)

        # Check that keywords are present
        self.assertGreater(len(analysis['keywords']), 0)

        # Test with a non-existent question
        analysis = self.parser.analyze_open_ended_responses('nonexistent')
        self.assertEqual(analysis['response_count'], 0)
        self.assertEqual(analysis['keywords'], [])

    @patch('app.response_parser.ADVANCED_NLP_AVAILABLE', False)
    def test_extract_themes_with_clustering_not_available(self):
        """Test theme extraction when advanced NLP is not available."""
        parser = ResponseParser()
        themes = parser._extract_themes_with_clustering(['text1', 'text2', 'text3'])
        self.assertEqual(themes, [])

    def test_generate_summary_report(self):
        """Test generating a summary report."""
        summary = self.parser.generate_summary_report()

        # Check that we got a summary with questions and total responses
        self.assertIn('questions', summary)
        self.assertIn('total_responses', summary)
        self.assertEqual(summary['total_responses'], 9)

        # Check that each question type is analyzed correctly
        for question in summary['questions']:
            if question['id'] == 'q1':
                self.assertEqual(question['type'], 'multiple_choice')
                self.assertIn('option_counts', question)
                self.assertEqual(question['option_counts'], {'q1_opt1': 2, 'q1_opt2': 1})

            elif question['id'] == 'q2':
                self.assertEqual(question['type'], 'yes_no')
                self.assertIn('counts', question)
                self.assertEqual(question['counts'], {'yes': 2, 'no': 1})  # 'ndio' is normalized to 'yes'

            elif question['id'] == 'q3':
                self.assertEqual(question['type'], 'open_ended')
                self.assertIn('keywords', question)
                self.assertGreater(len(question['keywords']), 0)

        # Test with no responses
        parser = ResponseParser()
        summary = parser.generate_summary_report()
        self.assertEqual(summary['total_responses'], 0)
        self.assertEqual(summary['questions'], [])

    def test_save_responses(self):
        """Test saving responses to a file."""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            temp_path = temp.name

        try:
            # Save the responses
            self.parser.save_responses(temp_path)

            # Read the saved file
            with open(temp_path, 'r', encoding='utf-8') as f:
                saved_responses = json.load(f)

            # Verify the content
            self.assertEqual(saved_responses, self.sample_responses)

            # Test with no responses
            parser = ResponseParser()
            with self.assertRaises(ValueError):
                parser.save_responses(temp_path)

        finally:
            # Clean up
            os.unlink(temp_path)

    def test_save_summary_report(self):
        """Test saving a summary report to a file."""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            temp_path = temp.name

        try:
            # Save the summary report
            self.parser.save_summary_report(temp_path)

            # Read the saved file
            with open(temp_path, 'r', encoding='utf-8') as f:
                saved_summary = json.load(f)

            # Verify the content
            self.assertIn('questions', saved_summary)
            self.assertIn('total_responses', saved_summary)
            self.assertEqual(saved_summary['total_responses'], 9)

            # Test with no responses
            parser = ResponseParser()
            with self.assertRaises(ValueError):
                parser.save_summary_report(temp_path)

        finally:
            # Clean up
            os.unlink(temp_path)


if __name__ == '__main__':
    unittest.main()
