"""GCP操作（Terraform管理外のオペレーション）"""
import os
import subprocess

from config import JOB_NAME, PROJECT_ID, REGION, dispatch, run


def _execute_job(env_overrides: dict[str, str] | None = None) -> None:
    """Cloud Run Jobを実行し、完了後にログを表示する。"""
    cmd = ["gcloud", "run", "jobs", "execute", JOB_NAME, f"--region={REGION}", "--wait", "--format=value(metadata.name)"]
    if env_overrides:
        pairs = ",".join(f"{k}={v}" for k, v in env_overrides.items())
        cmd += [f"--update-env-vars={pairs}"]

    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    execution_name = result.stdout.strip()
    if execution_name:
        print(f"\nexecution: {execution_name}")
        _logs(execution_name)


def ingest() -> None:
    _execute_job()


def search() -> None:
    """SEARCH_KEYWORD環境変数を渡してキーワード検索を実行する。"""
    keyword = os.environ.get("SEARCH_KEYWORD", "")
    if not keyword:
        print("Usage: make search Q=<keyword>")
        raise SystemExit(1)
    print(f'search: "{keyword}"')
    _execute_job({"SEARCH_KEYWORD": keyword})


def logs() -> None:
    """最新のexecutionのログを表示する。"""
    result = subprocess.run(
        ["gcloud", "run", "jobs", "executions", "list", f"--job={JOB_NAME}", f"--region={REGION}",
         "--limit=1", "--format=value(metadata.name)"],
        check=True, capture_output=True, text=True,
    )
    execution_name = result.stdout.strip()
    if not execution_name:
        print("no executions found")
        return
    print(f"execution: {execution_name}")
    _logs(execution_name)


def _logs(execution_name: str) -> None:
    """指定executionのログを表示する。"""
    run([
        "gcloud", "logging", "read",
        f'resource.type=cloud_run_job AND resource.labels.job_name={JOB_NAME} AND labels."run.googleapis.com/execution_name"={execution_name}',
        "--limit=50",
        "--format=value(textPayload)",
        f"--project={PROJECT_ID}",
        "--order=asc",
    ])


if __name__ == "__main__":
    dispatch({
        "ingest": ingest,
        "search": search,
        "logs": logs,
    })
