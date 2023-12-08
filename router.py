from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import uvicorn



app = FastAPI()
templates = Jinja2Templates('templates')

testing_dict = {'Call' : {'url':'google.com'},
                'answer' : {'url': 'duckduckgo.com'}}


@app.get('/')
def home(request : Request):
    print(request.url)
    return templates.TemplateResponse('home.html',{"request" : request, 'data': testing_dict })





if __name__ == '__main__':
    uvicorn.run('router:app', host='0.0.0.0', port= 8080,reload= True, workers= 2)