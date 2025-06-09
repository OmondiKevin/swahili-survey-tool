"""
Tests for the QuestionMapper module.
"""

import json
import os
import tempfile
import unittest
from unittest.mock import patch, mock_open

from app.question_mapper import QuestionMapper


class TestQuestionMapper(unittest.TestCase):
    """Test cases for the QuestionMapper class."""

    def setUp(self):
        """Set up test fixtures."""
        # Sample survey data for testing
        self.sample_survey = {
            "survey_id": "test_survey",
            "title": {
                "en": "Test Survey",
                "sw": "Uchunguzi wa Majaribio"
            },
            "description": {
                "en": "A survey for testing",
                "sw": "Uchunguzi kwa ajili ya kupima"
            },
            "questions": [
                {
                    "id": "q1",
                    "type": "multiple_choice",
                    "text": {
                        "en": "How are you?",
                        "sw": "Habari yako?"
                    },
                    "options": [
                        {
                            "id": "q1_opt1",
                            "text": {
                                "en": "Good",
                                "sw": "Nzuri"
                            }
                        },
                        {
                            "id": "q1_opt2",
                            "text": {
                                "en": "Bad",
                                "sw": "Mbaya"
                            }
                        }
                    ]
                },
                {
                    "id": "q2",
                    "type": "yes_no",
                    "text": {
                        "en": "Are you happy?",
                        "sw": "Je, una furaha?"
                    }
                },
                {
                    "id": "q3",
                    "type": "open_ended",
                    "text": {
                        "en": "What do you think?",
                        "sw": "Unafikiri nini?"
                    }
                }
            ]
        }

        # Create a mapper with the sample survey
        self.mapper = QuestionMapper()
        self.mapper.survey = self.sample_survey

    def test_init_without_survey_file(self):
        """Test initialization without a survey file."""
        mapper = QuestionMapper()
        self.assertIsNone(mapper.survey)

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='{"survey_id": "test"}')
    def test_init_with_survey_file(self, mock_file, mock_exists):
        """Test initialization with a survey file."""
        mapper = QuestionMapper(survey_file='test.json')
        self.assertEqual(mapper.survey, {"survey_id": "test"})

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='{"survey_id": "test"}')
    def test_load_survey(self, mock_file, mock_exists):
        """Test loading a survey from a file."""
        mapper = QuestionMapper()
        result = mapper.load_survey('test.json')
        self.assertEqual(result, {"survey_id": "test"})
        self.assertEqual(mapper.survey, {"survey_id": "test"})

    @patch('os.path.exists', return_value=False)
    def test_load_survey_file_not_found(self, mock_exists):
        """Test loading a survey from a non-existent file."""
        mapper = QuestionMapper()
        with self.assertRaises(FileNotFoundError):
            mapper.load_survey('nonexistent.json')

    def test_get_question_by_id(self):
        """Test getting a question by ID."""
        # Get an existing question
        question = self.mapper.get_question_by_id('q1')
        self.assertEqual(question['id'], 'q1')
        self.assertEqual(question['type'], 'multiple_choice')

        # Get a non-existent question
        question = self.mapper.get_question_by_id('nonexistent')
        self.assertIsNone(question)

        # Test with no survey loaded
        mapper = QuestionMapper()
        question = mapper.get_question_by_id('q1')
        self.assertIsNone(question)

    def test_get_questions_by_type(self):
        """Test getting questions by type."""
        # Get multiple choice questions
        questions = self.mapper.get_questions_by_type('multiple_choice')
        self.assertEqual(len(questions), 1)
        self.assertEqual(questions[0]['id'], 'q1')

        # Get yes/no questions
        questions = self.mapper.get_questions_by_type('yes_no')
        self.assertEqual(len(questions), 1)
        self.assertEqual(questions[0]['id'], 'q2')

        # Get open-ended questions
        questions = self.mapper.get_questions_by_type('open_ended')
        self.assertEqual(len(questions), 1)
        self.assertEqual(questions[0]['id'], 'q3')

        # Get non-existent type
        questions = self.mapper.get_questions_by_type('nonexistent')
        self.assertEqual(len(questions), 0)

        # Test with no survey loaded
        mapper = QuestionMapper()
        questions = mapper.get_questions_by_type('multiple_choice')
        self.assertEqual(len(questions), 0)

    def test_map_to_simple_format(self):
        """Test mapping to a simple format."""
        # Map to English
        simple_questions = self.mapper.map_to_simple_format('en')
        self.assertEqual(len(simple_questions), 3)
        self.assertEqual(simple_questions[0]['text'], 'How are you?')
        self.assertEqual(simple_questions[0]['options'][0]['text'], 'Good')

        # Map to Swahili
        simple_questions = self.mapper.map_to_simple_format('sw')
        self.assertEqual(len(simple_questions), 3)
        self.assertEqual(simple_questions[0]['text'], 'Habari yako?')
        self.assertEqual(simple_questions[0]['options'][0]['text'], 'Nzuri')

        # Map to a non-existent language
        simple_questions = self.mapper.map_to_simple_format('fr')
        self.assertEqual(len(simple_questions), 3)
        self.assertEqual(simple_questions[0]['text'], 'Question text not available in fr')

        # Test with no survey loaded
        mapper = QuestionMapper()
        simple_questions = mapper.map_to_simple_format('en')
        self.assertEqual(len(simple_questions), 0)

    def test_map_to_presentation_format(self):
        """Test mapping to a presentation format."""
        # Map to English
        presentation = self.mapper.map_to_presentation_format('en')
        self.assertEqual(presentation['title'], 'Test Survey')
        self.assertEqual(presentation['description'], 'A survey for testing')
        self.assertEqual(len(presentation['questions']), 3)

        # Map to Swahili
        presentation = self.mapper.map_to_presentation_format('sw')
        self.assertEqual(presentation['title'], 'Uchunguzi wa Majaribio')
        self.assertEqual(presentation['description'], 'Uchunguzi kwa ajili ya kupima')
        self.assertEqual(len(presentation['questions']), 3)

        # Map to a non-existent language
        presentation = self.mapper.map_to_presentation_format('fr')
        self.assertEqual(presentation['title'], 'Survey title not available in fr')
        self.assertEqual(presentation['description'], 'Survey description not available in fr')

        # Test with no survey loaded
        mapper = QuestionMapper()
        presentation = mapper.map_to_presentation_format('en')
        self.assertEqual(presentation, {})

    def test_map_response_to_question_multiple_choice(self):
        """Test mapping a response to a multiple choice question."""
        # Valid response
        result = self.mapper.map_response_to_question('q1_opt1', 'q1')
        self.assertEqual(result['question_id'], 'q1')
        self.assertEqual(result['response'], 'q1_opt1')
        self.assertTrue(result['valid'])
        self.assertIsNone(result['error'])

        # Invalid response
        result = self.mapper.map_response_to_question('invalid', 'q1')
        self.assertEqual(result['question_id'], 'q1')
        self.assertEqual(result['response'], 'invalid')
        self.assertFalse(result['valid'])
        self.assertIsNotNone(result['error'])

    def test_map_response_to_question_yes_no(self):
        """Test mapping a response to a yes/no question."""
        # Valid responses
        for response in ['yes', 'no', 'Yes', 'No', 'YES', 'NO', 'ndio', 'hapana']:
            result = self.mapper.map_response_to_question(response, 'q2')
            self.assertEqual(result['question_id'], 'q2')
            self.assertEqual(result['response'], response)
            self.assertTrue(result['valid'])
            self.assertIsNone(result['error'])

        # Invalid response
        result = self.mapper.map_response_to_question('maybe', 'q2')
        self.assertEqual(result['question_id'], 'q2')
        self.assertEqual(result['response'], 'maybe')
        self.assertFalse(result['valid'])
        self.assertIsNotNone(result['error'])

    def test_map_response_to_question_open_ended(self):
        """Test mapping a response to an open-ended question."""
        # Valid response
        result = self.mapper.map_response_to_question('This is my response', 'q3')
        self.assertEqual(result['question_id'], 'q3')
        self.assertEqual(result['response'], 'This is my response')
        self.assertTrue(result['valid'])
        self.assertIsNone(result['error'])

        # Invalid response (empty)
        result = self.mapper.map_response_to_question('', 'q3')
        self.assertEqual(result['question_id'], 'q3')
        self.assertEqual(result['response'], '')
        self.assertFalse(result['valid'])
        self.assertIsNotNone(result['error'])

    def test_map_response_to_question_nonexistent(self):
        """Test mapping a response to a non-existent question."""
        with self.assertRaises(ValueError):
            self.mapper.map_response_to_question('response', 'nonexistent')

    def test_save_survey(self):
        """Test saving a survey to a file."""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            temp_path = temp.name

        try:
            # Save the survey
            self.mapper.save_survey(temp_path)

            # Read the saved file
            with open(temp_path, 'r', encoding='utf-8') as f:
                saved_survey = json.load(f)

            # Verify the content
            self.assertEqual(saved_survey, self.sample_survey)

            # Test with no survey loaded
            mapper = QuestionMapper()
            with self.assertRaises(ValueError):
                mapper.save_survey(temp_path)

        finally:
            # Clean up
            os.unlink(temp_path)


if __name__ == '__main__':
    unittest.main()
