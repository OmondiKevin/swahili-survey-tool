# Swahili Survey Tool

A comprehensive engine for processing surveys in both English and Swahili, with support for text and audio responses.

## Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Components](#components)
- [Installation](#installation)
- [Usage](#usage)
- [Survey Format](#survey-format)
- [Audio Response Format](#audio-response-format)
- [Text Response Format](#text-response-format)
- [Output Format](#output-format)
- [Project Architecture](#project-architecture)
- [Troubleshooting](#troubleshooting)
- [Testing](#testing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

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

## Project Architecture

The Swahili Survey Engine follows a modular architecture with the following components:

```
swahili_survey_engine/
├── app/                      # Core application code
│   ├── asr.py                # Automatic Speech Recognition interface
│   ├── whisper_asr.py        # Whisper ASR implementation
│   ├── translator.py         # Translation service interface
│   ├── question_mapper.py    # Maps questions between formats
│   ├── response_matcher.py   # Matches responses to questions
│   ├── response_parser.py    # Parses and analyzes responses
│   └── pipeline.py           # Main orchestration component
├── data/                     # Data directory
│   ├── survey_questions.json # Example survey questions
│   └── outputs/              # Output directory for results
├── docs/                     # Documentation
├── tests/                    # Unit and integration tests
└── run_pipeline.py           # Command-line interface
```

The application follows these processing steps:

1. **Survey Loading**: Load survey questions from a JSON file
2. **Translation**: Translate questions between English and Swahili as needed
3. **Response Collection**: Process text and/or audio responses
4. **Speech Recognition**: Transcribe audio responses to text (if applicable)
5. **Response Matching**: Match responses to the appropriate questions
6. **Response Analysis**: Analyze responses to extract insights
7. **Output Generation**: Generate structured output with results and analysis

## Troubleshooting

### Common Issues

#### Google Cloud Translation API Issues

- **Error**: "API key not valid"
  - **Solution**: Ensure your Google Cloud API key is correctly set up and has access to the Translation API.
  - **Fix**: Set the environment variable `GOOGLE_APPLICATION_CREDENTIALS` to the path of your credentials file.

#### Audio Processing Issues

- **Error**: "No audio files found in directory"
  - **Solution**: Ensure audio files follow the naming convention `q{question_id}_{anything}.wav`.
  - **Fix**: Rename your audio files to match the pattern or use the `--free-form` flag.

- **Error**: "Failed to transcribe audio"
  - **Solution**: Ensure the audio file is in a supported format and is not corrupted.
  - **Fix**: Convert audio to WAV format with a standard sampling rate (16kHz recommended).

#### Memory Issues

- **Error**: "Memory error" when processing large audio files
  - **Solution**: Use a smaller Whisper model or process files in smaller batches.
  - **Fix**: Use the `--asr-model tiny` or `--asr-model base` option.

### Getting Help

If you encounter issues not covered here, please:
1. Check the logs with the `--verbose` flag for more detailed error information
2. Consult the documentation in the `docs/` directory
3. Open an issue on the project's GitHub repository

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
