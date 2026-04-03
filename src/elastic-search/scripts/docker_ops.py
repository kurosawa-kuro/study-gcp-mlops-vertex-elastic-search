"""Docker関連オペレーション"""
import subprocess
import sys

from config import JOB_NAME, IMAGE_URI


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def build() -> None:
    run(["docker", "build", "-t", JOB_NAME, "."])


def build_gcr() -> None:
    run(["docker", "build", "-t", IMAGE_URI, "."])


def push() -> None:
    build_gcr()
    run(["docker", "push", IMAGE_URI])


def docker_run() -> None:
    build()
    run(["docker", "run", "--env-file", ".env", JOB_NAME])


def clean() -> None:
    subprocess.run(["docker", "rmi", JOB_NAME], check=False)


if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else ""
    actions = {
        "build": build,
        "build-gcr": build_gcr,
        "push": push,
        "docker-run": docker_run,
        "clean": clean,
    }
    if action not in actions:
        print(f"Usage: {sys.argv[0]} [{'/'.join(actions)}]")
        sys.exit(1)
    actions[action]()
