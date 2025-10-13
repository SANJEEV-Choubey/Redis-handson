#!/bin/bash

# User with provided role
# ./ic_create_user.sh "ibm_cloud_api_user_with_role" "Password1234567890123" "+@read +@write"

# {
#   "task": {
#     "id": "crn:v1:bluemix:public:databases-for-redis:us-south:a/40ddc34a953a8c02f10987b59085b60e:6427cc65-7fe6-4e41-8545-543762824412:task:50a99ecb-a316-4ee5-91ba-79b5eda88498",
#     "description": "Creating user",
#     "status": "running",
#     "deployment_id": "crn:v1:bluemix:public:databases-for-redis:us-south:a/40ddc34a953a8c02f10987b59085b60e:6427cc65-7fe6-4e41-8545-543762824412::",
#     "progress_percent": 0,
#     "created_at": "2025-04-21T14:33:08.000Z"
#   }
# }


#Default Role

# ./ic_create_user.sh "ibm_cloud_api_user_with__default_role" "Password1234567890123"        
# {
#   "task": {
#     "id": "crn:v1:bluemix:public:databases-for-redis:us-south:a/40ddc34a953a8c02f10987b59085b60e:6427cc65-7fe6-4e41-8545-543762824412:task:5db6a956-fd09-4f65-a6f6-aee8e08a7783",
#     "description": "Creating user",
#     "status": "running",
#     "deployment_id": "crn:v1:bluemix:public:databases-for-redis:us-south:a/40ddc34a953a8c02f10987b59085b60e:6427cc65-7fe6-4e41-8545-543762824412::",
#     "progress_percent": 0,
#     "created_at": "2025-04-21T14:52:00.000Z"
#   }
# }


set -euo pipefail

# Input validation
if [[ -z "${1:-}" ]]; then
    echo "❌ Username is not set"; exit 1;
fi

if [[ -z "${2:-}" ]]; then
    echo "❌ User password is not set"; exit 1;
fi

USERNAME="$1"
PASSWORD="$2"
ROLE="${3:-}"  # Optional

# Set the API key
API_KEY="Eh_pJj2EMvJngoMRoGkV2YrfJ4ZarFDCiheM-Hd5EmV_"  # Replace with your actual API key

# Try to get a token and check for expiration
RELOGIN=false
if ! ibmcloud iam oauth-tokens &>/tmp/ibm_token_check.log; then
    RELOGIN=true
else
    if grep -q "Login expired" /tmp/ibm_token_check.log; then
        RELOGIN=true
    fi
fi

if $RELOGIN; then
    echo "IBM Cloud login expired or not logged in. Logging in with API key..."
    ibmcloud login --apikey "$API_KEY" -r us-south
    ibmcloud target -g default
fi

# Fetch IAM token
export AUTH_HEADER=$(ibmcloud iam oauth-tokens --output json | jq -r ".iam_token")

# Define constants
export HOST="api.us-south.databases.cloud.ibm.com"
export CRN="crn:v1:bluemix:public:databases-for-redis:us-south:a/40ddc34a953a8c02f10987b59085b60e:6427cc65-7fe6-4e41-8545-543762824412::"
export user_type="database"

# URL-encode CRN
ENCODED_CRN=$(python3 -c "import urllib.parse; print(urllib.parse.quote('${CRN}', safe=''))")

# Build JSON payload dynamically
if [[ -n "$ROLE" ]]; then
    USER_PAYLOAD=$(jq -n --arg username "$USERNAME" --arg password "$PASSWORD" --arg role "$ROLE" \
        '{user: {username: $username, password: $password, role: $role}}')
else
    USER_PAYLOAD=$(jq -n --arg username "$USERNAME" --arg password "$PASSWORD" \
        '{user: {username: $username, password: $password}}')
fi

# Make the request
curl -X POST "https://${HOST}/v5/ibm/deployments/${ENCODED_CRN}/users/${user_type}" \
     -H "Authorization: ${AUTH_HEADER}" \
     -H "Accept: application/json" \
     -H "Content-Type: application/json" \
     -d "$USER_PAYLOAD" | jq

