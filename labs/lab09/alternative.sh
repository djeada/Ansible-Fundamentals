#!/usr/bin/env bash
set +x  # Disable tracing before reading a private value.
set -euo pipefail
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
# shellcheck source=scripts/bash/lib.sh
source "$SCRIPT_DIR/../../scripts/bash/lib.sh"
input=dummy
while [ "$#" -gt 0 ]; do
    case $1 in
        --check) COURSE_CHECK=true ;;
        --prompt|--token-stdin)
            [ "$input" = dummy ] || course_die 'choose one token input method'
            input=$1
            ;;
        *) course_die 'expected --check, --prompt, or --token-stdin' ;;
    esac
    shift
done
token='example-not-a-secret'
case $input in
    --prompt)
        IFS= read -r -s -p 'Practice token: ' token < /dev/tty || course_die 'could not read a token from the terminal'
        printf '\n' > /dev/tty
        ;;
    --token-stdin)
        token=''
        if ! IFS= read -r token; then
            [ -n "$token" ] || course_die 'missing single-line token on stdin'
        fi
        ;;
esac
[ -n "$token" ] || course_die 'token must not be empty'
printf -v desired '%s\n' "$token"
course_init
course_ensure_dir "$BASH_COURSE_ROOT/lab09" 0700
course_write_file "$BASH_COURSE_ROOT/lab09/token.txt" 0600 "$desired"
unset token desired
course_note 'Token output suppressed; the runtime destination is plaintext. Encryption at rest needs a separate tool.'
course_finish
