"""
Tests for the Translator module.
"""

import unittest
from unittest.mock import patch, MagicMock

from app.translator import Translator


class TestTranslator(unittest.TestCase):
    """Test cases for the Translator class."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a mock for the Google Cloud Translation client
        self.client_patcher = patch('app.translator.translate.Client')
        self.mock_client = self.client_patcher.start()

        # Create a translator instance with the mocked client
        self.translator = Translator()

    def tearDown(self):
        """Tear down test fixtures."""
        self.client_patcher.stop()

    def test_init(self):
        """Test the initialization of the Translator class."""
        # Test that the client is initialized
        self.mock_client.assert_called_once()

        # Test that the supported languages are set correctly
        self.assertEqual(self.translator.supported_languages, {'en', 'sw'})

    def test_translate_text(self):
        """Test the translate_text method."""
        # Mock the translate method of the client
        self.translator.client.translate.return_value = {
            'translatedText': 'Habari dunia',
            'detectedSourceLanguage': 'en'
        }

        # Test translation
        result = self.translator.translate_text('Hello world', 'sw')

        # Verify the result
        self.assertEqual(result, 'Habari dunia')

        # Verify the client method was called correctly
        self.translator.client.translate.assert_called_once_with(
            'Hello world',
            target_language='sw',
            source_language=None
        )

    def test_translate_text_with_source_language(self):
        """Test the translate_text method with a source language."""
        # Mock the translate method of the client
        self.translator.client.translate.return_value = {
            'translatedText': 'Hello world',
            'detectedSourceLanguage': None
        }

        # Test translation with source language
        result = self.translator.translate_text('Habari dunia', 'en', 'sw')

        # Verify the result
        self.assertEqual(result, 'Hello world')

        # Verify the client method was called correctly
        self.translator.client.translate.assert_called_once_with(
            'Habari dunia',
            target_language='en',
            source_language='sw'
        )

    def test_translate_text_empty(self):
        """Test the translate_text method with empty text."""
        # Test translation of empty text
        result = self.translator.translate_text('', 'sw')

        # Verify the result is also empty
        self.assertEqual(result, '')

        # Verify the client method was not called
        self.translator.client.translate.assert_not_called()

    def test_translate_text_unsupported_language(self):
        """Test the translate_text method with an unsupported language."""
        # Test translation to an unsupported language
        with self.assertRaises(ValueError):
            self.translator.translate_text('Hello world', 'fr')

    def test_translate_dict(self):
        """Test the translate_dict method."""
        # Mock the translate_text method
        self.translator.translate_text = MagicMock()
        self.translator.translate_text.side_effect = lambda text, target, source=None: f"TRANSLATED_{text}"

        # Test dictionary translation
        data = {
            'greeting': 'Hello',
            'farewell': 'Goodbye',
            'nested': {
                'message': 'Welcome'
            },
            'list': ['One', 'Two', 'Three']
        }

        result = self.translator.translate_dict(data, 'sw')

        # Verify the result
        expected = {
            'greeting': 'TRANSLATED_Hello',
            'farewell': 'TRANSLATED_Goodbye',
            'nested': {
                'message': 'TRANSLATED_Welcome'
            },
            'list': ['TRANSLATED_One', 'TRANSLATED_Two', 'TRANSLATED_Three']
        }

        self.assertEqual(result, expected)

    def test_translate_survey_question(self):
        """Test the translate_survey_question method."""
        # Test question translation
        question = {
            'id': 'q1',
            'type': 'multiple_choice',
            'text': {
                'en': 'How are you?',
                'sw': 'Habari yako?'
            },
            'options': [
                {
                    'id': 'q1_opt1',
                    'text': {
                        'en': 'Good',
                        'sw': 'Nzuri'
                    }
                },
                {
                    'id': 'q1_opt2',
                    'text': {
                        'en': 'Bad',
                        'sw': 'Mbaya'
                    }
                }
            ]
        }

        # Translate to Swahili
        result = self.translator.translate_survey_question(question, 'sw')

        # Verify the result
        self.assertEqual(result['text'], 'Habari yako?')
        self.assertEqual(result['options'][0]['text'], 'Nzuri')
        self.assertEqual(result['options'][1]['text'], 'Mbaya')

    def test_translate_survey(self):
        """Test the translate_survey method."""
        # Test survey translation
        survey = {
            'survey_id': 'test_survey',
            'title': {
                'en': 'Test Survey',
                'sw': 'Uchunguzi wa Majaribio'
            },
            'description': {
                'en': 'A survey for testing',
                'sw': 'Uchunguzi kwa ajili ya kupima'
            },
            'questions': [
                {
                    'id': 'q1',
                    'type': 'multiple_choice',
                    'text': {
                        'en': 'How are you?',
                        'sw': 'Habari yako?'
                    },
                    'options': [
                        {
                            'id': 'q1_opt1',
                            'text': {
                                'en': 'Good',
                                'sw': 'Nzuri'
                            }
                        },
                        {
                            'id': 'q1_opt2',
                            'text': {
                                'en': 'Bad',
                                'sw': 'Mbaya'
                            }
                        }
                    ]
                }
            ]
        }

        # Mock the translate_survey_question method
        self.translator.translate_survey_question = MagicMock()
        self.translator.translate_survey_question.side_effect = lambda q, lang: {
            'id': q['id'],
            'type': q['type'],
            'text': q['text'][lang],
            'options': [{'id': opt['id'], 'text': opt['text'][lang]} for opt in q.get('options', [])]
        }

        # Translate to Swahili
        result = self.translator.translate_survey(survey, 'sw')

        # Verify the result
        self.assertEqual(result['title'], 'Uchunguzi wa Majaribio')
        self.assertEqual(result['description'], 'Uchunguzi kwa ajili ya kupima')
        self.translator.translate_survey_question.assert_called_once()


if __name__ == '__main__':
    unittest.main()
