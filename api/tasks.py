import os
import subprocess

def run_test(HOTEL: str, DAY: str, DATE: str):
    print(f"[TASK] Запуск теста для: {HOTEL}, {DAY}, {DATE}")
    env = os.environ.copy()
    env["HOTEL"] = HOTEL
    env["DAY"] = DAY
    env["DATE"] = DATE

    print(f"[TASK] Запускается pytest...")
    print(os.getcwd())
    result = subprocess.run(
        ["pytest", "-v", "-s", r"D:\appium-pytest-lab\api\tasks.py"],
        # ["echo", f"Запускается тест для {HOTEL}"],
        shell=True,
        env=env,
    )

    print(f"[TASK] Тест завершён. Код возврата: {result.returncode}")
    print(f"[TASK] STDOUT:\n{result.stdout}")
    print(f"[TASK] STDERR:\n{result.stderr}")

    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "returncode": result.returncode
    }