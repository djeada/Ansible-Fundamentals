#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
# shellcheck source=scripts/bash/lib.sh
source "$SCRIPT_DIR/../../scripts/bash/lib.sh"
course_parse_args "$@"
environment=${COURSE_ENVIRONMENT-development}
message=${COURSE_MESSAGE-Hello from Bash}
port=${COURSE_PORT-8080}
course_require_environment "$environment"
# Environment variables are text. Accept a bounded canonical decimal string
# before arithmetic or emitting an unquoted JSON number.
case $port in
    ''|*[!0-9]*|0*) course_die 'port must be a canonical decimal integer from 1025 to 65535' ;;
esac
[ "${#port}" -le 5 ] || course_die 'port must be from 1025 to 65535'
[ "$port" -ge 1025 ] && [ "$port" -le 65535 ] || course_die 'port must be from 1025 to 65535'
printf -v desired '{"environment":%s,"port":%s,"message":%s}\n' \
    "$(course_json_quote "$environment")" "$port" "$(course_json_quote "$message")"
course_init
course_ensure_dir "$BASH_COURSE_ROOT/lab06" 0755
course_write_file "$BASH_COURSE_ROOT/lab06/app.json" 0644 "$desired"
course_note 'Known JSON shape serialized from validated inputs; no general-purpose JSON parser was run.'
course_finish
