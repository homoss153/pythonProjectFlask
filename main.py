import flask
from flask import Flask, request, jsonify, json
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
db = SQLAlchemy(app)




class Transfer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    type_transfer = db.Column(db.Integer)
    name = db.Column(db.String)
    description = db.Column(db.String)
    price = db.Column(db.Integer)
    date_time = db.Column(db.String)
    icon = db.Column(db.String)
    category = db.Column(db.String)
    payment_name = db.Column(db.String)

    def __repr__(self):
        return '<Transfer %r>' % self.username

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'type_transfer': self.type_transfer,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "date_time": self.date_time,
            "icon": self.icon,
            "category": self.category,
            "payment_name": self.payment_name
        }


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    password = db.Column(db.String)
    name = db.Column(db.String)

    def __repr__(self):
        return '%r>' % self.id

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'user_id': self.id,
            'name': self.name
        }


class UserPayment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    payment_name = db.Column(db.String)
    payment_balance = db.Column(db.Integer)
    payment_type = db.Column(db.Integer)   # 1 - Наличка 2 - Банковская карта
    bank_icon = db.Column(db.Integer)


    def __repr__(self):
        return '%r>' % self.id

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'payment_name': self.payment_name,
            'payment_balance': self.payment_balance,
            'payment_type': self.payment_type,
            'bank_icon': self.bank_icon
        }



@app.route('/create_transfer', methods=['POST'])
def create_transfer():
    content = json.loads(request.json)

    user_id = content['user_id']
    type_transfer = content['type_transfer']
    name = content['name']
    description = content['description']
    price = content['price']
    date_time = content['date_time']
    icon = content['icon']
    category = content['category']
    payment_name = content['payment_name']
    transfer = Transfer(user_id=user_id, type_transfer=type_transfer, name=name, description=description, price=price, date_time=date_time, icon=icon, category=category, payment_name=payment_name)
    UserPayment.query.filter_by(payment_name=payment_name).first().payment_balance += price
    try:
        db.session.add(transfer)
        db.session.commit()
        resp = jsonify(success=True)
        return resp
    except:
        resp = jsonify()
        resp.status_code = 400
        return resp

@app.route('/get_transfer', methods=['POST'])
def get_transfer():

    content = json.loads(request.json)
    print(content)
    user_id = content['user_id']
    print(user_id)

    ret = [i.serialize for i in Transfer.query.filter(Transfer.user_id == user_id)]
    if ret:
        return jsonify(ret)
    else:
        return "no"


@app.route('/get_payment', methods=['POST'])
def get_payment():

    content = json.loads(request.json)
    print(content)
    user_id = content['user_id']
    print(user_id)

    ret = [i.serialize for i in UserPayment.query.filter(UserPayment.user_id == user_id)]
    if ret:
        return jsonify(ret)
    else:
        return "no"


@app.route('/del_payment', methods=['POST'])
def del_payment():

    content = json.loads(request.json)
    print(content)
    user_id = content['user_id']
    payment_name = content['payment_name']
    payment_balance = content['payment_balance']
    bank_icon = content['bank_icon']

    UserPayment.query.filter_by(user_id=user_id, payment_name=payment_name, payment_balance=payment_balance, bank_icon=bank_icon).delete()
    Transfer.query.filter_by(payment_name=payment_name).delete()
    db.session.commit()
    resp = jsonify()
    resp.status_code = 200
    return resp

@app.route('/del_transfer', methods=['POST'])
def del_transfer():

    content = json.loads(request.json)
    print(content)
    user_id = content['user_id']
    payment_name = content['payment_name']
    date = content['date']
    category = content['category']
    price = content['price']

    Transfer.query.filter_by(user_id=user_id, payment_name=payment_name, date_time=date, price=price, category=category).delete()
    try:
        UserPayment.query.filter_by(payment_name=payment_name).first().payment_balance -= price
    except:
        pass
    db.session.commit()
    resp = jsonify()
    resp.status_code = 200
    return resp


@app.route('/get_user', methods=['GET'])
def get_user():
    #content = request.get_json()
    #user_id = content['user_id']
    print(User.query.filter(User.email=="test").first().password)
    return "ad"
    #return jsonify(json_list=[i.serialize for i in User.query.all()])


@app.route('/login', methods=['POST'])
def login():
    content = json.loads(request.json)
    email = content['email']
    password = content['password']
    print(content)
    #print(User.query.filter(User.email==email, User.password==password).first().id)
    if (User.query.filter(User.email==email, User.password==password).first()):
        user = User.query.filter(User.email == email, User.password == password).first()
        resp = jsonify()
        resp.status_code = 200
        print(user)
        data = {'user_id': user.id, 'name': user.name}
        resp.data = data
        ret = [i.serialize for i in User.query.filter(User.email == email, User.password == password).first()]

        return jsonify(ret)
    else:
        return "no"


    #return jsonify(json_list=[i.serialize for i in User.query.all()])


@app.route('/create_user', methods=['POST'])
def create_user():
    content = json.loads(request.json)
    email = content['email']
    password = content['password']
    name = content['name']
    user = User(email=email, password=password, name=name)
    if User.query.filter(User.email == email).first():
        return "email"
    else:
        try:
            db.session.add(user)
            db.session.commit()
            resp = jsonify()
            resp.status_code = 200
            print(user)
            data = {'user_id': user.id}
            #resp.data = data
            print(user.id)
            #return jsonify(data), 200
            return str(user.id)
        except:
            resp = jsonify()
            resp.status_code = 400
            return resp


@app.route('/add_payment', methods=['POST'])
def add_payment():
    content = json.loads(request.json)

    user_id = content['user_id']
    print(user_id)
    payment_name = content['payment_name']
    payment_balance = content['payment_balance']
    payment_type = content['payment_type']  # 1 - Наличка 2 - Банковская карта
    bank_icon = content['bank_icon']

    user = UserPayment(user_id=user_id, payment_balance=payment_balance, payment_name=payment_name, payment_type=payment_type, bank_icon=bank_icon)

    try:
        db.session.add(user)
        db.session.commit()
        resp = jsonify()
        resp.status_code = 200
        return resp
    except:
        resp = jsonify()
        resp.status_code = 400
        return resp


@app.route('/')
def main_route():
    return flask.render_template('PrivacyPolicy.htm')


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, port=80)
