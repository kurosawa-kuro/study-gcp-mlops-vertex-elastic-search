"""共通設定（.envから読み取り）"""
import os

PROJECT_ID = os.environ["PROJECT_ID"]
REGION = os.environ["REGION"]
DEPLOYMENT_NAME = os.environ["DEPLOYMENT_NAME"]
JOB_NAME = os.environ["JOB_NAME"]
REPO_NAME = os.environ["REPO_NAME"]
SECRET_NAME = os.environ["SECRET_NAME"]
IMAGE_URI = f"{REGION}-docker.pkg.dev/{PROJECT_ID}/{REPO_NAME}/{JOB_NAME}:latest"
