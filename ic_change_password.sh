#!/bin/bash


# ./ic_change_password.sh "ibm_cloud_api_user_with_role" "1234567890Password123"
# 🔄 Updating password for user 'ibm_cloud_api_user_with_role'...
# {
#   "task": {
#     "id": "crn:v1:bluemix:public:databases-for-redis:us-south:a/40ddc34a953a8c02f10987b59085b60e:6427cc65-7fe6-4e41-8545-543762824412:task:006aec2e-9488-4946-960c-df8ca7bf6d1d",
#     "description": "Updating user",
#     "status": "running",
#     "deployment_id": "crn:v1:bluemix:public:databases-for-redis:us-south:a/40ddc34a953a8c02f10987b59085b60e:6427cc65-7fe6-4e41-8545-543762824412::",
#     "progress_percent": 0,
#     "created_at": "2025-04-21T14:44:42.000Z"
#   }
# }

set -euo pipefail

# Input validation
if [[ -z "${1:-}" ]]; then
    echo "❌ Username is not set"
    exit 1
fi

if [[ -z "${2:-}" ]]; then
    echo "❌ Password is not set"
    exit 1
fi

USERNAME="$1"
PASSWORD="$2"

# Set the API key
API_KEY="Eh_pJj2EMvJngoMRoGkV2YrfJ4ZarFDCiheM-Hd5EmV_"  # Replace with your actual API key

# Check for IBM Cloud login
RELOGIN=false
if ! ibmcloud iam oauth-tokens &>/tmp/ibm_token_check.log; then
    RELOGIN=true
else
    if grep -q "Login expired" /tmp/ibm_token_check.log; then
        RELOGIN=true
    fi
fi

if $RELOGIN; then
    echo "🔐 IBM Cloud login expired or not logged in. Logging in..."
    ibmcloud login --apikey "$API_KEY" -r us-south
    ibmcloud target -g default
fi

# Fetch IAM token
export AUTH_HEADER=$(ibmcloud iam oauth-tokens --output json | jq -r ".iam_token")

# Set constants
export HOST="api.us-south.databases.cloud.ibm.com"
export CRN="crn:v1:bluemix:public:databases-for-redis:us-south:a/40ddc34a953a8c02f10987b59085b60e:6427cc65-7fe6-4e41-8545-543762824412::"

# URL encode CRN
ENCODED_CRN=$(python3 -c "import urllib.parse; print(urllib.parse.quote('${CRN}', safe=''))")

# Make PATCH request to update user password
echo "🔄 Updating password for user '$USERNAME'..."
curl -s -X PATCH "https://${HOST}/v5/ibm/deployments/${ENCODED_CRN}/users/database/${USERNAME}" \
     -H "Authorization: ${AUTH_HEADER}" \
     -H "Accept: application/json" \
     -H "Content-Type: application/json" \
     -d "{\"user\":{\"password\":\"${PASSWORD}\"}}" \
     | jq
