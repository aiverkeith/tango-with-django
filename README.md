# How to run

Copy the sample ```.env``` file
```bash
cp .env.example .env
```

Generate a secret key and paste the result on the ```.env``` fie
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

Create google custom search API key
```bash
touch google-custom-search-api.key
```

- Go to https://developers.google.com/custom-search/v1/overview#api_key and follow the instruction to get the API key

Run the migration
```bash
python manage.py migrate
```

Create a superuser
```bash
python manage.py createsuperuser
```

Run the server
```bash
python manage.py runserver
```