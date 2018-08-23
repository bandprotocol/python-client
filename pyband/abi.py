abi = {
    "Account": {
        "constructor_params": [
            "Hash"
        ],
        "delegate_call": {
            "opcode": 1,
            "params": [
                "Buffer"
            ],
            "result": "Buffer",
            "type": "action"
        },
        "get_nonce": {
            "opcode": 2,
            "params": [],
            "result": "uint256_t",
            "type": "query"
        },
        "id": 1
    },
    "Creator": {
        "create": {
            "opcode": 1,
            "params": [
                "Buffer"
            ],
            "result": "Address",
            "type": "action"
        },
        "id": 0
    },
    "Governance": {
        "constructor_params": [
            "Address",
            "Address",
            "uint8_t",
            "uint8_t",
            "uint256_t",
            "uint64_t",
            "uint64_t"
        ],
        "id": 6,
        "propose_new_parameter": {
            "opcode": 1,
            "params": [
                "Address",
                "Buffer"
            ],
            "result": "uint256_t",
            "type": "action"
        },
        "resolve_proposal": {
            "opcode": 2,
            "params": [
                "uint256_t"
            ],
            "result": "void",
            "type": "action"
        }
    },
    "Registry": {
        "active_list_id_at": {
            "opcode": 10,
            "params": [
                "uint256_t"
            ],
            "result": "uint256_t",
            "type": "query"
        },
        "active_list_length": {
            "opcode": 9,
            "params": [],
            "result": "uint256_t",
            "type": "query"
        },
        "apply": {
            "opcode": 1,
            "params": [
                "String",
                "uint256_t"
            ],
            "result": "uint256_t",
            "type": "action"
        },
        "challenge": {
            "opcode": 5,
            "params": [
                "uint256_t",
                "String"
            ],
            "result": "uint256_t",
            "type": "action"
        },
        "claim_reward": {
            "opcode": 7,
            "params": [
                "uint256_t",
                "uint256_t"
            ],
            "result": "void",
            "type": "action"
        },
        "constructor_params": [
            "Address",
            "Address",
            "Address",
            "uint8_t",
            "uint8_t",
            "uint256_t",
            "uint64_t",
            "uint64_t",
            "uint64_t"
        ],
        "deposit": {
            "opcode": 2,
            "params": [
                "uint256_t",
                "uint256_t"
            ],
            "result": "void",
            "type": "action"
        },
        "exit": {
            "opcode": 4,
            "params": [
                "uint256_t"
            ],
            "result": "void",
            "type": "action"
        },
        "get_active_challenge": {
            "opcode": 13,
            "params": [
                "uint256_t"
            ],
            "result": "uint256_t",
            "type": "query"
        },
        "get_app_expire": {
            "opcode": 17,
            "params": [
                "uint256_t"
            ],
            "result": "uint64_t",
            "type": "query"
        },
        "get_challenger_id": {
            "opcode": 19,
            "params": [
                "uint256_t"
            ],
            "result": "Address",
            "type": "query"
        },
        "get_content": {
            "opcode": 11,
            "params": [
                "uint256_t"
            ],
            "result": "String",
            "type": "query"
        },
        "get_deposit": {
            "opcode": 12,
            "params": [
                "uint256_t"
            ],
            "result": "uint256_t",
            "type": "query"
        },
        "get_list_owner": {
            "opcode": 18,
            "params": [
                "uint256_t"
            ],
            "result": "Address",
            "type": "query"
        },
        "get_poll_id": {
            "opcode": 15,
            "params": [
                "uint256_t"
            ],
            "result": "uint256_t",
            "type": "query"
        },
        "get_reason": {
            "opcode": 20,
            "params": [
                "uint256_t"
            ],
            "result": "String",
            "type": "query"
        },
        "get_voting_id": {
            "opcode": 8,
            "params": [],
            "result": "Address",
            "type": "query"
        },
        "id": 4,
        "is_proposal": {
            "opcode": 16,
            "params": [
                "uint256_t"
            ],
            "result": "bool",
            "type": "query"
        },
        "need_update": {
            "opcode": 14,
            "params": [
                "uint256_t"
            ],
            "result": "bool",
            "type": "query"
        },
        "update_status": {
            "opcode": 6,
            "params": [
                "uint256_t"
            ],
            "result": "void",
            "type": "action"
        },
        "withdraw": {
            "opcode": 3,
            "params": [
                "uint256_t",
                "uint256_t"
            ],
            "result": "void",
            "type": "action"
        }
    },
    "Stake": {
        "claim_reward": {
            "opcode": 4,
            "params": [
                "uint256_t"
            ],
            "result": "void",
            "type": "action"
        },
        "constructor_params": [
            "Address",
            "Address"
        ],
        "create_party": {
            "opcode": 3,
            "params": [
                "uint256_t",
                "uint256_t",
                "uint256_t"
            ],
            "result": "uint256_t",
            "type": "action"
        },
        "id": 5,
        "reactivate_party": {
            "opcode": 5,
            "params": [
                "uint256_t"
            ],
            "result": "void",
            "type": "action"
        },
        "stake": {
            "opcode": 1,
            "params": [
                "uint256_t",
                "uint256_t"
            ],
            "result": "uint256_t",
            "type": "action"
        },
        "withdraw": {
            "opcode": 2,
            "params": [
                "uint256_t"
            ],
            "result": "void",
            "type": "action"
        }
    },
    "Token": {
        "balance": {
            "opcode": 5,
            "params": [
                "Address"
            ],
            "result": "uint256_t",
            "type": "query"
        },
        "bulk_price": {
            "opcode": 7,
            "params": [
                "uint256_t"
            ],
            "result": "uint256_t",
            "type": "query"
        },
        "buy": {
            "opcode": 3,
            "params": [
                "uint256_t"
            ],
            "result": "void",
            "type": "action"
        },
        "constructor_params": [
            "Address",
            "Buffer"
        ],
        "id": 2,
        "mint": {
            "opcode": 1,
            "params": [
                "uint256_t"
            ],
            "result": "void",
            "type": "action"
        },
        "sell": {
            "opcode": 4,
            "params": [
                "uint256_t"
            ],
            "result": "void",
            "type": "action"
        },
        "spot_price": {
            "opcode": 6,
            "params": [],
            "result": "uint256_t",
            "type": "query"
        },
        "transfer": {
            "opcode": 2,
            "params": [
                "Address",
                "uint256_t"
            ],
            "result": "void",
            "type": "action"
        }
    },
    "Voting": {
        "commit_vote": {
            "opcode": 4,
            "params": [
                "uint256_t",
                "Hash",
                "uint256_t"
            ],
            "result": "void",
            "type": "action"
        },
        "constructor_params": [
            "Address"
        ],
        "get_commit_end_time": {
            "opcode": 10,
            "params": [
                "uint256_t"
            ],
            "result": "uint64_t",
            "type": "query"
        },
        "get_period": {
            "opcode": 8,
            "params": [
                "uint256_t"
            ],
            "result": "uint8_t",
            "type": "query"
        },
        "get_result": {
            "opcode": 9,
            "params": [
                "uint256_t"
            ],
            "result": "uint8_t",
            "type": "query"
        },
        "get_reveal_end_time": {
            "opcode": 11,
            "params": [
                "uint256_t"
            ],
            "result": "uint64_t",
            "type": "query"
        },
        "get_vote_against": {
            "opcode": 7,
            "params": [
                "uint256_t"
            ],
            "result": "uint256_t",
            "type": "query"
        },
        "get_vote_for": {
            "opcode": 6,
            "params": [
                "uint256_t"
            ],
            "result": "uint256_t",
            "type": "query"
        },
        "get_voting_power": {
            "opcode": 12,
            "params": [
                "Address"
            ],
            "result": "uint256_t",
            "type": "query"
        },
        "id": 3,
        "request_voting_power": {
            "opcode": 1,
            "params": [
                "uint256_t"
            ],
            "result": "void",
            "type": "action"
        },
        "rescue_token": {
            "opcode": 3,
            "params": [
                "uint256_t"
            ],
            "result": "void",
            "type": "action"
        },
        "reveal_vote": {
            "opcode": 5,
            "params": [
                "uint256_t",
                "bool",
                "uint256_t"
            ],
            "result": "void",
            "type": "action"
        },
        "withdraw_voting_power": {
            "opcode": 2,
            "params": [
                "uint256_t"
            ],
            "result": "void",
            "type": "action"
        }
    }
}
