"""Exercise observable course behavior in a disposable copy; no external services."""
from __future__ import annotations

import argparse
import json
import os
import re
import secrets
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SIMULATED = ["-i", "inventories/simulated/hosts.yml"]


def executable(name: str) -> str:
    sibling = Path(sys.executable).parent / name
    found = str(sibling) if sibling.is_file() else shutil.which(name)
    if not found:
        raise RuntimeError(f"{name} not found; activate .venv and install requirements.txt")
    return found


def playbooks() -> list[Path]:
    return sorted(ROOT.glob("labs/*/playbook.yml")) + sorted(ROOT.glob("projects/*/*.yml")) + [
        ROOT / "playbooks/cleanup.yml"
    ]


class CourseRun:
    def __init__(self, root: Path):
        self.root = root
        self.env = {**os.environ, "ANSIBLE_CONFIG": str(root / "ansible.cfg"), "ANSIBLE_NOCOLOR": "1"}
        self.count = 0

    def command(self, args: list[str], *, stable=False, reject="") -> str:
        result = subprocess.run(
            args, cwd=self.root, env=self.env, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=180,
        )
        self.count += 1
        label = " ".join([Path(args[0]).name, *args[1:]])
        expected = result.returncode != 0 if reject else result.returncode == 0
        if not expected or (reject and reject not in result.stdout):
            raise AssertionError(f"Unexpected result ({result.returncode}): {label}\n{result.stdout}")
        if stable:
            changes = re.findall(r"\bchanged=(\d+)", result.stdout)
            if not changes or any(int(value) != 0 for value in changes):
                raise AssertionError(f"Repeat/check was not stable: {label}\n{result.stdout}")
        print(f"PASS {'expected rejection' if reject else 'stable' if stable else 'run'}: {label}", flush=True)
        return result.stdout

    def play(self, path: str, *args: str, simulated=False, stable=False, reject="") -> str:
        inventory = SIMULATED if simulated else []
        return self.command(
            [executable("ansible-playbook"), *inventory, path, *args], stable=stable, reject=reject
        )

    def read(self, path: str) -> str:
        return (self.root / ".sandbox" / path).read_text()

    def write(self, path: str, value: str):
        (self.root / ".sandbox" / path).write_text(value)


def syntax(run: CourseRun):
    for path in playbooks():
        relative = str(path.relative_to(ROOT))
        run.play(relative, "--syntax-check", simulated="rolling-release" in relative or "lab11" in relative)


def behaviors(run: CourseRun, private: Path):
    for number in range(1, 13):
        path = f"labs/lab{number:02}/playbook.yml"
        simulated = number == 11
        run.play(path, simulated=simulated)
        run.play(path, simulated=simulated, stable=True)
        run.play(path, "--check", "--diff", simulated=simulated, stable=True)

    assert run.read("lab02/managed.txt") == "Managed by Ansible.\n"
    run.write("lab02/managed.txt", "manual drift\n")
    run.play("labs/lab02/playbook.yml", "--check", "--diff")
    assert run.read("lab02/managed.txt") == "manual drift\n", "Check mode changed the file"
    run.play("labs/lab02/playbook.yml")
    assert run.read("lab02/managed.txt") == "Managed by Ansible.\n"

    run.play("labs/lab03/playbook.yml", "-e", "course_environment=staging")
    assert json.loads(run.read("lab03/variables.json"))["environment"] == "staging"
    run.play("labs/lab03/playbook.yml", "-e", "course_environment=production", reject="Assertion failed")
    assert json.loads(run.read("lab03/variables.json"))["environment"] == "staging"
    assert set(json.loads(run.read("lab04/facts.json"))) == {"system", "architecture"}
    assert run.read("lab05/web/service.conf") == "port=8080\n"
    assert not (run.root / ".sandbox/lab05/worker/service.conf").exists()

    message = 'Quotes " and <angle brackets>'
    run.play("labs/lab06/playbook.yml", "-e", json.dumps({"course_port": 9090, "course_message": message}))
    data = json.loads(run.read("lab06/app.json"))
    assert data["port"] == 9090 and data["message"] == message
    before = run.read("lab06/app.json")
    run.play("labs/lab06/playbook.yml", "-e", "course_port=9090", reject="course_port is integer")
    assert run.read("lab06/app.json") == before

    output = run.play("labs/lab07/playbook.yml", "-e", json.dumps({"course_message": "changed configuration"}))
    assert "RUNNING HANDLER" in output
    assert run.read("lab07/reload.txt") == "Loaded configuration: changed configuration\n"
    output = run.play("labs/lab07/playbook.yml", "-e", json.dumps({"course_message": "changed configuration"}), stable=True)
    assert "RUNNING HANDLER" not in output
    assert "My first reusable role" in run.read("lab08/index.html")

    vault_password = private / "vault-password"
    vault_password.write_text(secrets.token_urlsafe(24))
    vault_password.chmod(0o600)
    vault_input = private / "vault.local.yml"
    token = "test-token-" + secrets.token_hex(12)
    vault_input.write_text(f"course_api_token: {token}\n")
    vault_input.chmod(0o600)
    run.command([executable("ansible-vault"), "encrypt", str(vault_input), "--vault-password-file", str(vault_password)])
    assert vault_input.read_text().startswith("$ANSIBLE_VAULT;")
    vault_args = ["-e", "@" + str(vault_input), "--vault-password-file", str(vault_password), "--diff"]
    for stable in [False, True]:
        output = run.play("labs/lab09/playbook.yml", *vault_args, stable=stable)
        assert token not in output, "Secret leaked into normal task/diff output"
    token_file = run.root / ".sandbox/lab09/token.txt"
    assert token_file.read_text() == token + "\n"
    assert stat.S_IMODE(token_file.stat().st_mode) == 0o600

    assert run.read("lab10/live.conf") == "version=1\n"
    run.play("labs/lab10/playbook.yml", "-e", '{"course_candidate_valid": true}')
    assert run.read("lab10/live.conf") == "version=2\n"
    run.play("labs/lab10/playbook.yml", stable=True)
    assert run.read("lab10/live.conf") == "version=2\n"
    for host in ["node_a", "node_b"]:
        assert run.read(f"lab11/{host}/release.txt") == "release=v1\n"

    run.write("lab12/release.json", '{"version":"v9","healthy":true}\n')
    run.play("labs/lab12/playbook.yml", "--tags", "verify", reject="Assertion failed")
    assert json.loads(run.read("lab12/release.json"))["version"] == "v9", "Verification repaired evidence"
    run.play("labs/lab12/playbook.yml")
    assert json.loads(run.read("lab12/release.json")) == {"version": "v1", "healthy": True}

    site = "projects/01-learning-site/site.yml"
    run.play(site)
    run.play(site, stable=True)
    run.play(site, "--check", "--diff", stable=True)
    assert "Infrastructure learning journal" in run.read("projects/site/index.html")
    run.play(site, "-e", json.dumps({"training_site_title": "<script>learning</script>"}))
    page = run.read("projects/site/index.html")
    assert "&lt;script&gt;learning&lt;/script&gt;" in page and "<script>" not in page
    run.play(site, "-e", '{"training_site_title": ""}', reject="Assertion failed")

    bootstrap = "projects/02-rolling-release/bootstrap.yml"
    deploy = "projects/02-rolling-release/deploy.yml"
    run.play(bootstrap, simulated=True)
    run.play(bootstrap, simulated=True, stable=True)
    run.play(deploy, simulated=True)
    run.play(deploy, simulated=True, stable=True)
    run.play(deploy, "--check", "--diff", simulated=True, stable=True)
    for failure_host in ["node_a", "node_b"]:
        values = json.dumps({"course_release": "v3", "course_failure_host": failure_host})
        run.play(deploy, "-e", values, simulated=True, reject=f"Rolled back {failure_host}")
        assert run.read("projects/rollout/node_b/release.txt") == "v2\n"
        expected_a = "v2\n" if failure_host == "node_a" else "v3\n"
        assert run.read("projects/rollout/node_a/release.txt") == expected_a
    run.play(deploy, "-e", "course_release=v3", simulated=True)
    run.play(deploy, "-e", "course_release=v3", simulated=True, stable=True)
    assert all(run.read(f"projects/rollout/{host}/release.txt") == "v3\n" for host in ["node_a", "node_b"])

    backup = "projects/03-backup-restore/backup.yml"
    restore = "projects/03-backup-restore/restore.yml"
    for play in [backup, restore]:
        run.play(play)
        run.play(play, stable=True)
        run.play(play, "--check", "--diff", stable=True)
    original = run.read("projects/backup/source.json")
    assert run.read("projects/backup/restored.json") == original
    changed = json.loads(original)
    changed["learners"].append("Grace")
    run.write("projects/backup/source.json", json.dumps(changed) + "\n")
    run.play(backup, reject="Choose a new backup ID")
    run.play(backup, "-e", "course_backup_id=snapshot-002")
    run.play(restore, "-e", "course_backup_id=snapshot-002")
    restored = run.read("projects/backup/restored.json")
    assert json.loads(restored) == changed
    assert run.read("projects/backup/snapshots/snapshot-001.json") == original
    run.write("projects/backup/snapshots/snapshot-002.json", "corrupted snapshot\n")
    run.play(restore, "-e", "course_backup_id=snapshot-002", reject="Snapshot integrity check failed")
    assert run.read("projects/backup/restored.json") == restored, "Rejected restore overwrote the destination"
    run.play(restore)
    assert run.read("projects/backup/restored.json") == original
    run.play("playbooks/cleanup.yml")
    assert not (run.root / ".sandbox").exists(), "Cleanup left course artifacts behind"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--syntax-only", action="store_true", help="Parse all supported playbooks without runtime execution")
    args = parser.parse_args()
    if args.syntax_only:
        run = CourseRun(ROOT)
        syntax(run)
    else:
        with tempfile.TemporaryDirectory(prefix="ansible-course-", dir=ROOT.parent) as name:
            temporary = Path(name)
            copied = temporary / "course"
            shutil.copytree(ROOT, copied, ignore=shutil.ignore_patterns(".git", ".venv", ".sandbox", "__pycache__"))
            run = CourseRun(copied)
            syntax(run)
            behaviors(run, temporary)
    print(f"All {run.count} command checks and artifact assertions passed.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, RuntimeError, subprocess.TimeoutExpired) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
