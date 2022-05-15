from faker import Faker


def get_fake_infos():
    fake = Faker(["pt_BR"])
    infos = {
        '👤 Nome': fake.name(),
        '📍 Endereço': fake.administrative_unit(),
        '📅 Nascimento': fake.date(end_datetime='-15y'),
        '💼 Profissão': fake.job(),
        '💵 Salário': fake.pricetag(),
        '✒️ ': f'"{fake.catch_phrase()}"'
    }

    return infos
