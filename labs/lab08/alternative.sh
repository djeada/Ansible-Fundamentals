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
COURSE_TEMP_FILE=''

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

course_mode() {
    # GNU stat and BSD/macOS stat have different interfaces.
    stat -c '%a' "$1" 2>/dev/null || stat -f '%Lp' "$1"
}

course_changed() {
    COURSE_CHANGED=$((COURSE_CHANGED + 1))
    if [ "$COURSE_CHECK" = true ]; then
        printf 'WOULD_CHANGE %s\n' "$1"
    else
        printf 'CHANGED %s\n' "$1"
    fi
}

course_ensure_dir() {
    local path mode
    path=$1
    mode=$2
    course_guard_path "$path"
    [ ! -e "$path" ] || [ -d "$path" ] || course_die 'expected a directory'
    if [ ! -d "$path" ] || [ "$(course_mode "$path")" != "${mode#0}" ]; then
        if [ "$COURSE_CHECK" = false ]; then
            mkdir -p -- "$path"
            chmod "$mode" "$path"
        fi
        course_changed "$path"
    fi
}

course_init() {
    course_guard_path "$BASH_COURSE_ROOT"
    # The shared parent belongs to both implementations; only Bash children are managed here.
    [ ! -e "$BASH_COURSE_REPO_ROOT/.sandbox" ] ||
        [ -d "$BASH_COURSE_REPO_ROOT/.sandbox" ] || course_die 'expected .sandbox to be a directory'
    if [ "$COURSE_CHECK" = false ]; then
        mkdir -p -- "$BASH_COURSE_REPO_ROOT/.sandbox"
    fi
    course_ensure_dir "$BASH_COURSE_ROOT" 0700
}

course_write_file() {
    local path mode desired parent same
    path=$1
    mode=$2
    desired=$3
    parent=${path%/*}
    course_guard_path "$path"
    [ ! -e "$path" ] || [ -f "$path" ] || course_die 'expected a regular file'
    same=false
    if [ -f "$path" ] && printf '%s' "$desired" | cmp -s - "$path"; then
        same=true
    fi
    if [ "$same" = true ] && [ "$(course_mode "$path")" = "${mode#0}" ]; then
        return 0
    fi
    if [ "$COURSE_CHECK" = false ]; then
        [ -d "$parent" ] || course_die 'create the destination directory before writing'
        if [ "$same" = true ]; then
            chmod "$mode" "$path"
        else
            # Candidate and destination share a directory/filesystem. A failed write
            # leaves the old file intact; EXIT removes any unpromoted candidate.
            COURSE_TEMP_FILE=$(mktemp "$parent/.course.XXXXXX")
            printf '%s' "$desired" > "$COURSE_TEMP_FILE"
            chmod "$mode" "$COURSE_TEMP_FILE"
            mv -f -- "$COURSE_TEMP_FILE" "$path"
            COURSE_TEMP_FILE=''
        fi
    fi
    course_changed "$path"
}

course_html_escape() {
    local value char i
    value=$1
    i=0
    while [ "$i" -lt "${#value}" ]; do
        char=${value:$i:1}
        case $char in
            '&') printf '&amp;' ;;
            '<') printf '&lt;' ;;
            '>') printf '&gt;' ;;
            '"') printf '&quot;' ;;
            "'") printf '&#39;' ;;
            *) printf '%s' "$char" ;;
        esac
        i=$((i + 1))
    done
}

course_require_environment() {
    case $1 in
        development|staging) ;;
        *) course_die 'environment must be development or staging' ;;
    esac
}

course_finish() {
    printf 'SUMMARY changed=%s check=%s\n' "$COURSE_CHANGED" "$COURSE_CHECK"
}

course_render_site() {
    local destination title description environment host html
    destination=$1
    title=$2
    description=$3
    environment=$4
    host=$5
    [ -n "$title" ] || course_die 'site title must not be empty'
    course_require_environment "$environment"
    printf -v html '<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>%s</title>
</head>
<body>
  <h1>%s</h1>
  <p>%s</p>
  <dl><dt>Environment</dt><dd>%s</dd><dt>Managed host</dt><dd>%s</dd></dl>
</body>
</html>
' \
        "$(course_html_escape "$title")" "$(course_html_escape "$title")" \
        "$(course_html_escape "$description")" "$(course_html_escape "$environment")" \
        "$(course_html_escape "$host")"
    course_ensure_dir "$destination" 0755
    course_write_file "$destination/index.html" 0644 "$html"
}

course_cleanup_temp() {
    if [ -n "$COURSE_TEMP_FILE" ]; then
        rm -f -- "$COURSE_TEMP_FILE"
    fi
}

trap course_cleanup_temp EXIT

# Run this lab.
course_parse_args "$@"
environment=${COURSE_ENVIRONMENT-development}
title=${COURSE_SITE_TITLE-My first reusable Bash function}
description=${COURSE_SITE_DESCRIPTION-A page rendered from explicit function inputs.}
[ -n "$title" ] || course_die 'site title must not be empty'
course_require_environment "$environment"
course_init
course_render_site "$BASH_COURSE_ROOT/lab08" "$title" "$description" "$environment" localhost
course_finish
