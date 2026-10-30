#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
# shellcheck source=scripts/bash/lib.sh
source "$SCRIPT_DIR/../../scripts/bash/lib.sh"
course_parse_args "$@"
message=${COURSE_MESSAGE-Hello from Bash}
printf -v desired '%s\n' "$message"
course_init
course_ensure_dir "$BASH_COURSE_ROOT/lab07" 0755
course_write_file "$BASH_COURSE_ROOT/lab07/config.txt" 0644 "$desired"
if [ "$COURSE_LAST_CHANGED" = true ]; then
    course_note 'HANDLER simulated reload'
    printf -v receipt 'Loaded configuration: %s\n' "$message"
    course_write_file "$BASH_COURSE_ROOT/lab07/reload.txt" 0644 "$receipt"
fi
course_finish
