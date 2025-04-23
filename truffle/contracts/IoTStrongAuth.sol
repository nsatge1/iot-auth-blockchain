// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract IoTStrongAuth {
    address public admin;
    mapping(address => bool) public registeredDevices;
    mapping(address => uint256) public nonces;

    event DeviceRegistered(address device);
    event DeviceRevoked(address device);
    event AuthSuccess(address indexed device, bool success);

    constructor() {
        admin = msg.sender;
    }

    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin can perform this action");
        _;
    }

    function registerDevice(address device) public onlyAdmin {
        registeredDevices[device] = true;
        emit DeviceRegistered(device);
    }

    function revokeDevice(address device) public onlyAdmin {
        registeredDevices[device] = false;
        emit DeviceRevoked(device);
    }

    function getMessageHash(address device, uint256 nonce) public pure returns (bytes32) {
        return keccak256(abi.encodePacked(device, nonce));
    }

    function getEthSignedMessageHash(bytes32 messageHash) public pure returns (bytes32) {
        return keccak256(
            abi.encodePacked("\x19Ethereum Signed Message:\n32", messageHash)
        );
    }

    function authenticate(bytes32 messageHash, uint8 v, bytes32 r, bytes32 s) public returns (bool) {
        bytes32 ethSignedMessageHash = getEthSignedMessageHash(messageHash);
        address signer = ecrecover(ethSignedMessageHash, v, r, s);
        bool success = (registeredDevices[signer] && messageHash == getMessageHash(signer, nonces[signer]));
        if (success) {
            nonces[signer]++;
        }
        emit AuthSuccess(signer, success);
        return success;
    }

    function isAuthenticated(bytes32 messageHash, uint8 v, bytes32 r, bytes32 s) public view returns (bool) {
        bytes32 ethSignedMessageHash = getEthSignedMessageHash(messageHash);
        address signer = ecrecover(ethSignedMessageHash, v, r, s);
        return (registeredDevices[signer] && messageHash == getMessageHash(signer, nonces[signer]));
    }

    function getNonce(address device) public view returns (uint256) {
        return nonces[device];
    }
}
