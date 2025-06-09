# Swahili Survey Engine

A comprehensive engine for processing surveys in both English and Swahili, with support for text and audio responses.

## Overview

The Swahili Survey Engine is a Python-based application that provides end-to-end functionality for creating,
translating, and processing surveys in both English and Swahili. It supports multiple question types, text and audio
responses, and provides advanced analysis of survey results.

### Key Features

- **Bilingual Support**: Full support for both English and Swahili languages
- **Translation**: Automatic translation between English and Swahili using Google Cloud Translation API
- **Audio Processing**: Transcription of audio responses using OpenAI's Whisper model
- **Response Analysis**: Advanced analysis of survey responses, including keyword extraction and theme clustering
- **Multiple Question Types**: Support for multiple-choice, yes/no, and open-ended questions
- **Comprehensive Pipeline**: End-to-end processing from survey creation to response analysis

## Components

The engine consists of several key components:

1. **Translator**: Handles translation between English and Swahili using Google Cloud Translation API
2. **Question Mapper**: Maps survey questions between different formats and structures
3. **Response Parser**: Parses and analyzes survey responses, particularly open-ended responses
4. **ASR (Automatic Speech Recognition)**: Transcribes audio responses using OpenAI's Whisper model
5. **Pipeline**: Orchestrates the flow between all components to provide a complete survey processing pipeline

## Installation

### Prerequisites

- Python 3.8 or higher
- Google Cloud API key (for translation)
- Internet connection (for downloading models)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/swahili_survey_engine.git
   cd swahili_survey_engine
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up Google Cloud API credentials (for translation):
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/credentials.json"
   ```

## Usage

### Command Line Interface

The engine provides a command-line interface through the `run_pipeline.py` script:

```bash
python run_pipeline.py --survey data/survey_questions.json --output-dir data/outputs
```

#### Command Line Options

- `--survey`, `-s`: Path to the survey questions JSON file (required)
- `--audio-dir`, `-a`: Path to directory containing audio responses
- `--text-responses`, `-t`: Path to JSON file containing text responses
- `--output-dir`, `-o`: Directory to save output files (default: 'data/outputs')
- `--language`, `-l`: Language for processing ('en' or 'sw', default: 'sw')
- `--translator-key`, `-k`: Google Cloud API key for translation
- `--asr-model`, `-m`: Whisper model size for ASR ('tiny', 'base', 'small', 'medium', 'large', default: 'base')
- `--verbose`, `-v`: Enable verbose logging

### Programmatic Usage

You can also use the engine programmatically in your Python code:

```python
from app.pipeline import Pipeline

# Initialize the pipeline
pipeline = Pipeline(
   translator_api_key="your_api_key",
   asr_model_size="base"
)

# Run the full pipeline
analysis = pipeline.run_full_pipeline(
   survey_file="data/survey_questions.json",
   audio_directory="data/audio_samples",
   text_responses={"q1": "response1", "q2": "response2"},
   output_dir="data/outputs",
   language="sw"
)

# Print the analysis results
print(analysis)
```

## Survey Format

Surveys are defined in JSON format with the following structure:

```json
{
   "survey_id": "swahili_health_survey_2023",
   "title": {
      "en": "Health Survey 2023",
      "sw": "Uchunguzi wa Afya 2023"
   },
   "description": {
      "en": "This survey collects information about health practices.",
      "sw": "Uchunguzi huu hukusanya taarifa kuhusu mazoea ya afya."
   },
   "questions": [
      {
         "id": "q1",
         "type": "multiple_choice",
         "text": {
            "en": "How would you rate your overall health?",
            "sw": "Unawezaje kukadiria afya yako kwa ujumla?"
         },
         "options": [
            {
               "id": "q1_opt1",
               "text": {
                  "en": "Excellent",
                  "sw": "Bora sana"
               }
            },
            {
               "id": "q1_opt2",
               "text": {
                  "en": "Good",
                  "sw": "Nzuri"
               }
            }
         ]
      },
      {
         "id": "q2",
         "type": "yes_no",
         "text": {
            "en": "Have you visited a healthcare facility recently?",
            "sw": "Je, umetembelea kituo cha afya hivi karibuni?"
         }
      },
      {
         "id": "q3",
         "type": "open_ended",
         "text": {
            "en": "What challenges do you face in accessing healthcare?",
            "sw": "Ni changamoto gani unazokumbana nazo katika kupata huduma za afya?"
         }
      }
   ]
}
```

## Audio Response Format

Audio responses should be placed in a directory with filenames that include the question ID, following this pattern:

```
q1_response.wav
q2_response.wav
q3_response.wav
```

The engine supports WAV, MP3, FLAC, M4A, and OGG formats.

## Text Response Format

Text responses can be provided in a JSON file with the following structure:

```json
{
   "q1": "q1_opt1",
   "q2": "yes",
   "q3": "I face challenges with transportation to healthcare facilities."
}
```

## Output Format

The engine produces two main output files:

1. `responses.json`: Contains all processed responses
2. `analysis.json`: Contains analysis of the responses, including:
   - Counts for multiple-choice and yes/no questions
   - Keywords and themes for open-ended questions
   - Overall response statistics

## Testing

To run the tests:

```bash
python -m unittest discover tests
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for the Whisper ASR model
- Google Cloud for the Translation API
- The sentence-transformers library for text analysis
