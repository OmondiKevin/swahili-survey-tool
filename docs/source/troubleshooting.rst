Troubleshooting
==============

This section provides solutions to common issues you might encounter when using the Swahili Survey Engine.

Installation Issues
-----------------

Missing Dependencies
~~~~~~~~~~~~~~~~~~

**Issue**: Error messages about missing Python packages when running the engine.

**Solution**:
1. Ensure you've installed all dependencies:

   .. code-block:: bash

      pip install -r requirements.txt

2. If specific packages are causing issues, try installing them individually:

   .. code-block:: bash

      pip install openai-whisper
      pip install google-cloud-translate
      pip install sentence-transformers

3. Check for version conflicts and try creating a fresh virtual environment:

   .. code-block:: bash

      python -m venv .venv_new
      source .venv_new/bin/activate  # On Windows: .venv_new\Scripts\activate
      pip install -r requirements.txt

Python Version Issues
~~~~~~~~~~~~~~~~~~~

**Issue**: Errors related to Python syntax or incompatible packages.

**Solution**:
1. Verify your Python version:

   .. code-block:: bash

      python --version

2. Ensure you're using Python 3.8 or higher.
3. If needed, install a compatible Python version and create a new virtual environment with it.

Google Cloud API Issues
---------------------

API Key Not Found
~~~~~~~~~~~~~~~

**Issue**: "API key not found" or "Credentials not found" errors.

**Solution**:
1. Ensure your Google Cloud API key is correctly set up:

   .. code-block:: bash

      # On Windows
      set GOOGLE_APPLICATION_CREDENTIALS=path\to\your\credentials.json
      
      # On macOS/Linux
      export GOOGLE_APPLICATION_CREDENTIALS=path/to/your/credentials.json

2. Alternatively, specify the API key directly when initializing the Pipeline:

   .. code-block:: python

      from app.pipeline import Pipeline
      
      pipeline = Pipeline(translator_api_key="path/to/your/credentials.json")

API Quota Exceeded
~~~~~~~~~~~~~~~~

**Issue**: "Quota exceeded" errors when using the Google Cloud Translation API.

**Solution**:
1. Check your Google Cloud Console for quota limits and usage.
2. Consider upgrading your Google Cloud account or requesting a quota increase.
3. Implement rate limiting in your code to avoid hitting quota limits:

   .. code-block:: python

      import time
      from app.pipeline import Pipeline
      
      pipeline = Pipeline(translator_api_key="your_api_key")
      
      # Process in batches with delays
      for i in range(0, len(responses), 10):
          batch = responses[i:i+10]
          # Process batch
          time.sleep(1)  # Add delay between batches

Audio Processing Issues
---------------------

Audio File Format Issues
~~~~~~~~~~~~~~~~~~~~~

**Issue**: "Failed to load audio file" or "Unsupported audio format" errors.

**Solution**:
1. Ensure your audio files are in a supported format (WAV, MP3, FLAC, M4A, OGG).
2. Convert your audio files to WAV format with a standard sampling rate:

   .. code-block:: bash

      # Using ffmpeg
      ffmpeg -i input.mp3 -ar 16000 -ac 1 output.wav

3. Check that the audio files are not corrupted by playing them with a standard audio player.

No Audio Files Found
~~~~~~~~~~~~~~~~~

**Issue**: "No audio files found in directory" error.

**Solution**:
1. Ensure your audio files follow the naming convention:

   .. code-block:: text

      q{question_id}_{anything}.{extension}

   For example: `q1_response.wav`, `q2_john_doe.mp3`

2. If you want to process files that don't follow this convention, use the free-form mode:

   .. code-block:: bash

      python run_pipeline.py --survey data/survey_questions.json --audio-dir data/audio_responses --free-form

Memory Issues with ASR
~~~~~~~~~~~~~~~~~~~

**Issue**: Memory errors or crashes when processing large audio files.

**Solution**:
1. Use a smaller Whisper model:

   .. code-block:: bash

      python run_pipeline.py --survey data/survey_questions.json --audio-dir data/audio_responses --asr-model tiny

2. Process audio files in smaller batches:

   .. code-block:: python

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

3. Ensure your system has enough RAM (8GB or more recommended for larger models).

Survey Processing Issues
----------------------

Invalid Survey Format
~~~~~~~~~~~~~~~~~~

**Issue**: "Invalid survey format" or JSON parsing errors.

**Solution**:
1. Validate your survey JSON file using a JSON validator.
2. Ensure your survey follows the required structure (see :doc:`survey_format`).
3. Check for common JSON syntax errors like missing commas or quotes.
4. Use the following code to validate your survey:

   .. code-block:: python

      import json
      
      try:
          with open("path/to/your/survey.json", "r", encoding="utf-8") as f:
              survey = json.load(f)
          print("Survey JSON is valid!")
      except json.JSONDecodeError as e:
          print(f"Invalid JSON: {e}")

Missing Question IDs
~~~~~~~~~~~~~~~~~

**Issue**: "Question ID not found" errors when processing responses.

**Solution**:
1. Ensure all questions in your survey have unique IDs.
2. Check that the question IDs in your responses match the IDs in your survey.
3. If using audio responses, ensure the filenames contain the correct question IDs.
4. Consider using the free-form mode if question IDs are not available:

   .. code-block:: python

      pipeline.process_free_form_response("Your response text")

Response Analysis Issues
----------------------

Empty Analysis Results
~~~~~~~~~~~~~~~~~~~

**Issue**: Analysis results are empty or incomplete.

**Solution**:
1. Ensure you have processed at least one response before calling `analyze_responses()`.
2. Check that your responses are correctly formatted for the question types.
3. For multiple-choice questions, ensure responses match option IDs.
4. For yes/no questions, ensure responses are "yes" or "no".
5. Verify that the language of responses matches the expected language.

Incorrect Language Detection
~~~~~~~~~~~~~~~~~~~~~~~~~

**Issue**: Responses are processed in the wrong language.

**Solution**:
1. Explicitly specify the language when processing responses:

   .. code-block:: python

      pipeline.process_text_response("Nzuri sana", "q1", language="sw")
      pipeline.process_audio_response("audio.wav", "q2", language="sw")

2. Ensure your audio recordings are clear and have minimal background noise.
3. For text responses, make sure the text is correctly written in the expected language.

Performance Issues
----------------

Slow Processing
~~~~~~~~~~~~~

**Issue**: Processing takes a long time, especially for audio responses.

**Solution**:
1. Use a smaller Whisper model for ASR:

   .. code-block:: bash

      python run_pipeline.py --asr-model tiny

2. Process responses in parallel (if you have multiple CPU cores):

   .. code-block:: python

      import concurrent.futures
      from app.pipeline import Pipeline
      
      pipeline = Pipeline()
      pipeline.load_survey("data/survey_questions.json")
      
      audio_files = ["file1.wav", "file2.wav", "file3.wav"]
      question_ids = ["q1", "q2", "q3"]
      
      def process_audio(audio_file, question_id):
          return pipeline.process_audio_response(audio_file, question_id)
      
      with concurrent.futures.ThreadPoolExecutor() as executor:
          futures = [executor.submit(process_audio, af, qid) for af, qid in zip(audio_files, question_ids)]
          results = [f.result() for f in concurrent.futures.as_completed(futures)]

3. Optimize your workflow by pre-processing audio files to the optimal format.

High Memory Usage
~~~~~~~~~~~~~~

**Issue**: The application uses too much memory, especially with large surveys or many responses.

**Solution**:
1. Process responses in smaller batches.
2. Use a smaller ASR model.
3. Close and reopen the pipeline between large processing tasks:

   .. code-block:: python

      # Process first batch
      pipeline = Pipeline(asr_model_size="base")
      pipeline.load_survey("data/survey_questions.json")
      # Process some responses
      pipeline.save_responses("data/outputs/batch1_responses.json")
      del pipeline
      
      # Process second batch
      pipeline = Pipeline(asr_model_size="base")
      pipeline.load_survey("data/survey_questions.json")
      # Process more responses
      pipeline.save_responses("data/outputs/batch2_responses.json")

Getting Help
----------

If you encounter issues not covered in this troubleshooting guide:

1. Check the logs with the `--verbose` flag for more detailed error information:

   .. code-block:: bash

      python run_pipeline.py --survey data/survey_questions.json --verbose

2. Look for error messages in the console output and search for them online.

3. Check the project's GitHub repository for known issues and solutions.

4. If all else fails, create a detailed bug report including:
   - The exact command or code you're running
   - The complete error message
   - Your environment details (Python version, OS, etc.)
   - Steps to reproduce the issue