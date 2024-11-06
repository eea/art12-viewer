from time import sleep

from flask.cli import AppGroup

from art12 import models
from art12.factsheet import get_factsheet_url, check_if_species_is_non_native


check_factsheets_urls = AppGroup("check_factsheets_urls")


@check_factsheets_urls.command("run")
def run(**kwargs):
    dataset = models.Dataset.query.filter_by(id=1).first()
    model = models.LuDataBird
    lu_data_birds = (
        model.query.filter_by(dataset=dataset)
        .distinct()
        .with_entities(model.speciescode, model.speciesname)
        .order_by(model.speciesname)
        .all()
    )
    for speciescode, speciesname in lu_data_birds:
        sleep(0.1)
        factsheet_url = get_factsheet_url(speciescode, dataset)
        if not factsheet_url and not check_if_species_is_non_native(
            speciescode, dataset
        ):
            print(f"Missing factsheet for {speciescode} - {speciesname}")
        else:
            print(f"Factsheet for {speciescode} - {speciesname} is OK")

