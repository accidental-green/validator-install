# Ethereum Validator Install
Install and configure an Ethereum Validator (mainnet/testnet) in a few clicks, as opposed to hours normally spent on manual configuration.

Includes support for multiple clients (geth, besu, nethermind, teku, nimbus, lighthouse, prysm). Based on Somer Esat's guides, and supports installing execution, concensus, and MEV clients, along with importing validator keystores.

After running the script, the node will be fully configured and ready to sync.

If you'd like to run a validator, you can import an existing keystore that was previously generataed elsewhere.

You can also follow Somer's guide to safely generate keys offline and manually import the keystores.

**To run the script, use these commands**:

`sudo apt-get update && sudo apt-get install git curl -y && sudo pip install requests`

`git clone https://github.com/accidental-green/validator-install.git`

`python3 validator-install/validator_install_gui.py`
<br>
<br>
## **Installation Setup:**
<br>

![Screenshot from 2023-08-18 18-38-20](https://github.com/accidental-green/validator-install/assets/72235883/b668d37d-6048-4f3a-be64-95591e4ade41)




## **Successful Installation:**
<br>

![image](https://github.com/accidental-green/validator-install/assets/72235883/3dd1fb52-e457-4cb8-ae81-0bca578da125)


Once installation is complete, you can start the clients and begin syncing/attesting!

NOTE: This is an open source project and has not been audited. Still in testing. Do not use with mainnet validators.
