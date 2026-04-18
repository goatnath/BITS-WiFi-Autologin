# 🚀 wifi-autoconnect

A lightweight Python automation tool to handle the **BITS Goa Campnet** login process. This script eliminates the need to manually interact with the browser portal every time you connect to the campus Wi-Fi.

## 🛠 Features
* **Automatic Authentication:** Logs into the Fortinet/CyberRoam gateway via terminal.
* **Session Persistence:** Designed to keep your connection active without manual intervention.
* **Terminal-Friendly:** Perfect for headless setups or power users on Linux.

## 📋 Prerequisites
* **Python 3.x**
* **Requests Library:**
  ```bash
  pip install requests

## 📥 Installation & Setup

1. **Create your Scripts directory:**
   If you don't have one already, create a folder for your automation tools:
   ```bash
   mkdir -p ~/Scripts
   cd ~/Scripts

2. **Clone the Repository:**
    ```bash 
    git clone [https://github.com/goatnath/wifi-autoconnect.git](https://github.com/goatnath/wifi-autoconnect.git)
    cd wifi-autoconnect

3. **Install Dependencies:**
    ```	
    pip install requests

4. **Configure Credentials:**
   ```
   nano .env
	```
   Paste the following into the file(replace with your credentials)
   ```
   CAMPUS_ID=Username
   CAMPUS_PASSWORD=Password

5. **Run the Python Script:**
    ``` 
    python campnet_login.py

## ⚙️ Automation (Linux/systemd)

To ensure you are automatically logged in every time you open your laptop, you can set this up as a background service.

1. **Create the service file:**
   ```bash
   sudo nano /etc/systemd/system/campnet.service

2. **Paste the following configuration (Replace your-username with your actual username, like goatnath):**
	```bash
	Ini, TOML
	[Unit]
	Description=BITS Goa Campnet Auto-Login
	After=network-online.target
	Wants=network-online.target

	[Service]
	Type=simple
	User=your-username
	WorkingDirectory=/home/your-username/Scripts/wifi-autoconnect
	ExecStart=/usr/bin/python /home/your-username/Scripts/wifi-autoconnect/campnet_login.py
	Restart=always
	RestartSec=10

	[Install]
	WantedBy=multi-user.target

3.**Enable and start the service:**

	```
	sudo systemctl daemon-reload
	sudo systemctl enable campnet.service
	sudo systemctl start campnet.service

4. **Check the status:**
	```
	systemctl status campnet.service


🤝 **Contributing**
If the campus gateway URL changes or you have suggestions for the reconnection logic, feel free to open a Pull Request.
