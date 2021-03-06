import os
import pytest

from flask_migrate import Migrate,upgrade,migrate,init,downgrade

from unifispot import create_app
from unifispot.models import db as _db
from unifispot.models import user_datastore
from flask_security.utils import encrypt_password
from selenium import webdriver
from flask import current_app,url_for
import os
import shutil

from tests.data.data import init_data

#---------------enable logging while tests running-----------
import logging
from logging.handlers import RotatingFileHandler
logfile = 'alltests.log'
os.remove(logfile) if os.path.exists(logfile) else None
file_handler = RotatingFileHandler(logfile, 'a', 1 * 1024 * 1024, 10)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
##------------End logging Initilization-----------------------

@pytest.fixture(scope='session')
def app(request):
    """Session-wide test `Flask` application."""

    app = create_app(mode="testing")

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()
    
    ##------------More logging configuration---------------------
    app.logger.setLevel(logging.DEBUG)
    file_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(file_handler)
    app.logger.debug('--------------Starting Tests-----------------')
    ##------------More logging configuration END------------------
    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app

@pytest.fixture(scope='session')
def db(app, request):
    """Session-wide test database."""

    def teardown():
        pass
    _db.app = app

    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope='function')
def session(db, request):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)
    
    db.session = session
    init_data(session)
    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session


@pytest.fixture(scope='function')
def admin1_logged(request):
    '''fixture used to create a logged in instance of test_client 

        based on multiple examples like http://librelist.com/browser/flask/2012/7/1/giving-context-to-test-client/#dfb70ea7e1b300da59d9d0ba6a2c0d52
    '''
    username = 'admin1@admin.com'
    password = 'zaqxswcdevfr1'
    
    original_client = current_app.test_client
    logged_client = current_app.test_client()

    login_resp = logged_client.post(url_for('security.login'),data={ 'email':username, 'password': password },follow_redirects=True)
    assert 'Bad username or password' not in login_resp.data,'Login Failed '   

    current_app.test_client = logged_client  #temperarly replace test_client with instance of logged in client
    def teardown():
        current_app.test_client = original_client #change back client to original version

    request.addfinalizer(teardown)    
    return logged_client

@pytest.fixture(scope='function')
def client1_logged(request):
    '''fixture used to create a logged in instance of test_client 

        based on multiple examples like http://librelist.com/browser/flask/2012/7/1/giving-context-to-test-client/#dfb70ea7e1b300da59d9d0ba6a2c0d52
    '''
    username = 'client1@admin.com'
    password = 'zaqxswcdevfr1'

    original_client = current_app.test_client
    logged_client = current_app.test_client()

    login_resp = logged_client.post(url_for('security.login'),data={ 'email':username, 'password': password },follow_redirects=True)
    assert 'Bad username or password' not in login_resp.data,'Login Failed ' 

    current_app.test_client = logged_client  #temperarly replace test_client with instance of logged in client
    def teardown():
        current_app.test_client = original_client #change back client to original version

    request.addfinalizer(teardown)
    
    return logged_client

