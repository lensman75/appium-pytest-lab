from api.celery_app import app
import subprocess
import os

@app.task(bind=True)
def run_test(self, HOTEL: str, DAY: str, DATE: str):
    print(f"[TASK] Start test for: {HOTEL}, {DAY}, {DATE}")
    env = os.environ.copy()
    env["HOTEL"] = HOTEL
    env["DAY"] = DAY
    env["DATE"] = DATE
    env["TASK_ID"] = self.request.id

    os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/..")
    test_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "test.py"))

    result = subprocess.run(
        # ["pytest", "-v", "-s", "test.py"],
        ["pytest", "-v", "-s", test_path],
        # ["echo", f"Starting test for {HOTEL}"],
        shell=True,
        env=env
    )

    print(f"[TASK] Test finished. Response code: {result.returncode}")

    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "returncode": result.returncode
    }
