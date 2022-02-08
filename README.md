# chouseisan_py
chouseisan_py automates the operations of [調整さん](https://chouseisan.com/)(Chouseisan).
Currently, it only supports creating events.

![Test](https://github.com/ryu22e/chouseisan_py/actions/workflows/test.yml/badge.svg)
[![codecov](https://codecov.io/gh/ryu22e/chouseisan_py/branch/main/graph/badge.svg?token=rB5RS1bewF)](https://codecov.io/gh/ryu22e/chouseisan_py)

## Installation

```python
$ pip install chouseisan-py
```

## Usage

```python
>>> from datetime import datetime
>>> from chouseisan_py.chouseisan import Auth, Chouseisan
>>> auth = Auth(email="test@example.com", password="<secret>")
>>> chouseisan = Chouseisan(auth)
>>> chouseisan.create_event(
...    title="test event",
...    candidate_days=[datetime(2021, 10, 17, 19, 0), datetime(2021, 10, 18, 19, 0)]
... )
'https://chouseisan.com/s?h=f7b7fc11995b441782844bc3fddaf456'
```
