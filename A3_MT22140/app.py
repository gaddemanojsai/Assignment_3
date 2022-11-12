from flask import Flask, request, render_template_string, render_template
import datetime
from datetime import datetime
from datetime import timedelta
import pandas as pd


app = Flask(__name__)

@app.route('/')
def index1():
    return render_template('index.html')


def fun(Selected_Stock,START_DATE,End_DATE):
    Stock=Selected_Stock    
    ST=datetime.strptime(str(START_DATE), "%d/%m/%Y").date()
    ST=str(ST)
    if(End_DATE!=""):
        ED=datetime.strptime(str(End_DATE), "%d/%m/%Y").date()
        ED=str(ED)
    else:
        ED=""
    
    
    data = pd.read_csv(f"C:/Users/DELL/Desktop/manoj(mt22140)/archive/{Stock}.csv")
    for i in range(len(data)):
        data["Date"][i]=datetime.strptime(data["Date"][i], "%Y-%m-%d").date()
    S_1 = data['Date'].values[0] 

    

    DY={}
    ans = []
    DY['MAX']=[]
    DY['MIN']=[]
    def Calculate(df1,st,il,EN):
        ST_DT = datetime.strptime(st, "%Y-%m-%d").date()
        
        if(EN==''):
            ED_DT = ST_DT+timedelta(days=-52*7)
        else:
            ED_DT = datetime.strptime(EN, "%Y-%m-%d").date()
        
        if(ED_DT<=il):
            ED_DT = il
        
        if(ST_DT>=ED_DT):
            while(ST_DT>=ED_DT):
                if(len(df1.loc[df1['Date']==ED_DT,'High'].values)==1):
                    DY['MAX'].append(df1.loc[df1['Date']==ED_DT,'High'].values[0])
                if(len(df1.loc[df1['Date']==ED_DT,'Low'].values)==1):
                    DY['MIN'].append(df1.loc[df1['Date']==ED_DT,'Low'].values[0])
                   
                ED_DT = ED_DT+timedelta(days=1)
        else:
            while(ED_DT>=ST_DT):
                if(len(df1.loc[df1['Date']==ST_DT,'High'].values)==1):
                    DY['MAX'].append(df1.loc[df1['Date']==ST_DT,'High'].values[0])
                if(len(df1.loc[df1['Date']==ST_DT,'Low'].values)==1):
                    DY['MIN'].append(df1.loc[df1['Date']==ST_DT,'Low'].values[0])
                    
                ST_DT = ST_DT+timedelta(days=1)

        return DY
    
    DYT = Calculate(data,ST,S_1,ED)
    if(len(DYT["MAX"])!=0):
        ans.append(min(DY["MIN"]))
        ans.append(max(DY["MAX"]))
        return ans
    else:
        return False
  
def confirm(S_D,E_d,Stock):
  if(len(Stock)==0):
    return False
  try:    
      a=datetime.strptime(S_D, "%d/%m/%Y").date()
  except:
    return False
  df = pd.read_csv(f"C:/Users/DELL/Desktop/manoj(mt22140)/archive/{Stock[0]}.csv")
  for i in range(len(df)):
    df["Date"][i]=datetime.strptime(df["Date"][i], "%Y-%m-%d").date()
  temp = df["Date"].values[0]

  if E_d == "":
    if a<temp:
      return False
    return True
  try:    
      b=datetime.strptime(E_d, "%d/%m/%Y")
  except:
    return False
  
  return True

@app.route('/show_data', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        v1 = request.form.getlist('stocks')
        STOCK_name = v1
        print(STOCK_name)
    else:
        STOCK_name = ''

    if request.method == 'POST':
        v2 = request.form.getlist('startDate')
        START_DT = v2
        print(START_DT)
    else:
        START_DT = ''

    if request.method == 'POST':
        v3 = request.form.getlist('endDate')
        END_DT = v3
        print(END_DT)
    else:
        END_DT = ''




    # if(confirm(START_DT[0],END_DT[0],STOCK_name)): 
    #    if request.method=='POST':
    #     try:
    #         final = fun(STOCK_name[0],START_DT[0],END_DT[0])
    #         if(isinstance(final,list)):
    #             high = final[1]
    #             low = final[0]
    #             error=""
    #     except:
    #         high="NULL"
    #         low="NULL"
    #         error="SOME ERROR MESSAGE"

    # else:
    #   high="NULL"
    #   low="NULL"
    #   error="SOME ERROR MESSAGE"

    if(confirm(START_DT[0],END_DT[0],STOCK_name)):
        if request.method=='POST':
            ans = fun(STOCK_name[0],START_DT[0],END_DT[0])
            if(isinstance(ans,list)):
              high = ans[1]
              low = ans[0]
              error=""
            else:
                high="NULL"
                low="NULL"
                error="SOME ERROR MESSAGE"
    else:
      high="NULL"
      low="NULL"
      error="SOME ERROR MESSAGE"

    return render_template('index.html', result=STOCK_name, result2=START_DT, result3=END_DT,error=error,high=high,low=low)
app.run(debug=True)