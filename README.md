# SoundSpace

An IoT solution for renting music studios.
- Automation of tasks such as allowing people into the studio and unlocking of user's rented instruments.
- Predictive mantainence and user feedback increases customer satisfaction and lessens the need to routinely check for wear.
- Instruments are expensive: there are many security features included.

## Initial setup

Open a *command prompt* terminal in the root directory of the project and run the following.<br>
```bash
# Creates a Python virtual environment
python -m venv .venv

# Activates the virtual environment just created
# Command Prompt (not PowerShell!)
.venv\Scripts\activate.bat

# Installs necessary Python modules
pip install -r requirements.txt

# Installs necessary Node.js modules
npm install
```

In `src/config.js`, edit `apiServerIp` to match your IP address.
```js
const config = {
    apiServerIp: "192.168.X.X"
};

export default config;
```

If running the code for the BeagleBone Black Wireless in `BBBW Code`, edit `SERVER_IP_ADDRESS` to match your IP address.

```python
import ...

SERVER_IP_ADDRESS = "192.168.X.X"
```

## Running the demo

Open a terminal in the root directory of the project.

```bash
# Starts the Flask server
# Make sure the virtual environment is activated!
python run-flask-app.py

# Starts the NextJS server (development)
npm run dev
```

Visit `localhost:5000` in a web browser the view the website.<br>
To view Swagger UI (API documentation), visit `localhost:3000`.