"""
Question Mapper module for the Swahili Survey Engine.

This module provides functionality to map survey questions between different formats
and structures, particularly focusing on mapping between the internal JSON format
and formats suitable for presentation or processing.
"""

import json
import os
from typing import Dict, List, Optional


class QuestionMapper:
    """
    A class to handle mapping survey questions between different formats.
    
    This class provides methods to load survey questions from JSON files,
    map them to different formats, and filter questions based on various criteria.
    """

    def __init__(self, survey_file: Optional[str] = None):
        """
        Initialize the QuestionMapper with an optional survey file.
        
        Args:
            survey_file: Optional path to a JSON file containing survey questions.
                        If provided, the survey will be loaded during initialization.
        """
        self.survey = None

        if survey_file:
            self.load_survey(survey_file)

    def load_survey(self, survey_file: str) -> Dict:
        """
        Load a survey from a JSON file.
        
        Args:
            survey_file: Path to a JSON file containing survey questions.
        
        Returns:
            The loaded survey as a dictionary.
            
        Raises:
            FileNotFoundError: If the survey file does not exist.
            json.JSONDecodeError: If the survey file is not valid JSON.
        """
        if not os.path.exists(survey_file):
            raise FileNotFoundError(f"Survey file not found: {survey_file}")

        with open(survey_file, 'r', encoding='utf-8') as f:
            self.survey = json.load(f)

        return self.survey

    def get_question_by_id(self, question_id: str) -> Optional[Dict]:
        """
        Get a question from the loaded survey by its ID.
        
        Args:
            question_id: The ID of the question to retrieve.
        
        Returns:
            The question dictionary, or None if not found.
        """
        if not self.survey or 'questions' not in self.survey:
            return None

        for question in self.survey['questions']:
            if question.get('id') == question_id:
                return question

        return None

    def get_questions_by_type(self, question_type: str) -> List[Dict]:
        """
        Get all questions of a specific type from the loaded survey.
        
        Args:
            question_type: The type of questions to retrieve (e.g., 'multiple_choice', 'open_ended').
        
        Returns:
            A list of question dictionaries of the specified type.
        """
        if not self.survey or 'questions' not in self.survey:
            return []

        return [q for q in self.survey['questions'] if q.get('type') == question_type]

    def map_to_simple_format(self, language: str = 'en') -> List[Dict]:
        """
        Map the loaded survey to a simplified format with just question text and options.
        
        Args:
            language: The language code to use for the question text and options ('en' or 'sw').
        
        Returns:
            A list of simplified question dictionaries.
        """
        if not self.survey or 'questions' not in self.survey:
            return []

        simple_questions = []
        for question in self.survey['questions']:
            simple_question = {
                'id': question.get('id'),
                'type': question.get('type')
            }

            # Get the question text in the specified language
            if 'text' in question and isinstance(question['text'], dict) and language in question['text']:
                simple_question['text'] = question['text'][language]
            else:
                simple_question['text'] = f"Question text not available in {language}"

            # If the question has options, include them in the simplified format
            if 'options' in question and isinstance(question['options'], list):
                simple_options = []
                for option in question['options']:
                    simple_option = {'id': option.get('id')}
                    if 'text' in option and isinstance(option['text'], dict) and language in option['text']:
                        simple_option['text'] = option['text'][language]
                    else:
                        simple_option['text'] = f"Option text not available in {language}"
                    simple_options.append(simple_option)
                simple_question['options'] = simple_options

            simple_questions.append(simple_question)

        return simple_questions

    def map_to_presentation_format(self, language: str = 'en') -> Dict:
        """
        Map the loaded survey to a format suitable for presentation in a UI.
        
        Args:
            language: The language code to use for the presentation ('en' or 'sw').
        
        Returns:
            A dictionary with the survey in a presentation-friendly format.
        """
        if not self.survey:
            return {}

        presentation = {
            'survey_id': self.survey.get('survey_id', ''),
            'language': language
        }

        # Get the title in the specified language
        if 'title' in self.survey and isinstance(self.survey['title'], dict) and language in self.survey['title']:
            presentation['title'] = self.survey['title'][language]
        else:
            presentation['title'] = f"Survey title not available in {language}"

        # Get the description in the specified language
        if 'description' in self.survey and isinstance(self.survey['description'], dict) and language in self.survey[
            'description']:
            presentation['description'] = self.survey['description'][language]
        else:
            presentation['description'] = f"Survey description not available in {language}"

        # Map the questions to a presentation-friendly format
        presentation['questions'] = self.map_to_simple_format(language)

        return presentation

    def map_response_to_question(self, response: str, question_id: str) -> Dict:
        """
        Map a response to a specific question, validating it against the question type.
        
        Args:
            response: The response text or option ID.
            question_id: The ID of the question being responded to.
        
        Returns:
            A dictionary with the mapped response and validation status.
            
        Raises:
            ValueError: If the question is not found or the response is invalid for the question type.
        """
        question = self.get_question_by_id(question_id)
        if not question:
            raise ValueError(f"Question with ID '{question_id}' not found")

        result = {
            'question_id': question_id,
            'response': response,
            'valid': False,
            'error': None
        }

        question_type = question.get('type')

        # Validate the response based on the question type
        if question_type == 'multiple_choice':
            # For multiple choice, the response should be one of the option IDs
            valid_option_ids = [opt.get('id') for opt in question.get('options', [])]
            if response in valid_option_ids:
                result['valid'] = True
            else:
                result['error'] = f"Invalid option ID. Valid options are: {', '.join(valid_option_ids)}"

        elif question_type == 'yes_no':
            # For yes/no, the response should be 'yes' or 'no' (case insensitive)
            if response.lower() in ['yes', 'no', 'ndio', 'hapana']:
                result['valid'] = True
            else:
                result['error'] = "Invalid response. Expected 'yes' or 'no' (or 'ndio' or 'hapana' in Swahili)"

        elif question_type == 'open_ended':
            # For open-ended questions, any non-empty response is valid
            if response.strip():
                result['valid'] = True
            else:
                result['error'] = "Response cannot be empty"

        else:
            result['error'] = f"Unknown question type: {question_type}"

        return result

    def save_survey(self, output_file: str) -> None:
        """
        Save the current survey to a JSON file.
        
        Args:
            output_file: Path to the output JSON file.
            
        Raises:
            ValueError: If no survey is loaded.
        """
        if not self.survey:
            raise ValueError("No survey loaded to save")

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.survey, f, indent=2, ensure_ascii=False)
