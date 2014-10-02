from flask import Blueprint
from art12.views import Homepage, Summary, Progress, Reports, \
    ConnectedSelectBoxes

views = Blueprint('views', __name__)

views.add_url_rule('/', view_func=Homepage.as_view('homepage'))
views.add_url_rule('/summary', view_func=Summary.as_view('summary'))
views.add_url_rule('/summary/filter_form',
                   view_func=ConnectedSelectBoxes.as_view('filter_form'))
views.add_url_rule('/progress', view_func=Progress.as_view('progress'))
views.add_url_rule('/report', view_func=Reports.as_view('report'))
