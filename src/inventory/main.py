from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
from redis_creds import HOST, PASSWORD, PORT

redis = get_redis_connection(
    host= HOST,
    port=PORT,
    password=PASSWORD,
    decode_responses=True
)


class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis



app = FastAPI()

#allows frontend from running on different port without browser causing problems
#allows frontend to request APIs, fronend running on port 3000
app.add_middleware(CORSMiddleware,
                   allow_origins= ["http://localhost:3000"],
                   allow_methods= ["*"],
                   allow_headers= ["*"])


@app.get("/")
async def root():
    return {'message': "hello world"}


@app.get("/products")
def all_products():
    return [format(pk) for pk in Product.all_pks()]

# pass a primary key and get the product variables
def format(pk: str):
    product = Product.get(pk)
    return {
        'id': product.pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity
    }


@app.post("/products")
def create(product: Product):
    return product.save()

@app.get("/products/{primary_key}")
def get(primary_key:str):
    product = Product.get(primary_key)
    return {
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity
    }

@app.delete("/products/{primary_key}")
def delete(primary_key: str):
    product = Product.get(primary_key)
    product.delete(primary_key)
    return {'message': 'deleted product with pk: {}'.format(primary_key)}
