# Password Generator

A small, secure Python library for generating strong passwords and passphrases.

## Features

- Cryptographically secure (uses Python's `secrets` module)
- Configurable length and character sets
- Option to exclude ambiguous characters (l, 1, O, 0)
- Passphrase generator for memorable passwords
- Password strength checker

## Installation

```bash
git clone https://github.com/sarahokumasi42-code/Password-generator.git
cd Password-generator
pip install -r requirements.txt
```

## Usage

```python
from password_generator import generate_password, generate_passphrase, password_strength

# Default 12-character password
print(generate_password())

# Strong 20-character password
print(generate_password(length=20))

# Digits only (e.g. for a PIN)
print(generate_password(length=6, use_lowercase=False, use_uppercase=False, use_symbols=False))

# No confusing characters
print(generate_password(length=16, exclude_ambiguous=True))

# Memorable passphrase
print(generate_passphrase(word_count=4))
# -> "tiger-cloud-mango-river"

# Check password strength
print(password_strength("Abcd1234!@#$"))
# -> {'score': 4, 'label': 'Very Strong', 'feedback': ['Great password!']}
```

## Running tests

```bash
pip install pytest
pytest
```

## License

MIT