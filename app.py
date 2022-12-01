import requests
import csv
from flask import Flask, render_template,request

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()
rates_list=list()
codes=list()

with open ("rates.csv", "w") as csvfile:
    fieldnames=['currency','code','bid','ask']
    csvwriter=csv.DictWriter(csvfile,fieldnames=fieldnames, delimiter=';')
    csvwriter.writeheader()
    for element in data:
        rates=(element['rates'])
        for element in rates:
           csvwriter.writerow(element)
           codes.append((element['code']))

app=Flask(__name__)

@app.route("/",methods=['GET','POST'])
def index():
    codes_v2=codes
    
    if request.method == 'GET':
        return render_template('index.html', codes_v2=codes_v2)
    
    elif request.method == "POST":
        result=None
        quantity=request.form['quantity']
        selected=request.form['code']
        
        for element in rates:
            if element['code']==selected:
                result=round(element['ask']*float(quantity),2)
        
        return render_template('index.html', codes_v2=codes_v2, result=result, quantity=quantity, code=selected)

if __name__=="__main__":
    app.run(debug=True)