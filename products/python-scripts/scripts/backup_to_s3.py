#!/usr/bin/env python3
"""
Backup to S3
Version: 1.0.0

Backs up specified files and directories to AWS S3.
Supports gzip compression, incremental backups, and retention policies.

Usage:
    python backup_to_s3.py --config config.py

Requirements:
    pip install boto3

Environment variables (alternative to config):
    AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY
    AWS_DEFAULT_REGION
    S3_BUCKET
"""

import argparse
import gzip
import hashlib
import json
import os
import sys
import tarfile
import tempfile
from datetime import datetime
from pathlib import Path

try:
    import boto3
    from botocore.exceptions import ClientError
except ImportError:
    print("ERROR: boto3 not installed. Run: pip install boto3")
    sys.exit(1)


def compute_checksum(filepath: str, algorithm: str = "sha256") -> str:
    """Compute file checksum."""
    h = hashlib.new(algorithm)
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def create_backup_archive(sources: list, output_path: str, compress: bool = True) -> str:
    """Create a tar archive of all source files."""
    mode = "w:gz" if compress else "w"
    with tarfile.open(output_path, mode) as tar:
        for source in sources:
            source_path = Path(source)
            if not source_path.exists():
                print(f"  ⚠️  Source not found, skipping: {source}")
                continue
            if source_path.is_file():
                tar.add(source_path, arcname=source_path.name)
            else:
                tar.add(source_path, arcname=source_path.name)
    return output_path


def upload_to_s3(
    filepath: str,
    bucket: str,
    key: str,
    region: str,
    aws_access_key_id: str,
    aws_secret_access_key: str,
    metadata: Optional[dict] = None,
) -> bool:
    """Upload a file to S3."""
    extra_args = {"Metadata": metadata} if metadata else {}

    try:
        s3 = boto3.client(
            "s3",
            region_name=region,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )
        s3.upload_file(filepath, bucket, key, ExtraArgs=extra_args)
        return True
    except ClientError as e:
        print(f"  ❌ S3 upload error: {e}")
        return False


def list_s3_backups(bucket: str, prefix: str, region: str, aws_access_key_id: str, aws_secret_access_key: str) -> list:
    """List existing backups in S3."""
    s3 = boto3.client(
        "s3",
        region_name=region,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )
    try:
        response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
        return response.get("Contents", [])
    except ClientError:
        return []


def delete_old_backups(bucket: str, prefix: str, region: str, aws_access_key_id: str, aws_secret_access_key: str, keep_count: int):
    """Delete oldest backups, keeping only the most recent `keep_count`."""
    backups = list_s3_backups(bucket, prefix, region, aws_access_key_id, aws_secret_access_key)
    if len(backups) <= keep_count:
        return

    backups.sort(key=lambda x: x["LastModified"])
    to_delete = backups[:-keep_count]

    s3 = boto3.client(
        "s3",
        region_name=region,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )

    for obj in to_delete:
        key = obj["Key"]
        try:
            s3.delete_object(Bucket=bucket, Key=key)
            print(f"  🗑️  Deleted old backup: {key}")
        except ClientError as e:
            print(f"  ⚠️  Could not delete {key}: {e}")


def run_backup(config: dict):
    """Execute the backup process."""
    bucket = config["s3_bucket"]
    prefix = config.get("s3_prefix", "backups/")
    region = config.get("aws_region", "us-east-1")
    sources = config.get("sources", [])
    compress = config.get("compress", True)
    keep_backups = config.get("keep_backups", 10)

    aws_key = config.get("aws_access_key_id") or os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret = config.get("aws_secret_access_key") or os.environ.get("AWS_SECRET_ACCESS_KEY")

    if not aws_key or not aws_secret:
        print("❌ AWS credentials not provided")
        sys.exit(1)

    timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H%M%S")
    archive_name = f"backup_{timestamp}.tar.gz"
    archive_path = os.path.join(tempfile.gettempdir(), archive_name)

    print(f"📦 Creating backup archive...")
    create_backup_archive(sources, archive_path, compress=compress)
    checksum = compute_checksum(archive_path)

    s3_key = f"{prefix.rstrip('/')}/{archive_name}"
    print(f"⬆️  Uploading to s3://{bucket}/{s3_key}...")

    success = upload_to_s3(
        filepath=archive_path,
        bucket=bucket,
        key=s3_key,
        region=region,
        aws_access_key_id=aws_key,
        aws_secret_access_key=aws_secret,
        metadata={"checksum": checksum, "sources": json.dumps(sources)},
    )

    if success:
        print(f"  ✅ Backup complete: {s3_key}")
        print(f"  📋 Checksum: {checksum}")

        if keep_backups > 0:
            print(f"🧹 Cleaning up old backups (keeping {keep_backups})...")
            delete_old_backups(bucket, prefix, region, aws_key, aws_secret, keep_backups)
    else:
        print("❌ Backup failed")
        sys.exit(1)

    # Cleanup temp file
    os.unlink(archive_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Backup files to AWS S3")
    parser.add_argument("--config", required=True, help="Python config file with backup settings")
    args = parser.parse_args()

    import importlib.util

    spec = importlib.util.spec_from_file_location("backup_config", args.config)
    cfg_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cfg_module)
    config = {k: v for k, v in vars(cfg_module).items() if not k.startswith("_")}

    print(f"🚀 Backup started at {datetime.now().isoformat()}")
    run_backup(config)
    print(f"✅ Backup finished at {datetime.now().isoformat()}")
