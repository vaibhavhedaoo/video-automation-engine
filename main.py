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
    output_file = create_video("assets/backgrounds/test.mp4", voice_file, "final.mp4")

    print("Video created successfully:", output_file)

if __name__ == "__main__":
    run()
