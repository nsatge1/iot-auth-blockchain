# IoT Authentication via Ethereum Smart Contracts

Ce projet implémente un système d'authentification sécurisé pour les objets connectés (IoT) en utilisant des **smart contracts Ethereum**. Il combine :

- Des scripts **Python** pour les appareils et les opérations d'administration
- Un environnement local **Truffle + Ganache** pour tester les contrats intelligents
- Une communication entre Python et la blockchain Ethereum via **Web3.py**

---

## 🔧 Technologies utilisées

- [Python 3.10+](https://www.python.org/)
- [Web3.py](https://web3py.readthedocs.io/)
- [Truffle Suite](https://trufflesuite.com/)
- [Ganache CLI ou GUI](https://trufflesuite.com/ganache/)
- [Solidity](https://docs.soliditylang.org/)
- [Node.js](https://nodejs.org/) (nécessaire pour Truffle)

---

## 📁 Structure du projet


---

## 🚀 Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/nsatge1/iot-auth-blockchain.git
cd iot-auth-blockchain
```

### 2. Installer les dépendances Python

```bash
cd iot_simulation
pip install -r requirements.txt
```

### 3. Installer Truffle & Ganache (si ce n’est pas déjà fait)

```bash
npm install -g truffle
# Ganache GUI : https://trufflesuite.com/ganache/
# ou en CLI :
npm install -g ganache
cd truffle
npm install
```
---

## ⚙️ Utilisation

### 1. Démarrer Ganache (GUI ou en CLI)
```bash
ganache
```

### 2. Compiler et déployer le contrat
```bash
truffe compile
truffle migrate
```

### 3. Interagir avec le contrat via Python
```bash
cd iot_simulation
python admin_interface.py
python iot_device.py
python iot_device2.py
```
---
## ✅ Fonctionnalités principales
	•	Authentification des appareils via adresse Ethereum
	•	Enregistrement sécurisé via smart contract
	•	Communication Python ↔ Ethereum avec Web3.py
	•	Interface pour l'admin

---
## 🛡️ Sécurité
	•	Utilisation de clés privées Ethereum
	•	Smart contracts testés localement
	•	Données signées et vérifiables