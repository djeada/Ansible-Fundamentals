#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
# shellcheck source=scripts/bash/lib.sh
source "$SCRIPT_DIR/../../scripts/bash/lib.sh"
course_parse_args "$@"
course_init
printf 'host=localhost connection=local shell=Bash %s\n' "$BASH_VERSION"
course_note 'Local shell execution succeeded; no SSH, inventory parser, or Python module was involved.'
course_finish
