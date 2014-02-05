activate_this = '/home/albertyw/.virtualenvs/poo-mailer/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import os
import sys
current_location = os.path.dirname(os.path.realpath(__file__))+'/'
sys.path.append(current_location)
sys.path.append(current_location+'../src/')

from serve import app as application
