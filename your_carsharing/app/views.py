from app import app, db
from app.models import Car
from flask import render_template, request, redirect, url_for
from datetime import datetime


@app.route('/index')
@app.route('/')
def index():
    

    # Получаем все записи из таблицы Car
    car_list = Car.query.all()

    # Полученные наборы передаем в контекст
    context = {
        
        'car_list': car_list
    }

    return render_template('index.html', **context)
   


@app.route('/rental_log', methods=['POST', 'GET'])
def rental_log():
    return render_template('rental_log.html')




@app.route('/auto_detail/<int:car_id>', methods=[ 'POST','GET'])
def auto_deatail(car_id):

    # Получаем все записи из таблицы Car
    car = Car.query.get(car_id)
    rent=''
    rental_start_list = []
    rental_finish_list = []
    price_list = []
    price_rent = 0

    age = datetime.now().date() 
    context = None
    context_table = None
   
    price_rent = 0
    #Если метод пост
    if request.method == 'POST':
        #получаем значение из формы (кнопки) с названием Rent (Арендовать или Вернуть)
        # И добавляем эту ифнормацию в новую переменную new_rent 
        new_rent = request.form['Rent']
        #Если мы получаем переменную new_rent, мы проверяем, несёт ли она в себе 
        #значение "Арендовать", если да, мы присваеваем полю модели car.rent значение True
        #Если нет, то присваеваем значение False
        if new_rent:
            car.rent = True if new_rent == 'Арендовать' else False  
            #Если кнопка несёт в себе значение Арендовать, мы добовляем дату, в список "дат начала аренды"
            if  new_rent == 'Арендовать':
                rental_start_list.append(age)
            #Иначе мы добовляем дату в список "дат окончаия Аренды", расчитываем стоимость, так же доболвяем её в список "стоимостей"
            if  car.rent == False:
                rental_finish_list.append(age)
                price_rent = ((datetime.now().date() - age).seconds) // 60
                price_rent = car.price * price_rent 
                price_list.append(price_rent)
            #Создаём переменную rent, со значением "Вернуть", car.rent равно True, 
            #со значением "Арендовать", если car.rent равно False
            
        # сохраняем изменения в базе
        db.session.commit()
    rent = 'Вернуть' if car.rent == True else 'Арендовать'   
    in_rent_or_free = 'Занята' if car.rent == True else 'Свободна'
   
    
  
    # Полученные наборы передаем в контекст
    context = {
    'id': car.id,
    'title': car.name,
    'price': car.price,
    'transmission': car.transmission,
    'description': car.description,
    'rent': rent,
    'in_rent_or_free': in_rent_or_free
    }
    context_table = {
        'age': age,
        'price_rent': price_rent,
        'start_rent':  car.created,
        'rental_start_list': rental_start_list,
        ' rental_finish_list': rental_finish_list,
        ' price_list':  price_list

    }
        

    return render_template('auto_detail.html', **context, **context_table)


@app.route('/auto_detail/<int:car_id>', methods=['POST', 'GET'])
def del_product(product_id):
    
    car = Car.query.get(car_id)

    context = {
        'title': car.name,
        'price': car.price
        
    }
    
    db.session.delete(car)
    db.session.commit()

    return render_template('index.html', **context)



@app.route('/create_auto', methods=['POST', 'GET'])
def create_auto():

    context = None

    if request.method == 'POST':
        # Пришел запрос с методом POST (пользователь нажал на кнопку 'Добавить товар')
        # Получаем название товара - это значение поля input с атрибутом name="title"

        auto_name = request.form['name']

        auto_price = request.form['price'] 

        auto_description = request.form['description'] 

        auto_transmission = request.form['transmission']

        if auto_transmission: 
            auto_transmission = True if auto_transmission == 'ДА' else False

        # Добавляем товар в базу данных
        db.session.add(Car(name=auto_name, price=auto_price, description = auto_description, transmission = auto_transmission))

        # сохраняем изменения в базе
        db.session.commit()

        # Заполняем словарь контекста
        context = {
            'name': auto_name,
            'price': auto_price,
            'description ': auto_description,
            'transmission': auto_transmission
        }

    
        return redirect(url_for('index'))


    return render_template('create_auto.html')




