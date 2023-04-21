import os
import requests
import re
import tarfile
import shutil
import subprocess

def is_valid_network(network):
    valid_networks = ['MAINNET', 'GOERLI', 'SEPOLIA', 'RINKEBY', 'PRATER', 'GNOSIS']
    return network in valid_networks

while True:
    eth_network = input("\nSelect the network you would like to use \n(mainnet, goerli, sepolia, rinkeby, prater, gnosis): ").upper()
    if is_valid_network(eth_network):
        print(f"Selected network: {eth_network}")
        break
    else:
        print("Invalid network. Please try again.")

eth_network = eth_network.lower()
eth_network_cap = eth_network.capitalize()

import re

def is_valid_eth_address(address):
    pattern = re.compile("^0x[a-fA-F0-9]{40}$")
    return bool(pattern.match(address))

while True:
    fee_address = input("\n----------------------------------------\n---Set ETH address for Validator tips--- \n\nNote: Type 'skip' to set address later\n\nEnter Ethereum address you control: ")
    if fee_address.lower() == "skip":
        fee_address = "EMPTY"
        print("Skipping Ethereum address input. You can set it later.")
        break
    elif is_valid_eth_address(fee_address):
        print("Valid Ethereum address")
        break
    else:
        print("Invalid Ethereum address. Please try again.")

def prompt_checkpoint_sync_url():
    sync_urls = [
        ("No CheckpointSyncURL (skip)", None),
        ("ETHSTAKER", "https://beaconstate.ethstaker.cc"),
        ("BEACONCHA.IN", "https://sync-mainnet.beaconcha.in"),
        ("ATTESTANT", "https://mainnet-checkpoint-sync.attestant.io"),
        ("SIGMA PRIME", "https://mainnet.checkpoint.sigp.io"),
    ]

    while True:
        print("\n-----------------------------\n-------CHECKPOINT SYNC-------\nWould you like to enable Checkpoint Sync? (fast sync)\n\nPlease select a CheckpointSyncURL:\n")
        for idx, (display_text, url) in enumerate(sync_urls, start=1):
            print(f"{idx}. {display_text} - {url if url else ''}")

        user_choice = input("\nNote: You can also set your own CheckpointSyncURL after installation.\n\nEnter the number of the desired option (1-5): ")

        if user_choice.isdigit() and 1 <= int(user_choice) <= 5:
            display_text, selected_url = sync_urls[int(user_choice) - 1]
            print(f"Selected CheckpointSyncURL: {display_text} - {selected_url if selected_url else ''}")
            return selected_url
        else:
            print("Invalid choice. Please try again.")

sync_url = prompt_checkpoint_sync_url()

# Install ufw
subprocess.run(['sudo', 'apt', 'install', 'ufw'])

# Set default policies
subprocess.run(['sudo', 'ufw', 'default', 'deny', 'incoming'])
subprocess.run(['sudo', 'ufw', 'default', 'allow', 'outgoing'])

# Allow specific ports
subprocess.run(['sudo', 'ufw', 'allow', '6673/tcp'])
subprocess.run(['sudo', 'ufw', 'deny', '22/tcp'])
subprocess.run(['sudo', 'ufw', 'allow', '30303'])
subprocess.run(['sudo', 'ufw', 'allow', '9000'])

# Enable and check status
subprocess.run(['sudo', 'ufw', 'enable'])
subprocess.run(['sudo', 'ufw', 'status', 'numbered'])

# Create directory
subprocess.run(['sudo', 'mkdir', '-p', '/var/lib/jwtsecret'])

# Generate random hex string and save to file
rand_hex = subprocess.run(['openssl', 'rand', '-hex', '32'], stdout=subprocess.PIPE)
subprocess.run(['sudo', 'tee', '/var/lib/jwtsecret/jwt.hex'], input=rand_hex.stdout, stdout=subprocess.DEVNULL)

# Update and upgrade packages
subprocess.run(['sudo', 'apt', '-y', 'update'])
subprocess.run(['sudo', 'apt', '-y', 'upgrade'])

# Dist-upgrade and autoremove packages
subprocess.run(['sudo', 'apt', '-y', 'dist-upgrade'])
subprocess.run(['sudo', 'apt', '-y', 'autoremove'])

# Create users
subprocess.run(['sudo', 'useradd', '--no-create-home', '--shell', '/bin/false', 'geth'])
subprocess.run(['sudo', 'useradd', '--no-create-home', '--shell', '/bin/false', 'lighthousebeacon'])
subprocess.run(['sudo', 'useradd', '--no-create-home', '--shell', '/bin/false', 'lighthousevalidator'])

# Create directories
subprocess.run(['sudo', 'mkdir', '-p', '/var/lib/geth'])
subprocess.run(['sudo', 'mkdir', '-p', '/var/lib/lighthouse'])
subprocess.run(['sudo', 'mkdir', '-p', '/var/lib/lighthouse/beacon'])
subprocess.run(['sudo', 'mkdir', '-p', '/var/lib/lighthouse/validators'])

# Change ownership of directories
subprocess.run(['sudo', 'chown', '-R', 'geth:geth', '/var/lib/geth'])
subprocess.run(['sudo', 'chown', '-R', 'lighthousebeacon:lighthousebeacon', '/var/lib/lighthouse/beacon'])
subprocess.run(['sudo', 'chown', '-R', 'lighthousevalidator:lighthousevalidator', '/var/lib/lighthouse/validators'])

# Define the URL of the Geth download page
url = 'https://geth.ethereum.org/downloads/'

# Send a GET request to the download page and retrieve the HTML response
response = requests.get(url)
html = response.text

# Use regex to extract the URL of the latest Geth binary for Linux (amd64)
match = re.search(r'href="(https://gethstore\.blob\.core\.windows\.net/builds/geth-linux-amd64-[0-9]+\.[0-9]+\.[0-9]+-[0-9a-f]+\.tar\.gz)"', html)
if match:
    download_url = match.group(1)
    filename = os.path.expanduser('~/geth.tar.gz')
    print(f'Downloading {download_url}...')
    response = requests.get(download_url)
    with open(filename, 'wb') as f:
        f.write(response.content)
    print(f'Done! Binary saved to {filename}.')

    # Extract the contents of the tarball to the user's home folder
    with tarfile.open(filename, 'r:gz') as tar:
        dirname = tar.getnames()[0].split('/')[0]
        tar.extractall(os.path.expanduser('~'))

    # Remove the existing geth executable from /usr/local/bin if it exists
    if os.path.exists('/usr/local/bin/geth'):
        subprocess.run(['sudo', 'rm', '/usr/local/bin/geth'])
        print('Existing geth executable removed from /usr/local/bin.')

    # Copy the geth executable to /usr/local/bin
    src = os.path.expanduser(f'~/{dirname}/geth')
    subprocess.run(['sudo', 'cp', src, '/usr/local/bin/'])
    print('Geth executable copied to /usr/local/bin.')

    # Remove the downloaded file and extracted directory
    os.remove(filename)
    shutil.rmtree(os.path.expanduser(f'~/{dirname}'))
    print(f'Removed {filename} and directory {dirname}.')
else:
    print('Error: could not find download URL.')

# Change to the home folder
os.chdir(os.path.expanduser("~"))

# Define the Github API endpoint to get the latest release
url = 'https://api.github.com/repos/sigp/lighthouse/releases/latest'

# Send a GET request to the API endpoint
response = requests.get(url)

# Search for the asset with the name that ends in x86_64-unknown-linux-gnu.tar.gz
assets = response.json()['assets']
download_url = None
for asset in assets:
    if asset['name'].endswith('x86_64-unknown-linux-gnu.tar.gz'):
        download_url = asset['browser_download_url']
        break

if download_url is None:
    print("Error: Could not find the download URL for the latest release.")
    exit(1)

# Download the latest release binary
response = requests.get(download_url)

# Save the binary to the home folder
with open('lighthouse.tar.gz', 'wb') as f:
    f.write(response.content)

# Extract the binary to the home folder
with tarfile.open('lighthouse.tar.gz', 'r:gz') as tar:
    tar.extractall()

# Copy the binary to /usr/local/bin using sudo
os.system("sudo cp lighthouse /usr/local/bin")

# Remove the lighthouse.tar.gz file and extracted binary
os.remove('lighthouse.tar.gz')
os.remove('lighthouse')

print("Lighthouse binary installed successfully!")
print(f"Download URL: {download_url}")

# Define the name and location of the service files
geth_service_file_path = '/etc/systemd/system/geth.service'
beacon_service_file_path = '/etc/systemd/system/lighthousebeacon.service'
validator_service_file_path = '/etc/systemd/system/lighthousevalidator.service'

# Define the contents of the service files
geth_service_file = f'''[Unit]
Description=Geth Execution Client (Mainnet)
After=network.target
Wants=network.target

[Service]
User=geth
Group=geth
Type=simple
Restart=always
RestartSec=5
TimeoutStopSec=600
ExecStart=/usr/local/bin/geth \\
  --{eth_network} \\
  --datadir /var/lib/geth \\
  --authrpc.jwtsecret /var/lib/jwtsecret/jwt.hex \\
  --db.engine pebble

[Install]
WantedBy=default.target
'''

beacon_service_file = f'''[Unit]
Description=Lighthouse Consensus Client BN (Mainnet)
Wants=network-online.target
After=network-online.target

[Service]
User=lighthousebeacon
Group=lighthousebeacon
Type=simple
Restart=always
RestartSec=5
ExecStart=/usr/local/bin/lighthouse bn \\
  --network {eth_network} \\
  --datadir /var/lib/lighthouse \\
  --http \\
  --execution-endpoint http://127.0.0.1:8551 \\
  --execution-jwt /var/lib/jwtsecret/jwt.hex \\
  --checkpoint-sync-url {sync_url}

[Install]
WantedBy=multi-user.target
'''

beacon_service_file_no_cp = f'''[Unit]
Description=Lighthouse Consensus Client BN (Mainnet)
Wants=network-online.target
After=network-online.target

[Service]
User=lighthousebeacon
Group=lighthousebeacon
Type=simple
Restart=always
RestartSec=5
ExecStart=/usr/local/bin/lighthouse bn \\
  --network {eth_network} \\
  --datadir /var/lib/lighthouse \\
  --http \\
  --execution-endpoint http://127.0.0.1:8551 \\
  --execution-jwt /var/lib/jwtsecret/jwt.hex

[Install]
WantedBy=multi-user.target
'''

validator_service_file = f'''[Unit]
Description=Lighthouse Consensus Client VC (Mainnet)
Wants=network-online.target
After=network-online.target

[Service]
User=lighthousevalidator
Group=lighthousevalidator
Type=simple
Restart=always
RestartSec=5
ExecStart=/usr/local/bin/lighthouse vc \\
  --network {eth_network} \\
  --datadir /var/lib/lighthouse \\
  --suggested-fee-recipient {fee_address}
  
[Install]
WantedBy=multi-user.target
'''

# Write the service files
geth_temp_file = 'geth_temp.service'
beacon_temp_file = 'beacon_temp.service'
validator_temp_file = 'validator_temp.service'

with open(geth_temp_file, 'w') as f:
    f.write(geth_service_file)

with open(beacon_temp_file, 'w') as f:
    if sync_url is None:
        f.write(beacon_service_file_no_cp)
    else:
        f.write(beacon_service_file)

with open(validator_temp_file, 'w') as f:
    f.write(validator_service_file)

# Copy the files to their respective locations using sudo
os.system(f'sudo cp {geth_temp_file} {geth_service_file_path}')
os.system(f'sudo cp {beacon_temp_file} {beacon_service_file_path}')
os.system(f'sudo cp {validator_temp_file} {validator_service_file_path}')

# Remove temporary files
os.remove(geth_temp_file)
os.remove(beacon_temp_file)
os.remove(validator_temp_file)

# Reload the systemd daemon
subprocess.run(['sudo', 'systemctl', 'daemon-reload'])

# Print the final output
inbound_ports = subprocess.run(["sudo", "ufw", "status", "numbered"], stdout=subprocess.PIPE).stdout
if inbound_ports is not None:
    inbound_ports = inbound_ports.decode()
else:
    inbound_ports = ""
print(f'\nFirewall Status:\nInbound Ports: {inbound_ports}Outbound Ports: 9000, 30303, 6673/tcp')

geth_version = subprocess.run(["geth", "--version"], stdout=subprocess.PIPE).stdout
if geth_version is not None:
    geth_version = geth_version.decode()
else:
    geth_version = ""
print(f'\nGeth Version: \n{geth_version}')

lighthouse_version = subprocess.run(["lighthouse", "-V"], stdout=subprocess.PIPE).stdout
if lighthouse_version is not None:
    lighthouse_version = lighthouse_version.decode()
else:
    lighthouse_version = ""
print(f'Lighthouse Version: \n{lighthouse_version}')

print(f'Network: {eth_network_cap}')

print(f'CheckPointSyncURL: {sync_url}')

print(f'FeeRecipientAddress: {fee_address}')

print("\nInstallation successful! See details above")
