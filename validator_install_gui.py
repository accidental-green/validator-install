import os
import re
import fnmatch
import json
import random
import tarfile
import getpass
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path
import requests
import tkinter as tk
from tkinter import filedialog, font

# Define variables
temp_keystore_dir = f'{os.environ["HOME"]}/validator_keys_temp'

# GUI Code
def open_menu(event):
    event.widget.tk.call('tk::MenuInvoke', event.widget._nametowidget(event.widget.cget("menu")), 0)

def get_usb_mount_point():
    user = os.getlogin()
    return f"/media/{user}"

def import_keystore():
    file_path = filedialog.askopenfilename(title="Select a Keystore", initialdir=get_usb_mount_point(), filetypes=[("Keystore files", "*.json"), ("All files", "*.*")])

    if not file_path:  # If user cancels the dialog
        return None

    # Ensure the 'validator_keys_temp' directory exists
    if not os.path.exists(temp_keystore_dir):
        os.makedirs(temp_keystore_dir)

    # Copy the imported file into the 'validator_keys_temp' directory
    destination_path = os.path.join(temp_keystore_dir, os.path.basename(file_path))
    shutil.copy(file_path, destination_path)

    # Update the button after importing the keystore
    update_keystore_button()

    # Returns the path where the file was copied to
    return destination_path

def update_keystore_button():
    home_dir = os.path.expanduser('~')
    
    if os.path.exists(temp_keystore_dir) and os.listdir(temp_keystore_dir):
        # Directory exists and is not empty
        keystore_button.config(text="Keystore successfully imported!", bg="#90EE90", fg="#282C34") # Light green with changed text
    else:
        keystore_button.config(text="Import Keystore", bg="#61afef", fg="#282C34")  # Original color and text
   
def submit():
    global network_var, execution_var, consensus_var, mev_var, eth_address_entry

    eth_network = network_var.get()
    execution_client = execution_var.get()
    consensus_client = consensus_var.get()
    mev_on_off = mev_var.get()
    eth_address = eth_address_entry.get()

    root.destroy()

    return eth_network, execution_client, consensus_client, mev_on_off, eth_address

root = tk.Tk()
root.title("Ethereum Validator Installer")
root.configure(background="#282C34")

network_var = tk.StringVar()
execution_var = tk.StringVar()
consensus_var = tk.StringVar()
mev_var = tk.StringVar()

# Set font size
label_font = font.nametofont("TkDefaultFont").copy()
label_font.config(size=20)
entry_font = font.nametofont("TkDefaultFont").copy()
entry_font.config(size=18)

# Ethereum network selection
network_label = tk.Label(root, text="Choose Ethereum network:", bg="#282C34", fg="#ABB2BF", font=label_font, anchor='e')
network_label.grid(column=0, row=0, padx=30, pady=30, sticky='e')

networks = ('Mainnet', 'Goerli', 'Sepolia')
network_menu = tk.OptionMenu(root, network_var, *networks)
network_menu.config(bg="#4CAF50", fg="#FFFFFF", activebackground="#8BC34A", activeforeground="#FFFFFF", font=entry_font, takefocus=True)
network_menu["menu"].config(bg="#4CAF50", fg="#FFFFFF", activebackground="#8BC34A", activeforeground="#FFFFFF", font=entry_font)
network_menu.grid(column=1, row=0, padx=30, pady=30, ipadx=40, ipady=10)
network_menu.bind('<space>', open_menu)

# Execution client selection
execution_label = tk.Label(root, text="Choose Execution Client:", bg="#282C34", fg="#ABB2BF", font=label_font, anchor='e')
execution_label.grid(column=0, row=1, padx=30, pady=30, sticky='e')

execution_clients = ('Nethermind', 'Besu', 'Geth')
execution_menu = tk.OptionMenu(root, execution_var, *execution_clients)
execution_menu.config(bg="#2196F3", fg="#FFFFFF", activebackground="#64B5F6", activeforeground="#FFFFFF", font=entry_font, takefocus=True)
execution_menu["menu"].config(bg="#2196F3", fg="#FFFFFF", activebackground="#64B5F6", activeforeground="#FFFFFF", font=entry_font)
execution_menu.grid(column=1, row=1, padx=30, pady=30, ipadx=40, ipady=10)
execution_menu.bind('<space>', open_menu)

# Consensus client selection
consensus_label = tk.Label(root, text="Choose Consensus Client:", bg="#282C34", fg="#ABB2BF", font=label_font, anchor='e')
consensus_label.grid(column=0, row=2, padx=30, pady=30, sticky='e')

consensus_clients = ('Nimbus', 'Teku', 'Lighthouse', 'Prysm')
consensus_menu = tk.OptionMenu(root, consensus_var, *consensus_clients)
consensus_menu.config(bg="#FF9800", fg="#FFFFFF", activebackground="#FFA726", activeforeground="#FFFFFF", font=entry_font, takefocus=True)
consensus_menu["menu"].config(bg="#FF9800", fg="#FFFFFF", activebackground="#FFA726", activeforeground="#FFFFFF", font=entry_font)
consensus_menu.grid(column=1, row=2, padx=30, pady=30, ipadx=40, ipady=10)
consensus_menu.bind('<space>', open_menu)

# MEV Boost selection
mev_label = tk.Label(root, text="MEV Boost (On/Off):", bg="#282C34", fg="#ABB2BF", font=label_font, anchor='e')
mev_label.grid(column=0, row=3, padx=30, pady=30, sticky='e')

mev_options = ('On', 'Off')
mev_menu = tk.OptionMenu(root, mev_var, *mev_options)
mev_menu.config(bg="#9C27B0", fg="#FFFFFF", activebackground="#BA68C8", activeforeground="#FFFFFF", font=entry_font, takefocus=True)
mev_menu["menu"].config(bg="#9C27B0", fg="#FFFFFF", activebackground="#BA68C8", activeforeground="#FFFFFF", font=entry_font)
mev_menu.grid(column=1, row=3, padx=30, pady=30, ipadx=40, ipady=10)
mev_menu.bind('<space>', open_menu)

# Ethereum address input
eth_address_label = tk.Label(root, text="Ethereum address for tips (optional):", bg="#282C34", fg="#ABB2BF", font=label_font, anchor='e')
eth_address_label.grid(column=0, row=4, padx=30, pady=30, sticky='e')

eth_address_entry = tk.Entry(root, font=entry_font, takefocus=True)
eth_address_entry.grid(column=1, row=4, padx=30, pady=30, ipadx=40, ipady=10)

# Create the note label
note_label = tk.Label(root, text="Note: Installation / Key import continues in terminal", bg="#282C34", fg="#ABB2BF", font=label_font, anchor='w')
note_label.grid(column=0, row=6, padx=30, pady=60, sticky='w')

# Keystore import
keystore_label = tk.Label(root, text='Import existing validator keystore? (optional):', bg="#282C34", fg="#ABB2BF", font=label_font, anchor='e')
keystore_label.grid(column=0, row=5, padx=30, pady=30, sticky='e')

keystore_button = tk.Button(root, text="Import Keystore", command=import_keystore, bg="#282C34", fg="#ABB2BF", activebackground="#282C34", activeforeground="#ABB2BF", font=label_font, takefocus=True)
keystore_button.grid(column=1, row=5, padx=30, pady=30)


# Submit button
submit_button = tk.Button(root, text="Install", command=lambda: setattr(root, "saved_data", submit()), bg="#282C34", fg="#ABB2BF", activebackground="#61AFEF", activeforeground="#282C34", font=label_font, takefocus=True)
submit_button.grid(column=1, row=6, padx=30, pady=60)

root.saved_data = submit

update_keystore_button()

root.mainloop()

# Define User Input Variables
eth_network = root.saved_data[0]
execution_client = root.saved_data[1]
consensus_client = root.saved_data[2]
mev_on_off = root.saved_data[3].lower()
eth_address = root.saved_data[4]
checkpoint_sync = "On"  # Assume Checkpoint Sync is always set to "On"

# Print User Input Variables
print("\n##### User Selected Inputs #####")
print(f"Ethereum Network: {eth_network}")
print(f"Execution Client: {execution_client}")
print(f"Consensus Client: {consensus_client}")
print(f"Checkpoint Sync: {checkpoint_sync}")
print(f"MEV Boost: {mev_on_off}")
print(f"Ethereum Address: {eth_address}\n")

# Change to the home folder
os.chdir(os.path.expanduser("~"))

print("\n##### Validating User Inputs #####")

# Validator Network from User input
def is_valid_network(network):
    valid_networks = ['MAINNET', 'GOERLI', 'SEPOLIA']
    return network in valid_networks

while True:
    eth_network = eth_network.upper()
    if is_valid_network(eth_network):
        print(f"Ethereum network: {eth_network}")
        break
    else:
        print("Invalid network. Please try again.")

eth_network = eth_network.lower()
eth_network_cap = eth_network.capitalize()

# Validate execution_client from user input
def is_valid_client(client):
    valid_exec_clients = ['GETH', 'BESU', 'NETHERMIND']
    return client in valid_exec_clients

while True:
    execution_client = execution_client.upper()
    if is_valid_client(execution_client):
        print(f"Execution client: {execution_client}")
        break
    else:
        print("Invalid client. Please try again.")

execution_client = execution_client.lower()
execution_client_cap = execution_client.capitalize()

# Validate consensus client from user
def is_valid_consensus_client(client):
    valid_consensus_clients = ['LIGHTHOUSE', 'TEKU', 'PRYSM', 'NIMBUS']
    return client in valid_consensus_clients

while True:
    consensus_client = consensus_client.upper()
    if is_valid_consensus_client(consensus_client):
        print(f"Consensus client: {consensus_client}")
        break
    else:
        print("Invalid client. Please try again.")

consensus_client = consensus_client.lower()
consensus_client_cap = consensus_client.capitalize()

# Validate Ethereum Address from user
def is_valid_eth_address(address):
    pattern = re.compile("^0x[a-fA-F0-9]{40}$")
    return bool(pattern.match(address))

while True:
    user_address = eth_address.lower()
    fee_address = eth_address
    if fee_address.lower() == "":
        fee_address = "EMPTY"
        print("Skipping Ethereum address input. You can set it later.")
        break
    elif is_valid_eth_address(fee_address):
        print("Valid Ethereum address")
        break
    else:
        print("ERROR: Invalid Ethereum address. Exiting Install. Please try again.")
        sys.exit()

def get_random_sync_url(sync_urls):
    selected_sync_url = random.choice(sync_urls)
    return selected_sync_url[1]

if checkpoint_sync.lower() == "on" and consensus_client in ['lighthouse', 'teku', 'prysm']:
    mainnet_sync_urls = [
        ("ETHSTAKER", "https://beaconstate.ethstaker.cc"),
        ("BEACONCHA.IN", "https://sync-mainnet.beaconcha.in"),
        ("ATTESTANT", "https://mainnet-checkpoint-sync.attestant.io"),
        ("SIGMA PRIME", "https://mainnet.checkpoint.sigp.io"),
    ]

    goerli_sync_urls = [
        ("ETHSTAKER", "https://goerli.beaconstate.ethstaker.cc/"),
        ("BEACONSTATE", "https://goerli.beaconstate.info/"),
        ("EF DevOps", "https://checkpoint-sync.goerli.ethpandaops.io/"),
        ("LodeStart", "https://beaconstate-goerli.chainsafe.io/"),
    ]

    sepolia_sync_urls = [
        ("Beaconstate", "https://sepolia.beaconstate.info/"),
        ("LodeStart", "https://beaconstate-sepolia.chainsafe.io/"),
    ]

    if eth_network == "mainnet":
        checkpoint_sync_url = get_random_sync_url(mainnet_sync_urls)
    elif eth_network == "goerli":
        checkpoint_sync_url = get_random_sync_url(goerli_sync_urls)
    elif eth_network == "sepolia":
        checkpoint_sync_url = get_random_sync_url(sepolia_sync_urls)
else:
    checkpoint_sync_url = None

print("Checkpoint Sync URL:", checkpoint_sync_url)

sync_url = checkpoint_sync_url

if 'sync_url' not in locals() or sync_url is None:
    sync_url = None

# User names
execution_user = None
beacon_user = None
validator_user = None

if execution_client == 'geth':
    execution_user = 'geth'
elif execution_client == 'nethermind':
    execution_user = 'nethermind'
elif execution_client == 'besu':
    execution_user = 'besu'

if consensus_client == 'nimbus':
    beacon_user = 'nimbus'
    validator_user = "nimbus"
elif consensus_client == 'teku':
    beacon_user = 'teku'
    validator_user = "teku"
elif consensus_client == 'prysm':
    beacon_user = 'prysmbeacon'
    validator_user = 'prysmvalidator'
elif consensus_client == 'lighthouse':
    beacon_user = 'lighthousebeacon'
    validator_user = 'lighthousevalidator'

# MEV Relay Data
mainnet_relay_options = [
    {'name': 'Aestus', 'url': 'https://0xa15b52576bcbf1072f4a011c0f99f9fb6c66f3e1ff321f11f461d15e31b1cb359caa092c71bbded0bae5b5ea401aab7e@aestus.live'},
    {'name': 'Agnostic Gnosis', 'url': 'https://0xa7ab7a996c8584251c8f925da3170bdfd6ebc75d50f5ddc4050a6fdc77f2a3b5fce2cc750d0865e05d7228af97d69561@agnostic-relay.net'},
    {'name': 'Blocknative', 'url': 'https://0x9000009807ed12c1f08bf4e81c6da3ba8e3fc3d953898ce0102433094e5f22f21102ec057841fcb81978ed1ea0fa8246@builder-relay-mainnet.blocknative.com'},
    {'name': 'bloXroute Ethical', 'url': 'https://0xad0a8bb54565c2211cee576363f3a347089d2f07cf72679d16911d740262694cadb62d7fd7483f27afd714ca0f1b9118@bloxroute.ethical.blxrbdn.com'},
    {'name': 'bloXroute Max Profit', 'url': 'https://0x8b5d2e73e2a3a55c6c87b8b6eb92e0149a125c852751db1422fa951e42a09b82c142c3ea98d0d9930b056a3bc9896b8f@bloxroute.max-profit.blxrbdn.com'},
    {'name': 'bloXroute Regulated', 'url': 'https://0xb0b07cd0abef743db4260b0ed50619cf6ad4d82064cb4fbec9d3ec530f7c5e6793d9f286c4e082c0244ffb9f2658fe88@bloxroute.regulated.blxrbdn.com'},
    {'name': 'Eden Network', 'url': 'https://0xb3ee7afcf27f1f1259ac1787876318c6584ee353097a50ed84f51a1f21a323b3736f271a895c7ce918c038e4265918be@relay.edennetwork.io'},
    {'name': 'Flashbots', 'url': 'https://0xac6e77dfe25ecd6110b8e780608cce0dab71fdd5ebea22a16c0205200f2f8e2e3ad3b71d3499c54ad14d6c21b41a37ae@boost-relay.flashbots.net'},
    {'name': 'Manifold', 'url': 'https://0x98650451ba02064f7b000f5768cf0cf4d4e492317d82871bdc87ef841a0743f69f0f1eea11168503240ac35d101c9135@mainnet-relay.securerpc.com'},
    {'name': 'Ultra Sound', 'url': 'https://0xa1559ace749633b997cb3fdacffb890aeebdb0f5a3b6aaa7eeeaf1a38af0a8fe88b9e4b1f61f236d2e64d95733327a62@relay.ultrasound.money'}
]

mainnet_relay_names = [option['name'] for option in mainnet_relay_options]
mainnet_relay_names_sentence = ', '.join(mainnet_relay_names)

goerli_relay_options = [
    {'name': 'Flashbots', 'url': 'https://0xafa4c6985aa049fb79dd37010438cfebeb0f2bd42b115b89dd678dab0670c1de38da0c4e9138c9290a398ecd9a0b3110@builder-relay-goerli.flashbots.net'},
    {'name': 'bloXroute', 'url': 'https://0x821f2a65afb70e7f2e820a925a9b4c80a159620582c1766b1b09729fec178b11ea22abb3a51f07b288be815a1a2ff516@bloxroute.max-profit.builder.goerli.blxrbdn.com'},
    {'name': 'Blocknative', 'url': 'https://0x8f7b17a74569b7a57e9bdafd2e159380759f5dc3ccbd4bf600414147e8c4e1dc6ebada83c0139ac15850eb6c975e82d0@builder-relay-goerli.blocknative.com'},
    {'name': 'Eden Network', 'url': 'https://0xb1d229d9c21298a87846c7022ebeef277dfc321fe674fa45312e20b5b6c400bfde9383f801848d7837ed5fc449083a12@relay-goerli.edennetwork.io'},
    {'name': 'Manifold', 'url': 'https://0x8a72a5ec3e2909fff931c8b42c9e0e6c6e660ac48a98016777fc63a73316b3ffb5c622495106277f8dbcc17a06e92ca3@goerli-relay.securerpc.com/'},
    {'name': 'Aestus', 'url': 'https://0xab78bf8c781c58078c3beb5710c57940874dd96aef2835e7742c866b4c7c0406754376c2c8285a36c630346aa5c5f833@goerli.aestus.live'},
    {'name': 'Ultra Sound', 'url': 'https://0xb1559beef7b5ba3127485bbbb090362d9f497ba64e177ee2c8e7db74746306efad687f2cf8574e38d70067d40ef136dc@relay-stag.ultrasound.money'}
]

sepolia_relay_options = [
    {'name': 'Flashbots', 'url': 'https://0x845bd072b7cd566f02faeb0a4033ce9399e42839ced64e8b2adcfc859ed1e8e1a5a293336a49feac6d9a5edb779be53a@boost-relay-sepolia.flashbots.net'}
]

# Install ufw
subprocess.run(['sudo', 'apt', 'install', 'ufw'])

# Set default policies
subprocess.run(['sudo', 'ufw', 'default', 'deny', 'incoming'])
subprocess.run(['sudo', 'ufw', 'default', 'allow', 'outgoing'])

# Allow specific ports
subprocess.run(['sudo', 'ufw', 'allow', '6673/tcp'])
subprocess.run(['sudo', 'ufw', 'allow', '30303'])
subprocess.run(['sudo', 'ufw', 'allow', '9000'])

# Enable and check status
subprocess.run(['sudo', 'ufw', 'enable'])
subprocess.run(['sudo', 'ufw', 'status', 'numbered'])

# Install Go & MEV
if  mev_on_off == "on":
    # Step 1: Install Go 1.18+
    os.system("cd $HOME")
    os.system("wget -O go.tar.gz https://go.dev/dl/go1.19.6.linux-amd64.tar.gz")
    os.system("sudo rm -rf /usr/local/go && sudo tar -C /usr/local -xzf go.tar.gz")
    os.system("rm go.tar.gz")
    os.system('echo export PATH=$PATH:/usr/local/go/bin >> $HOME/.bashrc')
    os.system("source $HOME/.bashrc")
    os.system("go version")

    # Step 2: Create mevboost service account
    os.system("sudo useradd --no-create-home --shell /bin/false mevboost")

    # Step 3: Install mevboost
    os.system("sudo apt -y install build-essential")
    os.system('CGO_CFLAGS="-O -D__BLST_PORTABLE__" go install github.com/flashbots/mev-boost@latest')
    os.system("sudo cp $HOME/go/bin/mev-boost /usr/local/bin")
    os.system("sudo chown mevboost:mevboost /usr/local/bin/mev-boost")

# Create JWT directory
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

############ GETH ##################
if execution_client == 'geth':
    # Create User and directories
    subprocess.run(['sudo', 'useradd', '--no-create-home', '--shell', '/bin/false', 'geth'])
    subprocess.run(['sudo', 'mkdir', '-p', '/var/lib/geth'])
    subprocess.run(['sudo', 'chown', '-R', 'geth:geth', '/var/lib/geth'])

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

############ BESU ##################
if execution_client == 'besu':
	# Create User and directories
	subprocess.run(['sudo', 'useradd', '--no-create-home', '--shell', '/bin/false', 'besu'])
	subprocess.run(['sudo', 'mkdir', '-p', '/var/lib/besu'])
	subprocess.run(['sudo', 'chown', '-R', 'besu:besu', '/var/lib/besu'])

	# Get the latest version number
	url = "https://api.github.com/repos/hyperledger/besu/releases/latest"
	response = urllib.request.urlopen(url)
	data = json.loads(response.read().decode("utf-8"))
	latest_version = data['tag_name']

	besu_version = latest_version

	# Download the latest version
	download_url = f"https://hyperledger.jfrog.io/hyperledger/besu-binaries/besu/{latest_version}/besu-{latest_version}.tar.gz"
	urllib.request.urlretrieve(download_url, f"besu-{latest_version}.tar.gz")

	# Extract the tar.gz file
	with tarfile.open(f"besu-{latest_version}.tar.gz", "r:gz") as tar:
	    tar.extractall()

	# Copy the extracted besu folder to /usr/local/bin/besu
	subprocess.run(["sudo", "cp", "-a", f"besu-{latest_version}", "/usr/local/bin/besu"], check=True)

	# Remove the downloaded .tar.gz file
	os.remove(f"besu-{latest_version}.tar.gz")

	# Install OpenJDK-17-JRE
	subprocess.run(["sudo", "apt", "-y", "install", "openjdk-17-jre"])

	# Install libjemalloc-dev
	subprocess.run(["sudo", "apt", "install", "-y", "libjemalloc-dev"])

############ NETHERMIND ##################
if execution_client == 'nethermind':
    # Create User and directories
    subprocess.run(["sudo", "useradd", "--no-create-home", "--shell", "/bin/false", "nethermind"])
    subprocess.run(["sudo", "mkdir", "-p", "/var/lib/nethermind"])
    subprocess.run(["sudo", "chown", "-R", "nethermind:nethermind", "/var/lib/nethermind"])
    subprocess.run(["sudo", "apt-get", "install", "libsnappy-dev", "libc6-dev", "libc6", "unzip", "-y"], check=True)

    # Define the Github API endpoint to get the latest release
    url = 'https://api.github.com/repos/NethermindEth/nethermind/releases/latest'

    # Send a GET request to the API endpoint
    response = requests.get(url)

    # Search for the asset with the name that ends in linux-x64.zip
    assets = response.json()['assets']
    download_url = None
    zip_filename = None
    for asset in assets:
        if asset['name'].endswith('linux-x64.zip'):
            download_url = asset['browser_download_url']
            zip_filename = asset['name']
            break

    if download_url is None or zip_filename is None:
        print("Error: Could not find the download URL for the latest release.")
        exit(1)

    # Download the latest release binary
    response = requests.get(download_url)

    # Save the binary to a temporary file
    with tempfile.NamedTemporaryFile('wb', suffix='.zip', delete=False) as temp_file:
        temp_file.write(response.content)
        temp_path = temp_file.name

    # Create a temporary directory for extraction
    with tempfile.TemporaryDirectory() as temp_dir:
        # Extract the binary to the temporary directory
        with zipfile.ZipFile(temp_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        # Copy the contents of the temporary directory to /usr/local/bin/nethermind using sudo
        subprocess.run(["sudo", "cp", "-a", f"{temp_dir}/.", "/usr/local/bin/nethermind"])

    # chown nethermind:nethermind /usr/local/bin/nethermind
    subprocess.run(["sudo", "chown", "nethermind:nethermind", "/usr/local/bin/nethermind"])

    # chown nethermind:nethermind /usr/local/bin/nethermind/Nethermind.Runner
    subprocess.run(["sudo", "chown", "nethermind:nethermind", "/usr/local/bin/nethermind/Nethermind.Runner"])

    # chmod a+x /usr/local/bin/nethermind/Nethermind.Runner
    subprocess.run(["sudo", "chmod", "a+x", "/usr/local/bin/nethermind/Nethermind.Runner"])

    # Remove the temporary zip file
    os.remove(temp_path)

    nethermind_version = os.path.splitext(zip_filename)[0]

############ TEKU ##################
if consensus_client == 'teku':
    # Create User and directories
    subprocess.run(['sudo', 'useradd', '--no-create-home', '--shell', '/bin/false', 'teku'])
    subprocess.run(['sudo', 'mkdir', '-p', '/var/lib/teku'])
    subprocess.run(['sudo', 'mkdir', '-p', '/var/lib/teku/validator_keys'])

    # Change to the home folder
    os.chdir(os.path.expanduser("~"))

    # Define the Github API endpoint to get the latest release
    url = 'https://api.github.com/repos/ConsenSys/teku/releases/latest'

    # Send a GET request to the API endpoint
    response = requests.get(url)

    # Get the latest release tag
    latest_version = response.json()['tag_name']

    # Define the download URL for the latest release
    download_url = f"https://artifacts.consensys.net/public/teku/raw/names/teku.tar.gz/versions/{latest_version}/teku-{latest_version}.tar.gz"
    teku_version = latest_version
    # Download the latest release binary
    response = requests.get(download_url)

    # Save the binary to the home folder
    with open('teku.tar.gz', 'wb') as f:
        f.write(response.content)

    # Extract the binary to the home folder
    with tarfile.open('teku.tar.gz', 'r:gz') as tar:
        tar.extractall()

    # Copy the binary folder to /usr/local/bin using sudo
    os.system(f"sudo cp -r teku-{latest_version} /usr/local/bin/teku")

    # Remove the teku.tar.gz file and extracted binary folder
    os.remove('teku.tar.gz')
    shutil.rmtree(f'teku-{latest_version}')

    print("Teku binary installed successfully!")
    print(f"Download URL: {download_url}")
    
    ### IMPORT KEYSTORE ####

    # Check if temp_keystore_dir exists, then get the .json files
    json_files_in_source = [f for f in os.listdir(temp_keystore_dir)] if os.path.exists(temp_keystore_dir) else []

    json_files_in_source = [f for f in json_files_in_source if f.endswith('.json')]

    if len(json_files_in_source) > 0:  # Ensure source directory is not empty
        # Check if the teku validator_keys directory exists, otherwise create it
        validator_keys_dir = '/var/lib/teku/validator_keys'
        if not os.path.exists(validator_keys_dir):
            subprocess.run(['sudo', 'mkdir', '-p', validator_keys_dir])

        for json_file in json_files_in_source:
            source_path = os.path.join(temp_keystore_dir, json_file)
            dest_path = os.path.join(validator_keys_dir, json_file)
            
            if os.path.exists(dest_path):
                print(f"Ignoring keystore {json_file} as it already exists.")
            else:
                subprocess.run(['sudo', 'cp', source_path, dest_path])
                print(f"Successfully imported keystore {json_file}.")
        
        teku_keystore_dir = '/var/lib/teku/validator_keys'
        
        def get_and_store_password(json_file):
            txt_file_name = os.path.splitext(json_file)[0] + '.txt'
            txt_file_path = os.path.join(teku_keystore_dir, txt_file_name)
            
            # Prompt for the password and store it directly in a bytearray
            teku_pass = bytearray(getpass.getpass(prompt=f'Please enter password for {json_file}: '), 'utf-8')
            
            # Use a temporary file for writing the password.txt file
            temp_file_name = 'temp_password_file.txt'
            with open(temp_file_name, 'wb') as f:
                os.write(f.fileno(), teku_pass)
            
            # Use sudo to move the temp file to the actual desired location
            subprocess.run(['sudo', 'mv', temp_file_name, txt_file_path])
            
            # Modify permissions of the text file so it's not readable by others
            subprocess.run(['sudo', 'chmod', '600', txt_file_path])
            
            # Overwrite the password in memory with zero bytes
            for i in range(len(teku_pass)):
                teku_pass[i] = 0

        # List all files ending with .json in the teku keystore directory
        json_files = [f for f in os.listdir(teku_keystore_dir) if f.endswith('.json')]

        # For each json file, prompt for password and create a corresponding txt file
        for json_file in json_files:
            get_and_store_password(json_file)
    
    # Change ownership
    subprocess.run(['sudo', 'chown', '-R', 'teku:teku', '/var/lib/teku'])

################ PRYSM ###################
if consensus_client == 'prysm':
    # Create prysmbeacon user
    subprocess.run(['sudo', 'useradd', '--no-create-home', '--shell', '/bin/false', 'prysmbeacon'])

    # Create and set ownership for /var/lib/prysm/beacon directory
    subprocess.run(['sudo', 'mkdir', '-p', '/var/lib/prysm/beacon'])
    subprocess.run(['sudo', 'chown', '-R', 'prysmbeacon:prysmbeacon', '/var/lib/prysm/beacon'])

    # Create prysmvalidator user
    subprocess.run(['sudo', 'useradd', '--no-create-home', '--shell', '/bin/false', 'prysmvalidator'])

    # Create /var/lib/prysm/validator directory
    subprocess.run(['sudo', 'mkdir', '-p', '/var/lib/prysm/validator'])

    base_url = "https://api.github.com/repos/prysmaticlabs/prysm/releases/latest"
    response = requests.get(base_url)
    response_json = response.json()
    download_links = []

    for asset in response_json["assets"]:
        if re.search(r'beacon-chain-v\d+\.\d+\.\d+-linux-amd64$', asset["browser_download_url"]):
            download_links.append(asset["browser_download_url"])
        elif re.search(r'validator-v\d+\.\d+\.\d+-linux-amd64$', asset["browser_download_url"]):
            download_links.append(asset["browser_download_url"])

    if len(download_links) >= 2:
        for link in download_links[:2]:
            cmd = f"curl -LO {link}"
            os.system(cmd)

        os.system("mv beacon-chain-*-linux-amd64 beacon-chain")
        os.system("mv validator-*-linux-amd64 validator")
        os.system("chmod +x beacon-chain")
        os.system("chmod +x validator")
        os.system("sudo cp beacon-chain /usr/local/bin")
        os.system("sudo cp validator /usr/local/bin")
        os.system("rm beacon-chain && rm validator")
    else:
        print("Error: Could not find the latest release links.")

    # Check if temp_keystore_dir exists, import keys and create password .txt file
    if os.path.exists(temp_keystore_dir) and os.listdir(temp_keystore_dir):

        # Import validator keys
        print("Importing Validator Keystore...")
        
        subprocess.run([
            'sudo',
            '/usr/local/bin/validator',
            'accounts', 'import',
            '--keys-dir', temp_keystore_dir,
            '--wallet-dir', '/var/lib/prysm/validator',
            '--mainnet'
        ])
        
        def get_and_store_password():
            # Prompt for the password and store it directly in a bytearray
            prysm_pass = bytearray(getpass.getpass(prompt='Please enter your Prysm wallet password: '), 'utf-8')
            
            prysm_pass_temp_file = 'password_temp.txt'
            prysm_pass_path = '/var/lib/prysm/validator/password.txt'
            
            # Write the password to the temp file directly from the bytearray
            with open(prysm_pass_temp_file, 'wb') as f:
                os.write(f.fileno(), prysm_pass)

            # Use sudo to move the temp file to the actual desired location
            subprocess.run(['sudo', 'mv', prysm_pass_temp_file, prysm_pass_path])

            # Modify permissions of the text file so it's not readable by others
            subprocess.run(['sudo', 'chmod', '600', prysm_pass_path])
            
            # Overwrite the password in memory with zero bytes to erase it
            for i in range(len(prysm_pass)):
                prysm_pass[i] = 0

        get_and_store_password()
        
    # Set ownership of prysmvalidator
    subprocess.run(['sudo', 'chown', '-R', 'prysmvalidator:prysmvalidator', '/var/lib/prysm/validator'])    
    
################ NIMBUS ##################
if consensus_client == 'nimbus':
    # Create /var/lib/nimbus directory
    subprocess.run(['sudo', 'mkdir', '-p', '/var/lib/nimbus'])
    
    # Change Ownership
    subprocess.run(['sudo', 'chmod', '700', '/var/lib/nimbus'])
    
    # Create nimbus user
    subprocess.run(['sudo', 'useradd', '--no-create-home', '--shell', '/bin/false', 'nimbus'])

    # Change to the home folder
    os.chdir(os.path.expanduser("~"))

    # Define the Github API endpoint to get the latest release
    url = 'https://api.github.com/repos/status-im/nimbus-eth2/releases/latest'

    # Send a GET request to the API endpoint
    response = requests.get(url)

    # Search for the asset with the name that ends in _Linux_amd64.tar.gz
    assets = response.json()['assets']
    download_url = None
    for asset in assets:
        if '_Linux_amd64' in asset['name'] and asset['name'].endswith('.tar.gz'):
            download_url = asset['browser_download_url']
            break

    if download_url is None:
        print("Error: Could not find the download URL for the latest release.")
        exit(1)

    # Download the latest release binary
    response = requests.get(download_url)

    # Save the binary to the home folder
    with open('nimbus.tar.gz', 'wb') as f:
        f.write(response.content)

    # Extract the binary to the home folder
    with tarfile.open('nimbus.tar.gz', 'r:gz') as tar:
        tar.extractall()

    # Find the extracted folder
    extracted_folder = None
    for item in os.listdir():
        if item.startswith("nimbus-eth2_Linux_amd64"):
            extracted_folder = item
            break

    if extracted_folder is None:
        print("Error: Could not find the extracted folder.")
        exit(1)

    # Copy the binary to /usr/local/bin using sudo
    os.system(f"sudo cp {extracted_folder}/build/nimbus_beacon_node /usr/local/bin")

    # Remove the nimbus.tar.gz file and extracted folder
    os.remove('nimbus.tar.gz')
    os.system(f"rm -r {extracted_folder}")

    print("Nimbus binary installed successfully!")
    print(f"Download URL: {download_url}")

    # Check if the temp_keystore_dir exists and is not empty
    if os.path.exists(temp_keystore_dir) and os.listdir(temp_keystore_dir):

        # Import Validator keystore
        subprocess.run([
            'sudo',
            '/usr/local/bin/nimbus_beacon_node',
            'deposits', 'import',
            '--data-dir=/var/lib/nimbus',
            temp_keystore_dir
        ])
            
    # Set ownership for /var/lib/nimbus directory
    subprocess.run(['sudo', 'chown', '-R', 'nimbus:nimbus', '/var/lib/nimbus'])

############ LIGHTHOUSE ##################
if consensus_client == 'lighthouse':
    # Create User and directories
    subprocess.run(['sudo', 'useradd', '--no-create-home', '--shell', '/bin/false', 'lighthousebeacon'])
    subprocess.run(['sudo', 'useradd', '--no-create-home', '--shell', '/bin/false', 'lighthousevalidator'])
    subprocess.run(['sudo', 'mkdir', '-p', '/var/lib/lighthouse/beacon'])
    subprocess.run(['sudo', 'mkdir', '-p', '/var/lib/lighthouse/validators'])
    subprocess.run(['sudo', 'chown', '-R', 'lighthousebeacon:lighthousebeacon', '/var/lib/lighthouse/beacon'])

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

    # Check if the temp_keystore_dir exists and is not empty, then import
    if os.path.exists(temp_keystore_dir) and os.listdir(temp_keystore_dir):

        # Lighthouse Import Keystore
        print("Importing Validator Keystore...")

        subprocess.run([
            'sudo', 
            '/usr/local/bin/lighthouse', 
            '--network', 'mainnet', 
            'account', 'validator', 'import', 
            '--directory', temp_keystore_dir, 
            '--datadir', '/var/lib/lighthouse'
        ])
    
    # Change ownership of validator directory
    subprocess.run(['sudo', 'chown', '-R', 'lighthousevalidator:lighthousevalidator', '/var/lib/lighthouse/validators'])

###### GETH SERVICE FILE #############
if execution_client == 'geth':
    geth_service_file_lines = [
        '[Unit]',
        'Description=Geth Execution Client (Mainnet)',
        'Wants=network.target',
        'After=network.target',
        '',
        '[Service]',
        'User=geth',
        'Group=geth',
        'Type=simple',
        'Restart=always',
        'RestartSec=5',
        'TimeoutStopSec=600',
        'ExecStart=/usr/local/bin/geth \\',
        f'    --{eth_network} \\',
        '    --datadir /var/lib/geth \\',
        '    --authrpc.jwtsecret /var/lib/jwtsecret/jwt.hex',
        '',
        '[Install]',
        'WantedBy=default.target',
    ]

    geth_service_file = '\n'.join(geth_service_file_lines)

    geth_temp_file = 'geth_temp.service'
    geth_service_file_path = '/etc/systemd/system/geth.service'

    with open(geth_temp_file, 'w') as f:
        f.write(geth_service_file)

    os.system(f'sudo cp {geth_temp_file} {geth_service_file_path}')
    os.remove(geth_temp_file)

############ BESU SERVICE FILE ###############
if execution_client == 'besu':
    besu_service_file_lines = [
        '[Unit]',
        'Description=Besu Execution Client (Mainnet)',
        'Wants=network-online.target',
        'After=network-online.target',
        '',
        '[Service]',
        'User=besu',
        'Group=besu',
        'Type=simple',
        'Restart=always',
        'RestartSec=5',
        'Environment="JAVA_OPTS=-Xmx5g"',
        'ExecStart=/usr/local/bin/besu/bin/besu \\',
        f'    --network={eth_network} \\',
        '    --sync-mode=X_SNAP \\',
        '    --data-path=/var/lib/besu \\',
        '    --data-storage-format=BONSAI \\',
        '    --engine-jwt-secret=/var/lib/jwtsecret/jwt.hex',
        '',
        '[Install]',
        'WantedBy=multi-user.target',
    ]

    besu_service_file = '\n'.join(besu_service_file_lines)

    besu_temp_file = 'besu_temp.service'
    besu_service_file_path = '/etc/systemd/system/besu.service'

    with open(besu_temp_file, 'w') as f:
        f.write(besu_service_file)

    os.system(f'sudo cp {besu_temp_file} {besu_service_file_path}')
    os.remove(besu_temp_file)

####### NETHERMIND SERVICE FILE ###########
if execution_client == 'nethermind':
    nethermind_service_file_lines = [
        '[Unit]',
        'Description=Nethermind Execution Client (Mainnet)',
        'Wants=network.target',
        'After=network.target',
        '',
        '[Service]',
        'User=nethermind',
        'Group=nethermind',
        'Type=simple',
        'Restart=always',
        'RestartSec=5',
        'WorkingDirectory=/var/lib/nethermind',
        'Environment="DOTNET_BUNDLE_EXTRACT_BASE_DIR=/var/lib/nethermind"',
        'ExecStart=/usr/local/bin/nethermind/Nethermind.Runner \\',
        f'    --config {eth_network} \\',
        '    --datadir /var/lib/nethermind \\',
        '    --Sync.SnapSync true \\',
        '    --Sync.AncientBodiesBarrier 11052984 \\',
        '    --Sync.AncientReceiptsBarrier 11052984 \\',
        '    --JsonRpc.JwtSecretFile /var/lib/jwtsecret/jwt.hex',
        '',
        '[Install]',
        'WantedBy=default.target',
    ]

    nethermind_service_file = '\n'.join(nethermind_service_file_lines)

    nethermind_temp_file = 'nethermind_temp.service'
    nethermind_service_file_path = '/etc/systemd/system/nethermind.service'

    with open(nethermind_temp_file, 'w') as f:
        f.write(nethermind_service_file)

    os.system(f'sudo cp {nethermind_temp_file} {nethermind_service_file_path}')

    os.remove(nethermind_temp_file)

###### TEKU SERVICE FILE #######
if consensus_client == 'teku':
    teku_service_file_lines = [
        '[Unit]',
        'Description=Teku Consensus Client (Mainnet)',
        'Wants=network-online.target',
        'After=network-online.target',
        '',
        '[Service]',
        'User=teku',
        'Group=teku',
        'Type=simple',
        'Restart=always',
        'RestartSec=5',
        'Environment="JAVA_OPTS=-Xmx5g"',
        'Environment="TEKU_OPTS=-XX:-HeapDumpOnOutOfMemoryError"',
        'ExecStart=/usr/local/bin/teku/bin/teku \\',
        f'    --network={eth_network} \\',
        '    --data-path=/var/lib/teku \\',
        '    --validator-keys=/var/lib/teku/validator_keys:/var/lib/teku/validator_keys \\',
        '    --ee-endpoint=http://127.0.0.1:8551 \\',
        '    --ee-jwt-secret-file=/var/lib/jwtsecret/jwt.hex \\',
        *([f'    --initial-state={sync_url} \\'] if sync_url is not None else []),
        *([f'    --validators-builder-registration-default-enabled=true \\'] if mev_on_off == 'on' else []),
        *([f'    --builder-endpoint=http://127.0.0.1:18550 \\'] if mev_on_off == 'on' else []),
        f'    --validators-proposer-default-fee-recipient={fee_address}',
        '',
        '[Install]',
        'WantedBy=multi-user.target',
    ]

    teku_service_file = '\n'.join(teku_service_file_lines)

    teku_temp_file = 'teku_temp.service'
    teku_service_file_path = '/etc/systemd/system/teku.service'

    with open(teku_temp_file, 'w') as f:
        f.write(teku_service_file)

    os.system(f'sudo cp {teku_temp_file} {teku_service_file_path}')
    os.remove(teku_temp_file)

########### NIMBUS SERVICE FILE #############
if consensus_client == 'nimbus':
    nimbus_service_file_lines = [
        '[Unit]',
        'Description=Nimbus Consensus Client (Mainnet)',
        'Wants=network-online.target',
        'After=network-online.target',
        '',
        '[Service]',
        'User=nimbus',
        'Group=nimbus',
        'Type=simple',
        'Restart=always',
        'RestartSec=5',
        'ExecStart=/usr/local/bin/nimbus_beacon_node \\',
        f'    --network={eth_network} \\',
        '    --data-dir=/var/lib/nimbus \\',
        '    --web3-url=http://127.0.0.1:8551 \\',
        '    --jwt-secret=/var/lib/jwtsecret/jwt.hex \\',
        *([f'    --payload-builder=true \\'] if mev_on_off == 'on' else []),
        *([f'    --payload-builder-url=http://127.0.0.1:18550 \\'] if mev_on_off == 'on' else []),
        f'    --suggested-fee-recipient={fee_address}',
        '',
        '[Install]',
        'WantedBy=multi-user.target',
    ]

    nimbus_service_file = '\n'.join(nimbus_service_file_lines)

    nimbus_temp_file = 'nimbus_temp.service'
    nimbus_service_file_path = '/etc/systemd/system/nimbus.service'

    with open(nimbus_temp_file, 'w') as f:
        f.write(nimbus_service_file)

    os.system(f'sudo cp {nimbus_temp_file} {nimbus_service_file_path}')
    os.remove(nimbus_temp_file)

########### PRYSM SERVICE FILE ##############
if consensus_client == 'prysm':
    prysm_beacon_service_file_lines = [
        '[Unit]',
        'Description=Prysm Consensus Client BN (Mainnet)',
        'Wants=network-online.target',
        'After=network-online.target',
        '',
        '[Service]',
        'User=prysmbeacon',
        'Group=prysmbeacon',
        'Type=simple',
        'Restart=always',
        'RestartSec=5',
        'ExecStart=/usr/local/bin/beacon-chain \\',
        f'    --{eth_network} \\',
        '    --datadir=/var/lib/prysm/beacon \\',
        '    --execution-endpoint=http://127.0.0.1:8551 \\',
        '    --jwt-secret=/var/lib/jwtsecret/jwt.hex \\',
        f'    --suggested-fee-recipient={fee_address} \\',
        *([f'    --checkpoint-sync-url={sync_url} \\'] if sync_url is not None else []),
        *([f'    --genesis-beacon-api-url={sync_url} \\'] if sync_url is not None else []),
        *([f'    --http-mev-relay=http://127.0.0.1:18550 \\'] if mev_on_off == 'on' else []),
        '    --accept-terms-of-use',
        '',
        '[Install]',
        'WantedBy=multi-user.target',
    ]

    prysm_beacon_service_file = '\n'.join(prysm_beacon_service_file_lines)

    prysm_validator_service_file_lines = [
        '[Unit]',
        'Description=Prysm Consensus Client VC (Mainnet)',
        'Wants=network-online.target',
        'After=network-online.target',
        '',
        '[Service]',
        'User=prysmvalidator',
        'Group=prysmvalidator',
        'Type=simple',
        'Restart=always',
        'RestartSec=5',
        'ExecStart=/usr/local/bin/validator \\',
        '    --datadir=/var/lib/prysm/validator \\',
        '    --wallet-dir=/var/lib/prysm/validator \\',
        '    --wallet-password-file=/var/lib/prysm/validator/password.txt \\',
        f'    --suggested-fee-recipient={fee_address} \\',
        *([f'    --enable-builder \\'] if mev_on_off == 'on' else []),
        '    --accept-terms-of-use',
        '',
        '[Install]',
        'WantedBy=multi-user.target',
    ]

    prysm_validator_service_file = '\n'.join(prysm_validator_service_file_lines)

    prysm_beacon_temp_file = 'prysm_beacon_temp.service'
    prysm_beacon_service_file_path = '/etc/systemd/system/prysmbeacon.service'
    prysm_validator_temp_file = 'prysm_validator_temp.service'
    prysm_validator_service_file_path = '/etc/systemd/system/prysmvalidator.service'

    with open(prysm_beacon_temp_file, 'w') as f:
        f.write(prysm_beacon_service_file)

    with open(prysm_validator_temp_file, 'w') as f:
        f.write(prysm_validator_service_file)

    os.system(f'sudo cp {prysm_beacon_temp_file} {prysm_beacon_service_file_path}')
    os.remove(prysm_beacon_temp_file)
    os.system(f'sudo cp {prysm_validator_temp_file} {prysm_validator_service_file_path}')
    os.remove(prysm_validator_temp_file)

######## LIGHTHOUSE SERVICE FILES ###########
if consensus_client == 'lighthouse':
# Beacon Service File
    lh_beacon_service_file_lines = [
        '[Unit]',
        'Description=Lighthouse Consensus Client BN (Mainnet)',
        'Wants=network-online.target',
        'After=network-online.target',
        '',
        '[Service]',
        'User=lighthousebeacon',
        'Group=lighthousebeacon',
        'Type=simple',
        'Restart=always',
        'RestartSec=5',
        'ExecStart=/usr/local/bin/lighthouse bn \\',
        f'    --network {eth_network} \\',
        '    --datadir /var/lib/lighthouse \\',
        '    --http \\',
        '    --execution-endpoint http://127.0.0.1:8551 \\',
        '    --execution-jwt /var/lib/jwtsecret/jwt.hex \\',
        *([f'    --checkpoint-sync-url {sync_url} \\'] if sync_url is not None else []),
        *([f'    --builder http://127.0.0.1:18550 \\'] if mev_on_off == 'on' else []),
        '',
        '[Install]',
        'WantedBy=multi-user.target',
    ]

    lh_beacon_service_file = '\n'.join(lh_beacon_service_file_lines)

# Validator Service FIle
    lh_validator_service_file_lines = [
        '[Unit]',
        'Description=Lighthouse Consensus Client VC (Mainnet)',
        'Wants=network-online.target',
        'After=network-online.target',
        '',
        '[Service]',
        'User=lighthousevalidator',
        'Group=lighthousevalidator',
        'Type=simple',
        'Restart=always',
        'RestartSec=5',
        'ExecStart=/usr/local/bin/lighthouse vc \\',
        f'    --network {eth_network} \\',
        '    --datadir /var/lib/lighthouse \\',
        *([f'    --builder-proposals \\'] if mev_on_off == 'on' else []),
        f'    --suggested-fee-recipient {fee_address}',
        '',
        '[Install]',
        'WantedBy=multi-user.target',
    ]

    lh_validator_service_file = '\n'.join(lh_validator_service_file_lines)

# Write Service files
    lh_beacon_temp_file = 'lh_beacon_temp.service'
    lh_validator_temp_file = 'lh_validator_temp.service'
    lh_beacon_service_file_path = '/etc/systemd/system/lighthousebeacon.service'
    lh_validator_service_file_path = '/etc/systemd/system/lighthousevalidator.service'

    with open(lh_beacon_temp_file, 'w') as f:
	    f.write(lh_beacon_service_file)

    with open(lh_validator_temp_file, 'w') as f:
	    f.write(lh_validator_service_file)

    os.system(f'sudo cp {lh_beacon_temp_file} {lh_beacon_service_file_path}')
    os.system(f'sudo cp {lh_validator_temp_file} {lh_validator_service_file_path}')
    os.remove(lh_beacon_temp_file)
    os.remove(lh_validator_temp_file)

# MEV Service File
if mev_on_off == 'on':
    mev_boost_service_file_lines = [
        '[Unit]',
        'Description=mev-boost ethereum mainnet',
        'Wants=network-online.target',
        'After=network-online.target',
        '',
        '[Service]',
        'User=mevboost',
        'Group=mevboost',
        'Type=simple',
        'Restart=always',
        'RestartSec=5',
        'ExecStart=/usr/local/bin/mev-boost \\',
        f'    -{eth_network} \\',
        '    -min-bid 0.05 \\',
        '    -relay-check \\',
    ]

    # Add relay lines from relay_options
    
    if eth_network == 'mainnet':
        for relay in mainnet_relay_options:
            relay_line = f'    -relay {relay["url"]} \\'
            mev_boost_service_file_lines.append(relay_line)

        # Remove the trailing '\\' from the last relay line
        mev_boost_service_file_lines[-1] = mev_boost_service_file_lines[-1].rstrip(' \\')

        mev_boost_service_file_lines.extend([
            '',
            '[Install]',
            'WantedBy=multi-user.target',
    ])
    elif eth_network == 'goerli':
        for relay in goerli_relay_options:
            relay_line = f'    -relay {relay["url"]} \\'
            mev_boost_service_file_lines.append(relay_line)

        # Remove the trailing '\\' from the last relay line
        mev_boost_service_file_lines[-1] = mev_boost_service_file_lines[-1].rstrip(' \\')

        mev_boost_service_file_lines.extend([
            '',
            '[Install]',
            'WantedBy=multi-user.target',
    ])
    else:
        for relay in sepolia_relay_options:
            relay_line = f'    -relay {relay["url"]} \\'
            mev_boost_service_file_lines.append(relay_line)

        # Remove the trailing '\\' from the last relay line
        mev_boost_service_file_lines[-1] = mev_boost_service_file_lines[-1].rstrip(' \\')

        mev_boost_service_file_lines.extend([
            '',
            '[Install]',
            'WantedBy=multi-user.target',
    ])
    

    mev_boost_service_file = '\n'.join(mev_boost_service_file_lines)

    mev_boost_temp_file = 'mev_boost_temp.service'
    mev_boost_service_file_path = '/etc/systemd/system/mevboost.service'

    with open(mev_boost_temp_file, 'w') as f:
        f.write(mev_boost_service_file)

    os.system(f'sudo cp {mev_boost_temp_file} {mev_boost_service_file_path}')
    os.remove(mev_boost_temp_file)

# Reload the systemd daemon
subprocess.run(['sudo', 'systemctl', 'daemon-reload'])

# Delete temp keystore files
validator_keys_temp = os.path.join(os.environ["HOME"], 'validator_keys_temp')
subprocess.run(['sudo', 'rm', '-rf', validator_keys_temp])

# Print the final output
inbound_ports = subprocess.run(["sudo", "ufw", "status", "numbered"], stdout=subprocess.PIPE).stdout
if inbound_ports is not None:
    inbound_ports = inbound_ports.decode()
else:
    inbound_ports = ""
print(f'\nFirewall Status:\nInbound Ports: {inbound_ports}Outbound Ports: 9000, 30303, 6673/tcp\n')

if execution_client == 'geth':
    geth_version = subprocess.run(["geth", "--version"], stdout=subprocess.PIPE).stdout
    if geth_version is not None:
        geth_version = geth_version.decode()
        geth_version = geth_version.split(" ")[-1]
    else:
        geth_version = ""
    print(f'Geth Version: v{geth_version}')

if consensus_client == 'lighthouse':
    lighthouse_version = subprocess.run(["lighthouse", "-V"], stdout=subprocess.PIPE).stdout
    if lighthouse_version is not None:
        lighthouse_version = lighthouse_version.decode()
    else:
        lighthouse_version = ""
    print(f'Lighthouse Version: \n{lighthouse_version}')

if execution_client == 'besu':
    print(f'Besu Version: {besu_version}\n')
    
if execution_client == 'nethermind':
    print(f'Nethermind Version: \n{nethermind_version}\n')

if consensus_client == 'teku':
    print(f'Teku Version: {teku_version}\n')

if consensus_client == 'nimbus':
    nimbus_version = subprocess.run(["nimbus_beacon_node", "--version"], stdout=subprocess.PIPE).stdout
    if nimbus_version is not None:
        nimbus_version = nimbus_version.decode().splitlines()[0]
    else:
        nimbus_version = ""
    print(f'Nimbus Version: \n{nimbus_version}\n')

if consensus_client == 'prysm':
    prysm_version = subprocess.run(["beacon-chain", "--version"], stdout=subprocess.PIPE).stdout
    if prysm_version is not None:
        prysm_version = prysm_version.decode().splitlines()[0]
        prysm_version = prysm_version.split("/")[-2]
    else:
        prysm_version = ""
    print(f'Prysm Version: {prysm_version}\n')

print(f'Network: {eth_network_cap}')

if consensus_client in ['lighthouse', 'teku', 'prsym', 'nimbus']:
    print(f'CheckPointSyncURL: {sync_url}')

print(f'MEV Boost: {mev_on_off.upper()}')

print(f'Validator Fee Address: {fee_address}')

print("\nInstallation successful! See details above")

