import srt
import datetime
import argparse

def adjust_subtitle_timing(input_file, output_file, time_offset):
    """
    Adjusts the timing of subtitles in an SRT file.

    Args:
        input_file (str): Path to the input SRT file.
        output_file (str): Path to save the adjusted SRT file.
        time_offset (float): Time offset in seconds (positive or negative).
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            subtitles = list(srt.parse(f.read()))
    except Exception as e:
        print(f"Error reading the input file: {e}")
        return

    offset = datetime.timedelta(seconds=time_offset)

    # Apply the offset to each subtitle
    for subtitle in subtitles:
        subtitle.start += offset
        subtitle.end += offset

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(srt.compose(subtitles))
        print(f"Subtitle timings adjusted successfully! Saved to: {output_file}")
    except Exception as e:
        print(f"Error writing the output file: {e}")

def main():
    parser = argparse.ArgumentParser(description="Sync subtitles by adjusting timing.")
    parser.add_argument("input_file", help="Path to the input SRT file.")
    parser.add_argument("output_file", help="Path to save the adjusted SRT file.")
    parser.add_argument(
        "time_offset",
        type=float,
        help="Time offset in seconds (positive to delay, negative to advance)."
    )

    args = parser.parse_args()
    adjust_subtitle_timing(args.input_file, args.output_file, args.time_offset)

if __name__ == "__main__":
    main()

