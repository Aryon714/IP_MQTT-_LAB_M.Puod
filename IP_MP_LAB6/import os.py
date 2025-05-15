import paramiko
import paho.mqtt.publish as publish

# SSH credentials
SSH_HOST = "192.168.64.34"
SSH_USER = "osboxes"
SSH_PASSWORD = "osboxes.org"

# MQTT broker settings
MQTT_BROKER = "192.168.64.34"
MQTT_PORT = 1883
MQTT_TOPIC = "agent/commands"

def ssh_and_publish():
    try:
        # Connect via SSH
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)

        # Run commands
        stdin, stdout, stderr = client.exec_command("ls -1")
        directory = stdout.read().decode()

        stdin, stdout, stderr = client.exec_command("free -h")
        memory = stdout.read().decode()

        stdin, stdout, stderr = client.exec_command("hostname -I | awk '{print $1}'")
        ip = stdout.read().decode().strip()

        # Create test.txt
        client.exec_command("echo 'This is a test file.' > test.txt")

        client.close()

        # Format the message
        message = f"""IP: {ip}
Directory:
{directory}
Free Memory:
{memory}
"""

        # Publish to MQTT
        publish.single(MQTT_TOPIC, payload=message, hostname=MQTT_BROKER, port=MQTT_PORT, client_id="agent")

        print("Info successfully published to MQTT.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    ssh_and_publish()
