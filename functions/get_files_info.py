import os
def get_files_info(working_directory, directory="."):
    #We correctly define the paths of our diretories
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        #Now we check if our targect_dir falls within the absolute workind_directory path
        #Its very important because if we dont limitate the acces it can read sensitive files
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if valid_target_dir == False:
            #If not we will return an error message
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        #We rise another error if the string directory is not a directory
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        #Now we iterate over the items in the directory and we record the name, file size and wheter its a directory itself
        if directory == ".":
            dir_list = [f"Result for current directory"]
        else:
            dir_list = [f"Result for {directory} directory"]
        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir,item)
            dir_list.append(f'- {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}')
        return '\n'.join(dir_list)
    except Exception as e:
        return f'Error: {e}'
        


