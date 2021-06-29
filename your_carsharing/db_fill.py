from app import db
from app.models import Car


# создаем экземпляр класса Car
new_car = Car(name="BMW")

# добавляем изменения в базу данных (при этом база не сохраняется)
db.session.add(new_car)

# сохраняем изменения в базе
db.session.commit()
