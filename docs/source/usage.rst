Usage
=====

This section provides detailed instructions on how to use the Swahili Survey Engine for processing surveys in both English and Swahili.

Command Line Interface
---------------------

The Swahili Survey Engine provides a command-line interface through the ``run_pipeline.py`` script. This is the primary way to interact with the engine.

Basic Usage
~~~~~~~~~~

The most basic usage requires specifying a survey file:

.. code-block:: bash

   python run_pipeline.py --survey data/survey_questions.json --output-dir data/outputs

Command Line Options
~~~~~~~~~~~~~~~~~~

The following command-line options are available:

.. code-block:: text

   --survey, -s          Path to the survey questions JSON file (required)
   --audio-dir, -a       Path to directory containing audio responses
   --text-responses, -t  Path to JSON file containing text responses
   --output-dir, -o      Directory to save output files (default: 'data/outputs')
   --language, -l        Language for processing ('en' or 'sw', default: 'sw')
   --translator-key, -k  Google Cloud API key for translation
   --asr-model, -m       Whisper model size for ASR ('tiny', 'base', 'small', 'medium', 'large', default: 'base')
   --verbose, -v         Enable verbose logging
   --free-form, -f       Process responses as free-form without requiring question IDs

Examples
~~~~~~~

1. **Process a survey with text responses:**

   .. code-block:: bash

      python run_pipeline.py --survey data/survey_questions.json --text-responses data/responses.json

2. **Process a survey with audio responses:**

   .. code-block:: bash

      python run_pipeline.py --survey data/survey_questions.json --audio-dir data/audio_responses

3. **Process a survey with both text and audio responses:**

   .. code-block:: bash

      python run_pipeline.py --survey data/survey_questions.json --text-responses data/responses.json --audio-dir data/audio_responses

4. **Process a survey in English:**

   .. code-block:: bash

      python run_pipeline.py --survey data/survey_questions.json --language en

5. **Use a specific Whisper model for ASR:**

   .. code-block:: bash

      python run_pipeline.py --survey data/survey_questions.json --audio-dir data/audio_responses --asr-model medium

6. **Enable verbose logging:**

   .. code-block:: bash

      python run_pipeline.py --survey data/survey_questions.json --verbose

Programmatic Usage
-----------------

You can also use the Swahili Survey Engine programmatically in your Python code.

Basic Usage
~~~~~~~~~~

Here's a basic example of how to use the engine programmatically:

.. code-block:: python

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

Advanced Usage
~~~~~~~~~~~~

Here are some more advanced examples of programmatic usage:

1. **Load a survey and translate it:**

   .. code-block:: python

      from app.pipeline import Pipeline

      pipeline = Pipeline()
      
      # Load the survey
      pipeline.load_survey("data/survey_questions.json")
      
      # Translate the survey to Swahili
      pipeline.translate_survey("sw")
      
      # Get the survey presentation in Swahili
      swahili_survey = pipeline.get_survey_presentation("sw")
      print(swahili_survey)

2. **Process individual text responses:**

   .. code-block:: python

      from app.pipeline import Pipeline

      pipeline = Pipeline()
      pipeline.load_survey("data/survey_questions.json")
      
      # Process a text response for a specific question
      pipeline.process_text_response("Nzuri sana", "q1")
      
      # Process a free-form text response
      pipeline.process_free_form_response("Ninapenda huduma za afya", "sw")

3. **Process individual audio responses:**

   .. code-block:: python

      from app.pipeline import Pipeline

      pipeline = Pipeline(asr_model_size="base")
      pipeline.load_survey("data/survey_questions.json")
      
      # Process an audio response for a specific question
      pipeline.process_audio_response("data/audio_samples/q1_response.wav", "q1", "sw")
      
      # Process a free-form audio response
      pipeline.process_free_form_audio_response("data/audio_samples/response.wav", "sw")

4. **Analyze responses and save results:**

   .. code-block:: python

      from app.pipeline import Pipeline

      pipeline = Pipeline()
      pipeline.load_survey("data/survey_questions.json")
      
      # Process responses
      pipeline.process_text_response("Nzuri sana", "q1")
      pipeline.process_text_response("Ndio", "q2")
      
      # Analyze the responses
      analysis = pipeline.analyze_responses()
      
      # Save the responses and analysis
      pipeline.save_responses("data/outputs/responses.json")
      pipeline.save_analysis("data/outputs/analysis.json")

Working with Different Question Types
-----------------------------------

The Swahili Survey Engine supports multiple question types. Here's how to work with each type:

Multiple-Choice Questions
~~~~~~~~~~~~~~~~~~~~~~~

For multiple-choice questions, responses should be the ID of the selected option:

.. code-block:: python

   # In text responses JSON
   {
      "q1": "q1_opt1"  # Where q1_opt1 is the ID of the selected option
   }

   # Programmatically
   pipeline.process_text_response("q1_opt1", "q1")

Yes/No Questions
~~~~~~~~~~~~~~

For yes/no questions, responses should be "yes" or "no":

.. code-block:: python

   # In text responses JSON
   {
      "q2": "yes"  # or "no"
   }

   # Programmatically
   pipeline.process_text_response("yes", "q2")

Open-Ended Questions
~~~~~~~~~~~~~~~~~~

For open-ended questions, responses can be any text:

.. code-block:: python

   # In text responses JSON
   {
      "q3": "I face challenges with transportation to healthcare facilities."
   }

   # Programmatically
   pipeline.process_text_response("I face challenges with transportation to healthcare facilities.", "q3")

Working with Audio Responses
--------------------------

Audio responses should be placed in a directory with filenames that include the question ID, following this pattern:

.. code-block:: text

   q1_response.wav
   q2_response.wav
   q3_response.wav

The engine supports WAV, MP3, FLAC, M4A, and OGG formats.

To process a directory of audio responses:

.. code-block:: python

   from app.pipeline import Pipeline

   pipeline = Pipeline(asr_model_size="base")
   pipeline.load_survey("data/survey_questions.json")
   
   # Process all audio responses in a directory
   pipeline.process_directory_of_audio_responses("data/audio_samples", r'q(\d+)_.*\.wav', "sw")

Next Steps
---------

After processing your survey, you can analyze the results as described in the :doc:`response_processing` section.