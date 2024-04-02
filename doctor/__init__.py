from flask import Blueprint

doctor_blue = Blueprint('doctor', __name__)
from . import views