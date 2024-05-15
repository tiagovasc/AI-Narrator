import gspread
from google.colab import auth
from google.auth import default
from getpass import getpass
from openai import OpenAI
import random
import concurrent.futures
import gspread.utils as utils

# Authenticate and create the client object for Google Sheets
auth.authenticate_user()
creds, _ = default()
gc = gspread.authorize(creds)

# Initialize OpenAI client
client = OpenAI(api_key=getpass('Enter your OpenAI API key: '))

# Open the Google Sheets file by ID
sheet_id = '1KDM-06e0gTbcyM4WHeY06SDT08VnLeus-QGx-OQBK9Y'
sheet = gc.open_by_key(sheet_id)

# Choose the specific sheets you want to access
config_sheet = sheet.worksheet('config')
outcomes_sheet = sheet.worksheet('outcomes')
mood_sheet = sheet.worksheet('mood')
testing_sheet = sheet.worksheet('testing')

# Fetching configuration parameters
model = config_sheet.cell(2, 2).value
temperature = float(config_sheet.cell(3, 2).value)
system_message = config_sheet.cell(4, 2).value
user_message_template = config_sheet.cell(5, 2).value

# Number of rows and columns to process
rows_to_process = 3
columns_to_process = 3

# Function to ask GPT based on the cell value with specific system instructions and user prompt
def ask_gpt(system_message, user_message, model, temperature):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            temperature=temperature
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"An error occurred: {e}"

# Function to get the user message with replaced variables
def generate_user_message(district, job, event, title, name, mood):
    return user_message_template.format(district=district, job=job, event=event, title=title, name=name, mood=mood)

# Function to generate user messages and fetch responses in parallel
def generate_and_fetch_responses(i):
    district = testing_sheet.cell(i, 1).value
    job = testing_sheet.cell(i, 2).value
    outcomes_row = next((j for j in range(2, len(outcomes_sheet.col_values(1)) + 1) if outcomes_sheet.cell(j, 1).value == job), None)
    
    responses = []
    if outcomes_row:
        title = outcomes_sheet.cell(outcomes_row, 2).value
        event = outcomes_sheet.cell(outcomes_row, 5).value
        name = outcomes_sheet.cell(outcomes_row, 3).value if district == 'catberg' else outcomes_sheet.cell(outcomes_row, 4).value
        mood = random.choice(mood_list)
        
        user_message = generate_user_message(district, job, event, title, name, mood)
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(ask_gpt, system_message, user_message, model, temperature) for _ in range(columns_to_process)]
            for future in concurrent.futures.as_completed(futures):
                responses.append(future.result())
    
    return responses

# Collect all data to batch update
all_responses = []
for i in range(2, 2 + rows_to_process):
    row_responses = generate_and_fetch_responses(i)
    all_responses.append(row_responses)

# Update the sheet at once
range_start = 'C2'  # Starting cell for updates
range_end = utils.rowcol_to_a1(i, 2 + columns_to_process)  # Corrected ending cell for updates using gspread.utils.rowcol_to_a1
testing_sheet.update(f'{range_start}:{range_end}', all_responses)

# Function to log the first query data in a 'log' sheet
def log_first_query_data():
    log_sheet = sheet.worksheet('log')
    next_row = len(log_sheet.col_values(1)) + 1  # Find the next empty row
    i = 2  # Assuming logging the first processed query
    district = testing_sheet.cell(i, 1).value
    job = testing_sheet.cell(i, 2).value
    outcomes_row = next((j for j in range(2, len(outcomes_sheet.col_values(1)) + 1) if outcomes_sheet.cell(j, 1).value is not None), None)
    
    if outcomes_row:
        title = outcomes_sheet.cell(outcomes_row, 2).value
        event = outcomes_sheet.cell(outcomes_row, 5).value
        name = outcomes_sheet.cell(outcomes_row, 3).value if district == 'catberg' else outcomes_sheet.cell(outcomes_row, 4).value
        mood = random.choice(mood_list)
        
        user_message = generate_user_message(district, job, event, title, name, mood)
        
        # Log the details including the generated user message
        log_message = f"District: {district}, Event: {event}, Title: {title}, Name: {name}, Mood: {mood}. User Prompt: {user_message}"
        log_sheet.update_cell(next_row, 1, log_message)

# Call log function to log the first query
log_first_query_data()

# Final statement to indicate the completion of the operations
print("Queries and updates completed.")
