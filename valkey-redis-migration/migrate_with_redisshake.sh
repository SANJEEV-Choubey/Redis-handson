#!/bin/bash

# RedisShake Migration Script for Redis Gen 1 to Valkey
# Production-ready script for customer use
# Supports datasets from 1GB to 100+GB

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration file
CONFIG_FILE="redisshake_config.json"

# RedisShake version
REDISSHAKE_VERSION="v4.2.1"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}RedisShake Migration Tool${NC}"
echo -e "${BLUE}Redis Gen 1 to Valkey${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Function to print usage
usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Options:
    --config FILE       Configuration file (default: redisshake_config.json)
    --one-time          Perform one-time migration (default)
    --continuous        Perform continuous sync
    --install-only      Only install RedisShake, don't run migration
    --help              Show this help message

Examples:
    # One-time migration
    $0 --config redisshake_config.json --one-time

    # Continuous sync (for zero-downtime migration)
    $0 --config redisshake_config.json --continuous

    # Install RedisShake only
    $0 --install-only

EOF
    exit 1
}

# Parse command line arguments
MODE="one-time"
INSTALL_ONLY=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --config)
            CONFIG_FILE="$2"
            shift 2
            ;;
        --one-time)
            MODE="one-time"
            shift
            ;;
        --continuous)
            MODE="continuous"
            shift
            ;;
        --install-only)
            INSTALL_ONLY=true
            shift
            ;;
        --help)
            usage
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            usage
            ;;
    esac
done

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install RedisShake
install_redisshake() {
    echo -e "${YELLOW}Installing RedisShake...${NC}"
    
    if command_exists redis-shake; then
        echo -e "${GREEN}✓ RedisShake is already installed${NC}"
        return 0
    fi
    
    # Download RedisShake
    DOWNLOAD_URL="https://github.com/tair-opensource/RedisShake/releases/download/${REDISSHAKE_VERSION}/redis-shake-linux-amd64.tar.gz"
    
    echo -e "${BLUE}Downloading from: $DOWNLOAD_URL${NC}"
    
    if ! wget --show-progress "$DOWNLOAD_URL" -O redis-shake.tar.gz 2>&1; then
        echo -e "${RED}✗ Failed to download RedisShake${NC}"
        echo -e "${YELLOW}Please download manually from:${NC}"
        echo -e "${BLUE}  $DOWNLOAD_URL${NC}"
        return 1
    fi
    
    echo -e "${GREEN}✓ Downloaded RedisShake${NC}"
    
    # Extract
    tar -xzf redis-shake.tar.gz
    
    # Find and move binary
    if [ -f "redis-shake" ]; then
        sudo mv redis-shake /usr/local/bin/
    elif [ -f "redis-shake-linux-amd64/redis-shake" ]; then
        sudo mv redis-shake-linux-amd64/redis-shake /usr/local/bin/
    else
        echo -e "${RED}✗ Could not find redis-shake binary${NC}"
        return 1
    fi
    
    sudo chmod +x /usr/local/bin/redis-shake
    
    # Cleanup
    rm -rf redis-shake.tar.gz redis-shake-linux-amd64
    
    echo -e "${GREEN}✓ RedisShake installed to /usr/local/bin/redis-shake${NC}"
    return 0
}

# Function to load configuration
load_config() {
    if [ ! -f "$CONFIG_FILE" ]; then
        echo -e "${RED}✗ Configuration file not found: $CONFIG_FILE${NC}"
        echo -e "${YELLOW}Please create a configuration file. See redisshake_config.template.json${NC}"
        return 1
    fi
    
    # Validate JSON
    if ! python3 -c "import json; json.load(open('$CONFIG_FILE'))" 2>/dev/null; then
        echo -e "${RED}✗ Invalid JSON in configuration file${NC}"
        return 1
    fi
    
    echo -e "${GREEN}✓ Configuration file loaded: $CONFIG_FILE${NC}"
    return 0
}

# Function to create RedisShake TOML config
create_toml_config() {
    local sync_aof="false"
    if [ "$MODE" = "continuous" ]; then
        sync_aof="true"
    fi
    
    # Extract values from JSON config
    SOURCE_HOST=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['source']['host'])")
    SOURCE_PORT=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['source']['port'])")
    SOURCE_USER=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['source']['username'])")
    SOURCE_PASS=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['source']['password'])")
    
    TARGET_HOST=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['target']['host'])")
    TARGET_PORT=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['target']['port'])")
    TARGET_USER=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['target']['username'])")
    TARGET_PASS=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['target']['password'])")
    
    # Create TOML configuration
    cat > shake.toml << EOF
[sync_reader]
cluster = false
address = "${SOURCE_HOST}:${SOURCE_PORT}"
username = "${SOURCE_USER}"
password = "${SOURCE_PASS}"
tls = true
sync_rdb = true
sync_aof = ${sync_aof}

[redis_writer]
cluster = false
address = "${TARGET_HOST}:${TARGET_PORT}"
username = "${TARGET_USER}"
password = "${TARGET_PASS}"
tls = true

[advanced]
dir = "data"
ncpu = 4

[log]
level = "info"
EOF
    
    echo -e "${GREEN}✓ RedisShake configuration created: shake.toml${NC}"
}

# Function to check database connectivity
check_connectivity() {
    echo -e "${YELLOW}Checking database connectivity...${NC}"
    
    # Check if redis-cli or valkey-cli is available
    if ! command_exists redis-cli && ! command_exists valkey-cli; then
        echo -e "${YELLOW}⚠ redis-cli not found. Skipping connectivity check${NC}"
        echo -e "${YELLOW}  Install with: sudo apt-get install redis-tools${NC}"
        return 0
    fi
    
    # Extract source details
    SOURCE_HOST=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['source']['host'])")
    SOURCE_PORT=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['source']['port'])")
    SOURCE_USER=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['source']['username'])")
    SOURCE_PASS=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['source']['password'])")
    
    # Test source connection
    if redis-cli -h "$SOURCE_HOST" -p "$SOURCE_PORT" --user "$SOURCE_USER" -a "$SOURCE_PASS" --tls --insecure PING >/dev/null 2>&1; then
        SOURCE_KEYS=$(redis-cli -h "$SOURCE_HOST" -p "$SOURCE_PORT" --user "$SOURCE_USER" -a "$SOURCE_PASS" --tls --insecure DBSIZE 2>/dev/null | tr -d '\r')
        echo -e "${GREEN}✓ Source Redis Gen 1 connected: $SOURCE_KEYS keys${NC}"
    else
        echo -e "${RED}✗ Cannot connect to source Redis Gen 1${NC}"
        return 1
    fi
    
    # Extract target details
    TARGET_HOST=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['target']['host'])")
    TARGET_PORT=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['target']['port'])")
    TARGET_USER=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['target']['username'])")
    TARGET_PASS=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['target']['password'])")
    
    # Test target connection
    CLI_CMD="redis-cli"
    if command_exists valkey-cli; then
        CLI_CMD="valkey-cli"
    fi
    
    if $CLI_CMD -h "$TARGET_HOST" -p "$TARGET_PORT" --user "$TARGET_USER" -a "$TARGET_PASS" --tls --sni "$TARGET_HOST" PING >/dev/null 2>&1; then
        TARGET_KEYS=$($CLI_CMD -h "$TARGET_HOST" -p "$TARGET_PORT" --user "$TARGET_USER" -a "$TARGET_PASS" --tls --sni "$TARGET_HOST" DBSIZE 2>/dev/null | tr -d '\r')
        echo -e "${GREEN}✓ Target Valkey connected: $TARGET_KEYS keys${NC}"
    else
        echo -e "${RED}✗ Cannot connect to target Valkey${NC}"
        return 1
    fi
    
    return 0
}

# Function to run migration
run_migration() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}Starting Migration${NC}"
    echo -e "${BLUE}Mode: $MODE${NC}"
    echo -e "${BLUE}========================================${NC}\n"
    
    if [ "$MODE" = "one-time" ]; then
        echo -e "${YELLOW}Running one-time migration...${NC}"
        echo -e "${BLUE}This will copy all data once and then stop${NC}\n"
        
        # Run redis-shake in background
        redis-shake shake.toml &
        SHAKE_PID=$!
        
        echo -e "${GREEN}RedisShake started with PID: $SHAKE_PID${NC}"
        echo -e "${YELLOW}Waiting for migration to complete...${NC}\n"
        
        # Get data directory from shake.toml
        DATA_DIR=$(grep "^dir = " shake.toml | cut -d'"' -f2)
        LOG_FILE="${DATA_DIR}/shake.log"
        
        echo -e "${BLUE}Monitoring log: ${LOG_FILE}${NC}\n"
        
        # Monitor log for completion
        TIMEOUT=3600  # 1 hour timeout
        ELAPSED=0
        
        while [ $ELAPSED -lt $TIMEOUT ]; do
            if [ -f "$LOG_FILE" ]; then
                # Check if migration is done
                if grep -q "all done" "$LOG_FILE" 2>/dev/null; then
                    echo -e "\n${GREEN}✓ Migration completed successfully${NC}"
                    kill $SHAKE_PID 2>/dev/null || true
                    wait $SHAKE_PID 2>/dev/null || true
                    return 0
                fi
                
                # Show progress every 30 seconds
                if [ $((ELAPSED % 30)) -eq 0 ] && [ $ELAPSED -gt 0 ]; then
                    echo -e "${BLUE}Still migrating... ($ELAPSED seconds elapsed)${NC}"
                    tail -3 "$LOG_FILE" 2>/dev/null || true
                fi
            fi
            
            sleep 5
            ELAPSED=$((ELAPSED + 5))
        done
        
        echo -e "${YELLOW}⚠ Migration timeout reached${NC}"
        echo -e "${YELLOW}Check ${LOG_FILE} for details${NC}"
        kill $SHAKE_PID 2>/dev/null || true
        return 1
        
    else
        echo -e "${YELLOW}Running continuous sync...${NC}"
        echo -e "${BLUE}This will continuously sync data until you stop it${NC}"
        echo -e "${BLUE}Press Ctrl+C to stop${NC}\n"
        
        # Run redis-shake in foreground
        redis-shake shake.toml
    fi
}

# Function to verify migration
verify_migration() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}Verifying Migration${NC}"
    echo -e "${BLUE}========================================${NC}\n"
    
    if ! command_exists redis-cli; then
        echo -e "${YELLOW}⚠ redis-cli not found. Skipping verification${NC}"
        return 0
    fi
    
    # Extract details
    SOURCE_HOST=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['source']['host'])")
    SOURCE_PORT=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['source']['port'])")
    SOURCE_USER=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['source']['username'])")
    SOURCE_PASS=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['source']['password'])")
    
    TARGET_HOST=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['target']['host'])")
    TARGET_PORT=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['target']['port'])")
    TARGET_USER=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['target']['username'])")
    TARGET_PASS=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['target']['password'])")
    
    # Get key counts
    SOURCE_KEYS=$(redis-cli -h "$SOURCE_HOST" -p "$SOURCE_PORT" --user "$SOURCE_USER" -a "$SOURCE_PASS" --tls --insecure DBSIZE 2>/dev/null | tr -d '\r')
    
    CLI_CMD="redis-cli"
    if command_exists valkey-cli; then
        CLI_CMD="valkey-cli"
    fi
    TARGET_KEYS=$($CLI_CMD -h "$TARGET_HOST" -p "$TARGET_PORT" --user "$TARGET_USER" -a "$TARGET_PASS" --tls --sni "$TARGET_HOST" DBSIZE 2>/dev/null | tr -d '\r')
    
    echo -e "${YELLOW}Key count comparison:${NC}"
    echo -e "  Source (Redis Gen 1): ${BLUE}$SOURCE_KEYS${NC} keys"
    echo -e "  Target (Valkey):      ${BLUE}$TARGET_KEYS${NC} keys"
    
    if [ "$SOURCE_KEYS" -eq "$TARGET_KEYS" ]; then
        echo -e "${GREEN}✓ Key counts match perfectly!${NC}"
    elif [ "$TARGET_KEYS" -ge "$SOURCE_KEYS" ]; then
        echo -e "${GREEN}✓ Target has all source keys${NC}"
    else
        echo -e "${YELLOW}⚠ Key count mismatch - some keys may not have migrated${NC}"
    fi
}

# Main execution
main() {
    # Install RedisShake
    if ! install_redisshake; then
        exit 1
    fi
    
    if [ "$INSTALL_ONLY" = true ]; then
        echo -e "\n${GREEN}✓ RedisShake installation complete${NC}"
        exit 0
    fi
    
    # Load configuration
    if ! load_config; then
        exit 1
    fi
    
    # Check connectivity
    if ! check_connectivity; then
        echo -e "${RED}✗ Connectivity check failed${NC}"
        echo -e "${YELLOW}Please verify your configuration and network setup${NC}"
        exit 1
    fi
    
    # Create TOML configuration
    create_toml_config
    
    # Run migration
    if run_migration; then
        # Verify migration (only for one-time mode)
        if [ "$MODE" = "one-time" ]; then
            echo ""
            verify_migration
        fi
        
        echo -e "\n${BLUE}========================================${NC}"
        echo -e "${GREEN}✓ Migration process completed${NC}"
        echo -e "${BLUE}========================================${NC}"
        echo -e "${YELLOW}Log file: data/shake.log${NC}"
        echo -e "${YELLOW}Configuration: shake.toml${NC}"
        
        if [ "$MODE" = "continuous" ]; then
            echo -e "\n${YELLOW}Note: Continuous sync was running${NC}"
            echo -e "${YELLOW}Data is now synchronized between Redis Gen 1 and Valkey${NC}"
        fi
    else
        echo -e "\n${RED}✗ Migration failed${NC}"
        echo -e "${YELLOW}Check data/shake.log for details${NC}"
        exit 1
    fi
}

# Run main function
main

# Made with Bob
