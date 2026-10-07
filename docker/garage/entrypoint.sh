#!/bin/sh
set -eu

: "${GARAGE_RPC_SECRET:?GARAGE_RPC_SECRET is required}"
: "${GARAGE_ADMIN_TOKEN:?GARAGE_ADMIN_TOKEN is required}"

config_dir=/run/garage
config_file="${GARAGE_CONFIG_FILE:-${config_dir}/garage.toml}"
mkdir -p "$config_dir"
umask 077

cat > "$config_file" <<EOF
metadata_dir = "/var/lib/garage/meta"
data_dir = "/var/lib/garage/data"
db_engine = "sqlite"
replication_factor = 1
compression_level = 2
rpc_bind_addr = "[::]:3901"
rpc_public_addr = "garage:3901"
rpc_secret = "${GARAGE_RPC_SECRET}"

[s3_api]
s3_region = "${S3_REGION_NAME:-garage}"
api_bind_addr = "[::]:3900"

[admin]
api_bind_addr = "[::]:3903"
admin_token = "${GARAGE_ADMIN_TOKEN}"
EOF

exec /garage -c "$config_file" "$@"
