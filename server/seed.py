from models import db, Hero, HeroPower, Power
from app import app
from faker import Faker
import random

# instantite Faker
fake = Faker()


# function to seed database with sample data
def seed_database():
    # clear existing data in tables
    Hero.query.delete()
    HeroPower.query.delete()
    Power.query.delete()

    heroes = []
    for _ in range(10):
        # generate and add 10 Hero instances to heroes
        hero = Hero(
            name=fake.unique.name(),
            super_name=fake.word()
        )

        heroes.append(hero)

    db.session.add_all(heroes)

    strengths = ["Strong", "Weak", "Average"]
    heropowers = []
    for _ in range(10):
        # generate and add 10 HeroPower instances to heropowers
        heropower = HeroPower(
            strength=random.choice(strengths),
            hero_id=random.randint(1, 10),
            # hero_id=random.randint(range(1, len(heroes)+1)),
            power_id=random.randint(1, 10)
        )

        heropowers.append(heropower)

    db.session.add_all(heropowers)

    powers = []
    for _ in range(10):
        # generate and add 10 Power instances to powers
        power = Power(
            name=fake.unique.name(),
            description=fake.text(max_nb_chars=50)
        )

        powers.append(power)

    db.session.add_all(powers)

    db.session.commit()


# execute only if run/not if imported
if __name__ == "__main__":
    with app.app_context():
        # run function within app context
        seed_database()
