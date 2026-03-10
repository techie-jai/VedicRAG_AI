#!/bin/bash

echo "=========================================="
echo "Digital Nalanda - Data Ingestion Command"
echo "=========================================="
echo ""
echo "This script ingests scripture data into ChromaDB."
echo "It will automatically detect new/modified files and ingest only those."
echo ""

if [ ! -d "dharmaganj" ]; then
    echo "ERROR: dharmaganj directory not found!"
    exit 1
fi

python ingest.py
