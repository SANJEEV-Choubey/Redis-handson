#!/bin/bash

# Log the actions being performed
echo "Copying Python scripts to Redis instances..."

# Copy Python scripts to both Redis instances
for pod in c-$ID-m-0 c-$ID-m-1; do
    for script in bulk.py large_size.py large_ds.py; do
        kubectl cp /Users/sanjeevchoubey/go/src/github.com/SANJEEV-Choubey/Redis-handson/$script $pod:/tmp/$script -c mgmt
        if [[ $? -ne 0 ]]; then
            echo "Error: Failed to copy $script to $pod."
            exit 1
        fi
    done
done

# Log that we're executing the scripts
echo "Executing Python scripts inside Redis pod c-$ID-m-0..."

# Execute the scripts inside the Redis pod
kubectl exec c-$ID-m-0 -c mgmt -- /bin/bash <<EOF

    echo "Retrieving credentials using cdb command..."
    
    # Get credentials from cdb command and store them in a variable
    CREDENTIALS_JSON=\$(cdb execute redis get_credentials)
    if [[ \$? -ne 0 ]]; then
        echo "Error: Failed to retrieve credentials."
        exit 1
    fi

    # Extract the Redis user and password manually
    REDIS_USER=\$(echo \$CREDENTIALS_JSON | grep -o '"data":\["[^"]*' | sed 's/"data":\["//')
    REDIS_PASSWORD=\$(echo \$CREDENTIALS_JSON | grep -o '"[^"]*"\]' | sed 's/"\]//')

    # Print the extracted credentials for debugging
    echo "Extracted Redis User: \$REDIS_USER"
    echo "Extracted Redis Password: \$REDIS_PASSWORD"

    if [[ -z "\$REDIS_USER" || -z "\$REDIS_PASSWORD" ]]; then
        echo "Error: Redis user or password could not be extracted."
        exit 1
    fi

    for script in /tmp/bulk.py /tmp/large_size.py /tmp/large_ds.py; do
        echo "Running \$(basename \$script) with Redis credentials..."
        python \$script | redis-cli --user "\$REDIS_USER" --pass "\$REDIS_PASSWORD" --pipe
        if [[ \$? -ne 0 ]]; then
            echo "Error: Failed to run \$(basename \$script) or Redis command."
            exit 1
        else
            echo "Data successfully loaded into Redis using \$(basename \$script)."
        fi
    done

    # Check the current database size
    echo "Checking the database size..."
    DB_SIZE=\$(redis-cli --user "\$REDIS_USER" --pass "\$REDIS_PASSWORD" DBSIZE)
    echo "Current DB size: \$DB_SIZE keys"

    # List the files in the /data directory and their sizes
    echo "Listing files in /data directory..."
    ls -lh /data

EOF

if [[ $? -ne 0 ]]; then
    echo "Error: Script execution failed inside Redis pod."
else
    echo "Script executed successfully inside Redis pod."
fi
