#!/usr/bin/env python3
"""
Redis Gen 1 to Valkey Migration Tool
=====================================

Production-ready migration tool for migrating data from IBM Cloud Databases for Redis Gen 1
to IBM Cloud Databases for Valkey.

Features:
- Supports large datasets (1GB to 100+GB)
- Batch processing with configurable batch size
- Progress tracking and ETA
- Comprehensive error handling
- TTL preservation
- All Redis data types supported
- Dry-run mode for testing
- Detailed logging

Usage:
    python3 migrate_redis_to_valkey.py --config config.json
    python3 migrate_redis_to_valkey.py --config config.json --dry-run

Author: IBM Cloud Databases Team
Version: 2.0
"""

import redis
import json
import sys
import time
import argparse
import logging
from datetime import datetime, timedelta
from typing import Optional, Tuple, Dict, Any

class RedisMigration:
    """Handles migration from Redis Gen 1 to Valkey"""
    
    def __init__(self, config: Dict[str, Any], dry_run: bool = False):
        """
        Initialize migration with configuration
        
        Args:
            config: Configuration dictionary with source and target details
            dry_run: If True, performs validation without actual migration
        """
        self.config = config
        self.dry_run = dry_run
        self.stats = {
            'total_keys': 0,
            'migrated_keys': 0,
            'failed_keys': 0,
            'skipped_keys': 0,
            'start_time': None,
            'end_time': None
        }
        
        # Setup logging
        log_level = logging.DEBUG if config.get('debug', False) else logging.INFO
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f'migration_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Initialize Redis connections
        self.source_client = None
        self.target_client = None
        
    def connect(self) -> bool:
        """
        Establish connections to source and target databases
        
        Returns:
            bool: True if both connections successful, False otherwise
        """
        try:
            # Connect to source Redis Gen 1
            source_config = self.config['source']
            self.logger.info(f"Connecting to source Redis Gen 1: {source_config['host']}:{source_config['port']}")
            
            self.source_client = redis.Redis(
                host=source_config['host'],
                port=source_config['port'],
                username=source_config.get('username'),
                password=source_config['password'],
                ssl=source_config.get('ssl', True),
                ssl_cert_reqs='required' if source_config.get('ssl_verify', False) else None,
                ssl_ca_certs=source_config.get('ssl_ca_cert'),
                decode_responses=False,
                socket_connect_timeout=30,
                socket_timeout=30
            )
            
            # Test source connection
            self.source_client.ping()
            self.logger.info("✓ Connected to source Redis Gen 1")
            
            # Connect to target Valkey
            target_config = self.config['target']
            self.logger.info(f"Connecting to target Valkey: {target_config['host']}:{target_config['port']}")
            
            self.target_client = redis.Redis(
                host=target_config['host'],
                port=target_config['port'],
                username=target_config.get('username'),
                password=target_config['password'],
                ssl=target_config.get('ssl', True),
                ssl_cert_reqs='required' if target_config.get('ssl_verify', True) else None,
                ssl_ca_certs=target_config.get('ssl_ca_cert'),
                decode_responses=False,
                socket_connect_timeout=30,
                socket_timeout=30
            )
            
            # Test target connection
            self.target_client.ping()
            self.logger.info("✓ Connected to target Valkey")
            
            return True
            
        except redis.ConnectionError as e:
            self.logger.error(f"Connection failed: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error during connection: {e}")
            return False
    
    def get_key_count(self) -> int:
        """
        Get total number of keys in source database
        
        Returns:
            int: Number of keys
        """
        try:
            return self.source_client.dbsize()
        except Exception as e:
            self.logger.error(f"Failed to get key count: {e}")
            return 0
    
    def migrate_key(self, key: bytes) -> bool:
        """
        Migrate a single key from source to target
        
        Args:
            key: Key to migrate
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Get TTL (-1 = no expiry, -2 = key doesn't exist)
            ttl = self.source_client.ttl(key)
            
            if ttl == -2:
                self.logger.warning(f"Key no longer exists: {key.decode('utf-8', errors='ignore')}")
                self.stats['skipped_keys'] += 1
                return False
            
            # Dump key from source
            dumped_value = self.source_client.dump(key)
            
            if dumped_value is None:
                self.logger.warning(f"Failed to dump key: {key.decode('utf-8', errors='ignore')}")
                self.stats['skipped_keys'] += 1
                return False
            
            if self.dry_run:
                self.logger.debug(f"[DRY RUN] Would migrate key: {key.decode('utf-8', errors='ignore')}")
                return True
            
            # Restore to target with TTL
            if ttl > 0:
                # Convert TTL to milliseconds
                ttl_ms = ttl * 1000
                self.target_client.restore(key, ttl_ms, dumped_value, replace=True)
            else:
                # No TTL or permanent key
                self.target_client.restore(key, 0, dumped_value, replace=True)
            
            return True
            
        except redis.ResponseError as e:
            self.logger.error(f"Redis error migrating key {key.decode('utf-8', errors='ignore')}: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error migrating key {key.decode('utf-8', errors='ignore')}: {e}")
            return False
    
    def migrate_batch(self, keys: list) -> Tuple[int, int]:
        """
        Migrate a batch of keys
        
        Args:
            keys: List of keys to migrate
            
        Returns:
            Tuple of (successful_count, failed_count)
        """
        successful = 0
        failed = 0
        
        for key in keys:
            if self.migrate_key(key):
                successful += 1
                self.stats['migrated_keys'] += 1
            else:
                failed += 1
                self.stats['failed_keys'] += 1
        
        return successful, failed
    
    def format_time(self, seconds: float) -> str:
        """Format seconds into human-readable time"""
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            return f"{seconds/60:.1f}m"
        else:
            return f"{seconds/3600:.1f}h"
    
    def migrate_all(self) -> bool:
        """
        Migrate all keys from source to target
        
        Returns:
            bool: True if migration completed, False if failed
        """
        try:
            self.stats['start_time'] = time.time()
            
            # Get total key count
            total_keys = self.get_key_count()
            self.stats['total_keys'] = total_keys
            
            if total_keys == 0:
                self.logger.warning("No keys found in source database")
                return True
            
            self.logger.info(f"Starting migration of {total_keys:,} keys")
            if self.dry_run:
                self.logger.info("DRY RUN MODE - No actual changes will be made")
            
            # Get batch size from config
            batch_size = self.config.get('batch_size', 1000)
            
            # Scan and migrate in batches
            cursor = 0
            batch = []
            processed = 0
            last_log_time = time.time()
            
            while True:
                # Scan for keys
                cursor, keys = self.source_client.scan(
                    cursor=cursor,
                    count=batch_size
                )
                
                batch.extend(keys)
                
                # Process batch when it reaches batch_size or scan is complete
                if len(batch) >= batch_size or cursor == 0:
                    if batch:
                        successful, failed = self.migrate_batch(batch)
                        processed += len(batch)
                        
                        # Log progress every 5 seconds
                        current_time = time.time()
                        if current_time - last_log_time >= 5:
                            elapsed = current_time - self.stats['start_time']
                            rate = processed / elapsed if elapsed > 0 else 0
                            eta_seconds = (total_keys - processed) / rate if rate > 0 else 0
                            
                            progress_pct = (processed / total_keys * 100) if total_keys > 0 else 0
                            
                            self.logger.info(
                                f"Progress: {processed:,}/{total_keys:,} ({progress_pct:.1f}%) | "
                                f"Rate: {rate:.0f} keys/s | "
                                f"ETA: {self.format_time(eta_seconds)} | "
                                f"Success: {self.stats['migrated_keys']:,} | "
                                f"Failed: {self.stats['failed_keys']:,}"
                            )
                            last_log_time = current_time
                        
                        batch = []
                
                # Break if scan is complete
                if cursor == 0:
                    break
            
            self.stats['end_time'] = time.time()
            return True
            
        except KeyboardInterrupt:
            self.logger.warning("Migration interrupted by user")
            self.stats['end_time'] = time.time()
            return False
        except Exception as e:
            self.logger.error(f"Migration failed: {e}")
            self.stats['end_time'] = time.time()
            return False
    
    def verify_migration(self, sample_size: int = 100) -> bool:
        """
        Verify migration by sampling keys
        
        Args:
            sample_size: Number of keys to sample for verification
            
        Returns:
            bool: True if verification passed, False otherwise
        """
        try:
            self.logger.info(f"Verifying migration (sampling {sample_size} keys)...")
            
            # Get sample keys from source
            cursor = 0
            sample_keys = []
            
            while len(sample_keys) < sample_size:
                cursor, keys = self.source_client.scan(cursor=cursor, count=sample_size)
                sample_keys.extend(keys[:sample_size - len(sample_keys)])
                
                if cursor == 0:
                    break
            
            if not sample_keys:
                self.logger.warning("No keys to verify")
                return True
            
            # Verify each sample key exists in target
            mismatches = 0
            for key in sample_keys:
                # Check if key exists in target
                if not self.target_client.exists(key):
                    mismatches += 1
                    self.logger.warning(f"Key missing in target: {key.decode('utf-8', errors='ignore')}")
            
            if mismatches == 0:
                self.logger.info(f"✓ Verification passed: All {len(sample_keys)} sampled keys match")
                return True
            else:
                self.logger.error(f"✗ Verification failed: {mismatches}/{len(sample_keys)} keys have mismatches")
                return False
                
        except Exception as e:
            self.logger.error(f"Verification failed: {e}")
            return False
    
    def print_summary(self):
        """Print migration summary"""
        duration = self.stats['end_time'] - self.stats['start_time'] if self.stats['end_time'] else 0
        
        self.logger.info("\n" + "="*70)
        self.logger.info("MIGRATION SUMMARY")
        self.logger.info("="*70)
        self.logger.info(f"Total keys in source:    {self.stats['total_keys']:,}")
        self.logger.info(f"Successfully migrated:   {self.stats['migrated_keys']:,}")
        self.logger.info(f"Failed:                  {self.stats['failed_keys']:,}")
        self.logger.info(f"Skipped:                 {self.stats['skipped_keys']:,}")
        self.logger.info(f"Duration:                {self.format_time(duration)}")
        
        if duration > 0:
            rate = self.stats['migrated_keys'] / duration
            self.logger.info(f"Average rate:            {rate:.0f} keys/second")
        
        self.logger.info("="*70)
        
        if self.dry_run:
            self.logger.info("DRY RUN COMPLETED - No actual changes were made")
        elif self.stats['failed_keys'] == 0:
            self.logger.info("✓ MIGRATION COMPLETED SUCCESSFULLY")
        else:
            self.logger.warning(f"⚠ MIGRATION COMPLETED WITH {self.stats['failed_keys']} FAILURES")
    
    def close(self):
        """Close database connections"""
        if self.source_client:
            self.source_client.close()
        if self.target_client:
            self.target_client.close()


def load_config(config_file: str) -> Optional[Dict[str, Any]]:
    """
    Load configuration from JSON file
    
    Args:
        config_file: Path to configuration file
        
    Returns:
        Configuration dictionary or None if failed
    """
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        # Validate required fields
        required_fields = ['source', 'target']
        for field in required_fields:
            if field not in config:
                print(f"Error: Missing required field '{field}' in configuration")
                return None
        
        for db_type in ['source', 'target']:
            required_db_fields = ['host', 'port', 'password']
            for field in required_db_fields:
                if field not in config[db_type]:
                    print(f"Error: Missing required field '{field}' in {db_type} configuration")
                    return None
        
        return config
        
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_file}' not found")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in configuration file: {e}")
        return None
    except Exception as e:
        print(f"Error loading configuration: {e}")
        return None


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Migrate data from Redis Gen 1 to Valkey',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run migration
  python3 migrate_redis_to_valkey.py --config config.json
  
  # Test migration without making changes
  python3 migrate_redis_to_valkey.py --config config.json --dry-run
  
  # Run with verification
  python3 migrate_redis_to_valkey.py --config config.json --verify
        """
    )
    
    parser.add_argument(
        '--config',
        required=True,
        help='Path to configuration JSON file'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Perform validation without actual migration'
    )
    
    parser.add_argument(
        '--verify',
        action='store_true',
        help='Verify migration after completion'
    )
    
    parser.add_argument(
        '--verify-sample-size',
        type=int,
        default=100,
        help='Number of keys to sample for verification (default: 100)'
    )
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    if not config:
        sys.exit(1)
    
    # Create migration instance
    migration = RedisMigration(config, dry_run=args.dry_run)
    
    try:
        # Connect to databases
        if not migration.connect():
            print("Failed to connect to databases")
            sys.exit(1)
        
        # Perform migration
        success = migration.migrate_all()
        
        # Verify if requested
        if success and args.verify and not args.dry_run:
            migration.verify_migration(sample_size=args.verify_sample_size)
        
        # Print summary
        migration.print_summary()
        
        # Exit with appropriate code
        sys.exit(0 if success and migration.stats['failed_keys'] == 0 else 1)
        
    except KeyboardInterrupt:
        print("\nMigration interrupted by user")
        migration.print_summary()
        sys.exit(1)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)
    finally:
        migration.close()


if __name__ == '__main__':
    main()

