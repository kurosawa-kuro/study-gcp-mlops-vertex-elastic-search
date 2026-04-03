"""Terraformオペレーション"""
import subprocess
import sys

from config import JOB_NAME, PROJECT_ID, REGION, REPO_NAME, SECRET_NAME

TF_DIR = "terraform"


def tf_run(args: list[str]) -> None:
    subprocess.run(["terraform"] + args, cwd=TF_DIR, check=True)


def init() -> None:
    tf_run(["init"])


def plan() -> None:
    tf_run(["plan"])


def apply() -> None:
    tf_run(["apply", "-auto-approve"])


def destroy() -> None:
    tf_run(["destroy", "-auto-approve"])


def import_resources() -> None:
    imports = [
        ("google_artifact_registry_repository.hello",
         f"projects/{PROJECT_ID}/locations/{REGION}/repositories/{REPO_NAME}"),
        ("google_secret_manager_secret.elastic_api_key",
         f"projects/{PROJECT_ID}/secrets/{SECRET_NAME}"),
        ("google_cloud_run_v2_job.hello",
         f"projects/{PROJECT_ID}/locations/{REGION}/jobs/{JOB_NAME}"),
    ]
    for addr, resource_id in imports:
        tf_run(["import", addr, resource_id])


if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else ""
    actions = {
        "init": init,
        "plan": plan,
        "apply": apply,
        "destroy": destroy,
        "import": import_resources,
    }
    if action not in actions:
        print(f"Usage: {sys.argv[0]} [{'/'.join(actions)}]")
        sys.exit(1)
    actions[action]()
