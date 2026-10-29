name: Convert PDF to Markdown

on:
  push:
    paths:
      - '**.pdf'
  workflow_dispatch:

permissions:
  contents: write

jobs:
  convert:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install pdfplumber
        run: pip install pdfplumber

      - name: Run convert script
        run: python convert.py

      - name: Commit and Push
        uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: "Auto convert PDF to Markdown"
