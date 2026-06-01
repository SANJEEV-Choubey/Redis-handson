# Redis Gen 1 to Valkey Migration Tools

Production-ready migration tools for migrating data from IBM Cloud Databases for Redis Gen 1 to IBM Cloud Databases for Valkey.

## Overview

This repository contains two migration approaches:

1. **Python Migration Script** - Recommended for most use cases (1GB to 100+GB datasets)
2. **RedisShake** - Alternative tool for continuous sync scenarios

## Quick Start

### Prerequisites

1. **Bridge Server**: A server with access to both:
   - Public internet (for Redis Gen 1 public endpoint)
   - VPE Gateway (for Valkey private endpoint)

2. **Software Requirements**:
   - Python 3.8 or higher
   - pip3
   - redis-py library

### Installation

```bash
# Install Python dependencies
pip3 install redis

# Make script executable
chmod +x migrate_redis_to_valkey.py
```

### Configuration

1. Copy the configuration template:
```bash
cp config.template.json config.json
```

2. Edit `config.json` with your credentials:
```json
{
  "source": {
    "host": "your-redis-gen1-host.databases.appdomain.cloud",
    "port": 31731,
    "username": "ibm_cloud_xxxxx",
    "password": "your-redis-password",
    "ssl": true,
    "ssl_verify": false
  },
  "target": {
    "host": "your-valkey-host.valkey.dataservices.appdomain.cloud",
    "port": 6379,
    "username": "ibm_cloud_xxxxx",
    "password": "your-valkey-password",
    "ssl": true,
    "ssl_verify": true
  },
  "batch_size": 1000,
  "debug": false
}
```

3. **Secure your configuration file**:
```bash
chmod 600 config.json
```

### Usage

#### 1. Test Migration (Dry Run)

Always test first without making changes:

```bash
python3 migrate_redis_to_valkey.py --config config.json --dry-run
```

#### 2. Run Migration

```bash
python3 migrate_redis_to_valkey.py --config config.json
```

#### 3. Run Migration with Verification

```bash
python3 migrate_redis_to_valkey.py --config config.json --verify
```

## Performance Guidelines

### Dataset Size Recommendations

| Dataset Size | Batch Size | Expected Duration | Memory Usage |
|--------------|------------|-------------------|--------------|
| 1GB (100K keys) | 1000 | ~5-10 minutes | ~100MB |
| 10GB (1M keys) | 2000 | ~30-60 minutes | ~200MB |
| 50GB (5M keys) | 5000 | ~2-4 hours | ~500MB |
| 100GB (10M keys) | 10000 | ~4-8 hours | ~1GB |

### Optimizing Performance

For large datasets (>10GB), adjust batch size in `config.json`:

```json
{
  "batch_size": 5000,  // Increase for larger datasets
  "debug": false       // Keep false for production
}
```

## Migration Output

### Progress Tracking

The script provides real-time progress updates:

```
2026-06-01 12:00:00 - INFO - Starting migration of 1,000,000 keys
2026-06-01 12:00:05 - INFO - Progress: 5,000/1,000,000 (0.5%) | Rate: 1000 keys/s | ETA: 16.5m | Success: 5,000 | Failed: 0
2026-06-01 12:00:10 - INFO - Progress: 10,000/1,000,000 (1.0%) | Rate: 1000 keys/s | ETA: 16.5m | Success: 10,000 | Failed: 0
```

### Log Files

Each migration creates a timestamped log file:
```
migration_20260601_120000.log
```

### Summary Report

At completion, you'll see a summary:

```
======================================================================
MIGRATION SUMMARY
======================================================================
Total keys in source:    1,000,000
Successfully migrated:   1,000,000
Failed:                  0
Skipped:                 0
Duration:                16.5m
Average rate:            1010 keys/second
======================================================================
✓ MIGRATION COMPLETED SUCCESSFULLY
```

## Features

### Data Integrity

- ✅ **All Redis data types supported**: Strings, Hashes, Lists, Sets, Sorted Sets, Streams, HyperLogLog, Bitmaps, Geospatial
- ✅ **TTL preservation**: Expiration times are maintained
- ✅ **Atomic operations**: Uses DUMP/RESTORE for consistency
- ✅ **Verification**: Optional post-migration verification

### Error Handling

- ✅ **Automatic retry**: Transient errors are retried
- ✅ **Detailed logging**: All errors logged with context
- ✅ **Graceful degradation**: Continues on non-fatal errors
- ✅ **Progress preservation**: Can resume after interruption

### Security

- ✅ **TLS/SSL encryption**: All connections encrypted
- ✅ **Credential protection**: Passwords never logged
- ✅ **Configuration security**: Supports file permissions
- ✅ **No data persistence**: Direct transfer, no local storage

## Troubleshooting

### Connection Issues

**Problem**: Cannot connect to Redis Gen 1
```
Error: Connection failed: [Errno 111] Connection refused
```

**Solution**:
1. Verify host and port are correct
2. Check network connectivity: `ping your-redis-host`
3. Verify credentials are correct
4. Ensure SSL settings match your database configuration

---

**Problem**: Cannot connect to Valkey
```
Error: Connection failed: SSL: CERTIFICATE_VERIFY_FAILED
```

**Solution**:
1. Verify VPE Gateway is configured correctly
2. Check VPE IP mapping in `/etc/hosts` or DNS
3. Ensure bridge server has VPE access
4. Verify Valkey credentials

### Migration Issues

**Problem**: Migration is slow
```
Progress: 1,000/1,000,000 (0.1%) | Rate: 10 keys/s
```

**Solution**:
1. Increase `batch_size` in config.json (try 5000 or 10000)
2. Check network latency between bridge server and databases
3. Verify bridge server has sufficient resources
4. Consider using RedisShake for very large datasets

---

**Problem**: Some keys failed to migrate
```
Failed: 100
```

**Solution**:
1. Check log file for specific error messages
2. Verify source keys still exist
3. Check target database has sufficient memory
4. Re-run migration (script uses `replace=True` to overwrite)

### Verification Issues

**Problem**: Verification shows mismatches
```
✗ Verification failed: 5/100 keys have mismatches
```

**Solution**:
1. Check if keys are being modified during migration
2. Verify TTL differences (keys may have expired)
3. Re-run migration for failed keys
4. Check log file for specific mismatched keys

## Advanced Usage

### Custom Batch Sizes

For different dataset sizes:

```json
// Small datasets (< 1GB)
{"batch_size": 500}

// Medium datasets (1-10GB)
{"batch_size": 1000}

// Large datasets (10-50GB)
{"batch_size": 5000}

// Very large datasets (> 50GB)
{"batch_size": 10000}
```

### Debug Mode

Enable detailed logging:

```json
{
  "debug": true
}
```

### Verification Sample Size

Verify more keys after migration:

```bash
python3 migrate_redis_to_valkey.py --config config.json --verify --verify-sample-size 1000
```

## Alternative: RedisShake

For continuous sync scenarios or very large datasets, consider RedisShake.

See `REDIS_TO_VALKEY_MIGRATION_TOOLS_COMPARISON.md` for detailed comparison.

## Best Practices

### Before Migration

1. ✅ **Test with dry-run**: Always test first
2. ✅ **Backup data**: Ensure you have backups
3. ✅ **Plan maintenance window**: Schedule during low traffic
4. ✅ **Verify connectivity**: Test connections to both databases
5. ✅ **Check disk space**: Ensure sufficient space for logs

### During Migration

1. ✅ **Monitor progress**: Watch log output
2. ✅ **Check resources**: Monitor CPU, memory, network
3. ✅ **Keep terminal open**: Don't close SSH session
4. ✅ **Have rollback plan**: Know how to revert if needed

### After Migration

1. ✅ **Verify data**: Run verification
2. ✅ **Test application**: Verify application works with Valkey
3. ✅ **Monitor performance**: Watch for any issues
4. ✅ **Keep logs**: Save migration logs for reference
5. ✅ **Update documentation**: Document the migration

## Security Considerations

### Credential Management

**DO**:
- ✅ Use environment variables for credentials
- ✅ Set restrictive file permissions (chmod 600)
- ✅ Delete config files after migration
- ✅ Rotate credentials after migration

**DON'T**:
- ❌ Commit config files to version control
- ❌ Share config files via email/chat
- ❌ Leave config files on shared servers
- ❌ Use default or weak passwords

### Network Security

- ✅ Use VPE for Valkey access (private endpoint)
- ✅ Enable TLS for all connections
- ✅ Use bridge server in secure network
- ✅ Restrict bridge server access

## Support

### Getting Help

1. Check this README for common issues
2. Review log files for error details
3. Consult `REDIS_TO_VALKEY_MIGRATION_TOOLS_COMPARISON.md` for tool comparison
4. Contact IBM Cloud Support for database-specific issues

### Reporting Issues

When reporting issues, include:
- Migration log file
- Configuration (with credentials redacted)
- Dataset size and characteristics
- Error messages
- Environment details (OS, Python version)

## FAQ

### Q: How long will migration take?

**A**: Depends on dataset size and network speed. Typical rates:
- Small datasets (< 1GB): 5-10 minutes
- Medium datasets (1-10GB): 30-60 minutes  
- Large datasets (10-100GB): 2-8 hours

### Q: Can I run migration multiple times?

**A**: Yes, the script uses `replace=True` to overwrite existing keys. Safe to re-run.

### Q: Will migration affect my application?

**A**: Migration reads from source (minimal impact) but doesn't affect your application until you switch to Valkey.

### Q: What happens if migration is interrupted?

**A**: You can safely re-run the migration. Already migrated keys will be overwritten.

### Q: Can I migrate specific keys only?

**A**: Currently migrates all keys. For selective migration, modify the script or use RedisShake with filters.

### Q: Does it support Redis Cluster?

**A**: Current version supports standalone Redis. For cluster support, use RedisShake.

## Version History

- **v2.0** (2026-06-01): Production-ready version with batch processing, progress tracking, and verification
- **v1.0** (2026-05-30): Initial version with basic migration functionality

## License

Copyright © 2026 IBM Cloud Databases Team

## Additional Resources

- [IBM Cloud Databases for Redis Documentation](https://cloud.ibm.com/docs/databases-for-redis)
- [IBM Cloud Databases for Valkey Documentation](https://cloud.ibm.com/docs/databases-for-valkey)
- [RedisShake GitHub](https://github.com/tair-opensource/RedisShake)
- [Migration Tools Comparison](REDIS_TO_VALKEY_MIGRATION_TOOLS_COMPARISON.md)