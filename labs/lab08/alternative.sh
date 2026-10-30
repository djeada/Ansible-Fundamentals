#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
# shellcheck source=scripts/bash/lib.sh
source "$SCRIPT_DIR/../../scripts/bash/lib.sh"
# shellcheck source=scripts/bash/training_site.sh
source "$SCRIPT_DIR/../../scripts/bash/training_site.sh"
course_parse_args "$@"
environment=${COURSE_ENVIRONMENT-development}
title=${COURSE_SITE_TITLE-My first reusable Bash function}
description=${COURSE_SITE_DESCRIPTION-A page rendered from explicit function inputs.}
[ -n "$title" ] || course_die 'site title must not be empty'
course_require_environment "$environment"
course_init
course_render_site "$BASH_COURSE_ROOT/lab08" "$title" "$description" "$environment" localhost
course_finish
