"""
Pipeline module for the Swahili Survey Engine.

This module provides a pipeline that orchestrates the flow between all components
of the Swahili Survey Engine, including translation, question mapping, ASR, and
response parsing.
"""

import os
import json
from typing import Dict, List, Any, Optional, Union
import logging

from app.translator import Translator
from app.question_mapper import QuestionMapper
from app.response_parser import ResponseParser
from app.asr import ASR
from app.response_matcher import ResponseMatcher

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Pipeline:
    """
    A class to orchestrate the flow between all components of the Swahili Survey Engine.

    This class provides methods to process surveys end-to-end, from loading questions
    to analyzing responses, with support for both text and audio responses.
    """

    def __init__(self, 
                 survey_file: Optional[str] = None,
                 translator_api_key: Optional[str] = None,
                 asr_model_size: str = "base"):
        """
        Initialize the Pipeline with optional components.

        Args:
            survey_file: Optional path to a JSON file containing survey questions.
                        If provided, the survey will be loaded during initialization.
            translator_api_key: Optional Google Cloud API key for translation.
            asr_model_size: Size of the Whisper model to use for ASR.
        """
        # Initialize components
        self.translator = Translator(api_key=translator_api_key)
        self.question_mapper = QuestionMapper(survey_file=survey_file)
        self.response_parser = ResponseParser()
        self.asr = ASR(model_size=asr_model_size)
        self.response_matcher = ResponseMatcher()

        # Store the survey file path
        self.survey_file = survey_file

        # Initialize storage for responses
        self.responses = []

        logger.info("Pipeline initialized")

    def load_survey(self, survey_file: str) -> Dict:
        """
        Load a survey from a JSON file.

        Args:
            survey_file: Path to a JSON file containing survey questions.

        Returns:
            The loaded survey as a dictionary.
        """
        logger.info(f"Loading survey from {survey_file}")
        self.survey_file = survey_file
        return self.question_mapper.load_survey(survey_file)

    def translate_survey(self, target_language: str) -> Dict:
        """
        Translate the loaded survey to the target language.

        Args:
            target_language: The language code to translate to ('en' or 'sw').

        Returns:
            A new dictionary with the survey translated to the target language.
        """
        logger.info(f"Translating survey to {target_language}")
        if not self.question_mapper.survey:
            raise ValueError("No survey loaded to translate")

        return self.translator.translate_survey(self.question_mapper.survey, target_language)

    def get_survey_presentation(self, language: str = 'en') -> Dict:
        """
        Get a presentation-friendly version of the survey in the specified language.

        Args:
            language: The language code to use for the presentation ('en' or 'sw').

        Returns:
            A dictionary with the survey in a presentation-friendly format.
        """
        logger.info(f"Getting survey presentation in {language}")
        if not self.question_mapper.survey:
            raise ValueError("No survey loaded to present")

        return self.question_mapper.map_to_presentation_format(language)

    def process_text_response(self, response: str, question_id: str) -> Dict:
        """
        Process a text response to a survey question.

        Args:
            response: The text response.
            question_id: The ID of the question being responded to.

        Returns:
            A dictionary with the processed response and validation status.
        """
        logger.info(f"Processing text response for question {question_id}")
        # Map and validate the response
        mapped_response = self.question_mapper.map_response_to_question(response, question_id)

        # Add the response to our collection
        self.responses.append(mapped_response)

        return mapped_response

    def process_free_form_response(self, response: str, language: str = "sw") -> Dict:
        """
        Process a free-form response without requiring a question ID.

        This method automatically determines which question the response is answering
        based on the content of the response.

        Args:
            response: The free-form response text.
            language: Language code for the response. Default is "sw" for Swahili.

        Returns:
            A dictionary with the matched question ID, confidence score, and structured response.
        """
        logger.info(f"Processing free-form response: {response[:50]}...")

        if not self.question_mapper.survey:
            raise ValueError("No survey loaded to match response against")

        # If the response is in Swahili and we want to process in English, translate it
        if language == "sw" and language != "en":
            translated_response = self.translator.translate_text(response, "en", "sw")
            logger.info(f"Translated response: {translated_response[:50]}...")

            # Match the response to a question and structure it
            match_result = self.response_matcher.process_response(
                translated_response, 
                self.question_mapper.survey, 
                "en"
            )
        else:
            # Match the response to a question and structure it
            match_result = self.response_matcher.process_response(
                response, 
                self.question_mapper.survey, 
                language
            )

        # Create a response object in the format expected by the rest of the pipeline
        processed_response = {
            'question_id': match_result.get('question_id'),
            'response': match_result.get('structured_response'),
            'valid': match_result.get('question_id') is not None,
            'error': match_result.get('error'),
            'confidence': match_result.get('confidence')
        }

        # Add the response to our collection
        self.responses.append(processed_response)

        return processed_response

    def process_audio_response(self, audio_file: str, question_id: str, language: str = "sw") -> Dict:
        """
        Process an audio response to a survey question.

        Args:
            audio_file: Path to the audio file containing the response.
            question_id: The ID of the question being responded to.
            language: Language code for the audio. Default is "sw" for Swahili.

        Returns:
            A dictionary with the transcribed response and validation status.
        """
        logger.info(f"Processing audio response for question {question_id}")
        # Transcribe the audio
        transcription = self.asr.transcribe_audio(audio_file, language)
        text_response = transcription.get('text', '')

        # Map and validate the response
        mapped_response = self.question_mapper.map_response_to_question(text_response, question_id)
        mapped_response['audio_file'] = audio_file

        # Add the response to our collection
        self.responses.append(mapped_response)

        return mapped_response

    def process_free_form_audio_response(self, audio_file: str, language: str = "sw") -> Dict:
        """
        Process a free-form audio response without requiring a question ID.

        This method automatically determines which question the response is answering
        based on the content of the transcribed audio.

        Args:
            audio_file: Path to the audio file containing the response.
            language: Language code for the audio. Default is "sw" for Swahili.

        Returns:
            A dictionary with the matched question ID, confidence score, and structured response.
        """
        logger.info(f"Processing free-form audio response from {audio_file}")

        if not self.question_mapper.survey:
            raise ValueError("No survey loaded to match response against")

        # Transcribe the audio
        transcription = self.asr.transcribe_audio(audio_file, language)
        text_response = transcription.get('text', '')

        logger.info(f"Transcribed text: {text_response[:50]}...")

        # Process the transcribed text as a free-form response
        processed_response = self.process_free_form_response(text_response, language)

        # Add the audio file information
        processed_response['audio_file'] = audio_file

        return processed_response

    def batch_process_audio_responses(self, audio_files: List[str], question_ids: List[str], language: str = "sw") -> List[Dict]:
        """
        Process multiple audio responses to survey questions.

        Args:
            audio_files: List of paths to audio files containing responses.
            question_ids: List of question IDs corresponding to each audio file.
            language: Language code for the audio. Default is "sw" for Swahili.

        Returns:
            A list of dictionaries with transcribed responses and validation statuses.
        """
        logger.info(f"Batch processing {len(audio_files)} audio responses")
        # Transcribe all audio files
        transcribed_responses = self.asr.transcribe_to_responses(audio_files, question_ids, language)

        # Map and validate each response
        mapped_responses = []
        for i, response in enumerate(transcribed_responses):
            question_id = response['question_id']
            text_response = response['response']

            try:
                mapped_response = self.question_mapper.map_response_to_question(text_response, question_id)
                mapped_response['audio_file'] = audio_files[i]
                mapped_responses.append(mapped_response)

                # Add the response to our collection
                self.responses.append(mapped_response)
            except Exception as e:
                logger.error(f"Error mapping response for question {question_id}: {e}")
                mapped_responses.append({
                    'question_id': question_id,
                    'response': text_response,
                    'valid': False,
                    'error': str(e),
                    'audio_file': audio_files[i]
                })

        return mapped_responses

    def process_directory_of_audio_responses(self, directory: str, naming_pattern: str = r'q(\d+)_.*\.wav', language: str = "sw") -> List[Dict]:
        """
        Process all audio files in a directory as survey responses.

        Args:
            directory: Path to the directory containing audio files.
            naming_pattern: Regex pattern to extract question IDs from filenames.
                           Default pattern expects filenames like 'q1_response.wav'.
            language: Language code for the audio. Default is "sw" for Swahili.

        Returns:
            A list of dictionaries with transcribed responses and validation statuses.
        """
        import re

        logger.info(f"Processing audio responses from directory {directory}")
        if not os.path.exists(directory):
            raise FileNotFoundError(f"Directory not found: {directory}")

        # Get all audio files in the directory
        audio_files = []
        question_ids = []

        for root, _, files in os.walk(directory):
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in ['.wav', '.mp3', '.flac', '.m4a', '.ogg']:
                    # Try to extract question ID from filename
                    match = re.search(naming_pattern, file)
                    if match:
                        question_id = f"q{match.group(1)}"
                        audio_files.append(os.path.join(root, file))
                        question_ids.append(question_id)
                    else:
                        logger.warning(f"Could not extract question ID from filename: {file}")

        if not audio_files:
            logger.warning(f"No audio files found in directory: {directory}")
            return []

        # Process the audio files
        return self.batch_process_audio_responses(audio_files, question_ids, language)

    def analyze_responses(self) -> Dict:
        """
        Analyze all collected responses to generate insights.

        Returns:
            A dictionary with analysis results for each question.
        """
        logger.info("Analyzing responses")
        # Add all responses to the response parser
        for response in self.responses:
            self.response_parser.add_response(response)

        # Generate a summary report
        return self.response_parser.generate_summary_report()

    def save_responses(self, output_file: str) -> None:
        """
        Save all collected responses to a JSON file.

        Args:
            output_file: Path to the output JSON file.
        """
        logger.info(f"Saving responses to {output_file}")
        # Add all responses to the response parser if not already added
        for response in self.responses:
            if response not in self.response_parser.responses:
                self.response_parser.add_response(response)

        # Save the responses
        self.response_parser.save_responses(output_file)

    def save_analysis(self, output_file: str) -> None:
        """
        Generate and save an analysis report to a JSON file.

        Args:
            output_file: Path to the output JSON file.
        """
        logger.info(f"Saving analysis to {output_file}")
        # Add all responses to the response parser if not already added
        for response in self.responses:
            if response not in self.response_parser.responses:
                self.response_parser.add_response(response)

        # Save the analysis
        self.response_parser.save_summary_report(output_file)

    def run_full_pipeline(self, 
                         survey_file: str,
                         audio_directory: Optional[str] = None,
                         text_responses: Optional[Dict[str, str]] = None,
                         output_dir: str = 'data/outputs',
                         language: str = 'sw',
                         free_form: bool = False) -> Dict:
        """
        Run the full pipeline from loading the survey to analyzing responses.

        Args:
            survey_file: Path to the JSON file containing survey questions.
            audio_directory: Optional path to a directory containing audio responses.
            text_responses: Optional dictionary mapping question IDs to text responses.
            output_dir: Directory to save output files.
            language: Language code for processing. Default is "sw" for Swahili.
            free_form: If True, process all responses as free-form responses without
                      requiring question IDs. Default is False.

        Returns:
            A dictionary with the analysis results.
        """
        logger.info(f"Running full pipeline with survey {survey_file}")
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Load the survey
        self.load_survey(survey_file)

        # Process audio responses if provided
        if audio_directory:
            if free_form:
                # Process audio files as free-form responses
                logger.info(f"Processing audio files in {audio_directory} as free-form responses")
                audio_files = []

                # Get all audio files in the directory
                for root, _, files in os.walk(audio_directory):
                    for file in files:
                        ext = os.path.splitext(file)[1].lower()
                        if ext in ['.wav', '.mp3', '.flac', '.m4a', '.ogg']:
                            audio_files.append(os.path.join(root, file))

                # Process each audio file as a free-form response
                for audio_file in audio_files:
                    self.process_free_form_audio_response(audio_file, language)
            else:
                # Process audio files with question IDs from filenames
                self.process_directory_of_audio_responses(audio_directory, language=language)

        # Process text responses if provided
        if text_responses:
            if free_form:
                # Process text responses as free-form responses
                logger.info("Processing text responses as free-form responses")
                for response in text_responses.values():
                    self.process_free_form_response(response, language)
            else:
                # Process text responses with question IDs
                for question_id, response in text_responses.items():
                    self.process_text_response(response, question_id)

        # Analyze the responses
        analysis = self.analyze_responses()

        # Save the responses and analysis
        self.save_responses(os.path.join(output_dir, 'responses.json'))
        self.save_analysis(os.path.join(output_dir, 'analysis.json'))

        return analysis
