## Cursor Cloud specific instructions

- **Python**: 3.12 on the VM. README says 3.9.7 but all code works fine on 3.12.
- **Virtual environment**: `/workspace/.venv`. Always use `/workspace/.venv/bin/python` to run scripts.
- **Dependencies**: `pip install -r requirements.txt` inside the venv. Requires `python3-dev` system package for building `lru-dict` (C extension dep of `web3`).
- **No test suite, no linter, no build system** — this is a collection of standalone CLI scripts.
- **Scripts**:
  - `qna3_batch_create.py` — generates wallets locally (no external API needed).
  - `qna3_sign.py` — batch sign-in (needs `wallets.txt` with `address,private_key` per line + network access to `api.qna3.ai` and `opbnb.publicnode.com`).
  - `qna3_batch_tranf.py` — batch transfer (needs wallet files + funded wallets on opBNB).
- **Only `qna3_batch_create.py` can run fully offline.** The other two scripts require real wallets with opBNB funds and live API access.
