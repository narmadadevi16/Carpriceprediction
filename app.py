from flask import Flask, request, render_template
import pickle
import numpy as np


path='bcp.pkl'
model = pickle.load(open(path, 'rb'))
standard = pickle.load(open('ssc.pkl', 'rb'))


app=Flask(__name__)
@app.route('/')
def submit():
    return render_template('Car Price.html')

@app.route('/input',methods=['GET','POST'])
def input():
    details=request.form
    msg=""
    yr= int(details['yr'])
    yr=2022-yr
    km= int(details['km'])
    fuel = int(details['fuel'])
    seller=int(details['seller'])
    trans = int(details['trans'])
    owner=int(details['owner'])
    mileage=float(details['mileage'])
    engine=int(details['engine'])
    power=float(details['power'])
    seats=int(details['seats'])
    diesel=lpg=petrol=0
    if(fuel==1):
        petrol=1
    elif(fuel==2):
        lpg=1
    elif(fuel==3):
        diesel=1
    
    ind=tdeal=0
    if(seller==1):
        ind=1
    elif(seller==2):
        tdeal=1

    trans=int(details['trans'])

    second=third=fourth=other=0
    if(owner==1):
        second=1
    elif(owner==2):
        third=1
    elif(owner==3):
        fourth=1
    elif(owner==4):
        other=1

    #at=standard.fit_transform([[km , mileage, engine, power,seats, yr, diesel, lpg,petrol,ind,tdeal,trans,fourth,second,other,third]])
    at=standard.transform([[km , mileage, engine, power,seats, yr, diesel, lpg,petrol,ind,tdeal,trans,fourth,second,other,third]])

    #arr=[]
    #for i in at[0]:
       # arr.append(i)

    prediction=model.predict(at)
    
    prediction=np.exp(prediction)
    if(prediction<0):
        msg="The car cannot be sold"
    else:
        msg="The price is "+str(round(prediction[0],2))
    
    return render_template('output.html', msg=msg)

if __name__ == '__main__':
    app.run(debug=True)