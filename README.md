# BITS Goa Wi-Fi autologin

[![Python CI](https://github.com/goatnath/BITS-WiFi-Autologin/actions/workflows/ci.yml/badge.svg)](https://github.com/goatnath/BITS-WiFi-Autologin/actions/workflows/ci.yml)

A Python script that checks connectivity and attempts to log in to the BITS Goa Campnet portal when offline.

## Quick start

Requires Python 3, Git, and access to the BITS Goa network.

```bash
mkdir -p ~/Scripts
cd ~/Scripts
git clone https://github.com/goatnath/BITS-WiFi-Autologin.git
cd BITS-WiFi-Autologin
python3 -m venv .venv
.venv/bin/python -m pip install requests python-dotenv
```

Create a `.env` file in the repository directory, with your own credentials:

```dotenv
CAMPUS_ID=your_username
CAMPUS_PASSWORD=your_password
```

Restrict access to the credentials and start the script:

```bash
chmod 600 .env
.venv/bin/python -u campnet_login.py
```

The script runs continuously. Stop it with Ctrl+C. It checks connectivity every five minutes when online and retries failed logins after ten seconds.

**Security:** The script currently disables TLS certificate verification for the portal. This means it cannot verify the portal's identity when sending credentials. Use it only if you understand that risk.

## Start automatically with systemd

The following assumes the quick start directory and virtual environment above. Create `~/.config/systemd/user/campnet.service`:

```ini
[Unit]
Description=BITS Goa Campnet autologin
After=network-online.target

[Service]
Type=simple
WorkingDirectory=%h/Scripts/BITS-WiFi-Autologin
ExecStart=%h/Scripts/BITS-WiFi-Autologin/.venv/bin/python -u %h/Scripts/BITS-WiFi-Autologin/campnet_login.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=default.target
```

Enable it and inspect its logs:

```bash
systemctl --user daemon-reload
systemctl --user enable --now campnet.service
systemctl --user status campnet.service
journalctl --user -u campnet.service -f
```

To stop and disable it, run `systemctl --user disable --now campnet.service`. The user service starts when your user systemd session starts; it does not by itself guarantee login before you sign in.

## Contributing

If the campus gateway URL changes or you have suggestions for the reconnection logic, open an issue or pull request.

