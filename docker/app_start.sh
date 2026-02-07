if [ "$ENV"  = "localdev" ]
then

  python manage.py migrate
  # python manage.py initialize_db

fi
