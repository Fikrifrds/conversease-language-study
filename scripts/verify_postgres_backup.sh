#!/usr/bin/env bash
set -euo pipefail

: "${BACKUP_FILE:?BACKUP_FILE is required}"

CHECKSUM_FILE="${CHECKSUM_FILE:-${BACKUP_FILE}.sha256}"
RESTORE_DATABASE_URL="${RESTORE_DATABASE_URL:-}"
ALLOW_RESTORE_CLEAN="${ALLOW_RESTORE_CLEAN:-false}"

if ! command -v pg_restore >/dev/null 2>&1; then
  echo "pg_restore is required to verify PostgreSQL backups." >&2
  exit 1
fi

if [ ! -f "${BACKUP_FILE}" ]; then
  echo "Backup file not found: ${BACKUP_FILE}" >&2
  exit 1
fi

if [ ! -f "${CHECKSUM_FILE}" ]; then
  echo "Checksum file not found: ${CHECKSUM_FILE}" >&2
  exit 1
fi

expected_sha256="$(awk '{print $1}' "${CHECKSUM_FILE}")"
actual_sha256="$(shasum -a 256 "${BACKUP_FILE}" | awk '{print $1}')"

if [ "${expected_sha256}" != "${actual_sha256}" ]; then
  echo "Checksum mismatch for ${BACKUP_FILE}" >&2
  echo "Expected: ${expected_sha256}" >&2
  echo "Actual:   ${actual_sha256}" >&2
  exit 1
fi

pg_restore --list "${BACKUP_FILE}" >/dev/null
echo "Backup checksum and pg_restore catalog verified: ${BACKUP_FILE}"

if [ -z "${RESTORE_DATABASE_URL}" ]; then
  echo "Set RESTORE_DATABASE_URL and ALLOW_RESTORE_CLEAN=true to perform a staging restore test."
  exit 0
fi

if [ "${ALLOW_RESTORE_CLEAN}" != "true" ]; then
  echo "Refusing to restore because ALLOW_RESTORE_CLEAN is not true." >&2
  echo "Restore uses pg_restore --clean --if-exists and must target a disposable staging database." >&2
  exit 1
fi

if ! command -v psql >/dev/null 2>&1; then
  echo "psql is required to verify a restored PostgreSQL database." >&2
  exit 1
fi

pg_restore --dbname "${RESTORE_DATABASE_URL}" --clean --if-exists "${BACKUP_FILE}"
psql "${RESTORE_DATABASE_URL}" -v ON_ERROR_STOP=1 -c "select 1;" >/dev/null
echo "Backup restored and verified against staging database."
