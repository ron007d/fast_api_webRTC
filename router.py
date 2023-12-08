from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import uvicorn



app = FastAPI()
templates = Jinja2Templates('templates')

testing_dict = {'Call' : {'url':'call_page'},
                'answer' : {'url': 'answer_page'}}


@app.get('/')
def home(request : Request):
    # print(request.url)
    return templates.TemplateResponse('home.html',{"request" : request, 'data': testing_dict })

@app.get('/call_page')
def call_page(request: Request):
    return {'Message' : f'you have came to URL page {request.url}'}

@app.post('offer_data')
def saving_offers(user_name, offer):
    print(user_name)
    print(offer)
    return {'success' : True}


@app.get('/answer_page')
def answer_page(request: Request):
    return {'Message' : f'you have came to URL page {request.url}'}





if __name__ == '__main__':
    uvicorn.run('router:app', host='0.0.0.0', port= 8080,reload= True, workers= 2)