#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
# shellcheck source=scripts/bash/lib.sh
source "$SCRIPT_DIR/../../scripts/bash/lib.sh"
course_parse_args "$@"
release=${COURSE_RELEASE-v1}
limit=${COURSE_LIMIT-}
failure_host=${COURSE_FAILURE_HOST-}
[[ $release =~ ^v[0-9]+$ ]] || course_die 'release must match v followed by digits'
case $limit in ''|node_a|node_b) ;; *) course_die 'limit must be node_a or node_b' ;; esac
case $failure_host in ''|node_a|node_b) ;; *) course_die 'failure host must be node_a or node_b' ;; esac
[ -z "$limit" ] || [ -z "$failure_host" ] || [ "$limit" = "$failure_host" ] ||
    course_die 'failure host is outside the selected limit'
course_init
# These are logical names on this one machine, not remote SSH targets.
for host in node_a node_b; do
    if [ -n "$limit" ] && [ "$host" != "$limit" ]; then
        continue
    fi
    course_note "BATCH $host controller=localhost"
    if [ "$host" = "$failure_host" ]; then
        course_die "simulated failure on $host before deployment; later hosts were not processed"
    fi
    course_ensure_dir "$BASH_COURSE_ROOT/lab11/$host" 0755
    printf -v desired 'release=%s\n' "$release"
    course_write_file "$BASH_COURSE_ROOT/lab11/$host/release.txt" 0644 "$desired"
done
course_finish
