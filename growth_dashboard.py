# %%
import requests
import pandas as pd
res = requests.post('http://metabase.frontrow.co.in/api/session', 
                    headers = {"Content-Type": "application/json"},
                    json =  {"username": "mihir.dash@frontrow.co.in", 
                             "password": "Balio@123"}
                   )
assert res.ok == True
token = res.json()['id']


# %%

res = requests.post('http://metabase.frontrow.co.in/api/card/520/query/json', 
              headers = {'Content-Type': 'application/json',
                        'X-Metabase-Session': token
                        }
            )
df_ws=pd.DataFrame(res.json())


# %%
df_ws2=df_ws


# %%
df_ws2


# %%
import numpy as np
df_ws2['first_att_time']=pd.to_datetime(df_ws2['first_att_time']).dt.tz_localize(None)
df_ws2['app_install_time']=pd.to_datetime(df_ws2['app_install_time']).dt.tz_localize(None)
df_ws2['premium_purchase_at']=pd.to_datetime(df_ws2['premium_purchase_at']).dt.tz_localize(None)
df_ws['pre_att_premium_count']=np.where((~df_ws2['premium_purchase_at'].isna()) &((df_ws2['music_ws_att'].isna()) | (df_ws2['premium_purchase_at']<df_ws2['first_att_time'])),1,0)
df_ws['post_att_premium_count']=np.where((~df_ws2['premium_purchase_at'].isna()) & (~df_ws2['music_ws_att'].isna())&((df_ws2['premium_purchase_at']>=df_ws2['first_att_time'])),1,0)
df_ws['pre_att_premium_amount']=np.where((~df_ws2['premium_purchase_at'].isna()) &((df_ws2['music_ws_att'].isna()) | (df_ws2['premium_purchase_at']<df_ws2['first_att_time'])),df_ws2['inr_amount'],0)
df_ws['post_att_premium_amount']=np.where((~df_ws2['premium_purchase_at'].isna()) &(~df_ws2['music_ws_att'].isna())& ((df_ws2['premium_purchase_at']>=df_ws2['first_att_time'])),df_ws2['inr_amount'],0)
df_ws2['date']=df_ws['app_install_time'].dt.date



# %%
df_ws['pre_att_premium_count'].sum()


# %%
df_wsg=df_ws2.groupby(by=['date','utm_source']).agg({'user_id':'count','select_music':'count','music_ws_att':'count','passed_to_lsq':'count','is_called':'count','pre_att_premium_count':'sum','post_att_premium_count':'sum','pre_att_premium_amount':'sum','post_att_premium_amount':'sum'})
df_wsg.reset_index(inplace=True)


# %%
df_wsg[df_wsg['date'].astype(str)=='2022-08-23']


# %%
df_wsg.rename(columns={'user_id':'app_installs','select_music':'selected_music_community','music_ws_att':'attended_music_WS'},inplace=True)
df_wsg


# %%
df_wsg[df_wsg['date'].astype(str)=='2022-08-11']


# %%
df_wsg['pre_att_premium_count'].sum()


# %%
df_wsg['total_premium_count']=df_wsg['pre_att_premium_count']+df_wsg['post_att_premium_count']
df_wsg['total_premium_amount']=df_wsg['pre_att_premium_amount']+df_wsg['post_att_premium_amount']
df_wsg


# %%
import gspread
import os
pwd=os.getcwd()
from gspread_dataframe import get_as_dataframe, set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials
scope =["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds =ServiceAccountCredentials.from_json_keyfile_name(pwd+"/credentials.json", scope)
client = gspread.authorize(creds)



# %%
spreadsheet=client.open("Growth Dashboard-WS Flow")
wk=spreadsheet.worksheet("Data")
dfx=set_with_dataframe(wk,df_wsg)



# %%
spreadsheet = client.open("WIP-High ARPU Performance Tracker v3")
kmk="Spend_Breakdown"
wks1=spreadsheet.worksheet(kmk)
print()
dfx=pd.DataFrame(wks1.get_all_records())
dfx


# %%
dfx=dfx[dfx['Cat_To_Text']=='Workshop']
dfx=dfx[['Date','Total Cost']]
dfx


# %%
dfx['Date']=pd.to_datetime(dfx['Date']).dt.date
dfx


# %%
spreadsheet = client.open("Growth Dashboard-WS Flow")
kmk="Spends"
wks1=spreadsheet.worksheet(kmk)
print()
dfnp=pd.DataFrame(wks1.get_all_records())
dfnp['Date']=pd.to_datetime(dfnp['Date']).dt.date
dfnp


# %%
dfx


# %%
dfxf=dfx.append(dfnp)
dfxf.drop_duplicates(subset='Date',inplace=True)


# %%
spreadsheet=client.open("Growth Dashboard-WS Flow")
wk=spreadsheet.worksheet("Spends")
dfx=set_with_dataframe(wk,dfxf)





