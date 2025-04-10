# appium-pytest-lab

Automated UI tests using Appium and Pytest, executed on a real Android device running on Windows 11.

## Installation (Windows)
1. Install Appium inspector
2. Install Appium server
3. Install and run RabbitMQ server.
4. Download and configure Android SDK

Set up venv
```
python -m venv venv
.\.venv\Scripts\activate.ps1
pip install -r requirements.txt
```

## Running the project
1. In powershell start Appium server with debug:
```appium --log-level debug```
2. Launch RabbitMQ from Start menu
3. Activate venv:
```.\.venv\Scripts\activate.ps1```
4. Start fastapi:
```fastapi dev api/main.py```
5.Start celery:
```celery -A api.celery_app worker --loglevel=info --pool=solo```

## Sending test request
To run test send a get request to:
```http://localhost:8000/booking/?HOTEL=The%20Chester%20Grosvenor&DAY=21&DATE=May%202025```