"""Verify Bash lab behavior with standard Unix tools and no Ansible runtime."""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import stat
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Only these external tools are reachable by lab scripts under test.
UNIX_TOOLS = ["dirname", "stat", "mkdir", "chmod", "cmp", "mktemp", "mv", "rm", "uname"]


class BashCourse:
    def __init__(self, root: Path, shell: str, tool_path: Path):
        self.root = root
        self.shell = shell
        self.count = 0
        self.env = {
            key: value for key, value in os.environ.items()
            if not key.startswith("COURSE_") and key not in {"BASH_ENV", "ENV"}
        }
        self.env["PATH"] = str(tool_path)

    def run(self, number: int | str, *args: str, values=None, reject="", stable=False, stdin=None, cwd=None, trace=False):
        script = f"labs/lab{number:02}/alternative.sh" if isinstance(number, int) else number
        result = subprocess.run(
            [self.shell, *(["-x"] if trace else []), str(self.root / script), *args], cwd=cwd or self.root,
            env={**self.env, **(values or {})}, input=stdin, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=30,
        )
        self.count += 1
        label = f"{script} {' '.join(args)}".strip()
        if reject:
            assert result.returncode != 0 and reject in result.stdout, f"Expected {reject}: {label}\n{result.stdout}"
        else:
            assert result.returncode == 0, f"Failed {label}\n{result.stdout}"
            assert "SUMMARY changed=" in result.stdout, f"Missing completion report: {label}"
        if stable:
            assert re.search(r"SUMMARY changed=0 check=(true|false)\n", result.stdout), result.stdout
        print(f"PASS {'rejection' if reject else 'stable' if stable else 'run'}: {label}", flush=True)
        return result.stdout

    def read(self, relative: str) -> str:
        return (self.root / ".sandbox/bash" / relative).read_text()

    def write(self, relative: str, content: str):
        (self.root / ".sandbox/bash" / relative).write_text(content)

    def snapshot(self):
        base = self.root / ".sandbox"
        if not base.exists():
            return {}
        return {
            str(path.relative_to(base)): (
                stat.S_IMODE(path.stat().st_mode), path.read_bytes() if path.is_file() else None
            ) for path in base.rglob("*")
        }


def check_syntax(course: BashCourse):
    for script in sorted(course.root.glob("labs/*/alternative.sh")) + sorted(course.root.glob("scripts/bash/*.sh")):
        result = subprocess.run([course.shell, "-n", str(script)], text=True, capture_output=True, timeout=10)
        assert result.returncode == 0, f"Invalid shell syntax: {script}\n{result.stderr}"
    print("PASS syntax: all 12 alternatives and shared shell scripts", flush=True)


def check_behavior(course: BashCourse, temporary: Path):
    for number in range(1, 13):
        before = course.snapshot()
        course.run(number, "--check")
        assert course.snapshot() == before, f"Lab {number} check mode changed filesystem state"
        course.run(number)
        course.run(number, stable=True)
        before = course.snapshot()
        course.run(number, "--check", stable=True)
        assert course.snapshot() == before, f"Lab {number} warm check mode changed filesystem state"

    # Location is derived from the script, not the caller's working directory.
    course.run(2, cwd=temporary, stable=True)
    assert course.read("lab02/managed.txt") == "Managed by Bash.\n"
    course.write("lab02/managed.txt", "manual drift\n")
    before = course.snapshot()
    course.run(2, "--check")
    assert course.snapshot() == before
    course.run(2)
    assert course.read("lab02/managed.txt") == "Managed by Bash.\n"
    path = course.root / ".sandbox/bash/lab02/managed.txt"
    path.chmod(0o600)
    course.run(2)
    assert stat.S_IMODE(path.stat().st_mode) == 0o644

    course.run(3, values={"COURSE_ENVIRONMENT": "staging"})
    assert json.loads(course.read("lab03/variables.json"))["environment"] == "staging"
    before = course.snapshot()
    course.run(3, values={"COURSE_ENVIRONMENT": "production"}, reject="environment must")
    assert course.snapshot() == before
    assert set(json.loads(course.read("lab04/facts.json"))) == {"system", "architecture"}
    assert course.read("lab05/web/service.conf") == "port=8080\n"
    assert not (course.root / ".sandbox/bash/lab05/worker/service.conf").exists()
    course.run(5, values={"COURSE_WORKER_ENABLED": "true"})
    course.run(5, stable=True)
    assert course.read("lab05/worker/service.conf") == "port=9090\n", "Skipped copy incorrectly removed old state"
    course.run(5, values={"COURSE_WORKER_ENABLED": "yes"}, reject="boolean input")

    # An independent parser checks the Bash serializer, including every non-NUL
    # ASCII control byte, UTF-8, trailing newlines, quotes, and backslashes.
    message = '"quote" \\ slash <html> café 雪 🐧\n\n' + "".join(chr(i) for i in range(1, 32))
    course.run(6, values={"COURSE_PORT": "9090", "COURSE_MESSAGE": message})
    decoded = json.loads(course.read("lab06/app.json"))
    expected = {
        "environment": "development", "port": 9090, "message": message,
    }
    assert decoded == expected, f"Serializer round trip mismatch: {decoded!r} != {expected!r}"
    before = course.snapshot()
    for port in ["", "0", "08080", "1024", "65536", "1e4", "-1", "1+8080", "9" * 50]:
        course.run(6, values={"COURSE_PORT": port}, reject="port must")
        assert course.snapshot() == before, "Invalid input changed a deployed artifact"

    message = "changed configuration\nwith a trailing newline\n"
    output = course.run(7, values={"COURSE_MESSAGE": message})
    assert "HANDLER simulated reload" in output
    assert course.read("lab07/reload.txt") == f"Loaded configuration: {message}\n"
    output = course.run(7, values={"COURSE_MESSAGE": message}, stable=True)
    assert "HANDLER" not in output
    receipt = course.root / ".sandbox/bash/lab07/reload.txt"
    receipt.unlink()
    course.run(7, values={"COURSE_MESSAGE": message}, stable=True)
    assert not receipt.exists(), "An event receipt was treated as continuously maintained state"

    course.run(8, values={"COURSE_SITE_TITLE": '<script>"A&B"</script>'})
    page = course.read("lab08/index.html")
    assert "&lt;script&gt;&quot;A&amp;B&quot;&lt;/script&gt;" in page and "<script>" not in page
    course.run(8, values={"COURSE_SITE_TITLE": ""}, reject="site title")

    token = "practice-private-value-123"
    for stable in [False, True]:
        output = course.run(9, "--token-stdin", stdin=token + "\n", stable=stable)
        assert token not in output, "Token leaked to ordinary task output"
    output = course.run(9, "--token-stdin", stdin=token + "\n", stable=True, trace=True)
    assert token not in output, "Token leaked when the caller enabled shell tracing"
    token_path = course.root / ".sandbox/bash/lab09/token.txt"
    assert token_path.read_text() == token + "\n"
    assert stat.S_IMODE(token_path.stat().st_mode) == 0o600
    assert stat.S_IMODE(token_path.parent.stat().st_mode) == 0o700
    course.run(9, "--token-stdin", stdin="\n", reject="token must not be empty")

    assert course.read("lab10/live.conf") == "version=1\n"
    course.run(10, values={"COURSE_CANDIDATE_VALID": "true"})
    course.run(10, stable=True)
    assert course.read("lab10/live.conf") == "version=2\n"
    course.run(10, values={"COURSE_CANDIDATE_VALID": "yes"}, reject="boolean input")

    course.run(11, values={"COURSE_LIMIT": "node_a", "COURSE_RELEASE": "v2"})
    assert course.read("lab11/node_a/release.txt") == "release=v2\n"
    assert course.read("lab11/node_b/release.txt") == "release=v1\n"
    course.run(11, values={"COURSE_RELEASE": "v3", "COURSE_FAILURE_HOST": "node_a"}, reject="simulated failure on node_a")
    assert course.read("lab11/node_a/release.txt") == "release=v2\n"
    assert course.read("lab11/node_b/release.txt") == "release=v1\n"
    course.run(11, values={"COURSE_RELEASE": "v3", "COURSE_FAILURE_HOST": "node_b"}, reject="simulated failure on node_b")
    assert course.read("lab11/node_a/release.txt") == "release=v3\n"
    assert course.read("lab11/node_b/release.txt") == "release=v1\n"
    course.run(11)

    course.write("lab12/release.json", '{"version":"v9","healthy":true}\n')
    before = course.snapshot()
    course.run(12, "--verify-only", reject="release contract failed")
    assert course.snapshot() == before, "Verification repaired evidence of drift"
    course.run(12)
    assert json.loads(course.read("lab12/release.json")) == {"version": "v1", "healthy": True}
    course.run(12, "--verify-only", stable=True)
    course.run(12, "--verify-only", values={"COURSE_EXPECTED_VERSION": "v9"}, reject="release contract failed")

    # Refuse linked destinations, including ancestors, without touching their targets.
    outside = temporary / "outside.txt"
    outside.write_text("outside the course\n")
    managed = course.root / ".sandbox/bash/lab02/managed.txt"
    managed.unlink()
    managed.symlink_to(outside)
    course.run(2, reject="must not contain symlinks")
    assert outside.read_text() == "outside the course\n"
    managed.unlink()
    course.run(2)
    assert not list((course.root / ".sandbox/bash").rglob(".course.*")), "Unpromoted temporary files remain"

    sibling = course.root / ".sandbox/ansible-track-sentinel.txt"
    sibling.write_text("preserve this\n")
    before = course.snapshot()
    course.run("scripts/bash/cleanup.sh", "--check")
    assert course.snapshot() == before
    course.run("scripts/bash/cleanup.sh")
    assert not (course.root / ".sandbox/bash").exists()
    assert sibling.read_text() == "preserve this\n"
    course.run("scripts/bash/cleanup.sh", stable=True)
    before = course.snapshot()
    course.run(12, "--verify-only", reject="release contract failed")
    assert course.snapshot() == before, "Verify-only created directories on a cold target"

    sandbox = course.root / ".sandbox/bash"
    sandbox.symlink_to(temporary, target_is_directory=True)
    course.run(2, reject="must not be a symlink")
    course.run("scripts/bash/cleanup.sh", reject="must not be a symlink")
    sandbox.unlink()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bash", default=shutil.which("bash"), help="Bash 3.2+ interpreter")
    args = parser.parse_args()
    if not args.bash:
        parser.error("Bash is not installed")
    shell = str(Path(args.bash).resolve())
    version = subprocess.run([shell, "--version"], text=True, capture_output=True, check=True)
    print(version.stdout.splitlines()[0], flush=True)
    with tempfile.TemporaryDirectory(prefix="bash-course-", dir=ROOT.parent) as name:
        temporary = Path(name)
        copied = temporary / "course with spaces"
        shutil.copytree(ROOT, copied, ignore=shutil.ignore_patterns(".git", ".venv", ".sandbox", "__pycache__"))
        tools = temporary / "unix-tools"
        tools.mkdir()
        for command in UNIX_TOOLS:
            resolved = shutil.which(command)
            assert resolved, f"Required standard Unix tool not found: {command}"
            (tools / command).symlink_to(resolved)
        course = BashCourse(copied, shell, tools)
        check_syntax(course)
        check_behavior(course, temporary)
        print(f"All {course.count} Bash command checks and independent artifact assertions passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
