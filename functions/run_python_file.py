import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        file_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, file_abs]) == working_dir_abs
        if valid_target_dir == False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(file_abs):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_abs.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", file_path]
        if args is None:
            args = []
        command.extend(args)
        result = subprocess.run(command,capture_output=True,timeout = 30,text = True,cwd = working_dir_abs)
        output_string = ""
        if result.returncode != 0:
            output_string += f"Process exited with code {result.returncode}\n"
        if result.stdout == "" and result.stderr == "":
            output_string += "No output produced\n"
        else:
            if result.stdout != "":
                output_string += f"STDOUT:{result.stdout}\n"
            if result.stderr != "":
                output_string += f"STDERR:{result.stderr}\n"
        return output_string
    except Exception as e:
        return f"Error: executing Python file: {e}"