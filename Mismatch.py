import os
import filetype

def check_image_extensions(folder_path, log_file):
    # Open the log file for writing
    with open(log_file, 'w') as log:
        # Walk through the folder and all subfolders
        for root, dirs, files in os.walk(folder_path):
            for filename in files:
                file_path = os.path.join(root, filename)
                
                # Use filetype to guess the actual file type
                kind = filetype.guess(file_path)
                if kind is not None:
                    actual_extension = kind.extension.lower()
                    
                    # Use os.path.splitext for a more reliable extraction of the current extension
                    base, ext = os.path.splitext(filename)
                    provided_extension = ext.lstrip('.').lower()
                    
                    # Log the check for this file
                    log.write(f"Checking file '{filename}' in '{root}' - Actual: .{actual_extension}, Provided: .{provided_extension}\n")
                    
                    # If the file extension does not match the content's actual type
                    if actual_extension != provided_extension:
                        print(f"File '{filename}' in '{root}' has mismatched extension. Actual: .{actual_extension}, Provided: .{provided_extension}")
                        
                        # Ask the user if they want to rename the file with the correct extension
                        choice = input(f"Change extension of '{filename}' to .{actual_extension}? (y/n): ")
                        if choice.strip().lower() == 'y':
                            new_filename = base + "." + actual_extension
                            new_file_path = os.path.join(root, new_filename)
                            
                            # Check if a file with the new name already exists
                            if os.path.exists(new_file_path):
                                print(f"Cannot rename '{filename}' because '{new_filename}' already exists.")
                                log.write(f"Failed to rename '{filename}' to '{new_filename}': target file already exists.\n")
                            else:
                                os.rename(file_path, new_file_path)
                                print(f"Renamed '{filename}' to '{new_filename}'.")
                                log.write(f"Renamed '{filename}' to '{new_filename}'.\n")
                        else:
                            print(f"No changes made for '{filename}'.")
                            log.write(f"No changes made for '{filename}'.\n")
                    else:
                        # Log that the file had a matching extension
                        log.write(f"File '{filename}' in '{root}' has matching extension.\n")
                else:
                    log.write(f"Could not determine the type of file '{filename}' in '{root}'.\n")

if __name__ == "__main__":
    folder_path = input("Enter the path to the folder: ")
    log_file = "file_extension_log.txt"  # The log file will be created in the same directory as the script
    check_image_extensions(folder_path, log_file)
    print(f"All file checks have been logged to '{log_file}'.")
