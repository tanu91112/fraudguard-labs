
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract FraudLog {
    event FraudLogged(
        string transactionId,
        uint256 riskScore,
        uint256 timestamp
    );

    function logFraud(
        string memory transactionId,
        uint256 riskScore
    ) public {
        emit FraudLogged(transactionId, riskScore, block.timestamp);
    }
}
