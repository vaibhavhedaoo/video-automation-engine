from google_sheet import get_next_row
from generate_voice import create_voice
from create_video import create_video
import os

def run():
    print("STEP 1: Fetching next row from sheet...")
    row, index = get_next_row()
    print("Sheet row:", row)

    if not row:
        print("No pending rows found -> Exiting")
        return

    print("STEP 2: Generating voice file...")
    voice_file = create_voice(row["script"])
    print("Voice file created:", voice_file, os.path.exists(voice_file))

    print("STEP 3: Checking assets...")
    print("Background exists:", os.path.exists("assets/backgrounds/test.mp4"))
    print("Music exists:", os.path.exists("assets/music/bg.mp3"))

    print("STEP 4: Creating video...")
    output_file = create_video("assets/backgrounds/test.mp4", voice_file, "final.mp4")
    print("Video created:", output_file, os.path.exists(output_file))

if __name__ == "__main__":
    run()
