#!/usr/bin/env python3
"""
Main entry point for the Swahili Survey Engine.

This script provides a command-line interface to run the survey processing pipeline.
"""

import os
import sys
import json
import argparse
import logging
from typing import Dict, List, Optional

from app.pipeline import Pipeline

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description='Swahili Survey Engine')

    parser.add_argument('--survey', '-s', type=str, required=True,
                        help='Path to the survey questions JSON file')

    parser.add_argument('--audio-dir', '-a', type=str,
                        help='Path to directory containing audio responses')

    parser.add_argument('--text-responses', '-t', type=str,
                        help='Path to JSON file containing text responses')

    parser.add_argument('--output-dir', '-o', type=str, default='data/outputs',
                        help='Directory to save output files')

    parser.add_argument('--language', '-l', type=str, default='sw',
                        choices=['en', 'sw'],
                        help='Language for processing (en or sw)')

    parser.add_argument('--translator-key', '-k', type=str,
                        help='Google Cloud API key for translation')

    parser.add_argument('--asr-model', '-m', type=str, default='base',
                        choices=['tiny', 'base', 'small', 'medium', 'large'],
                        help='Whisper model size for ASR')

    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Enable verbose logging')

    parser.add_argument('--free-form', '-f', action='store_true',
                        help='Process responses as free-form without requiring question IDs')

    return parser.parse_args()

def load_text_responses(file_path: str) -> Dict[str, str]:
    """
    Load text responses from a JSON file.

    Args:
        file_path: Path to the JSON file containing text responses.

    Returns:
        A dictionary mapping question IDs to text responses.
    """
    if not os.path.exists(file_path):
        logger.error(f"Text responses file not found: {file_path}")
        sys.exit(1)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            responses = json.load(f)

        # Validate the format
        if not isinstance(responses, dict):
            logger.error(f"Invalid format in text responses file. Expected a dictionary mapping question IDs to responses.")
            sys.exit(1)

        return responses

    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in text responses file: {file_path}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error loading text responses: {e}")
        sys.exit(1)

def main():
    """Main entry point for the application."""
    args = parse_arguments()

    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Initialize the pipeline
    pipeline = Pipeline(
        translator_api_key=args.translator_key,
        asr_model_size=args.asr_model
    )

    # Load text responses if provided
    text_responses = None
    if args.text_responses:
        text_responses = load_text_responses(args.text_responses)

    try:
        # Run the full pipeline
        analysis = pipeline.run_full_pipeline(
            survey_file=args.survey,
            audio_directory=args.audio_dir,
            text_responses=text_responses,
            output_dir=args.output_dir,
            language=args.language,
            free_form=args.free_form
        )

        # Print a summary of the analysis
        print("\nSurvey Analysis Summary:")
        print(f"Total responses: {analysis.get('total_responses', 0)}")

        for question in analysis.get('questions', []):
            print(f"\nQuestion {question.get('id')}: ({question.get('type')})")
            print(f"Response count: {question.get('response_count', 0)}")

            if question.get('type') == 'multiple_choice':
                print("Option counts:")
                for option, count in question.get('option_counts', {}).items():
                    print(f"  {option}: {count}")

            elif question.get('type') == 'yes_no':
                counts = question.get('counts', {})
                yes_count = counts.get('yes', 0)
                no_count = counts.get('no', 0)
                print(f"Yes: {yes_count}, No: {no_count}")

            elif question.get('type') == 'open_ended':
                print("Top keywords:")
                for keyword, count in question.get('keywords', [])[:5]:
                    print(f"  {keyword}: {count}")

        print(f"\nDetailed results saved to {args.output_dir}")

    except Exception as e:
        logger.error(f"Error running pipeline: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
