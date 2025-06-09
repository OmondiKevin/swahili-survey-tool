"""
Translator module for the Swahili Survey Engine.

This module provides functionality to translate text between English and Swahili
using the Google Cloud Translation API.
"""

import os
from typing import Dict, List, Optional

from google.cloud import translate_v2 as translate


class Translator:
    """
    A class to handle translation between English and Swahili.
    
    This class uses the Google Cloud Translation API to translate text between
    English (en) and Swahili (sw).
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Translator with Google Cloud API credentials.
        
        Args:
            api_key: Optional Google Cloud API key. If not provided, will attempt
                    to use the GOOGLE_APPLICATION_CREDENTIALS environment variable.
        """
        if api_key:
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = api_key

        # Initialize the Google Cloud Translation client
        self.client = translate.Client()

        # Define supported languages
        self.supported_languages = {'en', 'sw'}

    def translate_text(self, text: str, target_language: str, source_language: Optional[str] = None) -> str:
        """
        Translate text to the target language.
        
        Args:
            text: The text to translate.
            target_language: The language code to translate to ('en' or 'sw').
            source_language: Optional language code of the source text.
                            If not provided, it will be auto-detected.
        
        Returns:
            The translated text.
            
        Raises:
            ValueError: If the target language is not supported.
        """
        if target_language not in self.supported_languages:
            raise ValueError(f"Target language '{target_language}' is not supported. "
                             f"Supported languages are: {', '.join(self.supported_languages)}")

        # Skip translation if the text is empty
        if not text:
            return text

        # Perform the translation
        result = self.client.translate(
            text,
            target_language=target_language,
            source_language=source_language
        )

        return result['translatedText']

    def translate_dict(self, data: Dict, target_language: str, source_language: Optional[str] = None) -> Dict:
        """
        Recursively translate all string values in a dictionary.
        
        Args:
            data: The dictionary containing strings to translate.
            target_language: The language code to translate to ('en' or 'sw').
            source_language: Optional language code of the source text.
        
        Returns:
            A new dictionary with all string values translated.
        """
        if not isinstance(data, dict):
            return data

        result = {}
        for key, value in data.items():
            if isinstance(value, str):
                result[key] = self.translate_text(value, target_language, source_language)
            elif isinstance(value, dict):
                result[key] = self.translate_dict(value, target_language, source_language)
            elif isinstance(value, list):
                result[key] = self.translate_list(value, target_language, source_language)
            else:
                result[key] = value

        return result

    def translate_list(self, data: List, target_language: str, source_language: Optional[str] = None) -> List:
        """
        Recursively translate all string values in a list.
        
        Args:
            data: The list containing strings to translate.
            target_language: The language code to translate to ('en' or 'sw').
            source_language: Optional language code of the source text.
        
        Returns:
            A new list with all string values translated.
        """
        if not isinstance(data, list):
            return data

        result = []
        for item in data:
            if isinstance(item, str):
                result.append(self.translate_text(item, target_language, source_language))
            elif isinstance(item, dict):
                result.append(self.translate_dict(item, target_language, source_language))
            elif isinstance(item, list):
                result.append(self.translate_list(item, target_language, source_language))
            else:
                result.append(item)

        return result

    def translate_survey_question(self, question: Dict, target_language: str) -> Dict:
        """
        Translate a survey question to the target language.
        
        This method assumes the question dictionary has a structure similar to
        the questions in survey_questions.json.
        
        Args:
            question: The question dictionary to translate.
            target_language: The language code to translate to ('en' or 'sw').
        
        Returns:
            A new dictionary with the question translated to the target language.
        """
        # Create a copy of the question to avoid modifying the original
        translated_question = question.copy()

        # If the question already has translations for the target language, use those
        if 'text' in question and isinstance(question['text'], dict) and target_language in question['text']:
            translated_question['text'] = question['text'][target_language]

        # If the question has options, translate those too
        if 'options' in question and isinstance(question['options'], list):
            translated_options = []
            for option in question['options']:
                translated_option = option.copy()
                if 'text' in option and isinstance(option['text'], dict) and target_language in option['text']:
                    translated_option['text'] = option['text'][target_language]
                translated_options.append(translated_option)
            translated_question['options'] = translated_options

        return translated_question

    def translate_survey(self, survey: Dict, target_language: str) -> Dict:
        """
        Translate an entire survey to the target language.
        
        This method assumes the survey dictionary has a structure similar to
        survey_questions.json.
        
        Args:
            survey: The survey dictionary to translate.
            target_language: The language code to translate to ('en' or 'sw').
        
        Returns:
            A new dictionary with the survey translated to the target language.
        """
        # Create a copy of the survey to avoid modifying the original
        translated_survey = survey.copy()

        # Translate the title and description
        if 'title' in survey and isinstance(survey['title'], dict) and target_language in survey['title']:
            translated_survey['title'] = survey['title'][target_language]

        if 'description' in survey and isinstance(survey['description'], dict) and target_language in survey[
            'description']:
            translated_survey['description'] = survey['description'][target_language]

        # Translate the questions
        if 'questions' in survey and isinstance(survey['questions'], list):
            translated_questions = []
            for question in survey['questions']:
                translated_question = self.translate_survey_question(question, target_language)
                translated_questions.append(translated_question)
            translated_survey['questions'] = translated_questions

        return translated_survey
