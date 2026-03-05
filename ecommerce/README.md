 python3 -m venv .venv  
  
 source .venv/bin/activate  
pip install django   
python -m pip install Pillow  
  
python3 manage.py  makemigrations   
python3 manage.py  migrate   
python3 manage.py createsuperuser

python3 manage.py  runserver 

git init .