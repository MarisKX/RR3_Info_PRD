import uuid
import os


def get_unique_file_path(instance, filename):
    # Get the file extension
    ext = filename.split('.')[-1]
    # Generate a unique filename
    unique_filename = f"{uuid.uuid4().hex}.{ext}"
    # Return the new file path
    return os.path.join('uploads/', unique_filename)
