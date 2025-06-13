API Reference
============

This section provides detailed information about the API of the Swahili Survey Engine.

Pipeline
-------

The ``Pipeline`` class is the main entry point for the Swahili Survey Engine API.

.. code-block:: python

   from app.pipeline import Pipeline

Constructor
~~~~~~~~~~

.. code-block:: python

   Pipeline(survey_file=None, translator_api_key=None, asr_model_size="base")

Parameters:
   - **survey_file** (str, optional): Path to the survey questions JSON file
   - **translator_api_key** (str, optional): Google Cloud API key for translation
   - **asr_model_size** (str, default="base"): Whisper model size for ASR ('tiny', 'base', 'small', 'medium', 'large')

Methods
~~~~~~

load_survey
^^^^^^^^^^

.. code-block:: python

   load_survey(survey_file)

Loads a survey from a JSON file.

Parameters:
   - **survey_file** (str): Path to the survey questions JSON file

Returns:
   - **dict**: The loaded survey

translate_survey
^^^^^^^^^^^^^^^

.. code-block:: python

   translate_survey(target_language)

Translates the survey to the target language.

Parameters:
   - **target_language** (str): Target language code ('en' or 'sw')

Returns:
   - **dict**: The translated survey

get_survey_presentation
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   get_survey_presentation(language='en')

Gets a presentation-friendly version of the survey in the specified language.

Parameters:
   - **language** (str, default='en'): Language code ('en' or 'sw')

Returns:
   - **dict**: The survey presentation

process_text_response
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   process_text_response(response, question_id)

Processes a text response for a specific question.

Parameters:
   - **response** (str): The text response
   - **question_id** (str): The ID of the question

Returns:
   - **dict**: The processed response

process_free_form_response
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   process_free_form_response(response, language="sw")

Processes a free-form text response without a specific question ID.

Parameters:
   - **response** (str): The text response
   - **language** (str, default="sw"): Language code ('en' or 'sw')

Returns:
   - **dict**: The processed response

process_audio_response
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   process_audio_response(audio_file, question_id, language="sw")

Processes an audio response for a specific question.

Parameters:
   - **audio_file** (str): Path to the audio file
   - **question_id** (str): The ID of the question
   - **language** (str, default="sw"): Language code ('en' or 'sw')

Returns:
   - **dict**: The processed response

process_free_form_audio_response
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   process_free_form_audio_response(audio_file, language="sw")

Processes a free-form audio response without a specific question ID.

Parameters:
   - **audio_file** (str): Path to the audio file
   - **language** (str, default="sw"): Language code ('en' or 'sw')

Returns:
   - **dict**: The processed response

batch_process_audio_responses
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   batch_process_audio_responses(audio_files, question_ids, language="sw")

Processes multiple audio responses for specific questions.

Parameters:
   - **audio_files** (List[str]): List of paths to audio files
   - **question_ids** (List[str]): List of question IDs
   - **language** (str, default="sw"): Language code ('en' or 'sw')

Returns:
   - **List[dict]**: List of processed responses

process_directory_of_audio_responses
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   process_directory_of_audio_responses(directory, naming_pattern=r'q(\d+)_.*\.wav', language="sw")

Processes all audio responses in a directory.

Parameters:
   - **directory** (str): Path to the directory containing audio files
   - **naming_pattern** (str, default=r'q(\d+)_.*\.wav'): Regex pattern for extracting question IDs from filenames
   - **language** (str, default="sw"): Language code ('en' or 'sw')

Returns:
   - **List[dict]**: List of processed responses

analyze_responses
^^^^^^^^^^^^^^^

.. code-block:: python

   analyze_responses()

Analyzes all processed responses.

Returns:
   - **dict**: Analysis of the responses

save_responses
^^^^^^^^^^^^

.. code-block:: python

   save_responses(output_file)

Saves all processed responses to a JSON file.

Parameters:
   - **output_file** (str): Path to the output file

save_analysis
^^^^^^^^^^^

.. code-block:: python

   save_analysis(output_file)

Saves the analysis of responses to a JSON file.

Parameters:
   - **output_file** (str): Path to the output file

run_full_pipeline
^^^^^^^^^^^^^^^

.. code-block:: python

   run_full_pipeline(survey_file, audio_directory=None, text_responses=None, output_dir='data/outputs', language='sw', free_form=False)

Runs the full pipeline from survey loading to response analysis.

Parameters:
   - **survey_file** (str): Path to the survey questions JSON file
   - **audio_directory** (str, optional): Path to directory containing audio responses
   - **text_responses** (Dict[str, str], optional): Dictionary mapping question IDs to text responses
   - **output_dir** (str, default='data/outputs'): Directory to save output files
   - **language** (str, default='sw'): Language code ('en' or 'sw')
   - **free_form** (bool, default=False): Whether to process responses as free-form

Returns:
   - **dict**: Analysis of the responses

Translator
---------

The ``Translator`` class handles translation between English and Swahili.

.. code-block:: python

   from app.translator import Translator

Constructor
~~~~~~~~~~

.. code-block:: python

   Translator(api_key=None)

Parameters:
   - **api_key** (str, optional): Google Cloud API key for translation

Methods
~~~~~~

translate
^^^^^^^^

.. code-block:: python

   translate(text, source_language, target_language)

Translates text from the source language to the target language.

Parameters:
   - **text** (str): Text to translate
   - **source_language** (str): Source language code ('en' or 'sw')
   - **target_language** (str): Target language code ('en' or 'sw')

Returns:
   - **str**: Translated text

detect_language
^^^^^^^^^^^^^

.. code-block:: python

   detect_language(text)

Detects the language of the text.

Parameters:
   - **text** (str): Text to detect language for

Returns:
   - **str**: Detected language code ('en' or 'sw')

ASR (Automatic Speech Recognition)
---------------------------------

The ``ASR`` class handles transcription of audio responses.

.. code-block:: python

   from app.asr import ASR

Constructor
~~~~~~~~~~

.. code-block:: python

   ASR(model_size="base")

Parameters:
   - **model_size** (str, default="base"): Whisper model size ('tiny', 'base', 'small', 'medium', 'large')

Methods
~~~~~~

transcribe
^^^^^^^^^

.. code-block:: python

   transcribe(audio_file, language=None)

Transcribes an audio file to text.

Parameters:
   - **audio_file** (str): Path to the audio file
   - **language** (str, optional): Language code ('en' or 'sw')

Returns:
   - **dict**: Transcription result with text and detected language

QuestionMapper
-------------

The ``QuestionMapper`` class maps survey questions between different formats.

.. code-block:: python

   from app.question_mapper import QuestionMapper

Constructor
~~~~~~~~~~

.. code-block:: python

   QuestionMapper()

Methods
~~~~~~

map_survey_to_presentation
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   map_survey_to_presentation(survey, language='en')

Maps a survey to a presentation-friendly format.

Parameters:
   - **survey** (dict): The survey to map
   - **language** (str, default='en'): Language code ('en' or 'sw')

Returns:
   - **dict**: The mapped survey

ResponseMatcher
--------------

The ``ResponseMatcher`` class matches responses to questions.

.. code-block:: python

   from app.response_matcher import ResponseMatcher

Constructor
~~~~~~~~~~

.. code-block:: python

   ResponseMatcher(survey)

Parameters:
   - **survey** (dict): The survey containing questions

Methods
~~~~~~

match_response
^^^^^^^^^^^^

.. code-block:: python

   match_response(response_text, language='en')

Matches a response text to the most appropriate question.

Parameters:
   - **response_text** (str): The response text to match
   - **language** (str, default='en'): Language code ('en' or 'sw')

Returns:
   - **str**: The matched question ID

ResponseParser
-------------

The ``ResponseParser`` class parses and analyzes responses.

.. code-block:: python

   from app.response_parser import ResponseParser

Constructor
~~~~~~~~~~

.. code-block:: python

   ResponseParser(survey)

Parameters:
   - **survey** (dict): The survey containing questions

Methods
~~~~~~

parse_response
^^^^^^^^^^^^

.. code-block:: python

   parse_response(response_text, question_id, language='en')

Parses a response for a specific question.

Parameters:
   - **response_text** (str): The response text to parse
   - **question_id** (str): The ID of the question
   - **language** (str, default='en'): Language code ('en' or 'sw')

Returns:
   - **dict**: The parsed response

analyze_responses
^^^^^^^^^^^^^^^

.. code-block:: python

   analyze_responses(responses)

Analyzes a list of responses.

Parameters:
   - **responses** (List[dict]): List of responses to analyze

Returns:
   - **dict**: Analysis of the responses

extract_keywords
^^^^^^^^^^^^^^

.. code-block:: python

   extract_keywords(text, language='en', max_keywords=10)

Extracts keywords from text.

Parameters:
   - **text** (str): Text to extract keywords from
   - **language** (str, default='en'): Language code ('en' or 'sw')
   - **max_keywords** (int, default=10): Maximum number of keywords to extract

Returns:
   - **List[Tuple[str, int]]**: List of keywords with their frequencies