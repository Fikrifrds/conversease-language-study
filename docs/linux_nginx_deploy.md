# Linux + Nginx Deployment Guide

Panduan ini untuk deploy Conversease ke satu remote server Linux dengan Nginx sebagai reverse proxy. Targetnya mudah dijalankan, mudah di-maintain, dan cukup aman untuk controlled paid beta manual transfer.

## Target Server Conversease.com

Bagian ini adalah jalur deploy yang dipakai untuk server sekarang:

```text
Domain utama   : conversease.com
Domain API     : api.conversease.com
Server IP      : 85.190.242.47
App path       : /var/www/conversease/app
Backup path    : /var/www/conversease/backups
Web internal   : 127.0.0.1:3010
API internal   : 127.0.0.1:8010
PostgreSQL     : 127.0.0.1:5432
Redis          : 127.0.0.1:6379
```

DNS yang dibutuhkan:

```text
@    A  85.190.242.47
www  A  85.190.242.47
api  A  85.190.242.47
```

Jangan pakai `A www` dan `CNAME www` bersamaan. Untuk setup ini pilih `A www`.

Environment production yang penting:

```bash
PUBLIC_APP_URL=https://conversease.com
API_BASE_URL=https://api.conversease.com
CORS_ORIGINS_RAW=https://conversease.com,https://www.conversease.com
NEXT_PUBLIC_API_BASE_URL=https://api.conversease.com/api
GOOGLE_OAUTH_REDIRECT_URI=https://api.conversease.com/api/auth/google/callback
```

Clone/update repo:

```bash
cd /var/www
git clone https://github.com/Fikrifrds/conversease-language-study.git conversease/app
cd /var/www/conversease/app
```

Jika repo sudah ada:

```bash
cd /var/www/conversease/app
git pull
```

Siapkan API virtualenv:

```bash
cd /var/www/conversease/app/apps/api
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
pip install -e ".[dev]"
```

Jalankan migration:

```bash
cd /var/www/conversease/app
set -a
. ./.env.production
set +a
apps/api/.venv/bin/alembic -c apps/api/alembic.ini upgrade head
PYTHONPATH=apps/api apps/api/.venv/bin/python -m app.db.migration_status
```

Build web:

```bash
cd /var/www/conversease/app
npm install
npm run build --workspace apps/web
mkdir -p apps/web/.next/standalone/apps/web/public
mkdir -p apps/web/.next/standalone/apps/web/.next/static
cp -R apps/web/public/. apps/web/.next/standalone/apps/web/public/
cp -R apps/web/.next/static/. apps/web/.next/standalone/apps/web/.next/static/
```

Systemd API:

```ini
[Unit]
Description=Conversease API
After=network.target postgresql.service redis-server.service

[Service]
Type=simple
WorkingDirectory=/var/www/conversease/app/apps/api
EnvironmentFile=/var/www/conversease/app/.env.production
ExecStart=/var/www/conversease/app/apps/api/.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8010 --workers 2
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Systemd web:

```ini
[Unit]
Description=Conversease Web
After=network.target

[Service]
Type=simple
WorkingDirectory=/var/www/conversease/app/apps/web/.next/standalone
EnvironmentFile=/var/www/conversease/app/.env.production
Environment=PORT=3010
Environment=HOSTNAME=127.0.0.1
ExecStart=/usr/bin/node apps/web/server.js
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Aktifkan service:

```bash
sudo cp infra/systemd/conversease-api.service /etc/systemd/system/conversease-api.service
sudo cp infra/systemd/conversease-web.service /etc/systemd/system/conversease-web.service
sudo systemctl daemon-reload
sudo systemctl enable conversease-api conversease-web
sudo systemctl restart conversease-api conversease-web
sudo systemctl status conversease-api
sudo systemctl status conversease-web
```

Cek internal:

```bash
curl http://127.0.0.1:8010/api/health
curl http://127.0.0.1:8010/api/ready
curl -I http://127.0.0.1:3010/
```

Nginx:

```bash
sudo cp infra/nginx/conversease.production.conf /etc/nginx/sites-available/conversease
sudo ln -s /etc/nginx/sites-available/conversease /etc/nginx/sites-enabled/conversease
sudo nginx -t
sudo systemctl reload nginx
sudo certbot --nginx -d conversease.com -d www.conversease.com -d api.conversease.com
sudo certbot renew --dry-run
```

Release check:

```bash
cd /var/www/conversease/app
set -a
. ./.env.production
set +a
PYTHONPATH=apps/api apps/api/.venv/bin/python scripts/release_preflight.py
PYTHONPATH=apps/api apps/api/.venv/bin/python scripts/release_smoke.py \
  --api-base-url "$API_BASE_URL/api" \
  --web-base-url "$PUBLIC_APP_URL" \
  --admin-api-key "$PAYMENT_ADMIN_API_KEY"
```

## Ringkasan Keputusan

Docker tidak wajib, tapi untuk proyek ini Docker Compose adalah opsi yang paling direkomendasikan.

Alasannya:

- Struktur repo sudah punya Dockerfile untuk API dan Web.
- PostgreSQL, Redis, API, dan Web bisa dikelola sebagai satu stack.
- Rollback dan restart lebih mudah.
- Dependency Python/Node tidak mencemari OS server.
- Nginx tetap berjalan di host sehingga HTTPS, log, firewall, dan Certbot mudah dikelola.

Rekomendasi production beta:

```text
Internet
  |
Nginx host :443
  |-- app.example.com -> 127.0.0.1:3000 -> web container
  |-- api.example.com -> 127.0.0.1:8000 -> api container

Docker Compose internal:
  web
  api
  postgres
  redis
```

PostgreSQL hanya dibuka ke `127.0.0.1:5432` untuk backup/admin lokal dari server, bukan publik.

## Kebutuhan Server

Minimal untuk beta kecil:

- Ubuntu 22.04 LTS atau 24.04 LTS
- 2 vCPU
- 2 GB RAM minimum, 4 GB lebih nyaman
- 30 GB disk minimum
- Domain/subdomain:
  - `app.example.com`
  - `api.example.com`
- Akses SSH sudo

DNS:

```text
app.example.com  A  <server-ip>
api.example.com  A  <server-ip>
```

## Install Package Dasar

Login ke server:

```bash
ssh root@<server-ip>
```

Update package:

```bash
apt update
apt upgrade -y
apt install -y git curl ca-certificates gnupg nginx certbot python3-certbot-nginx postgresql-client ufw
```

Install Docker:

```bash
curl -fsSL https://get.docker.com | sh
systemctl enable docker
systemctl start docker
```

Opsional: buat user deploy.

```bash
adduser deploy
usermod -aG sudo deploy
usermod -aG docker deploy
```

Logout lalu login ulang sebagai `deploy` agar group Docker aktif:

```bash
ssh deploy@<server-ip>
```

## Struktur Folder Server

Gunakan `/opt/conversease`:

```bash
sudo mkdir -p /opt/conversease
sudo chown -R "$USER:$USER" /opt/conversease
cd /opt/conversease
```

Clone repo:

```bash
git clone <repo-url> app
cd /opt/conversease/app
```

Folder backup:

```bash
sudo mkdir -p /opt/conversease/backups
sudo chown -R "$USER:$USER" /opt/conversease/backups
chmod 700 /opt/conversease/backups
```

## Environment Production

Copy template:

```bash
cp .env.production.example .env.production
chmod 600 .env.production
```

Edit:

```bash
nano .env.production
```

Wajib diganti:

```bash
POSTGRES_PASSWORD=<strong-postgres-password>
DATABASE_URL=postgresql+psycopg://conversease:<url-encoded-password>@postgres:5432/conversease_db
BACKUP_DATABASE_URL=postgresql+psycopg://conversease:<url-encoded-password>@127.0.0.1:5432/conversease_db

RELEASE_VERSION=2026.06.04
APP_ENV=production
PUBLIC_APP_URL=https://app.example.com
API_BASE_URL=https://api.example.com
CORS_ORIGINS_RAW=https://app.example.com
NEXT_PUBLIC_API_BASE_URL=https://api.example.com/api

JWT_SECRET=<random-min-32-char>
GOOGLE_OAUTH_CLIENT_ID=<google-client-id>
GOOGLE_OAUTH_CLIENT_SECRET=<google-client-secret>
GOOGLE_OAUTH_REDIRECT_URI=https://api.example.com/api/auth/google/callback

RESEND_API_KEY=<resend-api-key>
PAYMENT_ADMIN_API_KEY=<random-min-24-char>
PAYMENT_ADMIN_EMAIL=denahku.team@gmail.com
```

Generate secret:

```bash
openssl rand -base64 32
```

Catatan penting:

- Jangan commit `.env.production`.
- Jika password database mengandung karakter seperti `@`, `:`, `/`, `#`, atau spasi, URL-encode password itu di `DATABASE_URL`.
- `NEXT_PUBLIC_API_BASE_URL` dibake ke build Next.js. Kalau nilainya berubah, image web harus di-build ulang.
- Untuk beta manual transfer, `MIDTRANS_*` boleh kosong. Untuk public paid checkout otomatis, Midtrans harus diisi dan webhook perlu diuji.

## Build Dan Start Stack

Selalu pakai command ini dari root repo:

```bash
cd /opt/conversease/app
```

Validasi compose:

```bash
docker compose --env-file .env.production -f docker-compose.prod.yml config
```

Untuk validasi memakai template tanpa membuat `.env.production`:

```bash
CONVERSEASE_ENV_FILE=.env.production.example \
  docker compose --env-file .env.production.example -f docker-compose.prod.yml config
```

Build image:

```bash
docker compose --env-file .env.production -f docker-compose.prod.yml build
```

Start database/cache dulu:

```bash
docker compose --env-file .env.production -f docker-compose.prod.yml up -d postgres redis
```

Jalankan migration:

```bash
docker compose --env-file .env.production -f docker-compose.prod.yml run --rm api alembic -c alembic.ini upgrade head
```

Start API dan Web:

```bash
docker compose --env-file .env.production -f docker-compose.prod.yml up -d api web
```

Cek status:

```bash
docker compose --env-file .env.production -f docker-compose.prod.yml ps
```

Log cepat:

```bash
docker compose --env-file .env.production -f docker-compose.prod.yml logs --tail=100 api
docker compose --env-file .env.production -f docker-compose.prod.yml logs --tail=100 web
```

Tes dari host server:

```bash
curl http://127.0.0.1:8000/api/health
curl http://127.0.0.1:8000/api/ready
curl -I http://127.0.0.1:3000/
```

## Nginx

Copy contoh config:

```bash
sudo cp infra/nginx/conversease.production.conf /etc/nginx/sites-available/conversease
sudo nano /etc/nginx/sites-available/conversease
```

Ganti semua:

```text
app.example.com
api.example.com
```

dengan domain asli.

Enable site:

```bash
sudo ln -s /etc/nginx/sites-available/conversease /etc/nginx/sites-enabled/conversease
sudo nginx -t
sudo systemctl reload nginx
```

Jika file default mengganggu:

```bash
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx
```

## HTTPS Dengan Certbot

Pastikan DNS sudah mengarah ke server, lalu:

```bash
sudo certbot --nginx -d app.example.com -d api.example.com
```

Certbot biasanya akan mengubah config Nginx otomatis. Setelah selesai:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

Test renewal:

```bash
sudo certbot renew --dry-run
```

Jika certificate path berbeda dari contoh config, sesuaikan:

```text
/etc/letsencrypt/live/<cert-name>/fullchain.pem
/etc/letsencrypt/live/<cert-name>/privkey.pem
```

## Firewall

Aktifkan UFW:

```bash
sudo ufw allow OpenSSH
sudo ufw allow "Nginx Full"
sudo ufw enable
sudo ufw status
```

Jangan buka port berikut ke publik:

```text
3000 web internal
8000 api internal
5432 postgres local-only
6379 redis internal
```

Production compose sudah bind web/API/Postgres ke `127.0.0.1`, bukan `0.0.0.0`.
Container web hanya menerima `NEXT_PUBLIC_API_BASE_URL`; secret backend tetap di API/Postgres.

## Release Preflight

Untuk preflight dari host, install dependency API sekali:

```bash
cd /var/www/conversease/app/apps/api
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
pip install -e ".[dev]"
cd /var/www/conversease/app
```

Export env dari `.env.production` lalu jalankan:

```bash
set -a
. ./.env.production
set +a
PYTHONPATH=apps/api apps/api/.venv/bin/python scripts/release_preflight.py
```

Untuk controlled beta, hasil yang boleh tersisa sebagai warning:

- `midtrans_checkout_webhook`
- `ai_stt_tts_automation`

Jika ada fail, jangan buka traffic.

## Smoke Test Setelah Deploy

Jalankan:

```bash
set -a
. ./.env.production
set +a
PYTHONPATH=apps/api apps/api/.venv/bin/python scripts/release_smoke.py \
  --api-base-url "$API_BASE_URL/api" \
  --web-base-url "$PUBLIC_APP_URL" \
  --admin-api-key "$PAYMENT_ADMIN_API_KEY"
```

Harus menghasilkan:

```json
{"status":"pass"}
```

Script ini mengecek:

- API health, ready, metrics
- courses, lesson awal, A1 final test, plans
- landing, login, pricing
- security headers web
- admin email template list/render

## Human UAT Manual Transfer Bank Jago

Setelah smoke otomatis pass:

1. Buka `https://app.example.com`.
2. Register user baru.
3. Verify email dari Resend.
4. Login.
5. Buka Billing.
6. Pilih paket Pro.
7. Pastikan instruksi Bank Jago muncul.
8. Pastikan amount berisi unique code 3 digit.
9. Transfer tepat sesuai nominal.
10. User klik konfirmasi pembayaran.
11. Pastikan email masuk ke `PAYMENT_ADMIN_EMAIL`.
12. Buka `/admin/payments`.
13. Masukkan `PAYMENT_ADMIN_API_KEY`.
14. Cocokkan exact amount, unique code, tanggal, dan sender dengan mutasi Bank Jago.
15. Approve.
16. Pastikan akses user aktif.
17. Pastikan user menerima email approval.
18. Reload `/billing?order_id=<order-id>` dan pastikan status tetap benar.

## Update Release Berikutnya

Dari server:

```bash
cd /opt/conversease/app
git pull
```

Build ulang:

```bash
docker compose --env-file .env.production -f docker-compose.prod.yml build
```

Jalankan migration:

```bash
docker compose --env-file .env.production -f docker-compose.prod.yml run --rm api alembic -c alembic.ini upgrade head
```

Restart service:

```bash
docker compose --env-file .env.production -f docker-compose.prod.yml up -d
```

Verifikasi:

```bash
set -a
. ./.env.production
set +a
PYTHONPATH=apps/api apps/api/.venv/bin/python scripts/release_preflight.py
PYTHONPATH=apps/api apps/api/.venv/bin/python scripts/release_smoke.py \
  --api-base-url "$API_BASE_URL/api" \
  --web-base-url "$PUBLIC_APP_URL" \
  --admin-api-key "$PAYMENT_ADMIN_API_KEY"
```

Rollback sederhana jika release baru bermasalah:

```bash
git log --oneline -5
git checkout <previous-good-commit>
docker compose --env-file .env.production -f docker-compose.prod.yml build
docker compose --env-file .env.production -f docker-compose.prod.yml up -d
```

Jika migration sudah mengubah schema, rollback harus mengikuti prosedur migration/database backup. Jangan downgrade production tanpa backup.

## Monitoring Harian

Health endpoint:

```bash
curl -fsS https://api.example.com/api/health
curl -fsS https://api.example.com/api/ready
curl -fsS https://api.example.com/api/metrics
```

Container status:

```bash
docker compose --env-file .env.production -f docker-compose.prod.yml ps
docker compose --env-file .env.production -f docker-compose.prod.yml logs --tail=200 api
docker compose --env-file .env.production -f docker-compose.prod.yml logs --tail=200 web
```

Nginx logs:

```bash
sudo tail -n 100 /var/log/nginx/conversease-api.access.log
sudo tail -n 100 /var/log/nginx/conversease-api.error.log
sudo tail -n 100 /var/log/nginx/conversease-web.access.log
sudo tail -n 100 /var/log/nginx/conversease-web.error.log
```

Server resources:

```bash
df -h
free -m
docker stats --no-stream
docker system df
```

Rekomendasi monitoring eksternal:

- Uptime check untuk `https://api.example.com/api/ready`
- Uptime check untuk `https://app.example.com`
- Alert jika `/api/ready` bukan 200
- Alert disk jika root disk > 80 persen
- Alert backup jika tidak ada file backup baru dalam 24 jam
- Error tracking seperti Sentry sebelum public paid traffic

## Backup Database

Install `postgresql-client` di host sudah dilakukan di awal.

Backup manual:

```bash
set -a
. ./.env.production
set +a
DATABASE_URL="$BACKUP_DATABASE_URL" BACKUP_DIR="$BACKUP_DIR" bash scripts/backup_postgres.sh
```

Verify backup:

```bash
BACKUP_FILE=/opt/conversease/backups/conversease-YYYYMMDDTHHMMSSZ.dump \
  bash scripts/verify_postgres_backup.sh
```

Cron harian:

```bash
crontab -e
```

Contoh jam 02:15 UTC:

```cron
15 2 * * * cd /opt/conversease/app && set -a && . ./.env.production && set +a && DATABASE_URL="$BACKUP_DATABASE_URL" BACKUP_DIR="$BACKUP_DIR" AUTO_DELETE_BACKUPS=true bash scripts/backup_postgres.sh >> /opt/conversease/backups/backup.log 2>&1
```

Minimal:

- Backup harian.
- Retain 14 hari.
- Copy backup ke storage di luar server jika memungkinkan.
- Test restore ke staging sebelum public paid release.

## Restore Test Ke Staging

Jangan restore ke production kecuali sedang incident dan sudah diputuskan.

Untuk test restore:

```bash
BACKUP_FILE=/opt/conversease/backups/conversease-YYYYMMDDTHHMMSSZ.dump \
RESTORE_DATABASE_URL="$STAGING_DATABASE_URL" \
ALLOW_RESTORE_CLEAN=true \
bash scripts/verify_postgres_backup.sh
```

## Maintenance Commands

Restart API:

```bash
docker compose --env-file .env.production -f docker-compose.prod.yml restart api
```

Restart Web:

```bash
docker compose --env-file .env.production -f docker-compose.prod.yml restart web
```

Restart semua app service:

```bash
docker compose --env-file .env.production -f docker-compose.prod.yml up -d api web
```

Masuk shell API:

```bash
docker compose --env-file .env.production -f docker-compose.prod.yml exec api sh
```

Masuk Postgres:

```bash
psql "$BACKUP_DATABASE_URL"
```

Lihat migration status dari host:

```bash
set -a
. ./.env.production
set +a
PYTHONPATH=apps/api apps/api/.venv/bin/python -m app.db.migration_status
```

## Optional Systemd Wrapper

Docker restart policy sudah cukup untuk banyak VPS. Jika ingin command standar `systemctl`, buat service:

```bash
sudo nano /etc/systemd/system/conversease.service
```

Isi:

```ini
[Unit]
Description=Conversease Docker Compose stack
Requires=docker.service
After=docker.service network-online.target

[Service]
Type=oneshot
WorkingDirectory=/opt/conversease/app
ExecStart=/usr/bin/docker compose --env-file .env.production -f docker-compose.prod.yml up -d
ExecStop=/usr/bin/docker compose --env-file .env.production -f docker-compose.prod.yml stop
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
```

Enable:

```bash
sudo systemctl daemon-reload
sudo systemctl enable conversease
sudo systemctl start conversease
sudo systemctl status conversease
```

## Non-Docker Alternative

Non-Docker bisa, tapi lebih banyak yang harus di-maintain sendiri:

- Install Python/Node/PostgreSQL/Redis di host.
- Jalankan API dengan systemd.
- Jalankan Next standalone dengan systemd.
- Pastikan env production ada di file yang permission-nya aman.
- Pastikan migration dijalankan manual sebelum restart API.

Pola systemd API:

```ini
[Unit]
Description=Conversease API
After=network.target postgresql.service redis-server.service

[Service]
User=conversease
WorkingDirectory=/opt/conversease/app/apps/api
EnvironmentFile=/opt/conversease/app/.env.production
ExecStart=/opt/conversease/app/apps/api/.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 2
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Pola systemd Web:

```ini
[Unit]
Description=Conversease Web
After=network.target

[Service]
User=conversease
WorkingDirectory=/opt/conversease/app
EnvironmentFile=/opt/conversease/app/.env.production
ExecStart=/usr/bin/node apps/web/server.js
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Untuk proyek ini, gunakan non-Docker hanya jika server sudah punya standard operating procedure untuk Python/Node service.

## Troubleshooting

API ready 503:

```bash
curl https://api.example.com/api/ready
docker compose --env-file .env.production -f docker-compose.prod.yml logs --tail=200 api
```

Penyebab umum:

- Database belum siap.
- Migration belum head.
- `DATABASE_URL` salah.
- Container API belum restart setelah env berubah.

Web masih memanggil API lama:

- `NEXT_PUBLIC_API_BASE_URL` salah saat build.
- Build ulang web:

```bash
docker compose --env-file .env.production -f docker-compose.prod.yml build web
docker compose --env-file .env.production -f docker-compose.prod.yml up -d web
```

Admin key ditolak:

- Pastikan `PAYMENT_ADMIN_API_KEY` di `.env.production` sama dengan yang dimasukkan di `/admin/payments`.
- Restart API setelah env diganti.

Email tidak terkirim:

- Cek `RESEND_API_KEY`.
- Cek sender domain sudah verified di Resend.
- Jalankan `/api/admin/test-email/render`.
- Jalankan `/api/admin/test-email/send`.

Nginx 502:

```bash
docker compose --env-file .env.production -f docker-compose.prod.yml ps
curl http://127.0.0.1:3000/
curl http://127.0.0.1:8000/api/health
sudo tail -n 100 /var/log/nginx/conversease-api.error.log
```

Disk penuh:

```bash
df -h
docker system df
docker image prune
```

Jangan prune volume database.

## Final Release Checklist

Sebelum traffic user:

- DNS sudah benar.
- HTTPS aktif dan renew test pass.
- `.env.production` tidak berisi placeholder.
- `docker compose ps` semua healthy.
- `/api/ready` return 200.
- `release_preflight.py` pass.
- `release_smoke.py` pass.
- Test email admin sent true.
- Manual transfer UAT pass.
- Backup pertama berhasil dan checksum verified.
- Admin menyimpan `PAYMENT_ADMIN_API_KEY` di password manager.
