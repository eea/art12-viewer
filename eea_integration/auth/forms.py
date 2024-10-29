from flask_security import ForgotPasswordForm, ConfirmRegisterForm
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, BooleanField
from wtforms.validators import Optional, Email
from wtforms.widgets import HiddenInput

from flask_security.forms import (
    Required,
    RegisterFormMixin,
    unique_user_email,
)

# from .auth import auth
from .security import (
    no_ldap_user,
    custom_unique_user_email,
    check_duplicate_with_local_db,
    check_duplicate_with_ldap,
)


class CustomEmailStringField(StringField):
    def process_formdata(self, valuelist):
        super(CustomEmailStringField, self).process_formdata(valuelist)
        # if comma or semicolon addresses are provided, consider the first one
        if self.data:
            self.data = self.data.replace(",", " ").replace(";", " ").split()[0]


class EeaRegisterFormBase(object):

    name = StringField("Full name", validators=[Required("Full name is required")])
    institution = StringField("Institution", validators=[Optional()])
    abbrev = StringField("Abbrev.")
    MS = StringField(widget=HiddenInput())
    country_options = SelectField("Member State")
    other_country = StringField("Other country")
    qualification = StringField("Qualification", validators=[Optional()])

    def __init__(self, *args, **kwargs):
        super(EeaRegisterFormBase, self).__init__(*args, **kwargs)
        # Dataset = auth.models.Dataset
        # DicCountryCode = models.DicCountryCode
        # dataset = Dataset.query.order_by(Dataset.id.desc()).first()
        # countries = (DicCountryCode.query
        #     .with_entities(DicCountryCode.codeEU, DicCountryCode.name)
        #     .filter(DicCountryCode.dataset_id == dataset.id)
        #     .distinct()
        #     .order_by(DicCountryCode.name)
        #     .all())
        countries = []
        self.country_options.choices = (
            [("", "")] + countries + [("--", "Choose another country ...")]
        )
        self.obj = kwargs.get("obj", None)


class EeaForgotPasswordForm(ForgotPasswordForm):
    email = StringField(
        label=ForgotPasswordForm.email.args[0],
        validators=ForgotPasswordForm.email.kwargs["validators"] + [no_ldap_user],
    )


class EeaAdminEditUserForm(EeaRegisterFormBase, FlaskForm):
    active = BooleanField(
        "Active", description="User is allowed to login and gain roles."
    )
    email = StringField(
        "Email address",
        validators=[
            Required("Email is required"),
            Email("Invalid email address"),
            custom_unique_user_email,
        ],
    )


class EeaLDAPRegisterForm(EeaRegisterFormBase, RegisterFormMixin, FlaskForm):
    email = StringField(
        "Email address",
        validators=[
            Required("Email is required"),
            Email("Invalid email address"),
        ],
    )


class EeaLocalRegisterForm(EeaRegisterFormBase, ConfirmRegisterForm):
    id = StringField(
        "Username",
        validators=[
            Required("User ID is required"),
            check_duplicate_with_local_db,
            check_duplicate_with_ldap,
        ],
    )

    email = CustomEmailStringField(
        "Email address",
        validators=[
            Required("Email is required"),
            Email("Invalid email address"),
            unique_user_email,
        ],
    )
