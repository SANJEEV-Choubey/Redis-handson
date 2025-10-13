#!/bin/bash

# # Source icdctl environment so it works in script
# source "$(icdctl setup zsh)"

# CRN_FILE="crns.txt"
# REOL_DATE="2025-08-13T23:59:59z"

# while IFS= read -r crn || [[ -n "$crn" ]]; do
#     # Skip empty lines or lines not starting with 'crn:'
#     if [[ "$crn" == crn:* ]]; then

#         echo
#         echo "============================"
#         echo "Processing CRN:"
#         echo "$crn"
#         echo "============================"

#         # Step 1: Set CRN context
#         if ! icdctl dl "$crn"; then
#             echo "Failed to set context with icdctl dl. Skipping..."
#             continue
#         fi

#         # Step 2: Show current formation
#         if ! icdctl formation; then
#             echo "Failed to fetch formation. Skipping..."
#             continue
#         fi

#         # Step 3: Apply REOL exemption
#         if ! icdctl formation-lifecycle reol exempt 49990 --until "$REOL_DATE"; then
#             echo "Failed to apply REOL exemption. Skipping..."
#             continue
#         fi

#         # Step 4: Confirm update
#         icdctl formation
#     fi
# done < "$CRN_FILE"
# Source icdctl environment so it works in script
source "$(icdctl setup zsh)"

CRN_FILE="crns_qa_sesmic.txt"
REOL_DATE="2025-08-13T23:59:59z"

while IFS= read -r line || [[ -n "$line" ]]; do
    # Extract CRN using regex from the JSON-like line
    crn=$(echo "$line" | sed -n 's/.*"\(crn:[^"]*\)".*/\1/p')

    # Skip if no CRN found
    if [[ -z "$crn" ]]; then
        continue
    fi

    echo
    echo "============================"
    echo "Processing CRN:"
    echo "$crn"
    echo "============================"

    # Step 1: Set CRN context
    if ! icdctl dl "$crn"; then
        echo "Failed to set context with icdctl dl. Skipping..."
        continue
    fi

    # Step 2: Show current formation
    if ! icdctl formation; then
        echo "Failed to fetch formation. Skipping..."
        continue
    fi

    # Step 3: Apply REOL exemption
    if ! icdctl formation-lifecycle reol exempt 49990 --until "$REOL_DATE"; then
        echo "Failed to apply REOL exemption. Skipping..."
        continue
    fi

    # Step 4: Confirm update
    icdctl formation

done < "$CRN_FILE"