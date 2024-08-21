#!/bin/bash

# Instala las dependencias
pip install -r requirements.txt

# Ejecuta la recopilación de archivos estáticos
python3 manage.py collectstatic --noinput
