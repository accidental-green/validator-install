# Ethereum Validator - Automated Setup
Install and configure an Ethereum Validator (mainnet/testnet) in a few clicks, as opposed to hours normally spent on manual configuration.  

Now updated to include multiple clients (geth, besu, nethermind, teku, nimbus, lighthouse, prysm)


# Summary
Python script that simplifies and automates the installation and configuration of the Ethereum validator node.

It's based on [Somer Esat's - Lighthouse/Geth](https://someresat.medium.com/guide-to-staking-on-ethereum-ubuntu-lighthouse-773f5d982e03) guide and has been expanded to include multple execution and consensus engines with a single Python script to automate the setup process.

**Important Note:** This script does not generate any security-related items such as validator keystore, deposit data, or mnemonic. It simply prepares the node for staking by installing the binaries, creating users, writing service files, etc.

After running the script, your node will be installed and fully configured to begin syncing.

If you want to run a full validator, you'll also need to import an existing keystore or generate new keystores to run the validator. 

You can follow [Somer's guide](https://someresat.medium.com/guide-to-staking-on-ethereum-ubuntu-lighthouse-773f5d982e03) to safely generate keys offline and import the keystores. 

Key Generation Resources: [Waygu Key Generator](https://github.com/stake-house/wagyu-key-gen), [Ethereum Deposit CLI](https://github.com/ethereum/staking-deposit-cli), and [Ubuntu - Key Generation Guide](https://agstakingco.gitbook.io/eth-2-0-key-generation-ubuntu-live-usb/)

# Validator Install Script

**To run the script, use these commands:**

`sudo apt-get update`

`sudo apt-get install git`

`pip install requests`

`git clone https://github.com/accidental-green/validator-install.git`

`python3 validator-install/validator_install_multi.py`  

<br />  

**The final command will open the validator install menu:**

![Screenshot from 2023-05-14 22-21-14](https://github.com/accidental-green/validator-install/assets/72235883/ee1e9d42-47c7-48c1-bde7-26de6e587037)

Once you make the selections and click "Install" it will perform the following tasks:

1) Download and Install Execution Client (Nethermind, Besu, Geth)
2) Download and Install Consensus Client (Nimbus, Teku, Lighthouse, Prysm)
3) Turn on/off MEV Boost (optional)
4) Set your Ethereum address for validator tips (optional).
5) Install and configure Universal Firewall (ufw).
6) Create necessary users, directories, and files.
7) Writes and saves service files for Execution, Beacon, and Validator.
8) Displays a controller for easy 1 click validator controls


**After successful installation, the validator controller will pop up**

![Screenshot from 2023-05-14 22-07-23](https://github.com/accidental-green/validator-install/assets/72235883/0911a061-6e8e-40af-afd1-8072e89b51a9)


\
It's best to open the journals before starting the services, so you can see everything start up together.

The "Journals" button will open a new window for each relavent services (execution, beacon, validator, MEV). The journalctl command requires admin privileges, so you will need to enter your password in each new pop-up terminal window.

Once the journals are ready, click "Start Validators".

**Once the journals are opened and services started, it should look something like this:**

![Screenshot from 2023-05-14 23-57-29](https://github.com/accidental-green/validator-install/assets/72235883/cf12f61d-5dd7-4758-b127-2e1536c0dedb)




The services should start, find peers, and eventually begin syncing. If you notice any errors (red/yellow), visit [EthStaker Discord](https://discord.com/invite/ucsTcA2wTq) for help.

\
**Disclaimer:** This script is for testing purposes only. Do not use on mainnet Validators.
