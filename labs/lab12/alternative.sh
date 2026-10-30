#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
# shellcheck source=scripts/bash/lib.sh
source "$SCRIPT_DIR/../../scripts/bash/lib.sh"
verify_only=false
while [ "$#" -gt 0 ]; do
    case $1 in
        --check) COURSE_CHECK=true ;;
        --verify-only) verify_only=true ;;
        *) course_die 'expected --check, --verify-only, or no arguments' ;;
    esac
    shift
done
[ "$verify_only" = false ] || [ "$COURSE_CHECK" = false ] ||
    course_die '--verify-only and --check are separate modes'
expected_version=${COURSE_EXPECTED_VERSION-v1}
[[ $expected_version =~ ^v[0-9]+$ ]] || course_die 'expected version must match v followed by digits'
manifest="$BASH_COURSE_ROOT/lab12/release.json"
course_guard_path "$manifest"
if [ "$verify_only" = false ]; then
    course_init
    course_ensure_dir "$BASH_COURSE_ROOT/lab12" 0755
    course_write_file "$manifest" 0644 $'{"version":"v1","healthy":true}\n'
fi
if [ "$COURSE_CHECK" = false ]; then
    printf -v expected '{"version":%s,"healthy":true}\n' "$(course_json_quote "$expected_version")"
    # Verify actual bytes, not the preceding write result. A strict canonical-file
    # contract avoids pretending Bash includes a general-purpose JSON parser.
    if [ ! -f "$manifest" ] || ! printf '%s' "$expected" | cmp -s - "$manifest"; then
        course_die 'release contract failed (expected canonical JSON bytes); verification did not repair the file'
    fi
    course_note 'VERIFIED canonical release manifest'
fi
course_finish
