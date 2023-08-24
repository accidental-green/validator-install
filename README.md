# Ethereum Validator Install
Easily set up and configure an Ethereum Validator for mainnet or testnet within minutes using this installation script. The script is adapted fromn Somer Esat's guides, and simplifies a process that otherwise takes hours of manual configuration.

## Features:

- **Multi-client Support**: Works with various Ethereum clients including Geth, Besu, Nethermind, Teku, Nimbus, Lighthouse, and Prysm.
- **Execution, Consensus, and MEV Clients**: Provides the ability to install various Ethereum client types.
- **Import Validator Keystores**: Seamlessly import existing keystores to jump-start your validator setup.
- **Standard Configuration**: Whether you manually follow Somer's guides or use this installation script, the final configuration is identical.
- **GUI & CLI Versions**: Choose the version that suits your comfort level and setup.

## Prerequisites:

Execute the following commands to update your system, install packages, and clone the repo:

`sudo apt-get update && sudo apt-get install git curl -y && sudo pip install requests`

`git clone https://github.com/accidental-green/validator-install.git`

## Installation:
Note: Choose either GUI or CLI installation

**GUI Version:**

`python3 validator-install/validator_install_gui.py`

**or, CLI Version:**

`python3 validator-install/validator_install_cli.py`

### Installation Steps (GUI):

![Screenshot from 2023-08-18 18-38-20](https://github.com/accidental-green/validator-install/assets/72235883/b668d37d-6048-4f3a-be64-95591e4ade41)


- Make selections and click "Install". The GUI window will close and installation will proceed in the terminal.
- If importing validator keys, you'll be prompted to enter the keystore password in the terminal.

### Successful Installation:

![image](https://github.com/accidental-green/validator-install/assets/72235883/3dd1fb52-e457-4cb8-ae81-0bca578da125)


After the installation, you can start the clients to commence syncing and attesting.

## Important Note:

This project is open source and is still under testing. **It has not been audited**. We recommend not using it with mainnet validators until it has undergone further review.

## Credits:

Many thanks to [Somer Esat](https://github.com/SomerEsat/ethereum-staking-guides) for the insightful guides that served as the basis for this project.
