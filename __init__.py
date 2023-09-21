from flask import Flask, render_template, request, redirect , abort , session, g, url_for,jsonify
import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from database import user_relogin , user_login
from logs import logs
from database import repeated_data
from database import delete
from gevent import pywsgi
from database import add_chat
from database import get_chat
from math import ceil
from public import check,make_pagenation , get_code
import pymysql
import time 
from database import *
import random
from database import autoconn
from playsound import playsound
from public import Throw