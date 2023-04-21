# Ethereum Validator - Automated Setup
Install and configure an Ethereum Validator in 1 minute with just 1 click, as opposed to hours normally spent on manual configuration.

# Summary
This Python script simplifies and automates the installation and configuration process of an Ethereum validator node.

It's based on [Somer Esat's - Lighthouse/Geth](https://someresat.medium.com/guide-to-staking-on-ethereum-ubuntu-lighthouse-773f5d982e03) guide and uses a single Python script to automate the setup process.

**Important Note:** This script does not generate any security-related items such as validator keystore, deposit data, or mnemonic. It prepares the computer for staking by installing the binaries, creating users, writing service files, etc.

After running the script, Geth and Ligthouse will be installed and fully configured to begin syncing.

If you want to run a full validator, you'll also need import an existing keysore or generate new keystores to run the validator. Please refer to [Somer's guide](https://someresat.medium.com/guide-to-staking-on-ethereum-ubuntu-lighthouse-773f5d982e03) or this [Ubuntu - Key Generation Guide](https://agstakingco.gitbook.io/eth-2-0-key-generation-ubuntu-live-usb/) to learn more.

# Validator Install Script
The `validator_install.py` script performs the following tasks:

1) Prompts user to select Ethereum network (mainnet / testnet).
2) Prompts user to set Ethereum address for validator tips (optional).
3) Prompts user to set Checkpoint Sync (optional).
4) Installs and configures Universal Firewall (ufw).
5) Creates necessary users, directories, and files.
6) Downloads and installs the latest Geth and Lighthouse binaries.
7) Sets up and writes service files for Geth, Lighthouse Beacon, and Lighthouse Validator.
8) Displays a summary of the installation.

**To run the script, use these commands:**

`sudo apt-get update`

`sudo pip install requests`

`sudo apt-get install git`

`git clone https://github.com/PyStakers/validator_install.git`

`python3 validator_install/validator_install.py`  

<br />  

**After successful installation, you can start the services:**

`sudo systemctl start geth`

`sudo systemctl start lighthousebeacon`

`sudo systemctl start lighthousevalidator`

<br />

**Then open 3 new terminals and view the journals:**

`sudo journalctl -fu geth.service`

`sudo journalctl -fu lighthousebeacon.service`

`sudo journalctl -fu lighthousevalidator.service`

\
The services should start, find peers, and eventually begin syncing. If you notice any errors (red/yellow), visit [EthStaker Discord](https://discord.com/invite/ucsTcA2wTq) for help.


You can stop the services by changing the "start" commands to "stop".


That's it, happpy staking! Feel free to contribute to the project if you'd like to add other clients!

\
**Disclaimer:** This script is for testing purposes only. Do not use on mainnet Validators.
