import os

ALLOWED_EXTENSIONS = {'csv', 'xlsx'}
MAX_FILE_SIZE_MB = 5

def is_allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_valid_file_size(file):
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    return size <= MAX_FILE_SIZE_MB * 1024 * 1024
