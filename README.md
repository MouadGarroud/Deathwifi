# DeathWifi
This script is intended for educational purposes and penetration testing. Unauthorized use of this script on networks you do not own is illegal. Always seek permission before conducting any tests.
This script scans for available Wi-Fi networks and allows you to perform deauthentication attacks on selected networks.

# Projet overview
Wi-Fi Network Scanning: Uses nmcli and airodump-ng to discover nearby Wi-Fi networks with details such as SSID, MAC address, signal strength, encryption type, and more.
Deauthentication Attack: Select networks to perform a deauthentication attack, sending deauth packets to disconnect devices from the target network.
User Interaction: Users can select networks to target by entering the corresponding number from the displayed list.
Monitor Mode Activation: The script automatically starts the monitor mode on the Wi-Fi interface (wlan0) using airmon-ng.
**Disclaimer:** Use this script only on networks you own or have explicit permission to test.

# Requirements

- Python 3.x
- Required Python packages: `pandas`, `tabulate`
- Tools: `airmon-ng`, `airodump-ng`, `aireplay-ng` (must be installed and accessible)

# Usage

1. Run the script with root privileges.
2. The script will list available Wi-Fi networks.
3. Select networks to attack by entering their N°.
4. The script will start a deauthentication attack on the selected networks.
