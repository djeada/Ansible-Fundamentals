#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
# shellcheck source=scripts/bash/lib.sh
source "$SCRIPT_DIR/../../scripts/bash/lib.sh"
course_parse_args "$@"
system=$(uname -s)
architecture=$(uname -m)
printf -v desired '{"system":%s,"architecture":%s}\n' \
    "$(course_json_quote "$system")" "$(course_json_quote "$architecture")"
course_init
course_ensure_dir "$BASH_COURSE_ROOT/lab04" 0755
course_write_file "$BASH_COURSE_ROOT/lab04/facts.json" 0644 "$desired"
if [ "$system" = Linux ]; then
    course_note 'This task runs only when uname reports Linux.'
else
    course_note 'SKIPPED Linux-only explanation'
fi
course_finish
