import os
import srt
from datetime import datetime

def clean_srt(file_path, log_file):
    """Remove any subtitle lines containing 'YTS', 'RARBG', or 'YIFY' using the srt library."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        subtitles = list(srt.parse(content))
        
        initial_count = len(subtitles)
        cleaned_subtitles = [
            subtitle for subtitle in subtitles
            if "YTS" not in subtitle.content and 
               "RARBG" not in subtitle.content and
               "YIFY" not in subtitle.content
        ]
        final_count = len(cleaned_subtitles)
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(srt.compose(cleaned_subtitles))
        
        log_file.write(f"Processed: {file_path}\n")
        log_file.write(f"  Removed subtitles: {initial_count - final_count}\n\n")
        print(f"Processed: {file_path} - Removed subtitles: {initial_count - final_count}")
    
    except Exception as e:
        log_file.write(f"Error processing file {file_path}: {e}\n")
        print(f"Error processing file {file_path}: {e}")


def process_folders(root_folder):
    """Walk through folders and process all .srt files."""
    home_folder = os.path.expanduser("~")
    log_file_path = os.path.join(home_folder, ".subtitle_cleaner.log")
    
    with open(log_file_path, 'w', encoding='utf-8') as log_file:
        log_file.write(f"Subtitle Cleaner Log - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        log_file.write("=" * 50 + "\n\n")
        
        for root, dirs, files in os.walk(root_folder):
            for file in files:
                if file.endswith(".srt"):
                    file_path = os.path.join(root, file)
                    clean_srt(file_path, log_file)
        
        log_file.write("Processing completed.\n")
    
    print(f"Log file saved to: {log_file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python subtitle_cleaner.py <root_directory>")
        sys.exit(1)
    
    root_directory = sys.argv[1]

    if not os.path.isdir(root_directory):
        print(f"Error: The directory {root_directory} does not exist.")
        sys.exit(1)
    
    process_directory(root_directory)

