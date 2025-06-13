Introduction
============

What is Swahili Survey Engine?
------------------------------

The Swahili Survey Engine is a comprehensive Python-based application designed for processing surveys in both English and Swahili languages. It provides end-to-end functionality for creating, translating, and analyzing surveys with support for both text and audio responses.

This tool is particularly valuable for researchers, organizations, and individuals working with Swahili-speaking communities who need to collect and analyze survey data efficiently.

Key Features
-----------

- **Bilingual Support**: Full support for both English and Swahili languages
- **Translation**: Automatic translation between English and Swahili using Google Cloud Translation API
- **Audio Processing**: Transcription of audio responses using OpenAI's Whisper model
- **Response Analysis**: Advanced analysis of survey responses, including keyword extraction and theme clustering
- **Multiple Question Types**: Support for multiple-choice, yes/no, and open-ended questions
- **Comprehensive Pipeline**: End-to-end processing from survey creation to response analysis

Components
---------

The engine consists of several key components:

1. **Translator**: Handles translation between English and Swahili using Google Cloud Translation API
2. **Question Mapper**: Maps survey questions between different formats and structures
3. **Response Parser**: Parses and analyzes survey responses, particularly open-ended responses
4. **ASR (Automatic Speech Recognition)**: Transcribes audio responses using OpenAI's Whisper model
5. **Pipeline**: Orchestrates the flow between all components to provide a complete survey processing pipeline

Use Cases
--------

The Swahili Survey Engine is designed for a variety of use cases, including:

- **Academic Research**: Collecting and analyzing survey data from Swahili-speaking participants
- **Market Research**: Gathering consumer insights in East African markets
- **Public Health Surveys**: Collecting health-related data in Swahili-speaking regions
- **Educational Assessments**: Evaluating educational outcomes in bilingual settings
- **Community Feedback**: Gathering feedback from Swahili-speaking communities

Getting Started
-------------

To get started with the Swahili Survey Engine, see the :doc:`installation` and :doc:`usage` sections.