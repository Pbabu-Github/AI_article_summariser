from gtts import gTTS
import os
from PyPDF2 import PdfReader
import requests


def start(pdf_filename):
            try:
                with open(pdf_filename, 'rb') as book:
                    reader = PdfReader(book)

                    for page_number, page in enumerate(reader.pages, start=1):
                        content = page.extract_text()
                        #gets the summairsed content in a json file
                        summarized_content = summarizer(content)
                        #converst the json file to a txt file
                        summarized_content = json_to_string(summarized_content)

                        # Create a gTTS object with the extracted text
                        tts = gTTS(summarized_content)

                        # Save the speech as an audio file
                        output_filename = f"summarised_page_{page_number}.mp3"
                        tts.save(output_filename)

                        # Play the saved audio file 
                    # os.system(f"mpg321 {output_filename}")

            except Exception as e:
                print(f"An error occurred: {e}")

def summarizer(input_text):
    api_key = "ab6797d5-bc4e-4f9c-b15b-74ac898438ba"
    url = "https://api.oneai.com/api/v0/pipeline"

    headers = {
        "api-key": api_key, 
        "content-type": "application/json"
    }
    
    payload = {
        "input": input_text,
        "input_type": "conversation",
        "content_type": "application/json",
        "output_type": "json",
        "multilingual": {
            "enabled": True
        },
        "steps": [
            {
                "skill": "summarize"
            }
        ],
    }

    r = requests.post(url, json=payload, headers=headers)
    data = r.json()
    return data

def json_to_string(data):
      # Serialize JSON data to a string
    json_string = str(data)
    #create a txt file to put the data into
    filename='summarized_content.txt'

    # Save the serialized JSON string to a text file
    with open(filename, "w") as file:
        file.write(json_string)

"""
    This function goes through the different directories in the laptop and sees if the path of the file was found
"""
def search_files(start_dir, target_filename):
    for root, dirs, files in os.walk(start_dir):
        if target_filename in files:
            filepath = os.path.join(root, target_filename)
            return filepath
    return None


def main():
     
     pdf_filename = input("Enter the filename: ")
     found_filepath = search_files(".", pdf_filename)
"""
write the function to go through the directories to look for file and get the file path
"""
     
    
