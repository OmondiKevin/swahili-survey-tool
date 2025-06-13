Contributing
===========

Thank you for your interest in contributing to the Swahili Survey Engine! This document provides guidelines and instructions for contributing to the project.

Getting Started
-------------

1. **Fork the Repository**

   Start by forking the repository on GitHub.

2. **Clone Your Fork**

   .. code-block:: bash

      git clone https://github.com/yourusername/swahili_survey_engine.git
      cd swahili_survey_engine

3. **Set Up Development Environment**

   .. code-block:: bash

      # Create a virtual environment
      python -m venv .venv
      
      # Activate the virtual environment
      # On Windows
      .venv\Scripts\activate
      
      # On macOS/Linux
      source .venv/bin/activate
      
      # Install dependencies
      pip install -r requirements.txt
      
      # Install development dependencies
      pip install pytest pytest-cov flake8 sphinx

Development Workflow
------------------

1. **Create a Branch**

   Create a new branch for your feature or bugfix:

   .. code-block:: bash

      git checkout -b feature/your-feature-name
      # or
      git checkout -b bugfix/issue-number

2. **Make Your Changes**

   Implement your changes, following the coding standards described below.

3. **Write Tests**

   Add tests for your changes to ensure they work as expected and to prevent future regressions.

4. **Run Tests**

   Run the tests to make sure everything is working:

   .. code-block:: bash

      python -m pytest

5. **Check Code Quality**

   Run flake8 to check code quality:

   .. code-block:: bash

      flake8 app tests

6. **Commit Your Changes**

   Commit your changes with a descriptive commit message:

   .. code-block:: bash

      git add .
      git commit -m "Add feature: your feature description"

7. **Push to Your Fork**

   Push your changes to your fork on GitHub:

   .. code-block:: bash

      git push origin feature/your-feature-name

8. **Create a Pull Request**

   Go to the original repository on GitHub and create a pull request from your branch.

Coding Standards
--------------

Please follow these coding standards when contributing to the project:

1. **PEP 8**

   Follow the PEP 8 style guide for Python code.

2. **Docstrings**

   Use Google-style docstrings for all functions, methods, and classes:

   .. code-block:: python

      def function_name(param1, param2):
          """Short description of the function.
          
          Longer description if needed.
          
          Args:
              param1: Description of param1.
              param2: Description of param2.
              
          Returns:
              Description of return value.
              
          Raises:
              ExceptionType: When and why this exception is raised.
          """
          # Function implementation

3. **Type Hints**

   Use type hints for function and method parameters and return values:

   .. code-block:: python

      def function_name(param1: str, param2: int) -> bool:
          # Function implementation

4. **Error Handling**

   Use appropriate error handling with specific exception types and informative error messages.

5. **Logging**

   Use the logging module instead of print statements for debugging and information.

6. **Testing**

   Write unit tests for all new functionality and ensure existing tests pass.

Testing
------

The project uses pytest for testing. Tests are located in the `tests/` directory.

Running Tests
~~~~~~~~~~~

To run all tests:

.. code-block:: bash

   python -m pytest

To run tests with coverage:

.. code-block:: bash

   python -m pytest --cov=app

Writing Tests
~~~~~~~~~~~

When writing tests:

1. Create test files in the `tests/` directory with names starting with `test_`.
2. Use descriptive test names that explain what is being tested.
3. Use fixtures for common setup and teardown.
4. Mock external dependencies when appropriate.

Example test:

.. code-block:: python

   def test_translator_translates_text_correctly():
       # Arrange
       translator = Translator(api_key="mock_key")
       text = "Hello"
       source_language = "en"
       target_language = "sw"
       
       # Act
       result = translator.translate(text, source_language, target_language)
       
       # Assert
       assert result == "Jambo"

Documentation
-----------

The project uses Sphinx for documentation. Documentation source files are located in the `docs/source/` directory.

Building Documentation
~~~~~~~~~~~~~~~~~~~

To build the documentation:

.. code-block:: bash

   cd docs
   make html

The built documentation will be available in the `docs/build/html/` directory.

Writing Documentation
~~~~~~~~~~~~~~~~~~

When adding or updating documentation:

1. Use reStructuredText format.
2. Update the appropriate .rst files in the `docs/source/` directory.
3. Add new files to the toctree in `index.rst` if needed.
4. Include code examples where appropriate.
5. Build and check the documentation locally before submitting changes.

Reporting Issues
--------------

If you find a bug or have a suggestion for improvement:

1. Check the GitHub issues to see if it has already been reported.
2. If not, create a new issue with a descriptive title and detailed description.
3. Include steps to reproduce the issue, expected behavior, and actual behavior.
4. Include your environment details (Python version, OS, etc.).

Pull Request Process
------------------

1. Ensure your code follows the coding standards.
2. Update the documentation if needed.
3. Add or update tests as appropriate.
4. Make sure all tests pass.
5. Update the README.md if needed.
6. Submit your pull request with a clear description of the changes.
7. Link to any related issues.

Code Review Process
-----------------

All submissions will be reviewed before being merged. The review process includes:

1. Checking that the code follows the coding standards.
2. Verifying that all tests pass.
3. Ensuring the documentation is updated.
4. Checking that the changes meet the requirements of the issue or feature.

After the review, you may be asked to make changes before your pull request is merged.

License
------

By contributing to this project, you agree that your contributions will be licensed under the project's MIT License.

Thank You
--------

Thank you for contributing to the Swahili Survey Engine! Your help is greatly appreciated.