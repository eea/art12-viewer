import os

from flask import abort, flash, current_app, request, redirect, url_for
from flask_admin import Admin, AdminIndexView, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from art12.common import admin_perm
from art12.models import (
    Config,
    Dataset,
    EtcBirdsEu,
    EtcDataBird,
    LuDataBird,
    LuRestrictedDataBird,
    Wiki,
    WikiChange,
    WikiTrail,
    WikiTrailChange,
    db,
)
from werkzeug.utils import secure_filename


class CustomAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self):
        if not admin_perm.can():
            return abort(404)
        return super(CustomAdminIndexView, self).index()


class ProtectedModelView(ModelView):

    def is_accessible(self):
        return admin_perm.can()

    def inaccessible_callback(self, name, **kwargs):
        return abort(404)


class DatasetModelView(ProtectedModelView):
    can_export = True
    column_list = [
        "id",
        "name",
    ]
    column_export_list = [
        "id",
        "name",
    ]
    column_sortable_list = [
        "id",
        "name",
    ]


class ConfigModelView(ProtectedModelView):
    column_list = (
        "id",
        "default_dataset_id",
        "species_map_url",
        "sensitive_species_map_url",
    )
    column_filters = ["id", "default_dataset_id"]


class EtcBirdsEuModelView(ProtectedModelView):
    can_export = True
    can_set_page_size = True
    column_filters = ["speciescode", "speciesname", "dataset_id"]
    column_searchable_list = ["speciescode", "speciesname"]
    column_list = [
        "id",
        "dataset_id",
        "speciescode",
        "speciesname",
        "assessment_speciescode",
        "assessment_speciesname",
        "euringcode",
        "decision",
    ]
    column_sortable_list = [
        "id",
        "dataset_id",
        "speciescode",
        "speciesname",
        "assessment_speciescode",
        "assessment_speciesname",
        "euringcode",
        "decision",
    ]
    column_export_list = [
        "id",
        "speciescode",
        "speciesname",
        "reported_name",
        "speciesname_subpopulation",
        "assessment_speciescode",
        "assessment_speciesname",
        "assessment_subpopulation",
        "euringcode",
        "non_native",
        "br_range_surface_area",
        "br_range_surface_area_downrounded",
        "br_range_trend",
        "br_range_trend_long",
        "br_population_size",
        "br_distribution_surface_area",
        "br_distribution_trend",
        "br_distribution_trend_long",
        "br_population_minimum_size",
        "br_population_minimum_size_downrounded",
        "br_population_maximum_size",
        "br_population_maximum_size_uprounded",
        "br_population_size_unit",
        "br_population_trend",
        "br_population_trend_long",
        "br_conclusion_status_label",
        "br_contribution_target1",
        "br_red_list_cat",
        "wi_population_size",
        "wi_population_minimum_size",
        "wi_population_minimum_size_downrounded",
        "wi_population_maximum_size",
        "wi_population_maximum_size_uprounded",
        "wi_population_size_unit",
        "wi_population_trend",
        "wi_population_trend_long",
        "wi_conclusion_status_label",
        "wi_contribution_target1",
        "wi_red_list_cat",
        "conclusion_status_label",
        "conclusion_status_improving",
        "conclusion_status_br_wi",
        "conclusion_status_level1_record",
        "conclusion_status_level1",
        "conclusion_status_level2_record",
        "conclusion_status_level2",
        "conclusion_population_size_unit",
        "conclusion_population_minimum_size",
        "conclusion_population_minimum_size_downrounded",
        "conclusion_population_maximum_size",
        "conclusion_population_maximum_size_uprounded",
        "conclusion_population_trend",
        "conclusion_population_trend_long",
        "contribution_target1",
        "contribution_target1_label",
        "user",
        "last_update",
        "deleted_record",
        "decision",
        "user_decision",
        "last_update_decision",
        "addtionnal_record",
        "dataset_id",
        "use_for_statistics",
        "conclusion_status_label_prev",
        "conclusion_status_br_wi_prev",
        "red_list_cat_prev",
    ]


class EtcDataBirdModelView(ProtectedModelView):
    can_export = True
    can_set_page_size = True
    column_filters = [
        "dataset_id",
        "country",
        "group",
    ]
    column_searchable_list = [
        "speciescode",
        "speciesname",
        "subspecies_name",
        "eunis_species_code",
        "alternative_speciesname",
        "common_speciesname",
        "valid_speciesname",
        "n2000_species_code",
        "assessment_speciescode",
        "assessment_speciesname",
        "assessment_speciesname_changed",
    ]
    column_list = [
        "country",
        "group",
        "dataset_id",
        "euringcode",
        "code",
        "speciescode",
        "speciesname",
        "species_name_different",
        "subspecies_name",
        "eunis_species_code",
        "alternative_speciesname",
        "common_speciesname",
        "valid_speciesname",
        "n2000_species_code",
        "assessment_speciescode",
        "assessment_speciesname",
        "assessment_speciesname_changed",
    ]
    column_sortable_list = [
        "country",
        "group",
        "dataset_id",
        "euringcode",
        "code",
        "speciescode",
        "speciesname",
        "species_name_different",
        "subspecies_name",
        "eunis_species_code",
        "alternative_speciesname",
        "common_speciesname",
        "valid_speciesname",
        "n2000_species_code",
        "assessment_speciescode",
        "assessment_speciesname",
        "assessment_speciesname_changed",
    ]

    column_export_list = [
        "country",
        "country_isocode",
        "delivery",
        "envelope",
        "filename",
        "reported_name",
        "group",
        "family",
        "annex",
        "priority",
        "redlist",
        "euringcode",
        "code",
        "speciescode",
        "speciesname",
        "species_name_different",
        "subspecies_name",
        "eunis_species_code",
        "alternative_speciesname",
        "common_speciesname",
        "valid_speciesname",
        "n2000_species_code",
        "assessment_speciescode",
        "assessment_speciesname",
        "assessment_speciesname_changed",
        "grouped_assesment",
        "species_type",
        "species_type_asses",
        "range_surface_area_bs",
        "range_change_reason_bs",
        "percentage_range_surface_area_bs",
        "range_additional_info_record_bs",
        "range_additional_info_bs",
        "range_trend_period_bs",
        "range_trend_bs",
        "range_trend_magnitude_min_bs",
        "range_trend_magnitude_max_bs",
        "range_trend_long_period_bs",
        "range_trend_long_bs",
        "range_trend_long_magnitude_min_bs",
        "range_trend_long_magnitude_max_bs",
        "range_trend_additional_info_record_bs",
        "range_trend_additional_info_bs",
        "range_yearly_magnitude_bs",
        "complementary_favourable_range_op_bs",
        "complementary_favourable_range_bs",
        "population_minimum_size_bs",
        "percentage_population_minimum_size_bs",
        "population_maximum_size_bs",
        "percentage_population_maximum_size_bs",
        "population_size_bs",
        "population_size_method_bs",
        "filled_population_bs",
        "population_size_unit_bs",
        "population_units_agreed_bs",
        "population_units_other_bs",
        "population_estimateType_bs",
        "population_change_reason_bs",
        "number_of_different_population_units_bs",
        "different_population_percentage_bs",
        "percentage_population_mean_size_bs",
        "population_additional_info_record_bs",
        "population_additional_info_bs",
        "population_trend_period_bs",
        "population_trend_bs",
        "population_trend_magnitude_min_bs",
        "population_trend_magnitude_max_bs",
        "population_trend_magnitude_bs",
        "population_trend_long_period_bs",
        "population_trend_long_bs",
        "population_trend_long_magnitude_min_bs",
        "population_trend_long_magnitude_max_bs",
        "population_trend_long_magnitude_bs",
        "population_trend_additional_info_record_bs",
        "population_trend_additional_info_bs",
        "population_yearly_magnitude_bs",
        "complementary_favourable_population_op_bs",
        "complementary_favourable_population_bs",
        "filled_complementary_favourable_population_bs",
        "distribution_surface_area_bs",
        "distribution_surface_area_method_bs",
        "distribution_additional_info_record_bs",
        "distribution_additional_info_bs",
        "percentage_distribution_surface_area_bs",
        "distribution_trend_period_bs",
        "distribution_trend_bs",
        "distribution_trend_magnitude_min_bs",
        "distribution_trend_magnitude_max_bs",
        "distribution_trend_magnitude_bs",
        "distribution_trend_long_period_bs",
        "distribution_trend_long_bs",
        "distribution_trend_long_magnitude_min_bs",
        "distribution_trend_long_magnitude_max_bs",
        "distribution_trend_long_magnitude_bs",
        "distribution_trend_additional_info_record_bs",
        "distribution_trend_additional_info_bs",
        "population_minimum_size_ws",
        "percentage_population_minimum_size_ws",
        "population_maximum_size_ws",
        "percentage_population_maximum_size_ws",
        "population_size_ws",
        "population_size_method_ws",
        "filled_population_ws",
        "population_size_unit_ws",
        "population_units_agreed_ws",
        "population_units_other_ws",
        "population_estimateType_ws",
        "population_change_reason_ws",
        "number_of_different_population_units_ws",
        "different_population_percentage_ws",
        "percentage_population_mean_size_ws",
        "population_additional_info_record_ws",
        "population_additional_info_ws",
        "population_trend_period_ws",
        "population_trend_ws",
        "population_trend_magnitude_min_ws",
        "population_trend_magnitude_max_ws",
        "population_trend_magnitude_ws",
        "population_trend_long_period_ws",
        "population_trend_long_ws",
        "population_trend_long_magnitude_min_ws",
        "population_trend_long_magnitude_max_ws",
        "population_trend_long_magnitude_ws",
        "population_trend_additional_info_record_ws",
        "population_trend_additional_info_ws",
        "status_ws",
        "presence_bs",
        "presence_ws",
        "future_prospects",
        "conclusion_range_bs",
        "conclusion_population_bs",
        "conclusion_population_ws",
        "conclusion_future",
        "conclusion_assessment",
        "conclusion_assessment_trend",
        "conclusion_assessment_prev",
        "conclusion_assessment_change",
        "range_quality_bs",
        "range_trend_quality_bs",
        "range_trend_long_quality_bs",
        "population_quality_bs",
        "population_trend_quality_bs",
        "population_trend_long_quality_bs",
        "population_quality_ws",
        "population_trend_quality_ws",
        "population_trend_long_quality_ws",
        "further_information",
        "further_information_english",
        "range_grid_area",
        "percentage_range_grid_area",
        "distribution_grid_area",
        "percentage_distribution_grid_area",
        "use_for_statistics",
        "dataset_id",
    ]


class LuDataBirdModelView(ProtectedModelView):
    can_export = True
    can_set_page_size = True
    column_filters = ["speciescode", "speciesname", "dataset_id"]
    column_searchable_list = ["speciescode", "speciesname"]
    column_sortable_list = [
        "dataset_id",
        "speciescode",
        "speciesname",
    ]
    column_list = [
        "dataset_id",
        "speciescode",
        "speciesname",
    ]
    column_export_list = [
        "dataset_id",
        "speciescode",
        "speciesname",
    ]


class LuRestrictedDataBirdModelView(ProtectedModelView):
    can_export = True
    can_set_page_size = True
    column_filters = ["speciescode", "country", "dataset_id"]
    column_searchable_list = ["speciescode", "country"]

    column_sortable_list = [
        "speciescode",
        "country",
        "show_data",
        "dataset_id",
    ]
    column_list = [
        "speciescode",
        "country",
        "show_data",
        "dataset_id",
    ]
    column_export_list = [
        "speciescode",
        "country",
        "show_data",
        "dataset_id",
    ]


class WikiModelView(ProtectedModelView):
    can_export = True
    can_set_page_size = True
    column_filters = ["speciescode", "dataset_id"]
    column_searchable_list = ["speciescode"]
    column_sortable_list = [
        "id",
        "speciescode",
        "dataset_id",
    ]
    column_list = [
        "id",
        "speciescode",
        "dataset_id",
    ]
    column_export_list = [
        "id" "speciescode",
        "dataset_id",
    ]


class WikiChangeModelView(ProtectedModelView):
    can_export = True
    can_set_page_size = True
    column_filters = ["dataset_id"]
    column_sortable_list = [
        "id",
        "wiki_id",
        "body",
        "editor",
        "changed",
        "active",
        "dataset_id",
    ]
    column_list = [
        "id",
        "wiki_id",
        "body",
        "editor",
        "changed",
        "active",
        "dataset_id",
    ]
    column_export_list = [
        "id",
        "wiki_id",
        "body",
        "editor",
        "changed",
        "active",
        "dataset_id",
    ]


class WikiTrailModelView(ProtectedModelView):
    can_export = True
    can_set_page_size = True
    column_filters = ["dataset_id"]
    column_sortable_list = [
        "id",
        "speciescode",
        "reported_name",
        "reported_name_code",
        "dataset_id",
    ]
    column_list = [
        "id",
        "speciescode",
        "reported_name",
        "reported_name_code",
        "dataset_id",
    ]
    column_export_list = [
        "id",
        "speciescode",
        "reported_name",
        "reported_name_code",
        "dataset_id",
    ]


class WikiTrailChangeModelView(ProtectedModelView):
    can_export = True
    can_set_page_size = True
    column_filters = ["dataset_id", "wiki_id"]
    column_sortable_list = [
        "id",
        "wiki_id",
        "body",
        "editor",
        "changed",
        "active",
        "dataset_id",
    ]
    column_list = [
        "id",
        "wiki_id",
        "body",
        "editor",
        "changed",
        "active",
        "dataset_id",
    ]
    column_export_list = [
        "id",
        "wiki_id",
        "body",
        "editor",
        "changed",
        "active",
        "dataset_id",
    ]


class FileUploadView(BaseView):

    @expose("/", methods=("GET", "POST"))
    def index(self):
        if not admin_perm.can():
            return abort(404)

        if request.method == "POST" and "file" in request.files:
            f = request.files["file"]
            if f.filename == "":
                flash("No file selected", "error")
                return redirect(url_for(".index"))

            filename = secure_filename(f.filename)
            upload_dir = current_app.config.get("UPLOAD_FOLDER", "uploads")
            os.makedirs(upload_dir, exist_ok=True)
            filepath = os.path.join(upload_dir, filename)
            f.save(filepath)
            flash(f"File uploaded to {filepath}", "success")
            return redirect(url_for(".index"))

        return self.render("admin/upload.html")


def admin_register(app):
    admin = Admin(
        app,
        name="Article 12",
        template_mode="bootstrap3",
        index_view=CustomAdminIndexView(),
    )
    admin.add_view(ConfigModelView(Config, db.session))
    admin.add_view(DatasetModelView(Dataset, db.session))
    admin.add_view(EtcBirdsEuModelView(EtcBirdsEu, db.session))
    admin.add_view(EtcDataBirdModelView(EtcDataBird, db.session))
    admin.add_view(LuDataBirdModelView(LuDataBird, db.session))
    admin.add_view(LuRestrictedDataBirdModelView(LuRestrictedDataBird, db.session))
    admin.add_view(WikiModelView(Wiki, db.session, name="Wiki", endpoint="wiki_admin"))
    admin.add_view(
        WikiChangeModelView(
            WikiChange, db.session, name="Wiki Changes", endpoint="wikichange_admin"
        )
    )
    admin.add_view(
        WikiTrailModelView(
            WikiTrail, db.session, name="Wiki Trails", endpoint="wikitrail_admin"
        )
    )
    admin.add_view(
        WikiTrailChangeModelView(
            WikiTrailChange,
            db.session,
            name="Wiki Trail Changes",
            endpoint="wikitrailchange_admin",
        )
    )
    # register non-model upload view

    admin.add_view(
        FileUploadView(name="Upload File", endpoint="file_upload", category="Utilities")
    )


# Wiki
# WikiChange
# WikiTrail
# WikiTrailChange
# RegisteredUser
# Role
