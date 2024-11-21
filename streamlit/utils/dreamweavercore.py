import google.generativeai as genai
import os
import mimetypes
from pathlib import Path

class DreamCore:
    def __init__(self, api_key=None):
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-pro')
        else:
            raise ValueError("API key is required to initialize the DreamCore class.")

    def generate_content(self, prompt):
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"An error occurred while generating content: {str(e)}"

    def upload_files(self, path, mime_type=None, name=None, display_name=None, resumable=True):
        if not os.path.exists(path):
            return f'File {path} does not exist.'

        if mime_type is None:
            mime_type, _ = mimetypes.guess_type(path)
        
        try:
            response = genai.upload_file(
                path,
                mime_type=mime_type,
                name=name,
                display_name=display_name,
                resumable=resumable
            )
            return f'File {path} uploaded successfully: {response}'
        except Exception as e:
            return f"An error occurred while uploading the file: {str(e)}"

# if __name__ == '__main__':
    # testing = input("Insert your API key: ")
    # try:
    #     a = DreamCore(testing)
    #     prompt = input('Prompt: ')
    #     print("Generated Content:")
    #     print(a.generate_content(prompt))
        
    #     # Example of file upload
    #     file_path = input('Enter the path of the file you want to upload: ')
    #     mime_type = input('Enter the MIME type of the file (or press enter to auto-detect): ') or None
    #     name = input('Enter the name of the file in the destination (optional): ') or None
    #     display_name = input('Enter an optional display name for the file: ') or None
    #     resumable = input('Use resumable upload? (yes/no, default is yes): ').strip().lower() != 'no'
        
    #     print(a.upload_files(file_path, mime_type=mime_type, name=name, display_name=display_name, resumable=resumable))
        
    # except ValueError as ve:
    #     print(ve)
    # except Exception as e:
    #     print(f"An unexpected error occurred: {str(e)}")