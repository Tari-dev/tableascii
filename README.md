# Tableascii

A simple, lightweight, no-dependency Python library to create clean ASCII Table.

## Installation
Install from pypi
```bash
pip install tableascii
```
Or directly from Github
```bash
pip install git+https://github.com/Tari-dev/tableascii.git
```

## Usage Example
```python
from tableascii import Table

data = [
    ["Name", "Age"],
    ["Alice", 30],
    ["Bob", 25]
]

tb = Table(data)
print(tb.create())
```

```bash
+-------------+
| Name  | Age |
|-------------|
| Alice | 30  |
| Bob   | 25  |
+-------------+
```
## Features
- Pure ASCII output
- Simple and Lightweight
- No dependencies
- Automatically adjusts column width

## License
[MIT](https://github.com/Tari-dev/tableascii/blob/main/LICENSE)
