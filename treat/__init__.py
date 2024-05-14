from flask import Blueprint

treat_blue = Blueprint('treat', __name__)
from . import views