"""
Response Parser module for the Swahili Survey Engine.

This module provides functionality to parse, analyze, and categorize survey responses,
particularly focusing on open-ended responses that require natural language processing.
"""

import json
import os
import re
from collections import Counter
from typing import Dict, List, Tuple

# For more advanced NLP, we use sentence-transformers
try:
    from sentence_transformers import SentenceTransformer
    from sklearn.cluster import KMeans
    import numpy as np

    ADVANCED_NLP_AVAILABLE = True
except ImportError:
    ADVANCED_NLP_AVAILABLE = False


class ResponseParser:
    """
    A class to handle parsing and analyzing survey responses.
    
    This class provides methods to extract insights from survey responses,
    particularly focusing on open-ended responses that require text analysis.
    """

    def __init__(self, model_name: str = 'paraphrase-multilingual-MiniLM-L12-v2'):
        """
        Initialize the ResponseParser with an optional model for text embedding.
        
        Args:
            model_name: Name of the sentence-transformers model to use for text embedding.
                       Defaults to a multilingual model that supports both English and Swahili.
        """
        self.responses = []
        self.model = None
        self.model_name = model_name

        # Initialize the sentence transformer model if available
        if ADVANCED_NLP_AVAILABLE:
            try:
                self.model = SentenceTransformer(model_name)
            except Exception as e:
                print(f"Warning: Could not load sentence transformer model: {e}")

    def load_responses(self, responses_file: str) -> List[Dict]:
        """
        Load survey responses from a JSON file.
        
        Args:
            responses_file: Path to a JSON file containing survey responses.
        
        Returns:
            The loaded responses as a list of dictionaries.
            
        Raises:
            FileNotFoundError: If the responses file does not exist.
            json.JSONDecodeError: If the responses file is not valid JSON.
        """
        if not os.path.exists(responses_file):
            raise FileNotFoundError(f"Responses file not found: {responses_file}")

        with open(responses_file, 'r', encoding='utf-8') as f:
            self.responses = json.load(f)

        return self.responses

    def add_response(self, response: Dict) -> None:
        """
        Add a single response to the current set of responses.
        
        Args:
            response: A dictionary containing a survey response.
        """
        self.responses.append(response)

    def get_responses_for_question(self, question_id: str) -> List[str]:
        """
        Get all responses for a specific question.
        
        Args:
            question_id: The ID of the question to get responses for.
        
        Returns:
            A list of response strings for the specified question.
        """
        return [r.get('response', '') for r in self.responses
                if r.get('question_id') == question_id and r.get('valid', False)]

    def count_multiple_choice_responses(self, question_id: str) -> Dict[str, int]:
        """
        Count the frequency of each option in multiple-choice responses.
        
        Args:
            question_id: The ID of the multiple-choice question to analyze.
        
        Returns:
            A dictionary mapping option IDs to their frequency counts.
        """
        responses = self.get_responses_for_question(question_id)
        return dict(Counter(responses))

    def count_yes_no_responses(self, question_id: str) -> Dict[str, int]:
        """
        Count the frequency of 'yes' and 'no' responses.
        
        Args:
            question_id: The ID of the yes/no question to analyze.
        
        Returns:
            A dictionary with counts for 'yes' and 'no' responses.
        """
        responses = self.get_responses_for_question(question_id)

        # Normalize responses to lowercase and map Swahili responses
        normalized_responses = []
        for response in responses:
            response = response.lower()
            if response in ['ndio', 'ndiyo']:
                normalized_responses.append('yes')
            elif response in ['hapana', 'la']:
                normalized_responses.append('no')
            else:
                normalized_responses.append(response)

        return dict(Counter(normalized_responses))

    def extract_keywords(self, text: str, top_n: int = 5) -> List[Tuple[str, int]]:
        """
        Extract the most frequent keywords from a text.
        
        Args:
            text: The text to extract keywords from.
            top_n: The number of top keywords to return.
        
        Returns:
            A list of (keyword, frequency) tuples, sorted by frequency.
        """
        # Remove punctuation and convert to lowercase
        text = re.sub(r'[^\w\s]', '', text.lower())

        # Split into words
        words = text.split()

        # Remove common stop words (English and Swahili)
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'if', 'because', 'as', 'what',
            'which', 'this', 'that', 'these', 'those', 'then', 'just', 'so', 'than',
            'such', 'both', 'through', 'about', 'for', 'is', 'of', 'while', 'during',
            'to', 'na', 'kwa', 'ya', 'za', 'la', 'ni', 'wa', 'katika', 'kama', 'hii',
            'hizi', 'huo', 'hizo', 'huu', 'ile', 'zile', 'ule', 'hiyo', 'hilo', 'hayo'
        }

        filtered_words = [word for word in words if word not in stop_words and len(word) > 1]

        # Count word frequencies
        word_counts = Counter(filtered_words)

        # Return the top N keywords
        return word_counts.most_common(top_n)

    def analyze_open_ended_responses(self, question_id: str, top_keywords: int = 5) -> Dict:
        """
        Analyze open-ended responses to extract keywords and themes.
        
        Args:
            question_id: The ID of the open-ended question to analyze.
            top_keywords: The number of top keywords to extract.
        
        Returns:
            A dictionary with analysis results, including top keywords and themes.
        """
        responses = self.get_responses_for_question(question_id)

        if not responses:
            return {'keywords': [], 'themes': [], 'response_count': 0}

        # Combine all responses into a single text for keyword extraction
        combined_text = ' '.join(responses)

        # Extract top keywords
        keywords = self.extract_keywords(combined_text, top_keywords)

        # Extract themes using clustering if advanced NLP is available
        themes = []
        if ADVANCED_NLP_AVAILABLE and self.model and len(responses) >= 3:
            themes = self._extract_themes_with_clustering(responses)

        return {
            'keywords': keywords,
            'themes': themes,
            'response_count': len(responses)
        }

    def _extract_themes_with_clustering(self, texts: List[str], num_clusters: int = 3) -> List[Dict]:
        """
        Extract themes from texts using sentence embeddings and clustering.
        
        Args:
            texts: List of text responses to analyze.
            num_clusters: Number of themes/clusters to extract.
        
        Returns:
            A list of dictionaries, each representing a theme with example responses.
        """
        if not self.model:
            return []

        # Adjust number of clusters if we have few responses
        num_clusters = min(num_clusters, len(texts) // 2) if len(texts) > 3 else 1

        # Encode the texts to get embeddings
        embeddings = self.model.encode(texts)

        # Perform clustering
        kmeans = KMeans(n_clusters=num_clusters, random_state=42)
        clusters = kmeans.fit_predict(embeddings)

        # Group texts by cluster
        clustered_texts = {}
        for i, cluster_id in enumerate(clusters):
            if cluster_id not in clustered_texts:
                clustered_texts[cluster_id] = []
            clustered_texts[cluster_id].append(texts[i])

        # Create theme summaries
        themes = []
        for cluster_id, cluster_texts in clustered_texts.items():
            # Get a few example texts from this cluster
            examples = cluster_texts[:3]

            # Extract keywords from this cluster
            combined_text = ' '.join(cluster_texts)
            keywords = [k for k, _ in self.extract_keywords(combined_text, 5)]

            themes.append({
                'id': f"theme_{cluster_id}",
                'keywords': keywords,
                'examples': examples,
                'response_count': len(cluster_texts)
            })

        return themes

    def generate_summary_report(self) -> Dict:
        """
        Generate a summary report of all survey responses.
        
        Returns:
            A dictionary with summary statistics for each question.
        """
        if not self.responses:
            return {'questions': [], 'total_responses': 0}

        # Group responses by question ID
        questions = {}
        for response in self.responses:
            question_id = response.get('question_id')
            if not question_id:
                continue

            if question_id not in questions:
                questions[question_id] = {
                    'id': question_id,
                    'type': response.get('question_type', 'unknown'),
                    'responses': []
                }

            if response.get('valid', False):
                questions[question_id]['responses'].append(response.get('response', ''))

        # Analyze each question based on its type
        summary = {'questions': [], 'total_responses': len(self.responses)}

        for question_id, question_data in questions.items():
            question_summary = {
                'id': question_id,
                'type': question_data['type'],
                'response_count': len(question_data['responses'])
            }

            if question_data['type'] == 'multiple_choice':
                question_summary['option_counts'] = dict(Counter(question_data['responses']))

            elif question_data['type'] == 'yes_no':
                # Normalize yes/no responses
                normalized = []
                for resp in question_data['responses']:
                    resp = resp.lower()
                    if resp in ['ndio', 'ndiyo']:
                        normalized.append('yes')
                    elif resp in ['hapana', 'la']:
                        normalized.append('no')
                    else:
                        normalized.append(resp)

                question_summary['counts'] = dict(Counter(normalized))

            elif question_data['type'] == 'open_ended':
                # For open-ended, provide keyword analysis
                combined_text = ' '.join(question_data['responses'])
                question_summary['keywords'] = self.extract_keywords(combined_text, 10)

                # Add theme analysis if available
                if ADVANCED_NLP_AVAILABLE and self.model and len(question_data['responses']) >= 3:
                    question_summary['themes'] = self._extract_themes_with_clustering(
                        question_data['responses']
                    )

            summary['questions'].append(question_summary)

        return summary

    def save_responses(self, output_file: str) -> None:
        """
        Save the current responses to a JSON file.
        
        Args:
            output_file: Path to the output JSON file.
            
        Raises:
            ValueError: If no responses are loaded.
        """
        if not self.responses:
            raise ValueError("No responses loaded to save")

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.responses, f, indent=2, ensure_ascii=False)

    def save_summary_report(self, output_file: str) -> None:
        """
        Generate and save a summary report to a JSON file.
        
        Args:
            output_file: Path to the output JSON file.
            
        Raises:
            ValueError: If no responses are loaded.
        """
        if not self.responses:
            raise ValueError("No responses loaded to save")

        summary = self.generate_summary_report()

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
