#!/usr/bin/env python3
"""
💾 Backup-Agent
Backup & Disaster Recovery Specialist

Резервное копирование, восстановление, архивация.
"""

import argparse
from pathlib import Path
from typing import Dict


class BackupAgent:
    """
    💾 Backup-Agent
    
    Специализация: Data Protection
    Задачи: Backups, Restore, Archival
    """
    
    NAME = "💾 Backup-Agent"
    ROLE = "Backup Specialist"
    EXPERTISE = ["Backup", "Disaster Recovery", "S3", "Automation"]
    
    def process_request(self, request: str) -> Dict[str, str]:
        return {
            "backup-script.sh": self._generate_backup_script(),
            "docker-backup.yml": self._generate_docker_backup(),
            "restore-script.sh": self._generate_restore_script()
        }
    
    def _generate_backup_script(self) -> str:
        return '''#!/bin/bash
# Backup Script
# Автоматическое резервное копирование

set -e

# Конфигурация
BACKUP_DIR="/backups"
S3_BUCKET="s3://my-backups"
RETENTION_DAYS=30
DATE=$(date +%Y%m%d_%H%M%S)

# Цвета
GREEN='\\033[0;32m'
RED='\\033[0;31m'
NC='\\033[0m'

log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ERROR:${NC} $1"
}

# Создать директорию
mkdir -p "$BACKUP_DIR"

# Backup PostgreSQL
backup_postgres() {
    log "Backing up PostgreSQL..."
    pg_dump -h localhost -U postgres mydb | gzip > "$BACKUP_DIR/postgres_$DATE.sql.gz"
    log "PostgreSQL backup completed"
}

# Backup files
backup_files() {
    log "Backing up files..."
    tar czf "$BACKUP_DIR/files_$DATE.tar.gz" /var/www /etc/nginx
    log "Files backup completed"
}

# Upload to S3
upload_to_s3() {
    log "Uploading to S3..."
    aws s3 sync "$BACKUP_DIR" "$S3_BUCKET/daily/" --delete
    log "Upload completed"
}

# Cleanup old backups
cleanup() {
    log "Cleaning up old backups..."
    find "$BACKUP_DIR" -type f -mtime +$RETENTION_DAYS -delete
    aws s3 ls "$S3_BUCKET/daily/" | awk '{print $4}' | while read file; do
        aws s3 rm "$S3_BUCKET/daily/$file"
    done
    log "Cleanup completed"
}

# Main
main() {
    log "Starting backup process..."
    
    backup_postgres
    backup_files
    upload_to_s3
    cleanup
    
    log "Backup process completed successfully!"
}

main "$@"
'''
    
    def _generate_docker_backup(self) -> str:
        return '''version: '3.8'
services:
  backup:
    image: offen/docker-volume-backup:latest
    restart: unless-stopped
    environment:
      BACKUP_CRON_EXPRESSION: "0 2 * * *"
      BACKUP_RETENTION_DAYS: "30"
      BACKUP_FILENAME: backup-%Y-%m-%dT%H-%M-%S.tar.gz
      AWS_S3_BUCKET_NAME: my-backups
      AWS_ACCESS_KEY_ID: ${AWS_ACCESS_KEY_ID}
      AWS_SECRET_ACCESS_KEY: ${AWS_SECRET_ACCESS_KEY}
      AWS_ENDPOINT: s3.yandexcloud.net
      AWS_S3_PATH: docker-backups
      NOTIFICATION_URLS: ${NOTIFICATION_URL}
      NOTIFICATION_LEVEL: error
    volumes:
      - app_data:/backup/app_data:ro
      - db_data:/backup/db_data:ro
      - /var/run/docker.sock:/var/run/docker.sock:ro
    networks:
      - backup-network

volumes:
  app_data:
    external: true
  db_data:
    external: true

networks:
  backup-network:
    external: true
'''
    
    def _generate_restore_script(self) -> str:
        return '''#!/bin/bash
# Restore Script
# Восстановление из резервной копии

set -e

BACKUP_FILE=$1

if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 <backup_file>"
    exit 1
fi

# Restore PostgreSQL
restore_postgres() {
    echo "Restoring PostgreSQL from $BACKUP_FILE..."
    gunzip -c "$BACKUP_FILE" | psql -h localhost -U postgres mydb
    echo "Restore completed"
}

# Restore files
restore_files() {
    echo "Restoring files from $BACKUP_FILE..."
    tar xzf "$BACKUP_FILE" -C /
    echo "Restore completed"
}

echo "Starting restore..."
restore_postgres
restore_files
echo "Restore completed!"
'''


def main():
    parser = argparse.ArgumentParser(description="💾 Backup-Agent")
    parser.add_argument("--output", "-o", help="Папка для сохранения")
    args = parser.parse_args()
    
    agent = BackupAgent()
    files = agent.process_request("setup")
    
    if args.output:
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
        for filename, content in files.items():
            (output_dir / filename).write_text(content, encoding="utf-8")
            print(f"✅ {filename}")
    else:
        print(f"💾 {agent.NAME}")
        for filename in files.keys():
            print(f"  📄 {filename}")


if __name__ == "__main__":
    main()
