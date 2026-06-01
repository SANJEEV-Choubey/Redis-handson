# Quick Start Guide: Redis Gen 1 to Valkey Migration

Get started with migrating your Redis Gen 1 data to Valkey in minutes.

## Prerequisites Checklist

- [ ] Bridge server with VPE access configured
- [ ] Redis Gen 1 credentials (host, port, username, password)
- [ ] Valkey credentials (host, port, username, password)
- [ ] Python 3.8+ installed
- [ ] Network connectivity to both databases

## Option 1: Python Migration Script (Recommended)

### Step 1: Install Dependencies

```bash
pip3 install redis
```

### Step 2: Create Configuration

```bash
cp config.template.json config.json
chmod 600 config.json
nano config.json  # Edit with your credentials
```

### Step 3: Test Connection (Dry Run)

```bash
python3 migrate_redis_to_valkey.py --config config.json --dry-run
```

### Step 4: Run Migration

```bash
python3 migrate_redis_to_valkey.py --config config.json --verify
```

**That's it!** Your data is now migrated to Valkey.

---

## Option 2: RedisShake (For Large Datasets)

### Step 1: Create Configuration

```bash
cp redisshake_config.template.json redisshake_config.json
chmod 600 redisshake_config.json
nano redisshake_config.json  # Edit with your credentials
```

### Step 2: Make Script Executable

```bash
chmod +x migrate_with_redisshake.sh
```

### Step 3: Run Migration

**One-time migration:**
```bash
./migrate_with_redisshake.sh --config redisshake_config.json --one-time
```

**Continuous sync (for zero-downtime):**
```bash
./migrate_with_redisshake.sh --config redisshake_config.json --continuous
```

---

## Configuration Examples

### Python Script Configuration (config.json)

```json
{
  "source": {
    "host": "abc123.databases.appdomain.cloud",
    "port": 31731,
    "username": "ibm_cloud_xxxxx",
    "password": "your-redis-password",
    "ssl": true,
    "ssl_verify": false
  },
  "target": {
    "host": "xyz789.valkey.dataservices.appdomain.cloud",
    "port": 6379,
    "username": "ibm_cloud_xxxxx",
    "password": "your-valkey-password",
    "ssl": true,
    "ssl_verify": true
  },
  "batch_size": 1000
}
```

### RedisShake Configuration (redisshake_config.json)

```json
{
  "source": {
    "host": "abc123.databases.appdomain.cloud",
    "port": 31731,
    "username": "ibm_cloud_xxxxx",
    "password": "your-redis-password"
  },
  "target": {
    "host": "xyz789.valkey.dataservices.appdomain.cloud",
    "port": 6379,
    "username": "ibm_cloud_xxxxx",
    "password": "your-valkey-password"
  }
}
```

---

## Which Tool Should I Use?

### Use Python Script If:
- ✅ Your dataset is 1GB to 50GB
- ✅ You want detailed progress tracking
- ✅ You need to test before migrating (dry-run)
- ✅ You want built-in verification

### Use RedisShake If:
- ✅ Your dataset is >50GB
- ✅ You need continuous synchronization
- ✅ You want zero-downtime migration
- ✅ Speed is critical

---

## Expected Migration Times

| Dataset Size | Python Script | RedisShake |
|--------------|---------------|------------|
| 1GB | 5-10 minutes | 1-2 minutes |
| 10GB | 30-60 minutes | 5-10 minutes |
| 50GB | 2-4 hours | 30-60 minutes |
| 100GB | 4-8 hours | 1-2 hours |

---

## Troubleshooting

### Cannot connect to Redis Gen 1
```bash
# Test connection
redis-cli -h YOUR_REDIS_HOST -p 31731 \
  --user YOUR_USERNAME -a YOUR_PASSWORD \
  --tls --insecure PING
```

### Cannot connect to Valkey
```bash
# Test connection
valkey-cli -h YOUR_VALKEY_HOST -p 6379 \
  --user YOUR_USERNAME -a YOUR_PASSWORD \
  --tls --sni YOUR_VALKEY_HOST PING
```

### VPE not working
1. Verify VPE Gateway is created
2. Check VPE IP mapping in `/etc/hosts`
3. Ensure bridge server is in correct VPC
4. Test connectivity: `ping YOUR_VALKEY_HOST`

---

## Post-Migration Checklist

- [ ] Verify key count matches
- [ ] Test sample data
- [ ] Update application configuration
- [ ] Test application with Valkey
- [ ] Monitor for errors
- [ ] Delete configuration files
- [ ] Rotate credentials

---

## Getting Help

- **Detailed Documentation:** See README.md
- **Tool Comparison:** See MIGRATION_TOOLS_COMPARISON.md
- **Python Script Issues:** Check migration_*.log files
- **RedisShake Issues:** Check data/shake.log

---

## Security Reminders

1. **Protect your configuration files:**
   ```bash
   chmod 600 config.json
   chmod 600 redisshake_config.json
   ```

2. **Delete after migration:**
   ```bash
   rm config.json redisshake_config.json
   ```

3. **Rotate credentials:**
   - Change Redis Gen 1 password
   - Change Valkey password

---

## Quick Commands Reference

### Python Script
```bash
# Dry run (test without changes)
python3 migrate_redis_to_valkey.py --config config.json --dry-run

# Migrate with verification
python3 migrate_redis_to_valkey.py --config config.json --verify

# Migrate only (no verification)
python3 migrate_redis_to_valkey.py --config config.json
```

### RedisShake
```bash
# Install only
./migrate_with_redisshake.sh --install-only

# One-time migration
./migrate_with_redisshake.sh --config redisshake_config.json --one-time

# Continuous sync
./migrate_with_redisshake.sh --config redisshake_config.json --continuous
```

---

**Ready to migrate?** Choose your tool and follow the steps above!

For detailed information, see [README.md](README.md)