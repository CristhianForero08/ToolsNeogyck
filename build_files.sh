#!/bin/bash

# Instalar dependencias
pip install -r requirements.txt

# Aplicar migraciones
python manage.py migrate

# Recolectar archivos estáticos
python manage.py collectstatic --noinput

# Mover archivos recolectados al directorio esperado por Vercel
mv staticfiles/ staticfiles_build/
