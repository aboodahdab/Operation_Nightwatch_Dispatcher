# Operation_Nightwatch_Dispatcher
## How to run: 
### First create a folder ```mkdir NightWatch_Dispatcher_py```
### Next clone this repo ```git clone git@github.com:aboodahdab/Operation_Nightwatch_Dispatcher.git```
### Then install required dependencies ```npm install```
### Next navigate to the frontend ```cd frontend```
### After that run Tailwind ```npx @tailwindcss/cli -i style/css/input.css -o style/css/output.css --watch```
### Next open a new terminal
### Then navigate to the backend ```cd backend```
### After that make a virtual environment for python ```python3 -m venv venv```
### Next activate it ```source venv/bin/activate```
### Then download required dependencies ```pip install -r requirements.txt```
### After that install redis and enable it
<details>
<summary><h3>Installation and enabling by OS.</h3></summary>
  
### Installation
### - Ubuntu/Debian: `sudo apt install redis-server -y`
### - RHEL/CentOS/Fedora: `sudo dnf install redis -y`
### - macOS: `brew install redis`
### Enabling
### - Ubuntu/Debian: `sudo systemctl enable --now redis-server`
### - RHEL/CentOS/Fedora: `sudo systemctl enable --now redis`
### - macOS: `brew services start redis`
</details>

### Then run the fleet sender ```python3 fleet_server.py --host 127.0.0.1```
### After that open a new terminal
### Next run the receiver file ```python3 main.py```
### Then open a new terminal
### After that run the flask server ```python3 flask_server.py``` 
### Finally open your browser at port 4000 ```http://localhost:4000/```

## Details
### Please check out ```TASK.md``` for more details.
### For answers check out ```ANSWERS.md```
## Shoutout
### For [@WinterCore](https://github.com/WinterCore) For writing the task file of this program.
