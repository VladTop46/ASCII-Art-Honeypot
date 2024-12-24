# ASCII Art Honeypot

A simple but effective honeypot that masquerades as a network service, logs connection attempts, and responds with ASCII art. Perfect for monitoring potential intrusion attempts on your VPS or server.

## Features

- Customizable ASCII art and message display
- Detailed connection logging in both text and JSON formats
- Multi-threaded connection handling
- HTTP response support for browser compatibility
- Styled output with retro terminal aesthetics
- Minimal dependencies (Python standard library only)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/VladTop46/ASCII-Art-Honeypot.git
cd ASCII-Art-Honeypot
```

2. The script requires Python 3.6 or higher. No additional dependencies needed.

## Usage

### Basic Usage

1. Start the honeypot:
```bash
python3 honeypot.py
```

By default, it will run on port 8080. You can modify the port in the script.

### Running as a Service

1. Create a systemd service file:
```bash
sudo nano /etc/systemd/system/ascii-honeypot.service
```

2. Add the following content (modify paths as needed):
```ini
[Unit]
Description=ASCII Art Honeypot
After=network.target

[Service]
Type=simple
User=yourusername
WorkingDirectory=/path/to/ascii-honeypot
ExecStart=/usr/bin/python3 /path/to/ascii-honeypot/honeypot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

3. Enable and start the service:
```bash
sudo systemctl enable ascii-honeypot
sudo systemctl start ascii-honeypot
```

### Choosing a Port

Common ports that attackers often scan and might be suitable for honeypot deployment:
- 3306 (MySQL)
- 5432 (PostgreSQL)
- 21 (FTP)
- 6379 (Redis)
- 27017 (MongoDB)
- 9200 (Elasticsearch)
- 8888 (Common alternative HTTP port)

Note: Ensure the chosen port isn't being used by any other service on your system.

### Log Files

The honeypot generates two types of logs:
- `honeypot.log`: Plain text log file with connection timestamps and basic info
- `connections.json`: Detailed JSON format logs including all received data

Log file location: Same directory as the script

Example log output:
```
2024-12-24 13:10:11,209 - Connection from 192.168.1.1:49472
2024-12-24 13:10:11,209 - Received data: GET / HTTP/1.1
```

## Customization

### Modifying ASCII Art

Replace the `ASCII_ART` variable in the script with your preferred ASCII art:
```python
ASCII_ART = """
    Your
    ASCII Art
    Here
"""
```

### Changing the Response Message

Modify the `MESSAGE` variable to customize the text shown to visitors:
```python
MESSAGE = """
    Your custom message here
"""
```

### Styling the Output

The HTML/CSS styling can be modified in the `http_response` string:
```python
"<style>"
"body { background-color: black; color: #00ff00; font-family: monospace; }"
"pre { white-space: pre; }"
"</style>"
```

## Security Considerations

- The honeypot should run with minimal privileges
- Ensure your real services are properly secured
- Regularly monitor the logs for unusual patterns
- Consider using fail2ban in conjunction with this honeypot
- Don't deploy on ports used by critical services (SSH, etc.)

## License

This project is licensed under the MIT License

## Disclaimer

This tool is for educational and defensive purposes only. Users are responsible for how they deploy and use this honeypot.