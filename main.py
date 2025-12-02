name: Automated Video Creation Test

on:
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout
      uses: actions/checkout@v3

    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: "3.10"

    - name: Install FFmpeg
      run: sudo apt-get update && sudo apt-get install -y ffmpeg

    - name: Install dependencies
      run: pip install -r requirements.txt

    - name: Run video generator
      run: python main.py
      env:
        GOOGLE_SHEET_CREDENTIALS: ${{ secrets.GOOGLE_SHEET_CREDENTIALS }}
        SHEET_ID: ${{ secrets.SHEET_ID }}

    - name: Upload Rendered Video
      uses: actions/upload-artifact@v3
      with:
        name: final-video
        path: final.mp4
