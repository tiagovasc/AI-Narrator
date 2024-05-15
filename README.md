# Google Sheets and OpenAI Integration for Video Game Narration

## Overview
This project utilizes Google Sheets and OpenAI's API to facilitate batch testing and effective prompt engineering in a browser video game narrative context. It leverages Google Colab for executing Python scripts that interact dynamically with both Google Sheets and OpenAI's powerful models.

## Purpose
The purpose of this system is to streamline the testing and tuning of OpenAI model settings for generating narrative content based on various parameters set within a Google Sheet. This allows for rapid iteration over prompt configurations and easy scalability in managing different narrative elements for a video game.

## Logic and Execution
- **Spreadsheet Setup**: The main spreadsheet `1KDM-06e0gTbcyM4WHeY06SDT08VnLeus-QGx-OQBK9Y` contains multiple sheets (`config`, `outcomes`, `mood`, `testing`) that store parameters, outcomes, moods, and test results respectively.
- **Config Sheet**: This contains critical parameters such as the OpenAI model to use, the temperature setting for responses, a system message, and a user message template with placeholders.
- **Outcomes Sheet**: Organized to provide replacement strings for placeholders in the user message template based on game logic, such as job roles, titles, and events.
- **Mood Sheet**: A simple list of moods to randomly inject into queries to add variability to the narrative.
- **Testing Sheet**: Used for inputting parameters and displaying results of OpenAI queries. It supports the testing process by allowing multiple configurations and batch processing of queries.

## Workflow
1. **Parameter Setup**: Users define model parameters and message templates in the `config` sheet.
2. **Query Execution**: The script processes inputs from the `testing` sheet, fetches corresponding data from the `outcomes` and `mood` sheets, fills the template, and sends queries to OpenAI.
3. **Batch Processing**: Multiple queries are processed in parallel using concurrent threads to enhance efficiency.
4. **Results Handling**: Responses from OpenAI are batch updated back into the `testing` sheet for review.

## Key Functionalities
- **Dynamic Message Templating**: User messages are generated dynamically using a template that includes placeholders replaced by context-specific data from the sheets.
- **Batch Updates**: Google Sheets' batch update functionality is used to push results at once, minimizing API calls and improving performance.
- **Concurrency**: The use of Python’s `concurrent.futures` for parallel processing of API requests to OpenAI.

## Dependencies
- Google Colab
- OpenAI API
- Python Libraries: `gspread`, `openai`, `concurrent.futures`

## Setup and Operation
1. **Spreadsheet Access**: Ensure the Google Sheets API is enabled and accessible.
2. **API Key Configuration**: Securely input your OpenAI API key when prompted.
3. **Adjust Testing Parameters**: Modify rows and columns in the `testing` sheet as needed to fit the testing scale.

## Conclusion
This setup is designed for those looking to integrate advanced AI-driven content generation into their applications seamlessly, with a specific focus on gaming narratives. It provides a robust framework for managing and testing different narrative elements dynamically.

