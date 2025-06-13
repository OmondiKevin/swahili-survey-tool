# Swahili Survey Engine User Manual

## Table of Contents
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Getting Started](#getting-started)
4. [Creating Surveys](#creating-surveys)
5. [Processing Responses](#processing-responses)
6. [Analyzing Results](#analyzing-results)
7. [Advanced Features](#advanced-features)
8. [Troubleshooting](#troubleshooting)
9. [FAQ](#faq)

## Introduction

The Swahili Survey Engine is a comprehensive Python-based application designed for processing surveys in both English and Swahili languages. It provides end-to-end functionality for creating, translating, and analyzing surveys with support for both text and audio responses.

### Key Features

- **Bilingual Support**: Full support for both English and Swahili languages
- **Translation**: Automatic translation between English and Swahili using Google Cloud Translation API
- **Audio Processing**: Transcription of audio responses using OpenAI's Whisper model
- **Response Analysis**: Advanced analysis of survey responses, including keyword extraction and theme clustering
- **Multiple Question Types**: Support for multiple-choice, yes/no, and open-ended questions
- **Comprehensive Pipeline**: End-to-end processing from survey creation to response analysis

## Installation

### Prerequisites

Before installing the Swahili Survey Engine, ensure you have the following prerequisites:

- Python 3.8 or higher
- pip (Python package installer)
- Google Cloud API key (for translation)
- Internet connection (for downloading models)

### Installation Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/swahili_survey_engine.git
   cd swahili_survey_engine
   ```

2. **Create a Virtual Environment (Recommended)**

   ```bash
   # Using venv (Python 3.8+)
   python -m venv .venv
   
   # Activate the virtual environment
   # On Windows
   .venv\Scripts\activate
   
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Google Cloud API Credentials**

   To use the translation functionality, you need to set up Google Cloud API credentials:

   ```bash
   # On Windows
   set GOOGLE_APPLICATION_CREDENTIALS=path\to\your\credentials.json
   
   # On macOS/Linux
   export GOOGLE_APPLICATION_CREDENTIALS=path/to/your/credentials.json
   ```

5. **Verify Installation**

   ```bash
   python run_pipeline.py --help
   ```

## Getting Started

### Basic Usage

The most basic usage of the Swahili Survey Engine requires a survey file:

```bash
python run_pipeline.py --survey data/survey_questions.json --output-dir data/outputs
```

### Command Line Options

The following command-line options are available:

- `--survey`, `-s`: Path to the survey questions JSON file (required)
- `--audio-dir`, `-a`: Path to directory containing audio responses
- `--text-responses`, `-t`: Path to JSON file containing text responses
- `--output-dir`, `-o`: Directory to save output files (default: 'data/outputs')
- `--language`, `-l`: Language for processing ('en' or 'sw', default: 'sw')
- `--translator-key`, `-k`: Google Cloud API key for translation
- `--asr-model`, `-m`: Whisper model size for ASR ('tiny', 'base', 'small', 'medium', 'large', default: 'base')
- `--verbose`, `-v`: Enable verbose logging
- `--free-form`, `-f`: Process responses as free-form without requiring question IDs

### Example Workflow

1. Create a survey file (see [Creating Surveys](#creating-surveys))
2. Collect responses (text and/or audio)
3. Process the responses:

   ```bash
   python run_pipeline.py --survey data/survey_questions.json --text-responses data/responses.json --audio-dir data/audio_responses --output-dir data/outputs
   ```

4. Analyze the results in the output directory

## Creating Surveys

Surveys are defined in JSON format with a structure that supports bilingual content (English and Swahili) and multiple question types.

### Basic Structure

```json
{
   "survey_id": "unique_survey_identifier",
   "title": {
      "en": "Survey Title in English",
      "sw": "Survey Title in Swahili"
   },
   "description": {
      "en": "Survey description in English",
      "sw": "Survey description in Swahili"
   },
   "questions": [
      // Array of question objects
   ]
}
```

### Question Types

The Swahili Survey Engine supports three types of questions:

#### Multiple-Choice Questions

```json
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
}
```

#### Yes/No Questions

```json
{
   "id": "q2",
   "type": "yes_no",
   "text": {
      "en": "Have you visited a healthcare facility recently?",
      "sw": "Je, umetembelea kituo cha afya hivi karibuni?"
   }
}
```

#### Open-Ended Questions

```json
{
   "id": "q3",
   "type": "open_ended",
   "text": {
      "en": "What challenges do you face in accessing healthcare?",
      "sw": "Ni changamoto gani unazokumbana nazo katika kupata huduma za afya?"
   }
}
```

### Best Practices

When creating surveys, follow these best practices:

1. **Use Unique IDs**: Ensure that each question and option has a unique ID
2. **Provide Both Languages**: Always include both English and Swahili translations
3. **Keep Questions Clear**: Write clear, concise questions that are easy to understand
4. **Limit Multiple-Choice Options**: Keep the number of options reasonable (4-6 is usually good)
5. **Balance Question Types**: Use a mix of question types to gather different kinds of data

## Processing Responses

The Swahili Survey Engine can process both text and audio responses.

### Text Responses

Text responses should be provided in a JSON file with a structure that maps question IDs to responses:

```json
{
   "q1": "q1_opt1",
   "q2": "yes",
   "q3": "I face challenges with transportation to healthcare facilities."
}
```

To process text responses:

```bash
python run_pipeline.py --survey data/survey_questions.json --text-responses data/responses.json
```

### Audio Responses

Audio responses should be placed in a directory with filenames that include the question ID, following this pattern:

```
q{question_id}_{anything}.{extension}
```

For example:
- `q1_response.wav` - Response to question 1
- `q2_john_doe.mp3` - Response to question 2 from John Doe

To process audio responses:

```bash
python run_pipeline.py --survey data/survey_questions.json --audio-dir data/audio_responses
```

### Free-Form Processing

If your audio files don't follow the naming convention, you can use free-form processing:

```bash
python run_pipeline.py --survey data/survey_questions.json --audio-dir data/audio_responses --free-form
```

## Analyzing Results

The Swahili Survey Engine produces two main output files:

1. **responses.json**: Contains all processed responses
2. **analysis.json**: Contains analysis of the responses

### Analysis of Multiple-Choice Questions

For multiple-choice questions, the analysis includes:

- Counts for each option
- Percentages for each option
- The most common response

### Analysis of Yes/No Questions

For yes/no questions, the analysis includes:

- Counts for "yes" and "no" responses
- Percentages for "yes" and "no"
- The most common response

### Analysis of Open-Ended Questions

For open-ended questions, the analysis includes:

- Keywords and their frequencies
- Common themes across responses
- Sentiment analysis (positive, neutral, negative)

### Viewing Analysis Results

You can view the analysis results in the output directory:

```bash
cat data/outputs/analysis.json
```

## Advanced Features

### Programmatic Usage

You can use the Swahili Survey Engine programmatically in your Python code:

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

### Custom Analysis

You can perform custom analysis on the processed responses:

```python
from app.pipeline import Pipeline
import pandas as pd

pipeline = Pipeline()
pipeline.load_survey("data/survey_questions.json")

# Process responses
# ...

# Get all responses
responses = pipeline.responses

# Convert to pandas DataFrame for custom analysis
df = pd.DataFrame(responses)

# Perform custom analysis
# ...
```

### Batch Processing

For large surveys with many responses, you can process them in batches:

```python
from app.pipeline import Pipeline
import os

pipeline = Pipeline(asr_model_size="base")
pipeline.load_survey("data/survey_questions.json")

audio_dir = "data/audio_responses"
audio_files = [os.path.join(audio_dir, f) for f in os.listdir(audio_dir) if f.endswith(('.wav', '.mp3'))]

# Process in smaller batches
batch_size = 5
for i in range(0, len(audio_files), batch_size):
    batch = audio_files[i:i+batch_size]
    for audio_file in batch:
        # Process each file individually
        pipeline.process_free_form_audio_response(audio_file)
```

## Troubleshooting

### Common Issues

#### Google Cloud API Issues

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

If you encounter issues not covered here:

1. Check the logs with the `--verbose` flag for more detailed error information
2. Consult the documentation in the `docs/` directory
3. Open an issue on the project's GitHub repository

## FAQ

### General Questions

**Q: What languages are supported?**
A: The Swahili Survey Engine primarily supports English and Swahili, but the ASR component can recognize many languages.

**Q: Can I use this for commercial purposes?**
A: Yes, the project is licensed under the MIT License, which allows commercial use.

**Q: How accurate is the speech recognition?**
A: The accuracy depends on the quality of the audio and the Whisper model size used. Larger models are more accurate but require more resources.

### Technical Questions

**Q: Can I add support for other languages?**
A: Yes, but you would need to modify the translator component to support additional languages.

**Q: How can I improve performance for large surveys?**
A: Use a smaller ASR model, process responses in batches, and consider using parallel processing for audio transcription.

**Q: Can I deploy this as a web service?**
A: Yes, you can wrap the Pipeline class in a web API using frameworks like Flask or FastAPI.

### Usage Questions

**Q: How do I handle responses in languages other than English or Swahili?**
A: The engine will attempt to detect the language and translate it to the target language, but best results are achieved with English and Swahili.

**Q: Can I use this for real-time processing?**
A: The engine is designed for batch processing rather than real-time processing, but you can implement real-time processing with some modifications.

**Q: How do I export the results to other formats?**
A: You can write custom code to convert the JSON output to other formats like CSV, Excel, or PDF.