"""Docker関連オペレーション"""
import subprocess

from config import JOB_NAME, IMAGE_URI, dispatch, run

SRC_DIR = "src"


def build() -> None:
    run(["docker", "build", "-t", JOB_NAME, SRC_DIR])


def build_gcr() -> None:
    run(["docker", "build", "-t", IMAGE_URI, SRC_DIR])


def push() -> None:
    build_gcr()
    run(["docker", "push", IMAGE_URI])


def docker_run() -> None:
    build()
    run(["docker", "run", "--env-file", ".env", JOB_NAME])


def clean() -> None:
    subprocess.run(["docker", "rmi", JOB_NAME], check=False)


if __name__ == "__main__":
    dispatch({
        "build": build,
        "build-gcr": build_gcr,
        "push": push,
        "docker-run": docker_run,
        "clean": clean,
    })
