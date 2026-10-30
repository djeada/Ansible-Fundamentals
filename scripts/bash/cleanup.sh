#!/usr/bin/env bash
# Self-contained lab: all functions, data, and rendering logic are in this file.
# Runtime: Bash 3.2+ and the documented standard Unix utilities.
set -euo pipefail
umask 077
# Work bytewise so UTF-8 bytes survive consistently across Bash versions.
export LC_ALL=C
BASH_COURSE_REPO_ROOT=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd -P)
readonly BASH_COURSE_REPO_ROOT
BASH_COURSE_ROOT="$BASH_COURSE_REPO_ROOT/.sandbox/bash"
readonly BASH_COURSE_ROOT
COURSE_CHECK=false
COURSE_CHANGED=0

course_die() {
    printf 'ERROR: %s\n' "$*" >&2
    exit 1
}

course_parse_args() {
    while [ "$#" -gt 0 ]; do
        case $1 in
            --check) COURSE_CHECK=true ;;
            *) course_die "unsupported argument: $1 (expected --check or no arguments)" ;;
        esac
        shift
    done
}

course_guard_path() {
    local target relative part current
    target=$1
    case $target in
        "$BASH_COURSE_ROOT") relative='' ;;
        "$BASH_COURSE_ROOT"/*) relative=${target#"$BASH_COURSE_ROOT"/} ;;
        *) course_die 'path is outside the Bash course sandbox' ;;
    esac
    [ ! -L "$BASH_COURSE_REPO_ROOT/.sandbox" ] || course_die '.sandbox must not be a symlink'
    [ ! -L "$BASH_COURSE_ROOT" ] || course_die 'Bash sandbox must not be a symlink'
    current=$BASH_COURSE_ROOT
    while [ -n "$relative" ]; do
        part=${relative%%/*}
        case $part in ''|.|..) course_die 'invalid sandbox path component' ;; esac
        current="$current/$part"
        [ ! -L "$current" ] || course_die 'sandbox paths must not contain symlinks'
        case $relative in
            */*) relative=${relative#*/} ;;
            *) relative='' ;;
        esac
    done
}

course_changed() {
    COURSE_CHANGED=$((COURSE_CHANGED + 1))
    if [ "$COURSE_CHECK" = true ]; then
        printf 'WOULD_CHANGE %s\n' "$1"
    else
        printf 'CHANGED %s\n' "$1"
    fi
}

course_finish() {
    printf 'SUMMARY changed=%s check=%s\n' "$COURSE_CHANGED" "$COURSE_CHECK"
}

# Run this lab.
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
