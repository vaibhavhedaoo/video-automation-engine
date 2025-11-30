from google_sheet import get_next_row

def run():
    row, index = get_next_row()
    if not row:
        print("No pending rows found.")
        return

    print("Next pending row:")
    print(row)

if __name__ == "__main__":
    run()

