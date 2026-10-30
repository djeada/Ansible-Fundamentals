#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
# shellcheck source=scripts/bash/lib.sh
source "$SCRIPT_DIR/../../scripts/bash/lib.sh"
course_parse_args "$@"
services=(web worker)
ports=(8080 9090)
enabled=(true "${COURSE_WORKER_ENABLED-false}")
course_require_boolean "${enabled[1]}"
course_init
for i in "${!services[@]}"; do
    directory="$BASH_COURSE_ROOT/lab05/${services[$i]}"
    course_ensure_dir "$directory" 0755
    if [ "${enabled[$i]}" = true ]; then
        printf -v desired 'port=%s\n' "${ports[$i]}"
        course_write_file "$directory/service.conf" 0644 "$desired"
    else
        course_note "SKIPPED configuration for ${services[$i]} (existing files are retained)"
    fi
done
course_finish
