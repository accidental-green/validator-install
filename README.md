# Ethereum Validator Install
Easily set up and configure an Ethereum Validator for mainnet or testnet within minutes using this installation script. The script is adapted from Somer Esat's guides, and simplifies a process that otherwise takes hours of manual configuration.

## Features:

- **Multi-client Support**: Works with various clients including Geth, Besu, Nethermind, Teku, Nimbus, Lighthouse, and Prysm.
- **Execution, Consensus, and MEV Clients**: Configure various Ethereum clients and MEV settings.
- **Import Validator Keystores**: Seamlessly import existing keystores to jump-start your validator setup.
- **Standard Configuration**: Get the same results as manually following Somer's guides (service files, users, directories, etc.)
- **GUI & CLI Versions**: Choose the version that suits your comfort level and setup.

## Prerequisites:

Execute the following commands to update your system, install packages, and clone the repo:

`sudo apt-get update && sudo apt-get install git curl -y && sudo pip install requests && sudo apt install python3-tk`

`git clone https://github.com/accidental-green/validator-install.git`

## Installation:
Note: Choose either GUI or CLI installation. Program starts upon running one of these commands:

**GUI Version:**

`python3 validator-install/validator_install_gui.py`

**or CLI Version:**

`python3 validator-install/validator_install_cli.py`

### Installation Steps (GUI):

![Screenshot from 2023-08-18 18-38-20](https://github.com/accidental-green/validator-install/assets/72235883/b668d37d-6048-4f3a-be64-95591e4ade41)


- Make selections and click "Install". The GUI window will close and installation will proceed in the terminal.
- If importing validator keys, you'll be prompted to enter the keystore password in the terminal.

### Successful Installation:

![image](https://github.com/accidental-green/validator-install/assets/72235883/3dd1fb52-e457-4cb8-ae81-0bca578da125)


After the installation, you can start the clients to commence syncing and attesting.

### Installation Steps (CLI):

If you prefer to run the CLI version, the installation will look like this:

![Screenshot from 2023-07-25 00-06-29](https://github.com/accidental-green/validator-install/assets/72235883/d407c718-c18e-41ad-ae67-a4c5baf03d4b)


## Important Note:

This project has not been audited. It is open source and still under testing, so currently not recommended to use on mainnet.

## Credits:

Many thanks to [Somer Esat](https://github.com/SomerEsat/ethereum-staking-guides) for creating the staking guides which served as the basis for this project.
