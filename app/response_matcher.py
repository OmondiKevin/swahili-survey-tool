"""
Response Matcher module for the Swahili Survey Engine.

This module provides functionality to automatically match free-form responses
to survey questions based on their content, and to structure the responses
according to the question type.
"""

import re
from typing import Dict, List, Any, Optional, Union, Tuple
import logging

# For NLP and semantic matching
try:
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
    ADVANCED_NLP_AVAILABLE = True
except ImportError:
    ADVANCED_NLP_AVAILABLE = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ResponseMatcher:
    """
    A class to handle matching free-form responses to survey questions
    and structuring the responses according to the question type.
    """
    
    def __init__(self, model_name: str = 'paraphrase-multilingual-MiniLM-L12-v2'):
        """
        Initialize the ResponseMatcher with a model for semantic matching.
        
        Args:
            model_name: Name of the sentence-transformers model to use for semantic matching.
                       Defaults to a multilingual model that supports both English and Swahili.
        """
        self.model = None
        self.model_name = model_name
        
        # Initialize the sentence transformer model if available
        if ADVANCED_NLP_AVAILABLE:
            try:
                self.model = SentenceTransformer(model_name)
                logger.info(f"Loaded sentence transformer model '{model_name}'")
            except Exception as e:
                logger.warning(f"Could not load sentence transformer model: {e}")
    
    def match_response_to_question(self, response: str, questions: List[Dict], language: str = 'en') -> Dict:
        """
        Match a free-form response to the most relevant survey question.
        
        Args:
            response: The free-form response text.
            questions: List of question dictionaries from the survey.
            language: The language of the response and questions ('en' or 'sw').
        
        Returns:
            A dictionary with the matched question ID, confidence score, and structured response.
        """
        if not response.strip():
            return {
                'question_id': None,
                'confidence': 0.0,
                'structured_response': None,
                'error': "Empty response"
            }
        
        if not questions:
            return {
                'question_id': None,
                'confidence': 0.0,
                'structured_response': None,
                'error': "No questions provided"
            }
        
        # If advanced NLP is available, use semantic matching
        if ADVANCED_NLP_AVAILABLE and self.model:
            return self._match_with_semantic_similarity(response, questions, language)
        
        # Otherwise, fall back to keyword matching
        return self._match_with_keywords(response, questions, language)
    
    def _match_with_semantic_similarity(self, response: str, questions: List[Dict], language: str) -> Dict:
        """
        Match a response to a question using semantic similarity with sentence embeddings.
        
        Args:
            response: The free-form response text.
            questions: List of question dictionaries from the survey.
            language: The language of the response and questions ('en' or 'sw').
        
        Returns:
            A dictionary with the matched question ID, confidence score, and structured response.
        """
        # Get the question texts in the specified language
        question_texts = []
        for question in questions:
            if 'text' in question and isinstance(question['text'], dict) and language in question['text']:
                question_texts.append(question['text'][language])
            else:
                question_texts.append(f"Question text not available in {language}")
        
        # Encode the response and questions
        response_embedding = self.model.encode([response])[0]
        question_embeddings = self.model.encode(question_texts)
        
        # Calculate cosine similarities
        similarities = cosine_similarity([response_embedding], question_embeddings)[0]
        
        # Find the most similar question
        best_match_idx = np.argmax(similarities)
        best_match_score = similarities[best_match_idx]
        best_match_question = questions[best_match_idx]
        
        # Structure the response according to the question type
        structured_response = self._structure_response(response, best_match_question, language)
        
        return {
            'question_id': best_match_question.get('id'),
            'confidence': float(best_match_score * 100),  # Convert to percentage
            'structured_response': structured_response,
            'error': None
        }
    
    def _match_with_keywords(self, response: str, questions: List[Dict], language: str) -> Dict:
        """
        Match a response to a question using keyword matching as a fallback.
        
        Args:
            response: The free-form response text.
            questions: List of question dictionaries from the survey.
            language: The language of the response and questions ('en' or 'sw').
        
        Returns:
            A dictionary with the matched question ID, confidence score, and structured response.
        """
        # Simple keyword matching
        best_match_score = 0.0
        best_match_question = None
        
        response_lower = response.lower()
        
        for question in questions:
            if 'text' in question and isinstance(question['text'], dict) and language in question['text']:
                question_text = question['text'][language].lower()
                
                # Count how many words from the question appear in the response
                question_words = set(re.findall(r'\w+', question_text))
                response_words = set(re.findall(r'\w+', response_lower))
                
                common_words = question_words.intersection(response_words)
                
                if common_words:
                    # Calculate a simple score based on word overlap
                    score = len(common_words) / len(question_words)
                    
                    if score > best_match_score:
                        best_match_score = score
                        best_match_question = question
        
        if best_match_question:
            # Structure the response according to the question type
            structured_response = self._structure_response(response, best_match_question, language)
            
            return {
                'question_id': best_match_question.get('id'),
                'confidence': best_match_score * 100,  # Convert to percentage
                'structured_response': structured_response,
                'error': None
            }
        
        return {
            'question_id': None,
            'confidence': 0.0,
            'structured_response': None,
            'error': "No matching question found"
        }
    
    def _structure_response(self, response: str, question: Dict, language: str) -> Any:
        """
        Structure a free-form response according to the question type.
        
        Args:
            response: The free-form response text.
            question: The matched question dictionary.
            language: The language of the response and question ('en' or 'sw').
        
        Returns:
            A structured response appropriate for the question type.
        """
        question_type = question.get('type')
        
        if question_type == 'multiple_choice':
            return self._structure_multiple_choice(response, question, language)
        
        elif question_type == 'yes_no':
            return self._structure_yes_no(response, language)
        
        elif question_type == 'rating':
            return self._structure_rating(response, language)
        
        else:  # open_ended or unknown
            return response
    
    def _structure_multiple_choice(self, response: str, question: Dict, language: str) -> str:
        """
        Structure a response for a multiple-choice question by finding the closest option.
        
        Args:
            response: The free-form response text.
            question: The multiple-choice question dictionary.
            language: The language of the response and options ('en' or 'sw').
        
        Returns:
            The ID of the closest matching option.
        """
        if 'options' not in question or not isinstance(question['options'], list):
            return response
        
        options = question['options']
        option_texts = []
        
        for option in options:
            if 'text' in option and isinstance(option['text'], dict) and language in option['text']:
                option_texts.append(option['text'][language])
            else:
                option_texts.append(f"Option text not available in {language}")
        
        # If advanced NLP is available, use semantic similarity
        if ADVANCED_NLP_AVAILABLE and self.model:
            # Encode the response and options
            response_embedding = self.model.encode([response])[0]
            option_embeddings = self.model.encode(option_texts)
            
            # Calculate cosine similarities
            similarities = cosine_similarity([response_embedding], option_embeddings)[0]
            
            # Find the most similar option
            best_match_idx = np.argmax(similarities)
            
            return options[best_match_idx].get('id')
        
        # Otherwise, fall back to keyword matching
        response_lower = response.lower()
        best_match_score = 0.0
        best_match_option = None
        
        for i, option_text in enumerate(option_texts):
            option_lower = option_text.lower()
            
            # Count how many words from the option appear in the response
            option_words = set(re.findall(r'\w+', option_lower))
            response_words = set(re.findall(r'\w+', response_lower))
            
            common_words = option_words.intersection(response_words)
            
            if common_words:
                # Calculate a simple score based on word overlap
                score = len(common_words) / len(option_words)
                
                if score > best_match_score:
                    best_match_score = score
                    best_match_option = options[i]
        
        if best_match_option:
            return best_match_option.get('id')
        
        return response
    
    def _structure_yes_no(self, response: str, language: str) -> str:
        """
        Structure a response for a yes/no question.
        
        Args:
            response: The free-form response text.
            language: The language of the response ('en' or 'sw').
        
        Returns:
            'yes', 'no', or the original response if unclear.
        """
        response_lower = response.lower()
        
        # English yes patterns
        yes_patterns_en = ['yes', 'yeah', 'yep', 'sure', 'definitely', 'absolutely', 'correct', 'right', 'true']
        
        # English no patterns
        no_patterns_en = ['no', 'nope', 'nah', 'not', 'never', 'negative', 'incorrect', 'wrong', 'false']
        
        # Swahili yes patterns
        yes_patterns_sw = ['ndio', 'ndiyo', 'naam', 'sawa', 'kweli']
        
        # Swahili no patterns
        no_patterns_sw = ['hapana', 'la', 'sio', 'si', 'siyo']
        
        # Check for yes patterns
        yes_patterns = yes_patterns_en + yes_patterns_sw
        for pattern in yes_patterns:
            if pattern in response_lower or response_lower.startswith(pattern):
                return 'yes'
        
        # Check for no patterns
        no_patterns = no_patterns_en + no_patterns_sw
        for pattern in no_patterns:
            if pattern in response_lower or response_lower.startswith(pattern):
                return 'no'
        
        # If unclear, return the original response
        return response
    
    def _structure_rating(self, response: str, language: str) -> int:
        """
        Structure a response for a rating question by extracting a numerical rating.
        
        Args:
            response: The free-form response text.
            language: The language of the response ('en' or 'sw').
        
        Returns:
            A numerical rating from 1 to 5, or None if no rating can be extracted.
        """
        # First, check for explicit numbers in the response
        numbers = re.findall(r'\d+', response)
        if numbers:
            # Get the first number and ensure it's between 1 and 5
            rating = int(numbers[0])
            return max(1, min(5, rating))
        
        # If no explicit numbers, analyze sentiment to determine rating
        
        # Positive sentiment words (English and Swahili)
        positive_words = {
            'excellent': 5, 'perfect': 5, 'amazing': 5, 'outstanding': 5, 'exceptional': 5,
            'great': 4, 'very good': 4, 'very happy': 4, 'very satisfied': 4,
            'good': 3, 'satisfied': 3, 'happy': 3, 'pleased': 3,
            'okay': 2, 'average': 2, 'fair': 2, 'moderate': 2,
            'poor': 1, 'bad': 1, 'terrible': 1, 'awful': 1, 'horrible': 1,
            
            # Swahili
            'bora sana': 5, 'nzuri sana': 5, 'nzuri kabisa': 5, 'furahi sana': 5,
            'nzuri': 3, 'wastani': 2, 'mbaya': 1
        }
        
        response_lower = response.lower()
        
        # Check for positive sentiment words
        best_rating = None
        for word, rating in positive_words.items():
            if word in response_lower:
                if best_rating is None or rating > best_rating:
                    best_rating = rating
        
        # If we found a rating based on sentiment, return it
        if best_rating is not None:
            return best_rating
        
        # Default to a neutral rating if we couldn't determine one
        return 3
    
    def process_response(self, response: str, survey: Dict, language: str = 'en') -> Dict:
        """
        Process a free-form response by matching it to a question and structuring it.
        
        Args:
            response: The free-form response text.
            survey: The survey dictionary containing questions.
            language: The language of the response and survey ('en' or 'sw').
        
        Returns:
            A dictionary with the matched question ID, confidence score, and structured response.
        """
        if not survey or 'questions' not in survey or not isinstance(survey['questions'], list):
            return {
                'question_id': None,
                'confidence': 0.0,
                'structured_response': None,
                'error': "Invalid survey format"
            }
        
        # Match the response to a question
        match_result = self.match_response_to_question(response, survey['questions'], language)
        
        return match_result