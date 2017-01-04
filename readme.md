```
conda create --name us_election python=3
source activate us_election
pip install django

django-admin startproject us_election

python manage.py startapp dashboard

```

Steps:

- settings:
    - add app 'dashboard'
    - add templates directories
    - add static directories
- add urls
- create views
