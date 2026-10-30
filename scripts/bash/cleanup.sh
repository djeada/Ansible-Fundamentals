#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
# shellcheck source=scripts/bash/lib.sh
source "$SCRIPT_DIR/lib.sh"
course_parse_args "$@"
course_guard_path "$BASH_COURSE_ROOT"
if [ -e "$BASH_COURSE_ROOT" ]; then
    [ -d "$BASH_COURSE_ROOT" ] || course_die 'expected a Bash sandbox directory'
    if [ "$COURSE_CHECK" = false ]; then
        rm -rf -- "$BASH_COURSE_ROOT"
    fi
    course_changed "$BASH_COURSE_ROOT"
fi
course_finish
