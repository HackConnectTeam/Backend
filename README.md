# Backend


## 1. Install and configure pre-commit

To install `pre-commit`, execute this command:

```bash
pip install pre-commit
```

For installing `pre-commit` hooks you have to run:

```bash
pre-commit install && pre-commit install --hook-type commit-msg
```

---

## 2. Install psql

### For Linux

```bash
sudo apt-get install postgresql-client
```

### For MacOS

```bash
brew install libpq
```

## 3. Install Render:
### For MacOS/Linux

```bash
curl -fsSL https://raw.githubusercontent.com/render-oss/cli/refs/heads/main/bin/install.sh | sh
```

## 4. Run Fastapi:

```bash
uvicorn src.app.main:app --host 0.0.0.0 --port 8000
```
