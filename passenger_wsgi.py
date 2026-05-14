import sys
import os

PROJECT_ROOT = '/home/taxinq/sop_django_new'
sys.path.insert(0, PROJECT_ROOT)

VENV_PATH = '/home/taxinq/sop_django_new/env3_12_8'
sys.executable = os.path.join(VENV_PATH, 'bin', 'python3.12')
sys.path.insert(0, os.path.join(VENV_PATH, 'lib/python3.12/site-packages'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

