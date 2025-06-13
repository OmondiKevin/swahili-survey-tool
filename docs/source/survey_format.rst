Survey Format
============

The Swahili Survey Engine uses a specific JSON format for defining surveys. This section provides detailed information about this format and how to create your own surveys.

Overview
-------

Surveys are defined in JSON format with a structure that supports bilingual content (English and Swahili) and multiple question types. The survey definition includes metadata about the survey and a list of questions.

Basic Structure
-------------

A survey JSON file has the following basic structure:

.. code-block:: json

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

Survey Metadata
-------------

The survey metadata includes:

- **survey_id**: A unique identifier for the survey
- **title**: The survey title in both English and Swahili
- **description**: A description of the survey in both English and Swahili

Question Types
------------

The Swahili Survey Engine supports three types of questions:

1. **Multiple-Choice Questions**: Questions with predefined options
2. **Yes/No Questions**: Simple yes or no questions
3. **Open-Ended Questions**: Questions that allow free-form text responses

Each question type has a specific format in the survey JSON.

Multiple-Choice Questions
~~~~~~~~~~~~~~~~~~~~~~~

Multiple-choice questions have a type of "multiple_choice" and include an array of options:

.. code-block:: json

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
         },
         {
            "id": "q1_opt3",
            "text": {
               "en": "Fair",
               "sw": "Wastani"
            }
         },
         {
            "id": "q1_opt4",
            "text": {
               "en": "Poor",
               "sw": "Mbaya"
            }
         }
      ]
   }

Yes/No Questions
~~~~~~~~~~~~~~

Yes/No questions have a type of "yes_no" and do not include options:

.. code-block:: json

   {
      "id": "q2",
      "type": "yes_no",
      "text": {
         "en": "Have you visited a healthcare facility recently?",
         "sw": "Je, umetembelea kituo cha afya hivi karibuni?"
      }
   }

Open-Ended Questions
~~~~~~~~~~~~~~~~~~

Open-ended questions have a type of "open_ended" and do not include options:

.. code-block:: json

   {
      "id": "q3",
      "type": "open_ended",
      "text": {
         "en": "What challenges do you face in accessing healthcare?",
         "sw": "Ni changamoto gani unazokumbana nazo katika kupata huduma za afya?"
      }
   }

Complete Example
--------------

Here's a complete example of a survey JSON file:

.. code-block:: json

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
               },
               {
                  "id": "q1_opt3",
                  "text": {
                     "en": "Fair",
                     "sw": "Wastani"
                  }
               },
               {
                  "id": "q1_opt4",
                  "text": {
                     "en": "Poor",
                     "sw": "Mbaya"
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

Best Practices
------------

When creating surveys, follow these best practices:

1. **Use Unique IDs**: Ensure that each question and option has a unique ID
2. **Provide Both Languages**: Always include both English and Swahili translations
3. **Keep Questions Clear**: Write clear, concise questions that are easy to understand
4. **Limit Multiple-Choice Options**: Keep the number of options reasonable (4-6 is usually good)
5. **Balance Question Types**: Use a mix of question types to gather different kinds of data
6. **Test Your Survey**: Validate your JSON file and test the survey before deploying it

Validating Survey JSON
--------------------

You can validate your survey JSON file using the Swahili Survey Engine:

.. code-block:: python

   from app.pipeline import Pipeline
   
   try:
       pipeline = Pipeline()
       pipeline.load_survey("path/to/your/survey.json")
       print("Survey JSON is valid!")
   except Exception as e:
       print(f"Error validating survey JSON: {e}")

Next Steps
---------

After creating your survey, you can use it with the Swahili Survey Engine as described in the :doc:`usage` section.