from flask import Blueprint

treatstation_blue = Blueprint('treatstation', __name__)
from . import views