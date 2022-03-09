# Fernet CLI

A CLI to manage [Fernet](https://cryptography.io/en/latest/fernet/) encrypted env variables

## Commands

### generate

```bash
$> fernet generate
ixfFROV_uIYZsM4cB6mCs4Bi7mnlsDzOqk-WCsLsYiA=
```

This command generates a new fernet key (using `Fernet.generate_key()`) and prints it out.
Use this command to generate news keys to be securely stored.

### init

```bash
$> export FERNET_KEY='ixfFROV_uIYZsM4cB6mCs4Bi7mnlsDzOqk-WCsLsYiA='
$> export FERNET__VARIABLE_NAME='Z0FBQUFBQmlLTF9QZ3FuZjZxVllmTmJtcDhpU3p2MHAxdVpWTXlVa21jLU5PbEdoeFE0d01TR1R3QnZORGMyVlFXX1ZISG0tUFl3RnVXVmFWNlhVRG9ZWTFjWEQzRm9wQmJCTXhFdTZkZ0F4S2ZmZjg0RGhTdE09'
$> eval $(fernet init)
$> echo $VARIABLE_NAME
some-secret-value
```

This command will attempt to decrypt any env variables prefixed with `FERNET__` using the key provided in the `FERNET_KEY` env variable.
It then ouptuts a shell eval-able definition of decrypted variables, typically to be used as `eval $(fernet init)`.

### encrypt

```bash
$> export FERNET_KEY='ixfFROV_uIYZsM4cB6mCs4Bi7mnlsDzOqk-WCsLsYiA='
$> fernet encrypt 'some-secret-value'
Z0FBQUFBQmlLTF9QZ3FuZjZxVllmTmJtcDhpU3p2MHAxdVpWTXlVa21jLU5PbEdoeFE0d01TR1R3QnZORGMyVlFXX1ZISG0tUFl3RnVXVmFWNlhVRG9ZWTFjWEQzRm9wQmJCTXhFdTZkZ0F4S2ZmZjg0RGhTdE09
```

This command encrypts the passed argument using the fernet key provided in the `FERNET_KEY` env variable and prints it out.

### decrypt

```bash
$> export FERNET_KEY='ixfFROV_uIYZsM4cB6mCs4Bi7mnlsDzOqk-WCsLsYiA='
$> fernet decrypt 'Z0FBQUFBQmlLTF9QZ3FuZjZxVllmTmJtcDhpU3p2MHAxdVpWTXlVa21jLU5PbEdoeFE0d01TR1R3QnZORGMyVlFXX1ZISG0tUFl3RnVXVmFWNlhVRG9ZWTFjWEQzRm9wQmJCTXhFdTZkZ0F4S2ZmZjg0RGhTdE09'
some-secret-value
```

This command dencrypt the passed argument using the fernet key provided in the `FERNET_KEY` env variable and prints it out.
