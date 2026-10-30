#!/usr/bin/env bash
# Function interface: destination, title, description, environment, logical host.
# Source after lib.sh; a function is ordinary shell reuse, not an Ansible role.
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
