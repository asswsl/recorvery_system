from flask import Blueprint

nurse_blue = Blueprint('nurse', __name__)
from . import views
