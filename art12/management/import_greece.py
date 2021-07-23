from art12 import models
from flask.cli import AppGroup

import_greece = AppGroup("import_greece")


@import_greece.command("run")
def run(**kwargs):
    speciescodes = [
        data.speciescode
        for data in models.EtcDataBird.query.all()
        if data.dataset_id == 2 and data.country_isocode == "GR"
    ]

    for speciescode in speciescodes:
        ludatabird = models.LuDataBird.query.filter_by(speciescode=speciescode).first()
        if not models.LuDataBird.query.filter_by(
            speciescode=ludatabird.speciescode, dataset_id=2
        ).all():
            new_ludatabird = models.LuDataBird(
                speciescode=ludatabird.speciescode,
                speciesname=ludatabird.speciesname,
                dataset_id=2,
            )
            models.db.session.add(new_ludatabird)
            models.db.session.commit()
