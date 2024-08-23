#!/bin/bash

# Process the input data
icdctl up | grep postgresql | grep Init:0/1 | while read -r line; do
    # Skip the header line
    if [[ "$line" == "NAMESPACE"* ]]; then
        continue
    fi

    # Extract the second column
    pod=$(echo "$line" | awk '{print $2}')

    # Extract the UUID using grep
    formation=$(echo "$pod" | grep -oE '[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}')

    # Print the results
    if [ -n "$formation" ]; then
        echo "Second pods: $pod"
        echo "Extracted formation: $formation"
    fi
    icdctl formation $formation
    icdctl delete pod $pod
    
done



# run from terminal: Tested
# icdctl up | grep postgresql | grep Init:0/1 | while read -r line; do if [[ "$line" == "NAMESPACE"* ]]; then continue; fi; pod=$(echo "$line" | awk '{print $2}'); formation=$(echo "$pod" | grep -oE '[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}'); if [ -n "$formation" ]; then echo "Second pods: $pod"; echo "Extracted formation: $formation"; icdctl formation "$formation"; icdctl delete pod "$pod"; fi; done

# Run the script directly in the terminal
# bash << 'EOF'
# icdctl up | grep postgresql | grep Init:0/1 | while read -r line; do
#     # Skip the header line
#     if [[ "$line" == "NAMESPACE"* ]]; then
#         continue
#     fi

#     # Extract the second column
#     pod=$(echo "$line" | awk '{print $2}')

#     # Extract the UUID using grep
#     formation=$(echo "$pod" | grep -oE '[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}')

#     # Print the results and execute the commands
#     if [ -n "$formation" ]; then
#         echo "Second pods: $pod"
#         echo "Extracted formation: $formation"
#         icdctl formation "$formation"
#         icdctl delete pod "$pod"
#     fi
    
# done
# EOF