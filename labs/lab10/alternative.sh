#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
# shellcheck source=scripts/bash/lib.sh
source "$SCRIPT_DIR/../../scripts/bash/lib.sh"
course_parse_args "$@"
candidate_valid=${COURSE_CANDIDATE_VALID-false}
course_require_boolean "$candidate_valid"
course_init
course_ensure_dir "$BASH_COURSE_ROOT/lab10" 0755
live="$BASH_COURSE_ROOT/lab10/live.conf"
course_guard_path "$live"
if [ ! -e "$live" ]; then
    course_write_file "$live" 0644 $'version=1\n'
fi
# A failed condition is handled deliberately. set -e is not try/rescue.
if [ "$candidate_valid" = true ]; then
    course_write_file "$live" 0644 $'version=2\n'
else
    course_note 'RESCUED candidate rejected before promotion; no write was rolled back'
fi
if [ "$COURSE_CHECK" = false ]; then
    [ -f "$live" ] || course_die 'no surviving live configuration'
fi
course_note 'ALWAYS surviving configuration inspected (predicted writes are not verified in check mode)'
course_finish
