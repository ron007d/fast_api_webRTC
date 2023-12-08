from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import uvicorn



app = FastAPI()
templates = Jinja2Templates('templates')

testing_dict = {'Call' : {'url':'call_page'},
                'answer' : {'url': 'answer_page'}}

offers = {}

@app.get('/')
def home(request : Request):
    # print(request.url)
    return templates.TemplateResponse('home.html',{"request" : request, 'data': testing_dict })

@app.get('/call_page')
def call_page(request: Request):
    # return {'Message' : f'you have came to URL page {request.url}'}
    return templates.TemplateResponse('call_page.html',{'request':request, "offer_url" : "saving_offers"})

@app.post('/offer_data')
def saving_offers(request: Request,user_name, offer):
    print(user_name)
    print(offer)
    print(type(offer))
    offers[user_name] = {'offer': offer}
    return {'success' : True}

@app.get('/anser_data/{user_name}')
def answer_data(user_name):
    if user_name not in offers:
        return {'success' : False,'user_name':user_name}
    else:
        return {'success': True,'user_name':user_name,'answer':offers[user_name]['answer']}


@app.get('/get_offers')
def get_offers():
    return offers
@app.get('/get_offers/{user_name}')
def get_offers(user_name,request: Request):
    print(user_name)
    return {'Message' : f'you have came to URL page {request.url}'}


@app.get('/answer_page')
def answer_page(request: Request):
    return {'Message' : f'you have came to URL page {request.url}'}





if __name__ == '__main__':
    uvicorn.run('router:app', host='0.0.0.0', port= 8080,reload= True, workers= 2)