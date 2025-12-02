from google_sheet import get_next_row
from generate_voice import create_voice
from create_video import create_video

def run():
    row, index = get_next_row()
    if not row:
        print("No pending rows found.")
        return

    print("Generating voice...")
    voice_file = create_voice(row["script"])

    print("Creating video...")
    bg_video = "assets/backgrounds/test.mp4"  # placeholder video path
    output_file = create_video(bg_video, voice_file)

    print("Video created:", output_file)

if __name__ == "__main__":
    run()
