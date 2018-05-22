"""
Load static files on Amazon S3

Author:   Romary Dupuis <romary@me.com>

Copyright (C) 2017-2018 Romary Dupuis
"""
from commis import Command, color
from flask_s3 import create_all
from lifoid.constants import HEADER


class LoadstaticCommand(Command):
    """
    CLI to load static files needed by Lifoid web app on Amazon S3
    """
    name = 'loadstatic'
    help = 'load static files'
    args = {
        '--bucket': {
            'metavar': 'BUCKET',
            'required': True,
            'help': 'name of bucket on Amazon S3'
        }
    }

    def handle(self, args):
        """
        CLI to run the lifoid HTTP API server application.
        """        
        print(HEADER)
        from lifoid.www.app import app
        app.config['FLASKS3_BUCKET_NAME'] = args.bucket
        create_all(app)
        return color.format(" * Static files loaded", color.GREEN)
