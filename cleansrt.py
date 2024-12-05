import os
import sys
import srt
import chardet
from datetime import datetime

def detect_encoding(file_path):
    """Detect the encoding of a file."""
    with open(file_path, 'rb') as f:
        raw_data = f.read(1024)
        result = chardet.detect(raw_data)
        return result['encoding']

def is_srt_format(content):
    """Check if the file content is valid SRT format."""
    try:
        list(srt.parse(content))
        return True
    except Exception:
        return False

def clean_srt(file_path, log_file, display_only):
    """Remove any subtitle lines containing 'YTS', 'RARBG', or 'YIFY' using the srt library."""
    try:
        encoding = detect_encoding(file_path)

        with open(file_path, 'r', encoding=encoding, errors="ignore") as file:
            content = file.read()

        if not is_srt_format(content):
            log_file.write(f"Skipped (Unsupported format): {file_path}\n")
            print(f"Skipped (Unsupported format): {file_path}")
            return

        subtitles = list(srt.parse(content))
        initial_count = len(subtitles)

        matching_subtitles = [
            subtitle for subtitle in subtitles
            if "YTS" in subtitle.content or 
               "RARBG" in subtitle.content or
               "YIFY" in subtitle.content
        ]
        match_count = len(matching_subtitles)
        
        if display_only:
            if match_count > 0:
                print(f"Contains matching subtitles: {file_path}")
            return

        # Only clean if not in display-only mode
        cleaned_subtitles = [
            subtitle for subtitle in subtitles
            if "YTS" not in subtitle.content and 
               "RARBG" not in subtitle.content and
               "YIFY" not in subtitle.content
        ]
        final_count = len(cleaned_subtitles)
        
        with open(file_path, 'w', encoding="utf-8") as file:
            file.write(srt.compose(cleaned_subtitles))
        
        log_file.write(f"Processed: {file_path}\n")
        log_file.write(f"  Removed subtitles: {initial_count - final_count}\n\n")
        print(f"Processed: {file_path} - Removed subtitles: {initial_count - final_count}")
    
    except Exception as e:
        log_file.write(f"Error processing file {file_path}: {e}\n")
        print(f"Error processing file {file_path}: {e}")


def process_folders(root_folder, display_only=False):
    """Walk through folders and process all .srt files."""
    home_folder = os.path.expanduser("~")
    log_file_path = os.path.join(home_folder, ".subtitle_cleaner.log")
    
    with open(log_file_path, 'w', encoding='utf-8') as log_file:
        log_file.write(f"Subtitle Cleaner Log - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        log_file.write("=" * 50 + "\n\n")
        
        for root, dirs, files in os.walk(root_folder):
            dirs[:] = [d for d in dirs if d.lower() != "subs"]
            for file in files:
                if file.endswith(".srt"):
                    file_path = os.path.join(root, file)
                    clean_srt(file_path, log_file, display_only)
        
        if not display_only:
            log_file.write("Processing completed.\n")
    
    if not display_only:
        print(f"Log file saved to: {log_file_path}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Clean or display .srt files containing specific keywords.")
    parser.add_argument("root_directory", help="Root directory to search for .srt files.")
    parser.add_argument(
        "--display-only", action="store_true",
        help="Display files containing keywords without modifying them."
    )
    args = parser.parse_args()

    root_directory = args.root_directory

    if not os.path.isdir(root_directory):
        print(f"Error: The directory {root_directory} does not exist.")
        sys.exit(1)
    
    process_folders(root_directory, display_only=args.display_only)

