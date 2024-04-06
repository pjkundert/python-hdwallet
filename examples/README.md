
# v3+ Command Line Interface (CLI)

## Generate Command

### Entropy

Generate entropy from strength number
```
hdwallet generate entropy --name BIP39 --strength 160
```
alias
```
hdwallet g e -n BIP39 -s 160
```

<details open>
  <summary>Output</summary><br/>

```json5
{
    "name": "BIP39",
    "entropy": "10ad31cfb2860b312f0911fc9de22d836ca3eb14",
    "strength": 160
}
```
</details>


### Mnemoinic

Generate mnemonic from words number
```
hdwallet generate mnemonic --name BIP39 --words 15 --language russian
```
alias
```
hdwallet g m -n BIP39 -w 15 -l russian
```

<details open>
  <summary>Output</summary><br/>

```json5
{
    "name": "BIP39",
    "mnemonic": "шкура практика овраг замок реклама мирный факт пятьсот намерен свитер паутина спальня жуткий вальс спешить",
    "language": "Russian",
    "words": 15
}
```
</details>

Generate mnemonic from entropy hex string
```
hdwallet generate mnemonic --name BIP39 --entropy 10ad31cfb2860b312f0911fc9de22d836ca3eb14 --language english
```
alias
```
hdwallet g m -n BIP39 -e 10ad31cfb2860b312f0911fc9de22d836ca3eb14 -l english
```

<details open>
  <summary>Output</summary><br/>

```json5
{
    "name": "BIP39",
    "mnemonic": "awful hat initial govern gaze obtain rotate captain wish upper merge almost sketch void face",
    "language": "English",
    "words": 15
}
```
</details>

### Seed

Generate seed from mnemonic words
```
hdwallet generate seed --name BIP39 --passphrase meherett --mnemonic "awful hat initial govern gaze obtain rotate captain wish upper merge almost sketch void face"
```
alias
```
hdwallet g s -n BIP39 -p meherett -m "awful hat initial govern gaze obtain rotate captain wish upper merge almost sketch void face"
```

<details open>
  <summary>Output</summary><br/>

```json5
{
    "name": "BIP39",
    "seed": "e7bc9f2abb0827137b408c10d9942066a1f2f356d1cda46f6c0dd5fbc2f7c996328100e580adc26ac614de68644bec61e885afd03dc74eade545fd53b1312cdb"
}
```
</details>

## Dump Command

### BIP32 Hierarchical Deterministic (HD) 

```
hdwallet dump --symbol BTC --hd BIP32 --entropy 10ad31cfb2860b312f0911fc9de22d836ca3eb14 --path "m/524'/489'"
```
alias
```
hdwallet d -s BTC -h BIP32 -e 10ad31cfb2860b312f0911fc9de22d836ca3eb14 -p "m/524'/489'"
```

<details>
  <summary>Output</summary><br/>

```json5
{
    "cryptocurrency": "Bitcoin",
    "symbol": "BTC",
    "network": "mainnet",
    "coin_type": 0,
    "entropy": "10ad31cfb2860b312f0911fc9de22d836ca3eb14",
    "strength": 160,
    "mnemonic": "awful hat initial govern gaze obtain rotate captain wish upper merge almost sketch void face",
    "passphrase": null,
    "language": "English",
    "seed": "480e2d3d35c1e41c32ee2e480705e16e5b95ade415831a2aff4db7b3b9a0f5b1257cc63c251b602d50fc88830050b893ab2eb2ef650accb1b9410567e6ba838d",
    "ecc": "SLIP10-Secp256k1",
    "hd": "BIP32",
    "root_xprivate_key": "xprv9s21ZrQH143K3q1UgUwmqf71gy5GQXjSg71YCHK1hFcZZXbnPNne5QKfybnKw9zUAB9cEAA5KSeHVVB9BfbgT3Nv1Kr2BVropBWtU5y6obs",
    "root_xpublic_key": "xpub661MyMwAqRbcGK5wnWUnCo3kEzukozTJ3Kw8zfidFb9YSKvvvv6tdCe9pthSrH6E7t5uDCBL94hjeMBtGo6oU99vTh5arnUXBGTmxhf7qs6",
    "root_private_key": "b3792687bea479018f971a287fc489e19041e63aa353b5c8997e8a501da00734",
    "root_wif": "L3Eans1Cre2zLMx9Nz2mtbqYKjTq5aD1JvcgjSamFf1BM4PW4y7Q",
    "root_chain_code": "b1c4808dc0d6c008978ebb0b727f74b7ba0a9cf91aa9585930aad68b23f5aad1",
    "root_public_key": "03abc5c947c486430ff88b039781f99b9542f2baf523685b23abbe77385c4b0628",
    "strict": true,
    "public_key_type": "compressed",
    "wif_type": "wif-compressed",
    "derivation": {
        "at": {
            "path": "m/524'/489'",
            "indexes": [
                2147484172,
                2147484137
            ],
            "depth": 2,
            "index": 2147484137
        },
        "xprivate_key": "xprv9wCoQbJHg43tVRT5TgD4nJ4au6SivuUxHRS5JufFqWzczt3bQv1RiYXjDkj23nE61DsZ5TXAWSWjodHmY88ELskPU7dx8Cn2HBxG7AKjJpU",
        "xpublic_key": "xpub6AC9p6qBWRcBhuXYZhk59S1KT8HDLNCoeeMg7J4sPrXbsgNjxTKgGLrD54cDQr7UvUiVV2xotgBeaUt2xC9rLEkHCvYn41paSTGLtgWzjb5",
        "private_key": "42d77adad487f5299dc5844e8387f87b13a3ceb26364dc57d4f83afbdbece495",
        "wif": "KyTeDSq9c59iwNvbLY6gYgxYEikQbcvvNX8CeM75NiMLQmu9SC8m",
        "chain_code": "2baaaecb40760f0db829fa2c4732644a478203419cb0d0825b573f4193533a65",
        "public_key": "03ba785426897b478ffdab95558fa9647acfe5ae62eece5a69166334ca0570ac04",
        "uncompressed": "04ba785426897b478ffdab95558fa9647acfe5ae62eece5a69166334ca0570ac04bb6b71697828f7ea5a06b34cb84177038b3ff964b82df6004f243e2ad0025f89",
        "compressed": "03ba785426897b478ffdab95558fa9647acfe5ae62eece5a69166334ca0570ac04",
        "hash": "70c0cba06fc101eec24ef59353258f4953d31826",
        "fingerprint": "70c0cba0",
        "parent_fingerprint": "3983ea20",
        "addresses": {
            "p2pkh": "1BHBe9SA5GEhfTYmmgBQwiij1LuqHeb1du",
            "p2sh": "35JtxbpwcMTT7ygAvyx7y9ybzm5ZbYFggQ",
            "p2tr": "bc1pv0rc9z7yrvtpn0nmramv8jsjlq0g2xm5lj4cmv6h29ekdl7mdteqdhplyu",
            "p2wpkh": "bc1qwrqvhgr0cyq7asjw7kf4xfv0f9faxxpxdps3za",
            "p2wpkh-in-p2sh": "3QuxL19SX1PvYVEvBgFUYjBLp66n831JDy",
            "p2wsh": "bc1qtpa3qxwwvuummcjwwarlwa7et7jj6g53hs9vpd2kajpfsy8m06ysgzym3z",
            "p2wsh-in-p2sh": "3N6XWYabbLVrDjCANxf3bYM8g43PdSLA5E"
        }
    }
}
```
</details>

### BIP44 Hierarchical Deterministic (HD) 

```
hdwallet dump --symbol ALGO --hd BIP44 --derivation BIP44 --entropy 10ad31cfb2860b312f0911fc9de22d836ca3eb14 --account 1
```
alias
```
hdwallet d -s ALGO -h BIP44 -d BIP44 -e 10ad31cfb2860b312f0911fc9de22d836ca3eb14 -ac 1
```

<details>
  <summary>Output</summary><br/>

```json5
{
    "cryptocurrency": "Algorand",
    "symbol": "ALGO",
    "network": "mainnet",
    "coin_type": 283,
    "entropy": "10ad31cfb2860b312f0911fc9de22d836ca3eb14",
    "strength": 160,
    "mnemonic": "awful hat initial govern gaze obtain rotate captain wish upper merge almost sketch void face",
    "passphrase": null,
    "language": "English",
    "seed": "480e2d3d35c1e41c32ee2e480705e16e5b95ade415831a2aff4db7b3b9a0f5b1257cc63c251b602d50fc88830050b893ab2eb2ef650accb1b9410567e6ba838d",
    "ecc": "SLIP10-Ed25519",
    "hd": "BIP44",
    "root_xprivate_key": "xprv9s21ZrQH143K2ToS32WUpnH2nrCiRTm8M9Jx9dfMapx3fvDXJFvnHHKbcvY6M5KwLZE4rtDrZT8AqYCefHJNdovFyJ2pKhLJvuKnUmu3fiV",
    "root_xpublic_key": "xpub661MyMwAqRbcEwsu943VBvDmLt3CpvUyiNEYx24y9AV2YiYfqoF2q5e5U7REZQ5qLTVfRSL8hNDRa2q3j3oGA9cvTEs53JU2E1uH7UVuYLa",
    "root_private_key": "c4556dd571269b90010520ae06f60b57c44bddf01e0a82051e3ac04148fad8f3",
    "root_wif": "L3oMiQSQGuhkjCduZbQNLpbFVoE7sjBe34dKwtnutm5H6ECXNYTm",
    "root_chain_code": "2899790d6f0501b23d28e4711b9c88a7d1da7210257d93ef0ce5f8cdcad77643",
    "root_public_key": "00a1f74c4b857023038499b4d3d4fcc7c1c0756c3a6114664f11a04e73c369c130",
    "strict": true,
    "public_key_type": "compressed",
    "wif_type": "wif-compressed",
    "derivation": {
        "at": {
            "path": "m/44'/283'/1'/0/0",
            "indexes": [
                2147483692,
                2147483931,
                2147483649,
                0,
                0
            ],
            "depth": 5,
            "purpose": 44,
            "coin_type": 283,
            "account": 1,
            "change": "external-chain",
            "address": 0
        },
        "xprivate_key": "xprvA3TF81pZrbzz3mkCfiqdr3sgoukopx9gZ23SqknNCcLKZrhfiapahNNHZptJmPnrbcEC2qWRBjSryANF2eLsrrnaQEsXvBhiudEfi6krvH7",
        "xpublic_key": "xpub6GSbXXMTgyZHGFpfmkNeDBpRMwbJEQsXvEy3e9BykwsJSf2pG88qFAgmR2Ka1vRjnXniuw5C7MBgAuyw9EaLtwrF89wrCkCPr5AvMYoigLv",
        "private_key": "1cb6a834f04514fc4a383006e0a0f2162c5583e6633fd516ce5480175786456d",
        "wif": "KxBXUKvNu1hZuXUaTYbpuQHdWxBZMwq8nHvpF8kb7jCQ4ChT1uKp",
        "chain_code": "657428446ca43863a75c9d3e010277dca90da070395322ab22789119e2f4420f",
        "public_key": "004347ffe458c1172552450093b7aae21143b852d2e10c3ddb424b8d201e32f4ee",
        "uncompressed": "004347ffe458c1172552450093b7aae21143b852d2e10c3ddb424b8d201e32f4ee",
        "compressed": "004347ffe458c1172552450093b7aae21143b852d2e10c3ddb424b8d201e32f4ee",
        "hash": "7ed941734af30a7df90c6e3d2c6db3db55d98d23",
        "fingerprint": "7ed94173",
        "parent_fingerprint": "8bb39b38",
        "address": "IND77ZCYYELSKUSFACJ3PKXCCFB3QUWS4EGD3W2CJOGSAHRS6TXAUFAZ4I"
    }
}
```
</details>

### BIP49 Hierarchical Deterministic (HD) 

```
hdwallet dump --symbol BTC --hd BIP49 --derivation BIP49 --entropy 10ad31cfb2860b312f0911fc9de22d836ca3eb14 --address 5
```
alias
```
hdwallet d -s BTC -h BIP49 -d BIP49 -e 10ad31cfb2860b312f0911fc9de22d836ca3eb14 -ad 5
```

<details>
  <summary>Output</summary><br/>

```json5
{
    "cryptocurrency": "Bitcoin",
    "symbol": "BTC",
    "network": "mainnet",
    "coin_type": 0,
    "entropy": "10ad31cfb2860b312f0911fc9de22d836ca3eb14",
    "strength": 160,
    "mnemonic": "awful hat initial govern gaze obtain rotate captain wish upper merge almost sketch void face",
    "passphrase": null,
    "language": "English",
    "seed": "480e2d3d35c1e41c32ee2e480705e16e5b95ade415831a2aff4db7b3b9a0f5b1257cc63c251b602d50fc88830050b893ab2eb2ef650accb1b9410567e6ba838d",
    "ecc": "SLIP10-Secp256k1",
    "hd": "BIP49",
    "root_xprivate_key": "xprv9s21ZrQH143K3q1UgUwmqf71gy5GQXjSg71YCHK1hFcZZXbnPNne5QKfybnKw9zUAB9cEAA5KSeHVVB9BfbgT3Nv1Kr2BVropBWtU5y6obs",
    "root_xpublic_key": "xpub661MyMwAqRbcGK5wnWUnCo3kEzukozTJ3Kw8zfidFb9YSKvvvv6tdCe9pthSrH6E7t5uDCBL94hjeMBtGo6oU99vTh5arnUXBGTmxhf7qs6",
    "root_private_key": "b3792687bea479018f971a287fc489e19041e63aa353b5c8997e8a501da00734",
    "root_wif": "L3Eans1Cre2zLMx9Nz2mtbqYKjTq5aD1JvcgjSamFf1BM4PW4y7Q",
    "root_chain_code": "b1c4808dc0d6c008978ebb0b727f74b7ba0a9cf91aa9585930aad68b23f5aad1",
    "root_public_key": "03abc5c947c486430ff88b039781f99b9542f2baf523685b23abbe77385c4b0628",
    "strict": true,
    "public_key_type": "compressed",
    "wif_type": "wif-compressed",
    "derivation": {
        "at": {
            "path": "m/49'/0'/0'/0/5",
            "indexes": [
                2147483697,
                2147483648,
                2147483648,
                0,
                5
            ],
            "depth": 5,
            "purpose": 49,
            "coin_type": 0,
            "account": 0,
            "change": "external-chain",
            "address": 5
        },
        "xprivate_key": "xprvA3v1pJtMW1fKFNjLH4adw4Bj9Fjr7MV9LHRDYB9aFMrXEXuCjYuEGYxFNgToV24xBpxD7GaTjvuPqsWBb6icYNtiRee8hDyphfm2NcwhXRK",
        "xpublic_key": "xpub6GuNDpRFLPDcTrooP67eJC8ThHaLWpCzhWLpLZZBohPW7LEMH6DUpMGjDwyLb8S5GHCHFzotGGKPHzZ3e2Wzzx84tMmqyJcNzr1GgEsNkSk",
        "private_key": "efaf592d91cdd78316f7c7179bb57a78566df9e1456ec3a97ee2f1ef84578fea",
        "wif": "L5FdKrmFcZd3ExxkyT6wgYBvRoW2BuVFRNSH6ydrK4nYB46DQSbR",
        "chain_code": "aae5e8ef8b79624e677b60367e0a59cb2003a462ef6382713dfb20ba113281ef",
        "public_key": "032ebd820c10725442f7a56bad6a3e7283d294e3b469f0eaa386d482cf23f1221c",
        "uncompressed": "042ebd820c10725442f7a56bad6a3e7283d294e3b469f0eaa386d482cf23f1221c6eb413ea37cf2404349b3bf95ff7083e696bdb9010aea2c92a5c8a39a8764321",
        "compressed": "032ebd820c10725442f7a56bad6a3e7283d294e3b469f0eaa386d482cf23f1221c",
        "hash": "bb7c969462c9f5eb2bde3520e0344463f616c745",
        "fingerprint": "bb7c9694",
        "parent_fingerprint": "ca7f628c",
        "address": "3EtEvuKcPG9iXpG5rDVVgsACLz2uu7b2XX"
    }
}
```
</details>

### BIP84 Hierarchical Deterministic (HD) 

```
hdwallet dump --symbol BTC --hd BIP84 --derivation BIP84 --entropy 10ad31cfb2860b312f0911fc9de22d836ca3eb14 --address 10
```
alias
```
hdwallet d -s BTC -h BIP84 -d BIP84 -e 10ad31cfb2860b312f0911fc9de22d836ca3eb14 -ad 10
```

<details>
  <summary>Output</summary><br/>

```json5
{
    "cryptocurrency": "Bitcoin",
    "symbol": "BTC",
    "network": "mainnet",
    "coin_type": 0,
    "entropy": "10ad31cfb2860b312f0911fc9de22d836ca3eb14",
    "strength": 160,
    "mnemonic": "awful hat initial govern gaze obtain rotate captain wish upper merge almost sketch void face",
    "passphrase": null,
    "language": "English",
    "seed": "480e2d3d35c1e41c32ee2e480705e16e5b95ade415831a2aff4db7b3b9a0f5b1257cc63c251b602d50fc88830050b893ab2eb2ef650accb1b9410567e6ba838d",
    "ecc": "SLIP10-Secp256k1",
    "hd": "BIP84",
    "root_xprivate_key": "xprv9s21ZrQH143K3q1UgUwmqf71gy5GQXjSg71YCHK1hFcZZXbnPNne5QKfybnKw9zUAB9cEAA5KSeHVVB9BfbgT3Nv1Kr2BVropBWtU5y6obs",
    "root_xpublic_key": "xpub661MyMwAqRbcGK5wnWUnCo3kEzukozTJ3Kw8zfidFb9YSKvvvv6tdCe9pthSrH6E7t5uDCBL94hjeMBtGo6oU99vTh5arnUXBGTmxhf7qs6",
    "root_private_key": "b3792687bea479018f971a287fc489e19041e63aa353b5c8997e8a501da00734",
    "root_wif": "L3Eans1Cre2zLMx9Nz2mtbqYKjTq5aD1JvcgjSamFf1BM4PW4y7Q",
    "root_chain_code": "b1c4808dc0d6c008978ebb0b727f74b7ba0a9cf91aa9585930aad68b23f5aad1",
    "root_public_key": "03abc5c947c486430ff88b039781f99b9542f2baf523685b23abbe77385c4b0628",
    "strict": true,
    "public_key_type": "compressed",
    "wif_type": "wif-compressed",
    "derivation": {
        "at": {
            "path": "m/84'/0'/0'/0/10",
            "indexes": [
                2147483732,
                2147483648,
                2147483648,
                0,
                10
            ],
            "depth": 5,
            "purpose": 84,
            "coin_type": 0,
            "account": 0,
            "change": "external-chain",
            "address": 10
        },
        "xprivate_key": "xprvA4BNue7AKTZMkwKMqWRinYRDJRFvNUxxVMEPCu2Wy9h2K6PcexEiDwVM2EAPDGYtgSxCxUvfagzQHMSJBpY1DuzxjMahSbEvsTAPZeJV8bh",
        "xpublic_key": "xpub6HAjK9e49q7eyRPpwXxj9gMwrT6Qmwgora9z1HS8XVE1BtimCVYxmjopsWCpZYV8VHYhQx8kLJX3TxE6TkdRcrMwUwzQna4gv8kF6na7qYK",
        "private_key": "debd3d26d793d97ae3d483358d936e682ed66843e9d67ff33cddf632a000f471",
        "wif": "L4ggng5Sdgw7nAYTNrCb6sVmTtg3i4nd7BmW3QbJnfydshPxQX7X",
        "chain_code": "bdca23c16591657b4acdc6bd9adb2f49773215485bbdfb76fd0aeb42acaf45b6",
        "public_key": "0363f55f657611e5ff5ea61971ed1f2412d6b97f201ed692b020686666c15f196d",
        "uncompressed": "0463f55f657611e5ff5ea61971ed1f2412d6b97f201ed692b020686666c15f196d1cb33f7c8e213c9f3552c3c90423208fcdc9d7cc6dcf6468632874bf478fd885",
        "compressed": "0363f55f657611e5ff5ea61971ed1f2412d6b97f201ed692b020686666c15f196d",
        "hash": "9a118f52d622fe83551ab255c1e71ffc93ee68a8",
        "fingerprint": "9a118f52",
        "parent_fingerprint": "ee894753",
        "address": "bc1qnggc75kkytlgx4g6kf2ureclljf7u69g9c8w6x"
    }
}
```
</details>

### BIP86 Hierarchical Deterministic (HD) 

```
hdwallet dump --symbol BTC --hd BIP86 --derivation BIP86 --entropy 10ad31cfb2860b312f0911fc9de22d836ca3eb14
```
alias
```
hdwallet d -s BTC -h BIP86 -d BIP86 -e 10ad31cfb2860b312f0911fc9de22d836ca3eb14
```

<details>
  <summary>Output</summary><br/>

```json5
{
    "cryptocurrency": "Bitcoin",
    "symbol": "BTC",
    "network": "mainnet",
    "coin_type": 0,
    "entropy": "10ad31cfb2860b312f0911fc9de22d836ca3eb14",
    "strength": 160,
    "mnemonic": "awful hat initial govern gaze obtain rotate captain wish upper merge almost sketch void face",
    "passphrase": null,
    "language": "English",
    "seed": "480e2d3d35c1e41c32ee2e480705e16e5b95ade415831a2aff4db7b3b9a0f5b1257cc63c251b602d50fc88830050b893ab2eb2ef650accb1b9410567e6ba838d",
    "ecc": "SLIP10-Secp256k1",
    "hd": "BIP86",
    "derivation": {
        "at": {
            "path": "m/86'/0'/0'/0/0",
            "indexes": [
                2147483734,
                2147483648,
                2147483648,
                0,
                0
            ],
            "depth": 5,
            "purpose": 86,
            "coin_type": 0,
            "account": 0,
            "change": "external-chain",
            "address": 0
        },
        "xprivate_key": "xprvA3tdSqtrZ8Ab5uE5aTKoeiTrxkWgisun6rUcTwQp2rCbz7JDnF4E1XQdGifC4Ca5H3UWHnyhB2UbgMZf8KiaKihhN9NYuXcY6wCEyJcsMcH",
        "xpublic_key": "xpub6GsyrMRkPVitJPJYgUrp1rQbWnMB8LddU5QDGKpRbBjarudNKnNUZKj782DsdkCeLLiuGFxqBPJC2WE1A8JiqMBzgACt39RH1pXUJWDHfXE",
        "private_key": "9a18a1a101d59e8a03ae4120c0a81cd76d7f6b887bd53b0d0a9aaba535d5679b",
        "wif": "L2PFfzzLKpGyFeZQNk5exqv7Ztksbmjx5YWFdi5Ahk3hMmapzkxr",
        "chain_code": "ad2ae13223b269faa289f8ab94ab8441144f3db906535a4925efafc2bd5b2b13",
        "public_key": "03e7aff26a3a4ad9bf450a47857f7510fe388f56e82c020333ebfc5aadbc0b25df",
        "uncompressed": "04e7aff26a3a4ad9bf450a47857f7510fe388f56e82c020333ebfc5aadbc0b25df61c410657c92c2ad671c48efe6a61a50c5e4c587c48088991df577227a3580fb",
        "compressed": "03e7aff26a3a4ad9bf450a47857f7510fe388f56e82c020333ebfc5aadbc0b25df",
        "hash": "39f8ababe043dbda2e7f79bfc0ea5d11c0803345",
        "fingerprint": "39f8abab",
        "parent_fingerprint": "c73f468d",
        "address": "bc1py346t60yuw0t6kvvkuwlearmh6uz2tyahlke9jquq5k6uz9e0jys8gvjry"
    }
}
```
</details>

### BIP141 Hierarchical Deterministic (HD) 

```
hdwallet dump --symbol BTC --hd BIP141 --path "m/0'/0" --entropy 10ad31cfb2860b312f0911fc9de22d836ca3eb14
```
alias
```
hdwallet d -s BTC -h BIP141 -p "m/0'/0" -e 10ad31cfb2860b312f0911fc9de22d836ca3eb14
```

<details>
  <summary>Output</summary><br/>

```json5
{
    "cryptocurrency": "Bitcoin",
    "symbol": "BTC",
    "network": "mainnet",
    "coin_type": 0,
    "entropy": "10ad31cfb2860b312f0911fc9de22d836ca3eb14",
    "strength": 160,
    "mnemonic": "awful hat initial govern gaze obtain rotate captain wish upper merge almost sketch void face",
    "passphrase": null,
    "language": "English",
    "seed": "480e2d3d35c1e41c32ee2e480705e16e5b95ade415831a2aff4db7b3b9a0f5b1257cc63c251b602d50fc88830050b893ab2eb2ef650accb1b9410567e6ba838d",
    "ecc": "SLIP10-Secp256k1",
    "hd": "BIP141",
    "semantic": "P2WPKH",
    "root_xprivate_key": "xprv9s21ZrQH143K3q1UgUwmqf71gy5GQXjSg71YCHK1hFcZZXbnPNne5QKfybnKw9zUAB9cEAA5KSeHVVB9BfbgT3Nv1Kr2BVropBWtU5y6obs",
    "root_xpublic_key": "xpub661MyMwAqRbcGK5wnWUnCo3kEzukozTJ3Kw8zfidFb9YSKvvvv6tdCe9pthSrH6E7t5uDCBL94hjeMBtGo6oU99vTh5arnUXBGTmxhf7qs6",
    "root_private_key": "b3792687bea479018f971a287fc489e19041e63aa353b5c8997e8a501da00734",
    "root_wif": "L3Eans1Cre2zLMx9Nz2mtbqYKjTq5aD1JvcgjSamFf1BM4PW4y7Q",
    "root_chain_code": "b1c4808dc0d6c008978ebb0b727f74b7ba0a9cf91aa9585930aad68b23f5aad1",
    "root_public_key": "03abc5c947c486430ff88b039781f99b9542f2baf523685b23abbe77385c4b0628",
    "strict": true,
    "public_key_type": "compressed",
    "wif_type": "wif-compressed",
    "derivation": {
        "at": {
            "path": "m/0'/0",
            "indexes": [
                2147483648,
                0
            ],
            "depth": 2,
            "index": 0
        },
        "xprivate_key": "xprv9w64ECdcGqcCiXjkbjVAa7NBrX3JZQFfPn7wejkp3CT9CcSaHJSfPc57sNpnbLYFy13k7PxkQUp1SgrEa6MHRM9F1SbeA5y6QR21kkiybPS",
        "xpublic_key": "xpub6A5QdiAW7DAVw1pDhm2AwFJvQYsnxryWm13YT8ARbXz85QmipqkuwQPbig3mpostxYw3Ff7ATgJ8HNJCrHgJ9SeFRbN7y1j29TzeyiZPJpg",
        "private_key": "82fe61ee0a83daa8c2917b7c487b0ca0b434c8a3ed162cf17329d9362137c520",
        "wif": "L1cLzTBJqmCvwpN6aF3rCANCo5S1McrZp2567fd5Nv14sUbEm3h3",
        "chain_code": "baac6149800cfb7f1b022e15f4a090aaef8e71a45f151e2cbb304579298649ca",
        "public_key": "03a3dd0a459ee5bb0cbd511e55c25c3e0aca4ce85cbbc267d374a6d4dc2e09d442",
        "uncompressed": "04a3dd0a459ee5bb0cbd511e55c25c3e0aca4ce85cbbc267d374a6d4dc2e09d44294de047bd398e39077085f50cb9d133fd5b654cc3119eef6e9bfb4c640d6007d",
        "compressed": "03a3dd0a459ee5bb0cbd511e55c25c3e0aca4ce85cbbc267d374a6d4dc2e09d442",
        "hash": "e9b86b1503c8e123c54907d9a7e682cd4b56964f",
        "fingerprint": "e9b86b15",
        "parent_fingerprint": "29b1da55",
        "addresses": {
            "p2wpkh": "bc1qaxuxk9grersj832fqlv60e5ze494d9j0htnm88",
            "p2wpkh-in-p2sh": "3B4DDF1k1oYADQ6coWkrU7Pe7uK4FTzSAH",
            "p2wsh": "bc1qdxv7agxes064ruy9zqvj6pe2xr77ljpxk5cteacarl89fe42mp6q039ks3",
            "p2wsh-in-p2sh": "35zu8EpZToUqofdtocTUCTegyzwhi88Hrg"
        }
    }
}
```
</details>

### Cardano Hierarchical Deterministic (HD) 

#### Byron-Icarus

```
hdwallet dump --symbol ADA --hd Cardano --derivation BIP44 --cardano-type byron-icarus --entropy 10ad31cfb2860b312f0911fc9de22d836ca3eb14
```
alias
```
hdwallet d -s ADA -h Cardano -d BIP44 -ct byron-icarus -e 10ad31cfb2860b312f0911fc9de22d836ca3eb14
```

<details>
  <summary>Output</summary><br/>

```json5
{
    "cryptocurrency": "Cardano",
    "symbol": "ADA",
    "network": "mainnet",
    "coin_type": 1815,
    "entropy": "10ad31cfb2860b312f0911fc9de22d836ca3eb14",
    "strength": 160,
    "mnemonic": "awful hat initial govern gaze obtain rotate captain wish upper merge almost sketch void face",
    "passphrase": null,
    "language": "English",
    "seed": "10ad31cfb2860b312f0911fc9de22d836ca3eb14",
    "ecc": "Kholaw-Ed25519",
    "hd": "Cardano",
    "cardano_type": "byron-icarus",
    "root_xprivate_key": "xprv3QESAWYc9vDdZgb1AgGHAKNr4ZQQ9Jw1vM2MryL8ZYNc97csL4oaQo1JUwYMdreiyYzb9YiXadPfMT5FAfsnCYJPEiNdM1XVGHNCEtD3pC6t3PkyYkQAHKp4hdt2N6shhAaTyTRwKivDV6LnSyVUwPe",
    "root_xpublic_key": "xpub661MyMwAqRbcFwnvLG7WD8CwTZ4Rs9kKfUphf5tp7AqvsqTep598PMB2onJPEEhk54jycSkGQRVZ5CyoTnt94AJh62FeUYotiWPTFiuPKtJ",
    "root_private_key": "b0d7bb1850bc0465a1218d6c0668a02f1394ef11b2a543d80a5dbc3f5d856d5d52116b1adbcc4e391b2c136ba472c718c107ca4d5911f988c8ef98b3c7b7da22",
    "root_chain_code": "8ce478323929220d368ff0731d9a1bcbac0292461f5658b242e11c816ed647d4",
    "root_public_key": "00849c33f09f27f953100ec298fc4ef9ba24045c067eb81c9fb6d877480a483b59",
    "strict": true,
    "public_key_type": "compressed",
    "derivation": {
        "at": {
            "path": "m/44'/1815'/0'/0/0",
            "indexes": [
                2147483692,
                2147485463,
                2147483648,
                0,
                0
            ],
            "depth": 5,
            "purpose": 44,
            "coin_type": 1815,
            "account": 0,
            "change": "external-chain",
            "address": 0
        },
        "xprivate_key": "xprv3T6cWAbQTY7RNHGXSLgeBg7sYpebFaf2YsNxrE1nCoNkbtKThDVK2EP4CkEbkrKEKZFPkxMZpLW1GCYavYawmaqG3dBGAgNscy1LuY4shcFdLy2dqB1LTq5KfBZAvwG8PTQc58nDnpAsBAa7V49Jatc",
        "xpublic_key": "xpub6FemWjhVzq8x7zcgHCNKwCFr4i8f3G8VJL3eZM3VJvHRF7j6uBabunk2MwBcaa2CGi1NMHAJkB7xu3fGq1J4vnPxSTddKCooqzomXV1BeSo",
        "private_key": "207f8f5bf5cb8caa149a86cca72c5d55002beb77495410402d07041372856d5d28b64d275876cdc67fe7698b0d22cd0c9081d217da690574201034c5cc922bcb",
        "chain_code": "0777738e234ab4e02697376faf0b2e8506a1f03144c7f7ef3c0086dfd8dbc049",
        "public_key": "00af5b9332a793a83bb7a074cdabbdac4475251e9cf0e89099f6de26ca2b2bba91",
        "hash": "5cd394eb5c60b8b44cdad5f35027e0e56eff56ad",
        "fingerprint": "5cd394eb",
        "parent_fingerprint": "2033f125",
        "address": "Ae2tdPwUPEZ4Mexb3irFJMw9ypGcAXiPe78PE1fuHTJww15J4hcc6QWFtsG"
    }
}
```
</details>

#### Byron-Ledger

```
hdwallet dump --symbol ADA --hd Cardano --derivation BIP44 --cardano-type byron-ledger --mnemonic "awful hat initial govern gaze obtain rotate captain wish upper merge almost sketch void face"
```
alias
```
hdwallet d -s ADA -h Cardano -d BIP44 -ct byron-ledger -m "awful hat initial govern gaze obtain rotate captain wish upper merge almost sketch void face"
```

<details>
  <summary>Output</summary><br/>

```json5
{
    "cryptocurrency": "Cardano",
    "symbol": "ADA",
    "network": "mainnet",
    "coin_type": 1815,
    "entropy": "10ad31cfb2860b312f0911fc9de22d836ca3eb14",
    "strength": 160,
    "mnemonic": "awful hat initial govern gaze obtain rotate captain wish upper merge almost sketch void face",
    "passphrase": null,
    "language": "English",
    "seed": "480e2d3d35c1e41c32ee2e480705e16e5b95ade415831a2aff4db7b3b9a0f5b1257cc63c251b602d50fc88830050b893ab2eb2ef650accb1b9410567e6ba838d",
    "ecc": "Kholaw-Ed25519",
    "hd": "Cardano",
    "cardano_type": "byron-ledger",
    "root_xprivate_key": "xprv3QESAWYc9vDdZeMC5JbG2VeCU2WKnoqQwYQ43McoqGueUufCoiHNHpCvUAnMCVY88e8aUm6qxmarc6oCCtp8okzYRMBDSpmYbQXswfWGvofkq8DEXi14zciJwSEYzq2MF9kVq3FC7fnG6h4KT3pwPp4",
    "root_xpublic_key": "xpub661MyMwAqRbcFpFw9XG7oXuoJCMT77PULKzCEeMkGSfyqAkKXZYdRwGRcMLTb2V2JPJRT32YEN3cvcKRX3DevASXQtwRpfPK7n5Aku3n69V",
    "root_private_key": "d0aa5f2c07900eb644c2986a20dc9cc4f5f80dbeeddcdf517ee1a7cf313d6555952a9b3a687e99ecd30bdf8fc6579e1357328ec0f58024a4e466cc44786fa6a1",
    "root_chain_code": "7fd8534cf4a3cfbc39e57b5f9d369d2533a1e958ec416ba82ad83e288c73c551",
    "root_public_key": "00d518d347c676c32f2376ea9196d3533311d36f0eb62d2e538acd56aceac54077",
    "strict": true,
    "public_key_type": "compressed",
    "derivation": {
        "at": {
            "path": "m/44'/1815'/0'/0/0",
            "indexes": [
                2147483692,
                2147485463,
                2147483648,
                0,
                0
            ],
            "depth": 5,
            "purpose": 44,
            "coin_type": 1815,
            "account": 0,
            "change": "external-chain",
            "address": 0
        },
        "xprivate_key": "xprv3TDhU3oPsbK8RjBtgdo2fgJ234yQjhnz3oStUJ6EexxT4mupHjYtMop7EEGRV9PnLFvJUnkix1FGW6mRYJR7iQ2b3xA83VCZ3arknAu2jzSY9UZ5xq4WvQBBL3ykNNuKRtFfB29psci4ziC7ChUAzgz",
        "xpublic_key": "xpub6G4cwUHjHG3VdEhbrddjzvwyRQz9rwcUB1gesoRvjjXkGcpa7U224rJNHUvsbLKfCxbSLnSXYFZuhyU2mLdY7QaxuYt1wiCmXDmNNAXdT29",
        "private_key": "b826f57d5e6290cb4ee40c1f7ab27e82b952890d13d229d24d2809a5463d655512e8132b3c7c91c8e36b764da3ab4b41dfc4afcd119b6c9e0fd78c684667cec6",
        "chain_code": "15b410fe10e86f9e22bd9fa2c1eddc9e0e44d5ed2c738ea417de582accf92c3d",
        "public_key": "005477872ca0368f6c7befe4bb6c6574db7baf5598fdfcabe97854c1d5695617d3",
        "hash": "21b5c6b8bf8bd2b498153e7911db72ea77105db9",
        "fingerprint": "21b5c6b8",
        "parent_fingerprint": "582734e1",
        "address": "Ae2tdPwUPEZ47fok1HPbNKnw9cmpQz81Sh8e3yHhopwYaT8sxXthE1onEub"
    }
}
```
</details>

#### Byron-Legacy

```
hdwallet dump --symbol ADA --hd Cardano --path "m/0'/0'" --cardano-type byron-legacy --mnemonic "awful hat initial govern gaze obtain rotate captain wish upper merge almost sketch void face"
```
alias
```
hdwallet d -s ADA -h Cardano -p "m/0'/0'" -ct byron-legacy -m "awful hat initial govern gaze obtain rotate captain wish upper merge almost sketch void face"
```

<details>
  <summary>Output</summary><br/>

```json5
{
    "cryptocurrency": "Cardano",
    "symbol": "ADA",
    "network": "mainnet",
    "coin_type": 1815,
    "entropy": "10ad31cfb2860b312f0911fc9de22d836ca3eb14",
    "strength": 160,
    "mnemonic": "awful hat initial govern gaze obtain rotate captain wish upper merge almost sketch void face",
    "passphrase": null,
    "language": "English",
    "seed": "6812a38be40d2a09f6dd6f84b1e8386dec6edf6378d4360c3a9b628687eb73e2",
    "ecc": "Kholaw-Ed25519",
    "hd": "Cardano",
    "cardano_type": "byron-legacy",
    "root_xprivate_key": "xprv3QESAWYc9vDdZcMbHpiunuKZHMu2D7hcnBWf8Bh6NNpd7HDNwGv9HqALznjoPMYtDt88DwY4PH2PscrnNxsqj6eoJfduLu5VtsFh9LcGnpnq9iPkpnpmmenk29dWkDJYSH468BHzbT4npeMAAEQVuWf",
    "root_xpublic_key": "xpub661MyMwAqRbcFhYnqELWSkWY5W2Kwwp9GVwUHJtMNKQcyCjk4VhsE9kaoH6qnABDyibk2WcSokTKgbC3cNRCMYYzfg1MgL9QcGWQBxBaRY7",
    "root_private_key": "10ebfbe83e34999317573a2cbb4fde1d70ffdb9015e68c3dbf5e04c66d1d464bb11d39380741649c37b8394ca1d3426bca305a64a9bdcc821af731aff1a4982c",
    "root_chain_code": "7439dee2b82a2dff9d31e169f5aa63c7f2f15dc1988bdd359279db9173307a63",
    "root_public_key": "00d9d78f4e52bcacb4a51a442758618ba29f706c14556b39812595a3f6452f0788",
    "strict": true,
    "public_key_type": "compressed",
    "derivation": {
        "at": {
            "path": "m/0'/0'",
            "indexes": [
                2147483648,
                2147483648
            ],
            "depth": 2,
            "index": 2147483648
        },
        "xprivate_key": "xprv3ResHLWFKUay1Lx2gpxen5ae9mgx8C5V3dyN3LUv2vtk8YM4VZcXPedYhrPawye1EAz7ceHzWJHPNCgdxdgi5DW5tjj2cn5KpWD8aPSmrKjFEpB6S4rC8jW8ikvC5X5WYm5zbUL3oh3XsfTLULeb33N",
        "xpublic_key": "xpub6AnreczTDzH8GhqJJmRg4vDj8rSbv1HzPyfFw722GsGXeEf63rpKh6omy91YB4yPJg5dmDwKeoYoDVnmvT3JwBBfqFuf18EnXjZznB8ifqp",
        "private_key": "a3e2b3656d10d6aab166bc9afd21a0a4c640edc926af8e9600b7052f4796860bf08bc3dc71e53c01d869e510a8b8a442b7b1a9787d2b3b757f89d015cf43a327",
        "chain_code": "4160fbf93e1cc60086ffb84396cc17959c0baababa74f109ff4117414a7d33be",
        "public_key": "00b8d6b6fbfdd457a62578fa71149100a43b2256698d27eaf51f8a06ba3304b684",
        "hash": "333113dc34895173523c79fc3aad7a6f82e13bba",
        "fingerprint": "333113dc",
        "parent_fingerprint": "8aebc202",
        "address": "DdzFFzCqrhsyMfU3y9wN9cAwYFPZjbi9jGca4MUPsTyUmd98f2gErCSjSehNPw69nyrPcRM9XKRpJ6cosso9AcUuoot5Mxtw6ooB975p"
    }
}
```
</details>

#### Shelley-Icarus

For Staking address type

```
hdwallet dump --symbol ADA --hd Cardano --derivation CIP1852 --cardano-type shelley-icarus --entropy 10ad31cfb2860b312f0911fc9de22d836ca3eb14 --address-type staking --role 2
```
alias
```
hdwallet d -s ADA -h Cardano -d CIP1852 -ct shelley-icarus -e 10ad31cfb2860b312f0911fc9de22d836ca3eb14 -at staking -ro 2
```

<details>
  <summary>Output</summary><br/>

```json5
{
    "cryptocurrency": "Cardano",
    "symbol": "ADA",
    "network": "mainnet",
    "coin_type": 1815,
    "entropy": "10ad31cfb2860b312f0911fc9de22d836ca3eb14",
    "strength": 160,
    "mnemonic": "awful hat initial govern gaze obtain rotate captain wish upper merge almost sketch void face",
    "passphrase": null,
    "language": "English",
    "seed": "10ad31cfb2860b312f0911fc9de22d836ca3eb14",
    "ecc": "Kholaw-Ed25519",
    "hd": "Cardano",
    "cardano_type": "shelley-icarus",
    "root_xprivate_key": "xprv3QESAWYc9vDdZgb1AgGHAKNr4ZQQ9Jw1vM2MryL8ZYNc97csL4oaQo1JUwYMdreiyYzb9YiXadPfMT5FAfsnCYJPEiNdM1XVGHNCEtD3pC6t3PkyYkQAHKp4hdt2N6shhAaTyTRwKivDV6LnSyVUwPe",
    "root_xpublic_key": "xpub661MyMwAqRbcFwnvLG7WD8CwTZ4Rs9kKfUphf5tp7AqvsqTep598PMB2onJPEEhk54jycSkGQRVZ5CyoTnt94AJh62FeUYotiWPTFiuPKtJ",
    "root_private_key": "b0d7bb1850bc0465a1218d6c0668a02f1394ef11b2a543d80a5dbc3f5d856d5d52116b1adbcc4e391b2c136ba472c718c107ca4d5911f988c8ef98b3c7b7da22",
    "root_chain_code": "8ce478323929220d368ff0731d9a1bcbac0292461f5658b242e11c816ed647d4",
    "root_public_key": "00849c33f09f27f953100ec298fc4ef9ba24045c067eb81c9fb6d877480a483b59",
    "strict": true,
    "public_key_type": "compressed",
    "derivation": {
        "at": {
            "path": "m/1852'/1815'/0'/2/0",
            "indexes": [
                2147485500,
                2147485463,
                2147483648,
                2,
                0
            ],
            "depth": 5,
            "purpose": 1852,
            "coin_type": 1815,
            "account": 0,
            "role": "staking-key",
            "address": 0
        },
        "xprivate_key": "xprv3T8ZNNheWWbCvunovkqK4NFBPPLmdiuwp2dN2ujUt71dhiy2qTNrzBgMMQnJtBhLWvSWiPjSQL9ZRJJ16Ct9tMpAULGTxy7zV8AY3DWApxvaVZYiJRKWajCuHsdsCyGfi4RtVbHEh4Ng32NEWN5uJtj",
        "xpublic_key": "xpub6FmKTEseCTZT9xY1Lir5cTDKCkme44KBf6cwpY2Pz9tfQJeoeMYzeZYijsgVpw6ff378TiEy7RaAzEpBA3q1XcGcew6HTjC1SvMSQKsFoWc",
        "private_key": "18bd95162c8d887e85890edced5b23b736cbd63d1726b3debc22eb5f6b856d5de6afe6679a9bcc48cc55d30787e9fa10b825b5901ff92e6fa4a409dd6ed35748",
        "chain_code": "d04f4b9264917f2bcb97c7750529c97ff40682107ea5b6914ba3324436c501db",
        "public_key": "0020abee887fdd95da102dbe8518d244c38487fc8f2b5039ed50200d979df72e28",
        "hash": "e60e23be4385e8b3e48714348a5187a18fedced1",
        "fingerprint": "e60e23be",
        "parent_fingerprint": "2f91a2ec",
        "address": "stake1u9wrllw52se89k67sruegp9crl9qnhe43qc9q5ws33tdaqcmdh8lx"
    }
}
```
</details>

For Payment address type

```
hdwallet dump --symbol ADA --hd Cardano --derivation CIP1852 --cardano-type shelley-icarus --entropy 10ad31cfb2860b312f0911fc9de22d836ca3eb14 --address-type payment --role 0 --staking-public-key 0020abee887fdd95da102dbe8518d244c38487fc8f2b5039ed50200d979df72e28
```
alias
```
hdwallet d -s ADA -h Cardano -d CIP1852 -ct shelley-icarus -e 10ad31cfb2860b312f0911fc9de22d836ca3eb14 -at payment -ro 0 -stpub 0020abee887fdd95da102dbe8518d244c38487fc8f2b5039ed50200d979df72e28
```

<details>
  <summary>Output</summary><br/>

```json5
{
    "cryptocurrency": "Cardano",
    "symbol": "ADA",
    "network": "mainnet",
    "coin_type": 1815,
    "entropy": "10ad31cfb2860b312f0911fc9de22d836ca3eb14",
    "strength": 160,
    "mnemonic": "awful hat initial govern gaze obtain rotate captain wish upper merge almost sketch void face",
    "passphrase": null,
    "language": "English",
    "seed": "10ad31cfb2860b312f0911fc9de22d836ca3eb14",
    "ecc": "Kholaw-Ed25519",
    "hd": "Cardano",
    "cardano_type": "shelley-icarus",
    "root_xprivate_key": "xprv3QESAWYc9vDdZgb1AgGHAKNr4ZQQ9Jw1vM2MryL8ZYNc97csL4oaQo1JUwYMdreiyYzb9YiXadPfMT5FAfsnCYJPEiNdM1XVGHNCEtD3pC6t3PkyYkQAHKp4hdt2N6shhAaTyTRwKivDV6LnSyVUwPe",
    "root_xpublic_key": "xpub661MyMwAqRbcFwnvLG7WD8CwTZ4Rs9kKfUphf5tp7AqvsqTep598PMB2onJPEEhk54jycSkGQRVZ5CyoTnt94AJh62FeUYotiWPTFiuPKtJ",
    "root_private_key": "b0d7bb1850bc0465a1218d6c0668a02f1394ef11b2a543d80a5dbc3f5d856d5d52116b1adbcc4e391b2c136ba472c718c107ca4d5911f988c8ef98b3c7b7da22",
    "root_chain_code": "8ce478323929220d368ff0731d9a1bcbac0292461f5658b242e11c816ed647d4",
    "root_public_key": "00849c33f09f27f953100ec298fc4ef9ba24045c067eb81c9fb6d877480a483b59",
    "strict": true,
    "public_key_type": "compressed",
    "derivation": {
        "at": {
            "path": "m/1852'/1815'/0'/0/0",
            "indexes": [
                2147485500,
                2147485463,
                2147483648,
                0,
                0
            ],
            "depth": 5,
            "purpose": 1852,
            "coin_type": 1815,
            "account": 0,
            "role": "external-chain",
            "address": 0
        },
        "xprivate_key": "xprv3TGdmrWxcfYMJw7NP6aUhWv39JQkLvu15T2sHABQBmFH5qbo22ts5hgA5x1Rz52hsVLTcVhaVaye9y9b3n57R174X1UoLtFeuhc6WGFG9aQGDthSTsXL46mXsnbhVf6NkZFy6De71Lfg3onpkuR2sPj",
        "xpublic_key": "xpub6GEWF8QkaTWLD4UH2RPeqdcJCo8n2nZGXDe3CxTrqiSzn7RWUgx7G5np1F3kmrEoT3TWXmrxtpem74JvSiuaBv95Mh6NHMqvGqYuAkZCQQx",
        "private_key": "087eec92ee2d0a30a59426b416f42926d655d3190f2bd21058e169c172856d5d19028a1789a18fc8080a2a6fa1aafd5aab1019eefe0c91a1b349d7c851720fa8",
        "chain_code": "0378b93f0ad03afdc8c3ae7d9e2add972204073619ce636eaec214c42c2c0a22",
        "public_key": "008325cfa5733408f6d8868c01306c5f492261d2a31c9194dd346fba4b455a0ccc",
        "hash": "b0c24c27823cf371ff82baa7fce9057839027e08",
        "fingerprint": "b0c24c27",
        "parent_fingerprint": "6f56e59f",
        "address": "addr1qynjq4p7jqzskk8tm6pnxva247usvrxvyqxvzck2vcsp4lju8l7ag4pjwtd4aq8ejszts872p80ntzps2pgaprzkm6pscfgdz3"
    }
}
```
</details>

#### Shelley-Ledger

For Staking address type

```
hdwallet dump --symbol ADA --hd Cardano --derivation CIP1852 --cardano-type shelley-ledger --mnemonic "awful hat initial govern gaze obtain rotate captain wish upper merge almost sketch void face" --address-type staking --role 2 --passphrase meherett
```
alias
```
hdwallet d -s ADA -h Cardano -d CIP1852 -ct shelley-ledger -m "awful hat initial govern gaze obtain rotate captain wish upper merge almost sketch void face" -at staking -ro 2 -pp meherett
```

<details>
  <summary>Output</summary><br/>

```json5
{
    "cryptocurrency": "Cardano",
    "symbol": "ADA",
    "network": "mainnet",
    "coin_type": 1815,
    "entropy": "10ad31cfb2860b312f0911fc9de22d836ca3eb14",
    "strength": 160,
    "mnemonic": "awful hat initial govern gaze obtain rotate captain wish upper merge almost sketch void face",
    "passphrase": "meherett",
    "language": "English",
    "seed": "e7bc9f2abb0827137b408c10d9942066a1f2f356d1cda46f6c0dd5fbc2f7c996328100e580adc26ac614de68644bec61e885afd03dc74eade545fd53b1312cdb",
    "ecc": "Kholaw-Ed25519",
    "hd": "Cardano",
    "cardano_type": "shelley-ledger",
    "root_xprivate_key": "xprv3QESAWYc9vDdZRC8TdCmoxgZMvAa5boHxvFZuGiWp1z9HnjFW5czB3f7pdNfn65xSzNN6Q75gnxxL5H7AVmhmJBJHBx41CsgfP7F27WgcoHjXySmdvAzLeL5McMgbk8472DMz5dvC2J5XQQ4THupx2F",
    "root_xpublic_key": "xpub661MyMwAqRbcF3yEjZ9ptJaYJ4rVVUQzm8EpxvxJ1bKNLrAXbzrWtPiqks3RKmRbLsMn5HaWth7TCTJRhis4ZRwKmvgV2GmPefozGxaBm7k",
    "root_private_key": "e846f1dc083b8e6be29d0ea972e609009aa274eb624115659203577381d9d94914b51516e28f3dfd7479251ff1381adbcee68ab0ca5be491f7e88f503183784f",
    "root_chain_code": "33263e9fd3a6c73d7434a1ada76eeadf40b3924806560fdb96196fa26400ee31",
    "root_public_key": "0034ab707f073862bbc022fd2653fe0256216a33b2631dd39c51a4b5c9ed262cbf",
    "strict": true,
    "public_key_type": "compressed",
    "derivation": {
        "at": {
            "path": "m/1852'/1815'/0'/2/0",
            "indexes": [
                2147485500,
                2147485463,
                2147483648,
                2,
                0
            ],
            "depth": 5,
            "purpose": 1852,
            "coin_type": 1815,
            "account": 0,
            "role": "staking-key",
            "address": 0
        },
        "xprivate_key": "xprv3T2sGe1TmZTEWjzCS33yVhpotgLNBSKezUmEE3aLqvcMDDRRYSSrxjkci96ewHTjJebeWRNSVYwdFE1qsBEXxeAiCtqHUEZhXV3ns9undAHr28HASxJxeRPfqqmG1wWHJaNWZ7LvcyxqR2yHL3QETNw",
        "xpublic_key": "xpub6FSAEwtbu4KVCVv9XDoxzenUCXPjeoxGKuXh8ZYeCb5oUqfEo3GwDfVqcoXsEfXkBGUSBWvdeYYCTgTNyjzk69nHfXK6kjkuW1YP3AJ8Aeg",
        "private_key": "c8c97579a3a447fabeec9d2cf31c0f57d2043c9fc6efb42ba6da06499ed9d94968f933fc5ed0ef6110b3de9ee4175db2e060e6ba35b528d921704dc3856cdb6a",
        "chain_code": "3d41996680640425371425fb0cf33a08b9d1b70f9437180f114d0734e05d8a6c",
        "public_key": "00461b719be821d726f219e37c4b4a4a4f7ec37501de16c370810ecb9f7e96c704",
        "hash": "719d70024f8e2243cddf04531466d1e57b6e2db9",
        "fingerprint": "719d7002",
        "parent_fingerprint": "02a0bc94",
        "address": "stake1u8fhxypajx6dawc5kj3t5cwmw8czr3vpzvusfthx7ce4zucl39z4x"
    }
}
```
</details>

For Payment address type

```
hdwallet dump --symbol ADA --hd Cardano --derivation CIP1852 --cardano-type shelley-ledger --mnemonic "awful hat initial govern gaze obtain rotate captain wish upper merge almost sketch void face" --address-type payment --role 0 --passphrase meherett --staking-public-key 00461b719be821d726f219e37c4b4a4a4f7ec37501de16c370810ecb9f7e96c704
```
alias
```
hdwallet d -s ADA -h Cardano -d CIP1852 -ct shelley-ledger -m "awful hat initial govern gaze obtain rotate captain wish upper merge almost sketch void face" -at payment -ro 0 -pp meherett -stpub 00461b719be821d726f219e37c4b4a4a4f7ec37501de16c370810ecb9f7e96c704
```

<details>
  <summary>Output</summary><br/>

```json5
{
    "cryptocurrency": "Cardano",
    "symbol": "ADA",
    "network": "mainnet",
    "coin_type": 1815,
    "entropy": "10ad31cfb2860b312f0911fc9de22d836ca3eb14",
    "strength": 160,
    "mnemonic": "awful hat initial govern gaze obtain rotate captain wish upper merge almost sketch void face",
    "passphrase": "meherett",
    "language": "English",
    "seed": "e7bc9f2abb0827137b408c10d9942066a1f2f356d1cda46f6c0dd5fbc2f7c996328100e580adc26ac614de68644bec61e885afd03dc74eade545fd53b1312cdb",
    "ecc": "Kholaw-Ed25519",
    "hd": "Cardano",
    "cardano_type": "shelley-ledger",
    "root_xprivate_key": "xprv3QESAWYc9vDdZRC8TdCmoxgZMvAa5boHxvFZuGiWp1z9HnjFW5czB3f7pdNfn65xSzNN6Q75gnxxL5H7AVmhmJBJHBx41CsgfP7F27WgcoHjXySmdvAzLeL5McMgbk8472DMz5dvC2J5XQQ4THupx2F",
    "root_xpublic_key": "xpub661MyMwAqRbcF3yEjZ9ptJaYJ4rVVUQzm8EpxvxJ1bKNLrAXbzrWtPiqks3RKmRbLsMn5HaWth7TCTJRhis4ZRwKmvgV2GmPefozGxaBm7k",
    "root_private_key": "e846f1dc083b8e6be29d0ea972e609009aa274eb624115659203577381d9d94914b51516e28f3dfd7479251ff1381adbcee68ab0ca5be491f7e88f503183784f",
    "root_chain_code": "33263e9fd3a6c73d7434a1ada76eeadf40b3924806560fdb96196fa26400ee31",
    "root_public_key": "0034ab707f073862bbc022fd2653fe0256216a33b2631dd39c51a4b5c9ed262cbf",
    "strict": true,
    "public_key_type": "compressed",
    "derivation": {
        "at": {
            "path": "m/1852'/1815'/0'/0/0",
            "indexes": [
                2147485500,
                2147485463,
                2147483648,
                0,
                0
            ],
            "depth": 5,
            "purpose": 1852,
            "coin_type": 1815,
            "account": 0,
            "role": "external-chain",
            "address": 0
        },
        "xprivate_key": "xprv3TFihJFJ1yiNDtsBoSV5v2Khe8TBJ191tV1VEJUQqRay4hH2JCcx8fjVYt53SVsy3Y3AaY7E39TeDfX751Jb6vtv5Xd93RN8Zrf7QEsMa6vGuzGXxYUvjdjPuKfGqitW9zrcP6NDHCFBmV56LSoVXjm",
        "xpublic_key": "xpub6GBRZnRbXutvRgR93Dyd1QFwk6Ztwm6SStT8Sn8mBycXoVWqNi7xs1cMkXwKy26Qd2smG18stNzFNRaq96tp82Yr9AqovuKNQw1Sar5f97R",
        "private_key": "e81d4ffc96c7ba61927dc11eabce5138228ec9c41b46f7c4bb49d8469bd9d949e8f9f4be44de8bffcc34c5b1d2e5127e34599204d95f2ba87d6fab99814008fd",
        "chain_code": "f9bed77ca78cefa4058cf137dc598b507e9c1a400e2da87a073f34c281905874",
        "public_key": "00c768f160cd30010b735f94d4660917e38a3230713750d5efef3cc0961f342f50",
        "hash": "cd0974f087b180b17e55aefb4f82f93e229d6ced",
        "fingerprint": "cd0974f0",
        "parent_fingerprint": "681cf4b8",
        "address": "addr1q9sl4hwp97a5ywxzmhqjn4qud9jspdkwjug7dvysu4hzqlknwvgrmyd5m6a3fd9zhfsaku0sy8zczyeeqjhwda3n29esrdw0y4"
    }
}
```
</details>

### Electrum-V1 Hierarchical Deterministic (HD) 

```
hdwallet dump --symbol BTC --hd Electrum-V1 --derivation Electrum --entropy-name Electrum-V1  --entropy d36ee56e7948d94192ca1ad58df509e8 --public-key-type uncompressed
```
alias
```
hdwallet d -s BTC -h Electrum-V1 -d Electrum -en Electrum-V1 -e d36ee56e7948d94192ca1ad58df509e8 --public-key-type uncompressed
```

<details>
  <summary>Output</summary><br/>

```json5
{
    "cryptocurrency": "Bitcoin",
    "symbol": "BTC",
    "network": "mainnet",
    "coin_type": 0,
    "entropy": "d36ee56e7948d94192ca1ad58df509e8",
    "strength": 128,
    "mnemonic": "punch spider stick angel bounce battle ground gasp worry pull possess key",
    "passphrase": null,
    "language": "English",
    "seed": "cd4373469d00a829cc7c9d4782e8d7b592ffdc84fd370463222fe78248929a45",
    "ecc": "SLIP10-Secp256k1",
    "hd": "Electrum-V1",
    "master_private_key": "cd4373469d00a829cc7c9d4782e8d7b592ffdc84fd370463222fe78248929a45",
    "master_wif": "5KNgm889ev9wcA76wx7oifjBQ2mRcUg6cxBfxkhWGnRJjvRwK6c",
    "master_public_key": "04dd93ac1b8870872479df1ac2c23fd6673932ee9b4f03b513d4e9bdc1680988abaf3625ccee5fc5ec7dfce6c5694a7f3ec03b4328d3222addd8f63ac91525715c",
    "public_key_type": "uncompressed",
    "wif_type": "wif",
    "derivation": {
        "at": {
            "change": 0,
            "address": 0
        },
        "private_key": "af32ef79dea97638d8ff7703bf2c472e5b9f1c2d0060f1267a3de59b815c5c05",
        "wif": "5K9Soaom2PmU5Ve7YwmxLhbUDY8cMjgYfa95SWKdz2hHoTnTtsP",
        "public_key": "046a4a07afbc8b768f94a0ed1d280a0d7a6346260607cfd532c6a2eea9f2d333c1221b1cea48336cd3e3676bc8c765cc3e2288733e88d621165225cfa5b3c0e877",
        "uncompressed": "046a4a07afbc8b768f94a0ed1d280a0d7a6346260607cfd532c6a2eea9f2d333c1221b1cea48336cd3e3676bc8c765cc3e2288733e88d621165225cfa5b3c0e877",
        "compressed": "036a4a07afbc8b768f94a0ed1d280a0d7a6346260607cfd532c6a2eea9f2d333c1",
        "address": "18hWSvzs1o1i48nG783ihBuX6uK89GLzKB"
    }
}
```
</details>

### Electrum-V2 Hierarchical Deterministic (HD) 

```
hdwallet dump --symbol BTC --hd Electrum-V2 --derivation Electrum --entropy-name Electrum-V2  --entropy e6fec331ee9e4fbb924dfedc3a9cbf59 --public-key-type uncompressed
```
alias
```
hdwallet d -s BTC -h Electrum-V2 -d Electrum -en Electrum-V2 -e e6fec331ee9e4fbb924dfedc3a9cbf59 --public-key-type uncompressed
```

<details>
  <summary>Output</summary><br/>

```json5
{
    "cryptocurrency": "Bitcoin",
    "symbol": "BTC",
    "network": "mainnet",
    "coin_type": 0,
    "entropy": "e6fec331ee9e4fbb924dfedc3a9cbf59",
    "strength": 128,
    "mnemonic": "twenty indicate bubble universe orbit tonight lava oxygen differ art legal attack",
    "passphrase": null,
    "language": "English",
    "seed": "aca72f9983034cf832732402335d628ddd93280439ba000e6a568849db6258e5264e9aa5a2074766bc964b29a8fdf8a4341a5893ac4a5f5a01321af66e3af3d9",
    "ecc": "SLIP10-Secp256k1",
    "hd": "Electrum-V2",
    "mode": "standard",
    "mnemonic_type": "standard",
    "master_private_key": "bff9c2c6c47c50681a288f4611e934c7c1c8c3730fbe2679f15c310ca4add8ad",
    "master_wif": "5KGqLkJe1GodaXqwZRCKpzw5mCqyPp9TzSRh47AXx5WbSdPoSCT",
    "master_public_key": "047f104d982ff209ffa7ceec037106b63a6d51442f9ffacf7cf4870646140d6752e0989d66e9973db718bc5c84792c8c3c16dc7b666079efe7609a89d1872df47f",
    "public_key_type": "uncompressed",
    "wif_type": "wif",
    "derivation": {
        "at": {
            "change": 0,
            "address": 0
        },
        "private_key": "b1ecab1e43ccedb39da9f75f3a8f4d16bb038d8243de4f65dd142d06fcc439ac",
        "wif": "5KAeRXbiLFm2BMaPpbRwQmhFKQr5TDkoCz8ScrW6yXXj3tZ7ZTt",
        "public_key": "04bc2d7a9922af8fe095fda63926636b0a8c052f30ef69ab753cb1bdebaece4b85a8842e34e05f450f8ad25280f27c91f176a9bada036a930261a144ca78cede6d",
        "uncompressed": "04bc2d7a9922af8fe095fda63926636b0a8c052f30ef69ab753cb1bdebaece4b85a8842e34e05f450f8ad25280f27c91f176a9bada036a930261a144ca78cede6d",
        "compressed": "03bc2d7a9922af8fe095fda63926636b0a8c052f30ef69ab753cb1bdebaece4b85",
        "address": "1NwUPAtXp4sfHzRa63BF7PGK7xAwLCctTa"
    }
}
```
</details>

### Monero Hierarchical Deterministic (HD) 

```
hdwallet dump --symbol XMR --hd Monero --derivation Monero --entropy d0168dd591f0daa6daef028f01994da6
```
alias
```
hdwallet d -s XMR -h Monero -d Monero -e d0168dd591f0daa6daef028f01994da6
```

<details>
  <summary>Output</summary><br/>

```json5
{
    "cryptocurrency": "Monero",
    "symbol": "XMR",
    "network": "mainnet",
    "coin_type": 128,
    "entropy": "d0168dd591f0daa6daef028f01994da6",
    "strength": 128,
    "mnemonic": "source refuse install catalog asset fat hill theory monitor art fat ethics",
    "passphrase": null,
    "language": "English",
    "seed": "98aeb5d2f92496560c3b89b698f1476ffa858428c04a7cc372a9dc5d46667d63644b2cf589b45a093923f5350cffeea6952dafb7a78b15341330bee6dc582695",
    "ecc": "SLIP10-Ed25519-Monero",
    "hd": "Monero",
    "private_key": null,
    "spend_private_key": "b429ac54bb9bb8789e60ed9b7d57a2563f993ce3126dfa92aa977f3615108e04",
    "view_private_key": "56416d84b26e7a7da5302cae73a9af316efbf3e9f24b1ef23d6a33cfdc1a5809",
    "spend_public_key": "d542db4f8f1c228ce8167b7261bf7d0ba6106f02f1b8de5afdb721e72a9a9209",
    "view_public_key": "c8fd56f8491a76b5f5a5277f3dd1e178ced22bfe1c792661ca6e38d730951b59",
    "primary_address": "49hqttVKUrDQZyHdGZP5cp2x1Q6zrAzP7GDjC28iqSJ52dvpPNP54z1XSEfVNsqJpQMCzJKQTE9zMHMhBJaQ3M3xB7tnvbq",
    "derivation": {
        "at": {
            "minor": 1,
            "major": 0
        },
        "sub_address": "8BJMSSiktihHokhwNtW9wqZJiH2ammAR5VyTASFgHKcdKtvcqJMqkNehikMbAYmEG4YzuN1mGcdr4AQPca5Yw6d531ChqBs"
    }
}
```
</details>
