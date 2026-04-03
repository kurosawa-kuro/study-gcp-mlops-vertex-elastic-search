"""GCPデプロイ関連オペレーション"""
import os
import subprocess
import sys

from config import IMAGE_URI, JOB_NAME, PROJECT_ID, REGION, REPO_NAME, SECRET_NAME


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def create_repo() -> None:
    run([
        "gcloud", "artifacts", "repositories", "create", REPO_NAME,
        "--repository-format=docker",
        f"--location={REGION}",
    ])


def auth_docker() -> None:
    run(["gcloud", "auth", "configure-docker", f"{REGION}-docker.pkg.dev"])


def create_secret() -> None:
    api_key = os.environ["ELASTIC_API_KEY"]
    subprocess.run(
        [
            "gcloud", "secrets", "create", SECRET_NAME,
            "--data-file=-",
            "--replication-policy=user-managed",
            f"--locations={REGION}",
        ],
        input=api_key.encode(),
        check=True,
    )


def create_job() -> None:
    cloud_url = os.environ["ELASTIC_CLOUD_URL"]
    common = [
        f"--image={IMAGE_URI}",
        f"--region={REGION}",
        f"--set-env-vars=ELASTIC_CLOUD_URL={cloud_url}",
        f"--set-secrets=ELASTIC_API_KEY={SECRET_NAME}:latest",
        "--task-timeout=60s",
        "--max-retries=0",
    ]
    result = subprocess.run(["gcloud", "run", "jobs", "create", JOB_NAME] + common)
    if result.returncode != 0:
        run(["gcloud", "run", "jobs", "update", JOB_NAME] + common)


def execute() -> None:
    run(["gcloud", "run", "jobs", "execute", JOB_NAME, f"--region={REGION}", "--wait"])


def logs() -> None:
    run([
        "gcloud", "logging", "read",
        f"resource.type=cloud_run_job AND resource.labels.job_name={JOB_NAME}",
        "--limit=50",
        "--format=value(textPayload)",
        f"--project={PROJECT_ID}",
    ])


def cleanup() -> None:
    run(["gcloud", "run", "jobs", "delete", JOB_NAME, f"--region={REGION}", "--quiet"])
    run(["gcloud", "artifacts", "docker", "images", "delete", IMAGE_URI, "--quiet"])
    run(["gcloud", "secrets", "delete", SECRET_NAME, "--quiet"])


if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else ""
    actions = {
        "create-repo": create_repo,
        "auth-docker": auth_docker,
        "create-secret": create_secret,
        "create-job": create_job,
        "execute": execute,
        "logs": logs,
        "cleanup": cleanup,
    }
    if action not in actions:
        print(f"Usage: {sys.argv[0]} [{'/'.join(actions)}]")
        sys.exit(1)
    actions[action]()
