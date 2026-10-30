#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
# shellcheck source=scripts/bash/lib.sh
source "$SCRIPT_DIR/../../scripts/bash/lib.sh"
course_parse_args "$@"
course_init
course_ensure_dir "$BASH_COURSE_ROOT/lab02" 0755
course_write_file "$BASH_COURSE_ROOT/lab02/managed.txt" 0644 $'Managed by Bash.\n'
course_finish
