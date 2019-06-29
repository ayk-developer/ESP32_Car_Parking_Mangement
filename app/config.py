import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # ...
    SQLALCHEMY_DATABASE_URI = \
        'postgres://atwzycuaabdruo:91fedb3eee2d763d798890cf015a50f4254b41e84c065cb631eb8d84742c5c40@ec2-174-129-41-127.compute-1.amazonaws.com:5432/d444nf8njcg92a?sslmode=require'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    '''JOBS = [
        {
            'id': 'job1',
            'func': 'app.cutbill1:job1',
            'args': (),
            'trigger': 'interval',

        }
    ]'''

    SCHEDULER_API_ENABLED = True
