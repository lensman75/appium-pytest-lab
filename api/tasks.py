# import os
# import subprocess

# def run_test(HOTEL: str, DAY: str, DATE: str):
#     print(f"[TASK] Запуск теста для: {HOTEL}, {DAY}, {DATE}")
#     env = os.environ.copy()
#     env["HOTEL"] = HOTEL
#     env["DAY"] = DAY
#     env["DATE"] = DATE

#     print(f"[TASK] Запускается pytest...")
#     print(os.getcwd())
#     result = subprocess.run(
#         ["pytest", "-v", "-s", r"D:\appium-pytest-lab\api\tasks.py"],
#         # ["echo", f"Запускается тест для {HOTEL}"],
#         shell=True,
#         env=env,
#     )

#     print(f"[TASK] Тест завершён. Код возврата: {result.returncode}")
#     print(f"[TASK] STDOUT:\n{result.stdout}")
#     print(f"[TASK] STDERR:\n{result.stderr}")

#     return {
#         "stdout": result.stdout,
#         "stderr": result.stderr,
#         "returncode": result.returncode
#     }

from api.celery_app import app
import subprocess
import os

@app.task
def run_test(HOTEL: str, DAY: str, DATE: str):
    print(f"[TASK] Запуск теста для: {HOTEL}, {DAY}, {DATE}")
    env = os.environ.copy()
    env["HOTEL"] = HOTEL
    env["DAY"] = DAY
    env["DATE"] = DATE

    os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/..")
    test_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "test.py"))

    result = subprocess.run(
        # ["pytest", "-v", "-s", "test.py"],
        ["pytest", "-v", "-s", test_path],
        # ["echo", f"Запускается тест для {HOTEL}"],
        shell=True,
        env=env
    )

    print(f"[TASK] Тест завершён. Код возврата: {result.returncode}")

    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "returncode": result.returncode
    }
