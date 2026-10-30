#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
# shellcheck source=scripts/bash/lib.sh
source "$SCRIPT_DIR/../../scripts/bash/lib.sh"
course_parse_args "$@"
environment=${COURSE_ENVIRONMENT-development}
message=${COURSE_MESSAGE-Hello from Bash}
course_require_environment "$environment"
printf -v desired '{"environment":%s,"message":%s}\n' \
    "$(course_json_quote "$environment")" "$(course_json_quote "$message")"
course_init
course_ensure_dir "$BASH_COURSE_ROOT/lab03" 0755
course_write_file "$BASH_COURSE_ROOT/lab03/variables.json" 0644 "$desired"
printf 'File changed: %s\n' "$COURSE_LAST_CHANGED"
course_finish
