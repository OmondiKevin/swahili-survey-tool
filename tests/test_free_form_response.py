"""
Test script for free-form response processing.

This script tests the system's ability to process free-form responses without
requiring question IDs, particularly focusing on the example from the issue description.
"""

import sys
from pathlib import Path
from unittest.mock import patch

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from app.pipeline import Pipeline


def main():
    """Test free-form response processing."""
    # Mock the Translator class
    with patch('app.pipeline.Translator') as MockTranslator:
        # Configure the mock to return a specific translation for our example
        mock_translator_instance = MockTranslator.return_value
        mock_translator_instance.translate_text.return_value = "I am very happy with the service, it is very good."

        # Initialize the pipeline with the mocked Translator
        pipeline = Pipeline()

        # Replace the real translator with our mock
        pipeline.translator = mock_translator_instance

        # Load the survey
        survey_file = "data/survey_questions.json"
        pipeline.load_survey(survey_file)

    # Example from the issue description
    example_response = "Nimefurahi sana na huduma, ni nzuri kabisa"
    print(f"Processing example response: {example_response}")

    # Process the example response
    result = pipeline.process_free_form_response(example_response, language="sw")

    # Print the result
    print("\nResult:")
    print(f"Question ID: {result.get('question_id')}")
    print(f"Response: {result.get('response')}")
    print(f"Confidence: {result.get('confidence')}%")

    # Verify the result
    expected_question_id = "satisfaction_rating"
    expected_response = 5

    if result.get('question_id') == expected_question_id:
        print("\n✅ Successfully mapped to the correct question!")
    else:
        print(
            f"\n❌ Failed to map to the correct question. Expected {expected_question_id}, got {result.get('question_id')}")

    if result.get('response') == expected_response:
        print("✅ Successfully extracted the correct rating!")
    else:
        print(f"❌ Failed to extract the correct rating. Expected {expected_response}, got {result.get('response')}")

    # Print all available questions for reference
    print("\nAvailable questions:")
    for question in pipeline.question_mapper.survey.get('questions', []):
        print(f"ID: {question.get('id')}, Type: {question.get('type')}")
        if 'text' in question and isinstance(question['text'], dict):
            print(f"  Text (en): {question['text'].get('en')}")
            print(f"  Text (sw): {question['text'].get('sw')}")

    return result


if __name__ == "__main__":
    main()
