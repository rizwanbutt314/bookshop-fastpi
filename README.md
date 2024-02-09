### 1. PreReqs

```bash
1. Python 3.11+
2. Docker / Postgres is installed
```

### 2. Install dependecies with virtual environment

```bash
python3.11 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### 3. Configurations

```bash
* Create file .env
* Copy the content of .env.example into .env file and change settings accordingly
```

### 4. Setup databases (Docker)

```bash
### Setup two databases
docker-compose up -d

### Alembic migrations upgrade
bash init.sh

NOTE: If docker isn't available then setup postgres databases for app and tests and adds it's settings in .env file
```

### 3. Run App / Tests

```bash
# To Run Server
* uvicorn app.main:app --reload

# To Run Tests
* pytest
```