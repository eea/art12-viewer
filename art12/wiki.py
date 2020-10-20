from flask import (
    Blueprint,
    views,
    render_template,
    request,
    url_for,
    redirect,
    abort,
)

from art12.models import (
    Dataset,
    Wiki,
    WikiChange,
    WikiTrail,
    WikiTrailChange,
)


wiki = Blueprint('wiki', __name__)


class CommonSection(object):

    def get_req_args(self):
        return {arg: request.args.get(arg, '') for arg in ['subject', 'period', 'reported_name']}

    def get_wiki(self):
        r = self.get_req_args()

        return (
            self.wiki_cls.query
            .filter(
                self.wiki_cls.subject == r['subject'],
                self.wiki_cls.dataset_id == r['period'])
            .first()
        )

    def get_wiki_changes(self):
        return self.wiki_change_cls.query.filter_by(wiki=self.get_wiki())

    def get_active_change(self):
        return self.get_wiki_changes().filter_by(active=1).first()

    def get_context(self):
        active_change = self.get_active_change()

        request_args = self.get_req_args()
        period = request_args.get('period') or abort(404)
        dataset = Dataset.query.get(period) or abort(404)

        return {
            'wiki_body': [active_change.body] if active_change else [],
            'dataset': dataset,
            'home_url': url_for(self.home_endpoint, **request_args),
            'page_title': self.page_title
        }


class DataSheetSection(CommonSection):
    wiki_cls = Wiki
    wiki_change_cls = WikiChange
    page_title = 'Data Sheet Info'
    home_endpoint = '.datasheet'


class WikiView(views.View):
    methods = ['GET', 'POST']
    template_name = 'wiki/wiki.html'

    def __init__(self, section):
        self.section = section()

    def dispatch_request(self):
        context = self.section.get_context()

        if request.method == 'POST':
            if self.process_post_request():
                return redirect(context['home_url'])

        return render_template(self.template_name, **context)


class AuditTrailSection(CommonSection):
    wiki_cls = WikiTrail
    wiki_change_cls = WikiTrailChange
    page_title = 'Audit Trail'
    home_endpoint = '.audittrail'


class AuditView(views.View):
    methods = ['GET']
    template_name = 'wiki/wiki.html'

    def __init__(self, section):
        self.section = section()

    def get_wiki_changes_for_period_2018(self, rq, wikis):

        if len(wikis) > 1 and rq['reported_name'] == '':
            return ['only available at subspecific level']
        else:
            wikis = self.section.wiki_cls.query.filter(
                    self.section.wiki_cls.subject == rq['subject'],
                    self.section.wiki_cls.dataset_id == rq['period'],
                )
            if rq['reported_name']:
                wikis = (wikis.filter(self.section.wiki_cls.reported_name_code == rq['reported_name']).all())
            else:
                wikis = (wikis.all())

            wiki_body = []

            for wiki in wikis:
                change = (
                    self.section.wiki_change_cls.query
                    .filter_by(
                        wiki=wiki,
                        active=1,
                    ).first()
                )
                if change:
                    wiki_body.append(change.body)
            return wiki_body


    def dispatch_request(self):
        rq = self.section.get_req_args()

        wikis = (
            self.section.wiki_cls.query
            .filter(
                self.section.wiki_cls.subject == rq['subject'],
                self.section.wiki_cls.dataset_id == rq['period']
            )
            .all()
        )
        if rq['period'] ==  u'3':
            wiki_body = self.get_wiki_changes_for_period_2018(rq, wikis)
        else:
            wiki_body = []

            for wiki in wikis:
                change = (
                    self.section.wiki_change_cls.query
                    .filter_by(
                        wiki=wiki,
                        active=1,
                    ).first()
                )
                if change:
                    wiki_body.append(change.body)

        return render_template(self.template_name,
                               page_title=self.section.page_title,
                               dataset=rq['period'],
                               wiki_body=wiki_body)


wiki.add_url_rule('/summary/datasheet/',
                  view_func=WikiView
                  .as_view('datasheet', section=DataSheetSection))

wiki.add_url_rule('/summary/audittrail/',
                  view_func=AuditView
                  .as_view('audittrail', section=AuditTrailSection))
