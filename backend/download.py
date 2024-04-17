import csv
import os

from sqlalchemy import select

from database import LocalSession
from src.models import Ingredient, Tag

MODEL_CSV = {
    'ingredients.csv': Ingredient,
    'tags.csv': Tag,
}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_or_create(session, model, **kwargs):
    statement = select(model).filter_by(**kwargs)
    instance = session.scalar(statement)
    if not instance:
        instance = model(**kwargs)
        session.add(instance)

    return instance


def handle(session):
    for file, model in MODEL_CSV.items():
        csv_file = os.path.join(
            os.path.join(BASE_DIR, 'data'),
            file,
        )
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            if model == Ingredient:
                for row in reader:
                    name, measurement_unit = row
                    get_or_create(
                        session,
                        model,
                        name=name,
                        measurement_unit=measurement_unit,
                    )
            else:
                for row in reader:
                    name, color, slug = row
                    get_or_create(
                        session,
                        model,
                        name=name,
                        color=color,
                        slug=slug,
                    )
            session.commit()


if __name__ == "__main__":
    session = LocalSession()
    handle(session)
