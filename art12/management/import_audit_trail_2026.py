import pandas as pd
import click

from art12 import models

from flask.cli import AppGroup

import_audit_trail_2026 = AppGroup("import_audit_trail_2026")

@import_audit_trail_2026.command("run")
@click.option("-f", "--file", "file")
def run(**kwargs):
    df = pd.read_excel(kwargs["file"])
    df = df.where(pd.notnull(df), "")  # Replace all NaN with None
    data = df.to_dict(orient="records")

    for data_object in data:
        new_wiki_trail = models.WikiTrail(
            dataset_id=4,
            speciescode=data_object["species_scientific_name"],
            reported_name=f"{data_object["species_scientific_name"]} {data_object['subspecific_population']} {data_object['subunit_flyway']}",
            reported_name_code=data_object["species_code"],
        )
        models.db.session.add(new_wiki_trail)
        models.db.session.commit()
    #     import pdb;pdb.set_trace();
    #     new_wiki_trail = models.WikiTrail(
    #         dataset_id=kwargs["id"],
    #         reported_name=data_object["reported_name"],
    #         reported_name_code=data_object["speciescode"],
    #         speciescode=data_object["assessment_speciesname"],
    #     )
    #     models.db.session.add(new_wiki_trail)
    #     models.db.session.commit()
    #     new_wiki_trail_change = models.WikiTrailChange(
    #         body=data_object["merge"],
    #         editor="Admin",
    #         active=1,
    #         dataset_id=kwargs["id"],
    #         wiki=new_wiki_trail,
    #     )
    #     models.db.session.add(new_wiki_trail_change)
    #     models.db.session.commit()
