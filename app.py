# A very simple Flask Hello World app for you to get started with...


from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

# Crear la app
app= Flask(__name__)

# permitir el acceso al frontend a las rutas de la app del backend
CORS(app)

#configuro la base de datos, con el nombre el usuario y la clave
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://manliowydler2301:python23010@manliowydler23010.mysql.pythonanywhere-services.com/manliowydler2301$default'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)
ma=Marshmallow(app)

class shop_products(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    category=db.Column(db.String(25))
    name=db.Column(db.String(25))
    image=db.Column(db.String(400))
    description=db.Column(db.String(1000))
    descriptionExt=db.Column(db.String(300))
    price=db.Column(db.Float)

    def __init__(self,category,name,image,description,descriptionExt,price):
        self.name=name
        self.category=category
        self.name=name
        self.image=image
        self.description=description
        self.descriptionExt=descriptionExt
        self.price=price

with app.app_context():
    db.create_all()

class shop_productsSchema(ma.Schema):
    class Meta:
        fields=('id','category','name','image','description','descriptionExt','price')

producto_schema=shop_productsSchema()
producto_schema=shop_productsSchema(many=True)


# rutas de los endpoint
#PUT
@app.route('/productos/<id>' ,methods=['PUT'])
def update_producto(id):
    producto=shop_products.query.get(id)
    category=request.json['category']
    name=request.json['name']
    image=request.json['image']
    description=request.json['description']
    descriptionExt=request.json['descriptionExt']
    price=request.json['price']

    producto.category=category
    producto.name=name
    producto.image=image
    producto.description=description
    producto.descriptionExt=descriptionExt
    producto.price=price
    db.session.commit()

    return producto_schema.jsonify(producto)

#get
@app.route('/productos',methods=['GET']) #all products
def get_productos():
    all_productos=shop_products.query.all()
    result=producto_schema.dump(all_productos)
    return jsonify(result)

#get for ID
@app.route('/productos/<id>',methods=['GET'])
def get_producto(id):

    producto=shop_products.query.get(id)
    return producto_schema.jsonify(producto)



#delete
@app.route('/productos/<id>',methods=['DELETE'])
def delete_producto(id):
    # Consultar por id, a la clase Producto.
    #  Se hace una consulta (query) para obtener (get) un registro por id
    producto=shop_products.query.get(id)

    # A partir de db y la sesión establecida con la base de datos borrar
    # el producto.
    # Se guardan lo cambios con commit
    db.session.delete(producto)
    db.session.commit()

#Create
@app.route("/productos", methods=['POST'])
def create_producto():

    category=request.json['category']
    name=request.json['name']
    image=request.json['image']
    description=request.json['description']
    descriptionExt=request.json['descriptionExt']
    price=request.json['price']

    # INSERTAR EN DB
    new_producto = shop_products(category, name, image, description, descriptionExt, price)
    db.session.add(new_producto)
    db.session.commit()

    return producto_schema.jsonify(new_producto)
