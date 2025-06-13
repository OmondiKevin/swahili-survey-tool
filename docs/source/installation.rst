Installation
===========

Prerequisites
------------

Before installing the Swahili Survey Engine, ensure you have the following prerequisites:

- Python 3.8 or higher
- pip (Python package installer)
- Google Cloud API key (for translation)
- Internet connection (for downloading models)

System Requirements
-----------------

- **CPU**: Any modern multi-core processor
- **RAM**: Minimum 4GB, 8GB or more recommended for processing large audio files
- **Disk Space**: At least 2GB for the application and dependencies
- **Operating System**: Windows 10+, macOS 10.15+, or Linux (Ubuntu 18.04+ recommended)

Installation Steps
----------------

1. Clone the Repository
~~~~~~~~~~~~~~~~~~~~~

First, clone the repository from GitHub:

.. code-block:: bash

   git clone https://github.com/yourusername/swahili_survey_engine.git
   cd swahili_survey_engine

2. Create a Virtual Environment (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It's recommended to create a virtual environment to isolate the dependencies:

.. code-block:: bash

   # Using venv (Python 3.8+)
   python -m venv .venv
   
   # Activate the virtual environment
   # On Windows
   .venv\Scripts\activate
   
   # On macOS/Linux
   source .venv/bin/activate

3. Install Dependencies
~~~~~~~~~~~~~~~~~~~~

Install the required dependencies using pip:

.. code-block:: bash

   pip install -r requirements.txt

This will install all the necessary packages, including:

- OpenAI Whisper for speech recognition
- Google Cloud Translation API client
- Sentence transformers for text analysis
- Other supporting libraries

4. Set Up Google Cloud API Credentials
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To use the translation functionality, you need to set up Google Cloud API credentials:

1. Create a Google Cloud account if you don't have one
2. Create a new project in the Google Cloud Console
3. Enable the Cloud Translation API for your project
4. Create an API key or service account credentials
5. Set the environment variable to point to your credentials file:

.. code-block:: bash

   # On Windows
   set GOOGLE_APPLICATION_CREDENTIALS=path\to\your\credentials.json
   
   # On macOS/Linux
   export GOOGLE_APPLICATION_CREDENTIALS=path/to/your/credentials.json

Alternatively, you can specify the path to your credentials file when running the application.

5. Verify Installation
~~~~~~~~~~~~~~~~~~~

To verify that the installation was successful, run the following command:

.. code-block:: bash

   python run_pipeline.py --help

This should display the help message with all available command-line options.

Troubleshooting Installation
--------------------------

Common installation issues and their solutions:

1. **Missing Dependencies**

   If you encounter errors about missing dependencies, try installing them individually:

   .. code-block:: bash

      pip install <package_name>

2. **Google Cloud API Issues**

   If you encounter issues with the Google Cloud API:
   
   - Ensure your API key has the necessary permissions
   - Verify that the Cloud Translation API is enabled for your project
   - Check that the environment variable is set correctly

3. **Python Version Issues**

   If you're using an older version of Python, you may encounter compatibility issues. Upgrade to Python 3.8 or higher.

4. **Memory Errors During Installation**

   If you encounter memory errors when installing dependencies, try installing them one by one:

   .. code-block:: bash

      pip install -r requirements.txt --no-cache-dir

Next Steps
---------

After installation, proceed to the :doc:`usage` section to learn how to use the Swahili Survey Engine.