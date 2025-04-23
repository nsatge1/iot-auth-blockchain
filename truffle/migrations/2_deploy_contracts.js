const IoTStrongAuth = artifacts.require("IoTStrongAuth");

module.exports = function (deployer) {
  deployer.deploy(IoTStrongAuth);
};
