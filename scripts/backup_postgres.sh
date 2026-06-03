#!/usr/bin/env bash
set -euo pipefail

: "${DATABASE_URL:?DATABASE_URL is required}"

BACKUP_DIR="${BACKUP_DIR:-./backups}"
BACKUP_RETENTION_DAYS="${BACKUP_RETENTION_DAYS:-14}"
AUTO_DELETE_BACKUPS="${AUTO_DELETE_BACKUPS:-false}"
timestamp="$(date -u +%Y%m%dT%H%M%SZ)"
backup_file="${BACKUP_DIR}/conversease-${timestamp}.dump"
checksum_file="${backup_file}.sha256"
manifest_file="${backup_file}.manifest.json"

if ! command -v pg_dump >/dev/null 2>&1; then
  echo "pg_dump is required to create PostgreSQL backups." >&2
  exit 1
fi

mkdir -p "${BACKUP_DIR}"

pg_dump "${DATABASE_URL}" --format=custom --file="${backup_file}"
backup_sha256="$(shasum -a 256 "${backup_file}" | awk '{print $1}')"
printf "%s  %s\n" "${backup_sha256}" "${backup_file}" > "${checksum_file}"

if backup_size_bytes="$(stat -c%s "${backup_file}" 2>/dev/null)"; then
  :
else
  backup_size_bytes="$(stat -f%z "${backup_file}")"
fi

cat > "${manifest_file}" <<JSON
{
  "service": "conversease",
  "created_at": "${timestamp}",
  "backup_file": "$(basename "${backup_file}")",
  "format": "pg_dump_custom",
  "sha256": "${backup_sha256}",
  "size_bytes": ${backup_size_bytes},
  "retention_days": ${BACKUP_RETENTION_DAYS}
}
JSON

echo "Created ${backup_file}"
echo "Checksum ${checksum_file}"
echo "Manifest ${manifest_file}"

if [ "${AUTO_DELETE_BACKUPS}" = "true" ]; then
  find "${BACKUP_DIR}" -name "conversease-*.dump" -mtime "+${BACKUP_RETENTION_DAYS}" -delete
  find "${BACKUP_DIR}" -name "conversease-*.dump.sha256" -mtime "+${BACKUP_RETENTION_DAYS}" -delete
  find "${BACKUP_DIR}" -name "conversease-*.dump.manifest.json" -mtime "+${BACKUP_RETENTION_DAYS}" -delete
else
  echo "Backups older than ${BACKUP_RETENTION_DAYS} days:"
  find "${BACKUP_DIR}" -name "conversease-*.dump" -mtime "+${BACKUP_RETENTION_DAYS}" -print
fi
