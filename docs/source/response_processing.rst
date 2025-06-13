Response Processing
==================

This section explains how the Swahili Survey Engine processes and analyzes survey responses, including text and audio responses.

Overview
-------

The Swahili Survey Engine provides comprehensive processing of survey responses, including:

1. **Text Response Processing**: Parsing and analyzing text responses
2. **Audio Response Processing**: Transcribing and analyzing audio responses
3. **Response Matching**: Matching responses to the appropriate questions
4. **Response Analysis**: Analyzing responses to extract insights

Text Response Processing
----------------------

Text responses can be provided in a JSON file with a structure that maps question IDs to responses:

.. code-block:: json

   {
      "q1": "q1_opt1",
      "q2": "yes",
      "q3": "I face challenges with transportation to healthcare facilities."
   }

The engine processes these responses differently based on the question type:

- **Multiple-Choice Questions**: The response should be the ID of the selected option
- **Yes/No Questions**: The response should be "yes" or "no"
- **Open-Ended Questions**: The response can be any text

Audio Response Processing
-----------------------

Audio responses are processed using the following steps:

1. **Audio Loading**: The audio file is loaded and preprocessed
2. **Speech Recognition**: The audio is transcribed using OpenAI's Whisper model
3. **Language Detection**: The language of the transcription is detected
4. **Translation**: If needed, the transcription is translated to the target language
5. **Response Matching**: The transcription is matched to the appropriate question
6. **Response Analysis**: The response is analyzed based on the question type

Audio File Naming Convention
~~~~~~~~~~~~~~~~~~~~~~~~~~

Audio files should follow a specific naming convention to be automatically matched to questions:

.. code-block:: text

   q{question_id}_{anything}.{extension}

For example:
- `q1_response.wav` - Response to question 1
- `q2_john_doe.mp3` - Response to question 2 from John Doe

Supported audio formats include WAV, MP3, FLAC, M4A, and OGG.

Free-Form Audio Processing
~~~~~~~~~~~~~~~~~~~~~~~~

The engine also supports processing free-form audio responses that don't follow the naming convention. In this case, the engine will attempt to match the transcribed content to the most appropriate question based on semantic similarity.

To enable free-form processing, use the `--free-form` flag in the command-line interface or set `free_form=True` in the programmatic API.

Response Matching
---------------

The Swahili Survey Engine uses several techniques to match responses to questions:

1. **Explicit Matching**: Using question IDs in file names or JSON keys
2. **Semantic Matching**: Using natural language processing to match responses to questions based on content
3. **Keyword Matching**: Identifying keywords in responses that match question content

Response Analysis
--------------

After processing responses, the engine performs analysis to extract insights:

Multiple-Choice Analysis
~~~~~~~~~~~~~~~~~~~~~~

For multiple-choice questions, the engine:

1. Counts the number of responses for each option
2. Calculates percentages for each option
3. Identifies the most common response

.. code-block:: json

   {
      "id": "q1",
      "type": "multiple_choice",
      "response_count": 100,
      "option_counts": {
         "q1_opt1": 25,
         "q1_opt2": 40,
         "q1_opt3": 30,
         "q1_opt4": 5
      },
      "percentages": {
         "q1_opt1": 25.0,
         "q1_opt2": 40.0,
         "q1_opt3": 30.0,
         "q1_opt4": 5.0
      },
      "most_common": "q1_opt2"
   }

Yes/No Analysis
~~~~~~~~~~~~~

For yes/no questions, the engine:

1. Counts the number of "yes" and "no" responses
2. Calculates percentages for "yes" and "no"
3. Identifies the most common response

.. code-block:: json

   {
      "id": "q2",
      "type": "yes_no",
      "response_count": 100,
      "counts": {
         "yes": 65,
         "no": 35
      },
      "percentages": {
         "yes": 65.0,
         "no": 35.0
      },
      "most_common": "yes"
   }

Open-Ended Analysis
~~~~~~~~~~~~~~~~~

For open-ended questions, the engine:

1. Extracts keywords and phrases from responses
2. Identifies common themes across responses
3. Performs sentiment analysis on responses
4. Clusters similar responses together

.. code-block:: json

   {
      "id": "q3",
      "type": "open_ended",
      "response_count": 100,
      "keywords": [
         ["transportation", 45],
         ["distance", 30],
         ["cost", 25],
         ["time", 20],
         ["availability", 15]
      ],
      "themes": [
         "Transportation issues",
         "Financial constraints",
         "Time limitations",
         "Service availability"
      ],
      "sentiment": {
         "positive": 10.0,
         "neutral": 35.0,
         "negative": 55.0
      }
   }

Output Format
-----------

The engine produces two main output files:

1. **responses.json**: Contains all processed responses
2. **analysis.json**: Contains analysis of the responses

Responses JSON
~~~~~~~~~~~~

The responses.json file contains all processed responses, including:

- The original response text
- The transcribed text (for audio responses)
- The translated text (if applicable)
- The matched question ID
- The response type

.. code-block:: json

   {
      "responses": [
         {
            "question_id": "q1",
            "response_type": "text",
            "original_text": "q1_opt1",
            "language": "en"
         },
         {
            "question_id": "q2",
            "response_type": "audio",
            "original_audio": "data/audio_samples/q2_response.wav",
            "transcribed_text": "Yes, I visited a clinic last week.",
            "language": "en"
         }
      ]
   }

Analysis JSON
~~~~~~~~~~~

The analysis.json file contains the analysis of all responses, including:

- Overall statistics about the survey
- Question-specific analysis based on question type
- Aggregated insights across all questions

.. code-block:: json

   {
      "survey_id": "swahili_health_survey_2023",
      "total_responses": 100,
      "questions": [
         {
            "id": "q1",
            "type": "multiple_choice",
            "response_count": 100,
            "option_counts": {
               "q1_opt1": 25,
               "q1_opt2": 40,
               "q1_opt3": 30,
               "q1_opt4": 5
            }
         },
         {
            "id": "q2",
            "type": "yes_no",
            "response_count": 100,
            "counts": {
               "yes": 65,
               "no": 35
            }
         },
         {
            "id": "q3",
            "type": "open_ended",
            "response_count": 100,
            "keywords": [
               ["transportation", 45],
               ["distance", 30],
               ["cost", 25],
               ["time", 20],
               ["availability", 15]
            ]
         }
      ],
      "overall_insights": {
         "completion_rate": 100.0,
         "common_themes": [
            "Transportation issues",
            "Financial constraints",
            "Time limitations"
         ]
      }
   }

Advanced Analysis
---------------

The Swahili Survey Engine also provides advanced analysis capabilities:

Cross-Question Analysis
~~~~~~~~~~~~~~~~~~~~~

The engine can identify correlations between responses to different questions:

.. code-block:: python

   from app.pipeline import Pipeline
   
   pipeline = Pipeline()
   pipeline.load_survey("data/survey_questions.json")
   
   # Process responses
   # ...
   
   # Get cross-question analysis
   analysis = pipeline.analyze_responses()
   
   # Look for correlations between q1 and q3
   correlations = analysis.get("correlations", {})
   q1_q3_correlation = correlations.get("q1_q3", {})
   print(f"Correlation between q1 and q3: {q1_q3_correlation}")

Custom Analysis
~~~~~~~~~~~~~

You can also perform custom analysis on the processed responses:

.. code-block:: python

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

Next Steps
---------

After processing and analyzing responses, you can use the insights to inform decision-making and take action based on the survey results.