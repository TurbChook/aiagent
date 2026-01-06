import os
def write_file(working_directory, file_path, content):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        file_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, file_abs]) == working_dir_abs
        if valid_target_dir == False:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(file_abs):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        os.makedirs(file_path,exist_ok=True)
        try:
            with open(file_abs, "w") as f:
                f.write(content)
                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        except Exception as e:
            return f'Error: {e}'
    except Exception as e:
        return f'Error: {e}'