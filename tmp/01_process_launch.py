import os
import subprocess

env = os.environ.copy()


# $env:HOTEL="The Grosvenor Hotel"; 
env["HOTEL"] = "The Chester Grosvenor"

# $env:DAY="15"; 
env["DAY"]= "15" 
# $env:DATE="July 2025"; 
env["DATE"]= "July 2025"
# pytest -v -s test.py

# subprocess.run(["ls", "-l"])  # Linux/macOS
subprocess.run(["pytest", "-v", "-s", r"test.py"], shell=True, env=env)  # Windows
# subprocess.run([""], shell=True)  # Windows
