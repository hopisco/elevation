import sys
import os
sys.path.append('{}/..'.format(os.path.dirname(__file__)))

# We need to monkey_patch everything
from flask import request, abort

import json

import lib.opentopodata as opentopodata

class indexView():
    def __init__(self, app):
        self.application = app
        app.add_url_rule('/', 'getelevation', self.getelevation, methods=['POST'])
        app.add_url_rule('/', 'getelevation/details', self.getelevationdetails, methods=['POST'])

    def getelevation(self):
        try:
            data = request.json
        except:
            abort(400)
            
        try: 
            d = data['line']
        except:
            abort(400)

        r = opentopodata.getElevation(d)
        r.pop('details')
        return json.dumps(r)

    def getelevationdetails(self):
        try:
            data = request.json
        except:
            abort(400)
            
        try: 
            d = data['line']
        except:
            abort(400)

        r = opentopodata.getElevation(d)
        return json.dumps(r)