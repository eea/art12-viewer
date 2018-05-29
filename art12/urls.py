from flask import Blueprint
from art12.views import Homepage, Summary, Progress, Reports, \
    ConnectedSelectBoxes, FilterFormCountries, EuMap
from art12.factsheet import factsheet
from art12.factsheet import BirdFactsheet, FactsheetHeader, FactsheetFooter

views = Blueprint('views', __name__)

views.add_url_rule('/', view_func=Homepage.as_view('homepage'))
views.add_url_rule('/summary', view_func=Summary.as_view('summary'))
views.add_url_rule('/summary/filter_form',
                   view_func=ConnectedSelectBoxes.as_view('filter_form'))
views.add_url_rule('/summary/filter_form/countries',
                   view_func=FilterFormCountries.as_view('filter_form_countries'))
views.add_url_rule('/progress', view_func=Progress.as_view('progress'))
views.add_url_rule('/report', view_func=Reports.as_view('report'))
views.add_url_rule('/eu_map', view_func=EuMap.as_view('eu_map'))

factsheet.add_url_rule('/factsheet/',
                       view_func=BirdFactsheet.as_view('factsheet'))
factsheet.add_url_rule('/factsheet/header/',
                       view_func=FactsheetHeader.as_view('header'))
factsheet.add_url_rule('/factsheet/footer/',
                       view_func=FactsheetFooter.as_view('footer'))
