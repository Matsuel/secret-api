## How to install

### Create venv

```py
python -m venv venv
```

### Activate venv

```py
venv/Scripts/activate
```

### Install libs 
```py
pip install -r requirements.txt
```

### Docker

#### Create .env file 

```env
DATABASE_USER=your_user
DATABASE_PASSWORD=your_password
DATABASE_NAME=sekret
```

#### Run docker compose

```bash
docker compose --env-file .env up -d
```

## Run unittest

```bash
python -m unittest discorver -s tests
```
or
```bash
python3 -m unittest discover -s tests
```