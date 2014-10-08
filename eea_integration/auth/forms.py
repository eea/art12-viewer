from flask.ext.security import ForgotPasswordForm, ConfirmRegisterForm
from flask.ext.wtf import Form
from wtforms import SelectField, TextField, BooleanField
from wtforms.validators import Optional
from wtforms.widgets import HiddenInput
from flask.ext.security.forms import (
    Required, email_validator, RegisterFormMixin, unique_user_email,
)
from . import auth
from .security import (
    no_ldap_user, custom_unique_user_email, check_duplicate_with_local_db,
    check_duplicate_with_ldap,
)


class CustomEmailTextField(TextField):

    def process_formdata(self, valuelist):
        super(CustomEmailTextField, self).process_formdata(valuelist)
        # if comma or semicolon addresses are provided, consider the first one
        if self.data:
            self.data = self.data.replace(',', ' ').replace(';', ' ').split()[0]


class EeaRegisterFormBase(object):

    name = TextField('Full name',
        validators=[Required("Full name is required")])
    institution = TextField('Institution',
        validators=[Optional()])
    abbrev = TextField('Abbrev.')
    MS = TextField(widget=HiddenInput())
    country_options = SelectField('Member State')
    other_country = TextField('Other country')
    qualification = TextField('Qualification', validators=[Optional()])

    def __init__(self, *args, **kwargs):
        super(EeaRegisterFormBase, self).__init__(*args, **kwargs)
        Dataset = auth.models.Dataset
        #DicCountryCode = models.DicCountryCode
        dataset = (Dataset.query.order_by(Dataset.id.desc()).first())
        # countries = (DicCountryCode.query
        #     .with_entities(DicCountryCode.codeEU, DicCountryCode.name)
        #     .filter(DicCountryCode.dataset_id == dataset.id)
        #     .distinct()
        #     .order_by(DicCountryCode.name)
        #     .all())
        countries = []
        self.country_options.choices = (
            [('', '')] + countries + [('--', 'Choose another country ...')]
        )
        self.obj = kwargs.get('obj', None)


class EeaForgotPasswordForm(ForgotPasswordForm):
    email = TextField(
        label=ForgotPasswordForm.email.args[0],
        validators=ForgotPasswordForm.email.kwargs['validators']
                   + [no_ldap_user],
    )


class EeaAdminEditUserForm(EeaRegisterFormBase, Form):
    active = BooleanField('Active',
                          description='User is allowed to login and gain roles.')
    email = TextField('Email address',
                      validators=[Required("Email is required"),
                                  email_validator,
                                  custom_unique_user_email])


class EeaLDAPRegisterForm(EeaRegisterFormBase, RegisterFormMixin, Form):
    email = TextField('Email address',
                      validators=[Required("Email is required"),
                                  email_validator])


class EeaLocalRegisterForm(EeaRegisterFormBase, ConfirmRegisterForm):
    id = TextField('Username',
                   validators=[Required("User ID is required"),
                               check_duplicate_with_local_db,
                               check_duplicate_with_ldap])

    email = CustomEmailTextField('Email address',
                                 validators=[Required("Email is required"),
                                             email_validator,
                                             unique_user_email])
