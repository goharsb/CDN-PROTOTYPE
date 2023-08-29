import web
import os
import uuid
import datetime
import sys

class Index:
    def GET(self):
        return "server running"

class Upload:
    def POST(self):
        data = web.input(file={})
        if 'file' in data:
            file_info = data.file
            original_filename = file_info.filename
            file_extension = original_filename.split('.')[-1].lower()

            # Check if the file extension is allowed
            if file_extension not in ALLOWED_EXTENSIONS:
                return f"File extension '{file_extension}' is not allowed."

            file_content = file_info.file.read()

            # Generate a unique filename using a combination of timestamp and UUID
            unique_id = uuid.uuid4().hex
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            unique_filename = f"{timestamp}_{unique_id}.{file_extension}"

            # Specify the directory to save the uploaded files inside container
            save_directory = "assets"
            full_path = os.path.join(save_directory, unique_filename)

            # Create the directory if it doesn't exist
            os.makedirs(save_directory, exist_ok=True)

            # Save the uploaded file to the specified directory
            with open(full_path, 'wb') as file:
                file.write(file_content)

            # Generate the CDN URL for the uploaded asset
            cdn_url = f"http://{web.config.kong_url}:8000/{unique_filename}"

            return f"File uploaded successfully. CDN URL: {cdn_url}"
        else:
            return "No file uploaded."

class Retrieve:
    def POST(self):
        data = web.input(filename=None)
        if data.filename:
            # Specify the directory where the uploaded files are stored inside container
            upload_directory = "assets"
            requested_file_path = os.path.join(upload_directory, data.filename)

            # Check if the requested file exists
            if os.path.exists(requested_file_path):
                # Generate a mock CDN URL for the requested asset with localhost as the host
                cdn_url = f"http://{web.config.kong_url}:8000/{data.filename}"
                return f"Mock CDN URL: {cdn_url}"
            else:
                return f"File not found."
        else:
            return "No filename provided."

def get_kong_url_argument():
    for i, arg in enumerate(sys.argv):
        if arg == "--kong_url":
            if i + 1 < len(sys.argv):
                return sys.argv[i + 1]
    return None

if __name__ == "__main__":
    
    kong_url = get_kong_url_argument()
    if not kong_url:
        print("Usage: python your_script_name.py --kong_url 127.0.0.1")
        sys.exit(1)
    
    # Enable CORS for all origins
    web.httpserver.allow_origin = ["*"]
    
    web.config.update({"kong_url" : kong_url})
    
    urls = (
        '/', 'Index',
        '/upload', 'Upload',
        '/retrieve', 'Retrieve'
    )
    
    # Add or remove extensions accordingly
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    
    app = web.application(urls, globals())

    app.run()