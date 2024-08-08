![SoundSpace Logo](src/assets/soundspace-logo.jpg)

# SoundSpace

An IoT solution for renting music studios.
- Automation of tasks such as allowing people into the studio and unlocking of user's rented instruments.
- Predictive mantainence and user feedback increases customer satisfaction and lessens the need to routinely check for wear.
- Instruments are expensive: there are many security features included.

## Initial setup

Open a *command prompt* terminal in the root directory of the project and run the following:
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

# Creates a production build of the Next.js app
npm run build
```

If you are planning to view the website on a different device than which the Flask app is running on,  
in `src/config.js`, edit `apiServerIp` to the IP address that the Flask app is running on.
```js
const config = {
    apiServerIp: "localhost"
};

export default config;
```

For the code for the BeagleBone Black Wireless in `BBBW Code`, edit `SERVER_IP_ADDRESS` to the IP address that the Flask app is running on.

```python
import ...

SERVER_IP_ADDRESS = "192.168.X.X"
```

## Running the demo

Open a terminal in the root directory of the project.

```bash
# Starts the Flask app on the IP address of the machine
# Make sure the virtual environment is activated!
python run-flask-app.py

# Starts the Next.js app
npm start
```

Visit `localhost:5000` in a web browser the view the website.
To view the Swagger UI (API documentation), visit `localhost:3000`.

Replace `localhost` with the IP address of which the Flask app is running on if viewing from a different device.