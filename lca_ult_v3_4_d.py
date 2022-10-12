import multiprocessing
def foo():    
    import requests
    import pandas as pd
    import numpy as np
    import json
    import sys
    import random
    import pickle
    res = requests.post('http://metabase.frontrow.co.in/api/session', 
                        headers = {"Content-Type": "application/json"},
                        json =  {"username": "mihir.dash@frontrow.co.in", 
                                "password": "Balio@123"}
                    )
    assert res.ok == True
    token = res.json()['id']

    # %%
    res = requests.post('http://metabase.frontrow.co.in/api/card/488/query/json', 
                headers = {'Content-Type': 'application/json',
                            'X-Metabase-Session': token
                            }
                )
    df_ws=pd.DataFrame(res.json())

    # %%
    from datetime import datetime
    dt=datetime.now()
    df_ws['curr_dt']=dt
    df_ws['start_date']=pd.to_datetime(df_ws['start_date']).dt.tz_localize(None)
    df_ws['td']=(df_ws['curr_dt']-df_ws['start_date']).astype('timedelta64[m]')
    df_ws.replace(['YES','NO'],[':+1:',':x:'],inplace=True)
    mx=['Writing','Dance','Gaming']
    nx=['Writing','Dance']
    x=[2,3,4,5]
    y=[9,10,11,12,13,14]
    z=[14,15,16]
    df_ws

    # %%
    def formatter1(df_in,fn):
        df1=df_in
        df1c=df1

        of=open(fn,"rb")
        lst=pickle.load(of)
        of.close()
        df1=df1[~df1['room_id'].isin(lst)]
        cip=df1c['room_id'].tolist()
        ofn=open(fn,"wb")
        pickle.dump(cip,ofn)
        ofn.close()
        lst,cip
        msg=""
        m2=""
        msg2=""
        if(len(df1.index)>0):
            s_d=df1['start_date'].tolist()
            c_c=df1['category'].tolist()
            i_n=df1['instructor_name'].tolist()
            i_c=df1['instructor_contact'].tolist()
            i_a=df1['inst_has_joined'].tolist()
            i_l=df1['sub_category'].tolist()
            u_n=df1['name'].tolist()
            u_c=df1['contact'].tolist()
            u_a=df1['user_has_joined'].tolist()
            r_l=df1['room_link_url'].tolist()
            msg=" *_Start Date:_* "+str(s_d[0])
            msg2=" *_Start Date:_* "+str(s_d[0])
            m2=msg
            for i in range(len(i_n)):
                if(i<12):
                    p0=" *_Category:_* "+str(c_c[i])
                    p1=" *_Instructor:_* "+str(i_n[i])+', '+str(i_c[i])+', '+str(i_l[i])+' '+str(i_a[i])
                    p2=" *_User:_* "+str(u_n[i])+', '+ str(u_c[i])+' '+str(u_a[i])
                    p3=" *_Room Link:_* "+str(r_l[i])
                    msg=msg+'\n'+p0+'\n'+p1+'\n'+p2+'\n'+p3+'\n'
                if(i>=12):
                    p0=" *_Category:_* "+str(c_c[i])
                    p1=" *_Instructor:_* "+str(i_n[i])+', '+str(i_c[i])+', '+str(i_l[i])+' '+str(i_a[i])
                    p2=" *_User:_* "+str(u_n[i])+', '+ str(u_c[i])+' '+str(u_a[i])
                    p3=" *_Room Link:_* "+str(r_l[i])
                    msg2=msg2+'\n'+p0+'\n'+p1+'\n'+p2+'\n'+p3+'\n'
        
        return m2,msg,msg2


    # %%
    def sender1(mess,m,adr,head,hue):
        if (mess!=m):
            url = adr
            message = (mess)
            title = (f":alert: "+head+" :alert:")
            slack_data = {
                "username": "NotificationBot",
                "icon_emoji": ":satellite:",
                #"channel" : "#somerandomcahnnel",
                "attachments": [
                    {
                        "color": hue,
                        "fields": [
                            {
                                "title": title,
                                "value": message
                            }
                        ]
                    }
                ]
            }
            headers = {'Content-Type': "application/json"}
            response = requests.post(url, data=json.dumps(slack_data), headers=headers)
            if response.status_code != 200:
                raise Exception(response.status_code, response.text)

    # %%
    #main
    #cat1
    dfd=df_ws
    url="https://hooks.slack.com/services/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"
    dfd1=dfd.loc[(dfd['user_has_joined']==':x:') & (dfd['inst_has_joined']==':x:')]
    color="#FF0000"
    dfd11=dfd1[dfd1['td'].astype(int).isin(x)]
    title="MENTORSHIP-3 Min Alert"
    pn="mk1.pkl"
    m,mess,mess2=formatter1(dfd11,pn)
    sender1(mess,m,url,title,color)
    sender1(mess2,m,url,title,color)
    dfd11=dfd1[dfd1['td'].astype(int).isin(y)]
    title="MENTORSHIP-10 Min Alert"
    pn="mk1c.pkl"
    m,mess,mess2=formatter1(dfd11,pn)
    sender1(mess,m,url,title,color)
    sender1(mess2,m,url,title,color)
    #cat2
    dfd1=dfd.loc[(dfd['user_has_joined']==':x:') & (dfd['inst_has_joined']==':+1:')]
    color="#FFFF00"
    dfd11=dfd1[dfd1['td'].astype(int).isin(x)]
    title="MENTORSHIP-3 Min Alert"
    pn="mk2.pkl"
    m,mess,mess2=formatter1(dfd11,pn)
    sender1(mess,m,url,title,color)
    sender1(mess2,m,url,title,color)
    dfd11=dfd1[dfd1['td'].astype(int).isin(y)]
    title="MENTORSHIP-10 Min Alert"
    pn="mk2c.pkl"
    m,mess,mess2=formatter1(dfd11,pn)
    sender1(mess,m,url,title,color)
    sender1(mess2,m,url,title,color)
    #cat3
    dfd1=dfd.loc[(dfd['user_has_joined']==':+1:') & (dfd['inst_has_joined']==':x:')]
    url="https://hooks.slack.com/services/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"
    color="#A020F0"
    dfd11=dfd1[dfd1['td'].astype(int).isin(x)]
    title="MENTORSHIP-3 Min Alert"
    pn="mk3.pkl"
    m,mess,mess2=formatter1(dfd11,pn)
    sender1(mess,m,url,title,color)
    sender1(mess2,m,url,title,color)
    dfd11=dfd1[dfd1['td'].astype(int).isin(y)]
    title="MENTORSHIP-10 Min Alert"
    pn="mk3c.pkl"
    m,mess,mess2=formatter1(dfd11,pn)
    sender1(mess,m,url,title,color)
    sender1(mess2,m,url,title,color)

    # %%
    import requests
    import pandas as pd
    import numpy as np
    import json
    import sys
    import random
    import pickle
    import os
    import time
    import logging
    from slack_sdk import WebClient
    from slack_sdk.errors import SlackApiError
    pwd=os.getcwd()
    res = requests.post('http://metabase.frontrow.co.in/api/session', 
                        headers = {"Content-Type": "application/json"},
                        json =  {"username": "mihir.dash@frontrow.co.in", 
                                "password": "Balio@123"}
                    )
    assert res.ok == True
    token = res.json()['id']

    # %%
    res = requests.post('http://metabase.frontrow.co.in/api/card/469/query/json', 
                headers = {'Content-Type': 'application/json',
                            'X-Metabase-Session': token
                            }
                )
    df_ws=pd.DataFrame(res.json())
    pns=df_ws

    # %%
    res = requests.post('http://metabase.frontrow.co.in/api/card/465/query/json', 
                headers = {'Content-Type': 'application/json',
                            'X-Metabase-Session': token
                            }
                )
    df_uc=pd.DataFrame(res.json())

    # %%
    #LIVE COURSE MASTER SHEET
    df_ur=df_uc
    df_ur.drop_duplicates(subset=['class_start_time','instructor_id','user_id'],inplace=True)

    # %%
    df_ur

    # %%
    df_ur['class_start_time']=pd.to_datetime(df_ur['class_start_time']).dt.tz_localize(None)
    df_ur['joined_at']=pd.to_datetime(df_ur['joined_at']).dt.tz_localize(None)
    df_ur['td']=(df_ur['joined_at']-df_ur['class_start_time']).astype('timedelta64[m]')


    # %%
    import numpy as np
    df_ur['peak_duration']=df_ur['duration_mins']
    df_ur=df_ur[df_ur['has_attended']==1]
    pns.sort_values(by='joined_at',ascending=False,ignore_index=True,inplace=True)
    pns.drop_duplicates(subset='lesson_id',inplace=True)
    
    # %%
    df_ucg=df_ur.groupby(by=['class_start_time','course_id','batch_id','lesson_id','instructor_id','course_type']).agg({'has_attended':'sum','peak_duration':'max','duration_mins':'mean'})
    df_ucg.reset_index(inplace=True)
    df_ucg=pd.merge(pns,df_ucg[['lesson_id','has_attended','peak_duration','duration_mins']],how='left',on='lesson_id')
    #df_ucg['date']=pd.to_datetime(df_ucg['class_start_time']).dt.tz_localize(None)
    df_ucg.rename(columns={'has_attended_y':'user_count','has_attended_x':'instructor_att','new_duration_mins':'instructor_dur','duration_mins':'avg_duration'},inplace=True)
    df_ucg

    # %%
    import gspread
    from gspread_dataframe import get_as_dataframe, set_with_dataframe
    from oauth2client.service_account import ServiceAccountCredentials
    scope =["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds =ServiceAccountCredentials.from_json_keyfile_name(pwd+"/credentials.json", scope)
    client = gspread.authorize(creds)

    # %%
    spreadsheet = client.open("Live Course Master Sheet")
    kmk="Test2"
    wks1=spreadsheet.worksheet(kmk)
    print()
    df1=pd.DataFrame(wks1.get_all_records())

    # %%

    df1['class_start_time']=pd.to_datetime(df1['class_start_time'])
    # %%
    df_ucf=df_ucg.append(df1,ignore_index=True)
    df_ucf['lesson_id']=df_ucf['lesson_id'].astype(int)
    df_ucf['class_start_time']=pd.to_datetime(df_ucf['class_start_time']).dt.tz_localize(None)
    df_ucf['course_id']=df_ucf['course_id'].astype(int)
    df_ucf['batch_id']=df_ucf['batch_id'].astype(int)
    df_ucf['instructor_id']=df_ucf['instructor_id'].astype(int)
    df_ucf.drop_duplicates(subset=['class_start_time','course_id','batch_id','lesson_id','instructor_id'],inplace=True)
    df_ucf.sort_values(by='class_start_time',ascending=False,ignore_index=True,inplace=True)

    # %%
    spreadsheet=client.open("Live Course Master Sheet")
    wk=spreadsheet.worksheet("Test2")
    dfx=set_with_dataframe(wk,df_ucf)

    # %%
    #user count for lca
    df_uc.drop_duplicates(subset=['class_start_time','instructor_id','user_id'],inplace=True)

    # %%
    df_ucg=df_uc.groupby(by=['class_start_time','instructor_id']).agg({'joined_at':'count'})
    df_ucg.reset_index(inplace=True)
    df_ucg['class_start_time']=pd.to_datetime(df_ucg['class_start_time']).dt.tz_localize(None)
    df_ucg.rename(columns={'joined_at':'user_count'},inplace=True)
    df_ucg['user_count']=df_ucg['user_count'].astype(int)

    # %%
    df_ucg

    # %%
    df_sa=df_ws
    df_sa['lesson_id']=df_sa['lesson_id'].astype(int)

    # %%
    #merge inst and user count details
    df_sa['class_start_time']=pd.to_datetime(df_sa['class_start_time']).dt.tz_localize(None)
    df_sa['joined_at']=pd.to_datetime(df_sa['joined_at']).dt.tz_localize(None)
    df_sa.sort_values(by=['class_start_time','instructor_id','joined_at'],ascending=False,ignore_index=True,inplace=True)
    xn9=df_sa
    df_sa=df_sa[df_sa['course_type']=='LIVE_COURSE']
    df_sa.drop_duplicates(subset=['instructor_id','class_start_time'],inplace=True)
    df_sa=pd.merge(df_sa,df_ucg[['class_start_time','instructor_id','user_count']],how='left',on=['class_start_time','instructor_id'])

    df_sa['user_count'].fillna(value=0,inplace=True)
    df_sa['user_count']=df_sa['user_count'].astype(int)
    df_sa

    # %%
    from datetime import datetime
    dt=datetime.now()
    df_sa['curr_dt']=dt
    #df_sa['class_start_time']=pd.to_datetime(df_sa['class_start_time']).dt.tz_localize(None)
    df_sa['td']=(df_sa['curr_dt']-df_sa['class_start_time']).astype('timedelta64[m]')
    df_sa.replace(['YES','NO'],[':+1:',':x:'],inplace=True)
    mx=['Writing','Dance','Gaming']
    nx=['Writing','Dance']
    x=[2,3,4,5]
    y=[6,7,8,9]
    z=[10,11,12,13]
    df_sa

    # %% [markdown]
    # 

    # %%
    def formatter(df_in,fn):
        df1=df_in
        df1c=df1

        of=open(fn,"rb")
        lst=pickle.load(of)
        of.close()
        df1=df1[~df1['lesson_id'].isin(lst)]
        cip=df1c['lesson_id'].tolist()
        ofn=open(fn,"wb")
        pickle.dump(cip,ofn)
        ofn.close()
        lst,cip
        msg=""
        m2=""
        msg2=""
        if(len(df1.index)>0):
            s_d=df1['class_start_time'].tolist()
            b_i=df1['batch_id'].tolist()
            i_d=df1['instructor_id'].tolist()
            i_n=df1['name'].tolist()
            c_c=df1['parent_category_name'].tolist()
            i_c=df1['contact'].tolist()
            i_a=df1['has_attended'].tolist()
            u_n=df1['user_count'].tolist()
            r_l=df1['link'].tolist()
            msg=" *_Start Date:_* "+str(s_d[0])
            msg2=" *_Start Date:_* "+str(s_d[0])
            m2=msg
            for i in range(len(i_n)):
                if(i<12):
                    p0=" *_Batch ID:_* "+str(b_i[i])
                    p4=" *_Category:_* "+str(c_c[i])
                    p1=" *_Instructor:_* "+str(i_d[i])+', '+str(i_n[i])+', '+str(i_c[i])+' '+str(i_a[i])
                    p2=" *_Users:_* "+str(u_n[i])
                    p3=" *_Room Link:_* "+str(r_l[i])
                    msg=msg+'\n'+p0+'\n'+p4+'\n'+p1+'\n'+p2+'\n'+p3+'\n'
                if(i>=12):
                    p0=" *_Batch ID:_* "+str(b_i[i])
                    p4=" *_Category:_* "+str(c_c[i])
                    p1=" *_Instructor:_* "+str(i_d[i])+', '+str(i_n[i])+', '+str(i_c[i])+' '+str(i_a[i])
                    p2=" *_Users:_* "+str(u_n[i])
                    p3=" *_Room Link:_* "+str(r_l[i])
                    msg2=msg2+'\n'+p0+'\n'+p4+'\n'+p1+'\n'+p2+'\n'+p3+'\n'
        
        return m2,msg,msg2


    # %%
    def sender(mess,m,adr,head,hue):
        if (mess!=m):
            url = adr
            message = (mess)
            title = (f":alert: "+head+" :alert:")
            slack_data = {
                "username": "NotificationBot",
                "icon_emoji": ":satellite:",
                #"channel" : "#somerandomcahnnel",
                "attachments": [
                    {
                        "color": hue,
                        "fields": [
                            {
                                "title": title,
                                "value": message
                            }
                        ]
                    }
                ]
            }
            headers = {'Content-Type': "application/json"}
            response = requests.post(url, data=json.dumps(slack_data), headers=headers)
            if response.status_code != 200:
                raise Exception(response.status_code, response.text)

    # %%
    #main
    #cat1
    dfd=df_sa
    url="https://hooks.slack.com/services/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"
    dfd1=dfd.loc[(dfd['user_count']==0) & (dfd['has_attended']==':x:')]
    color="#FF0000"
    dfd11=dfd1[dfd1['td'].astype(int).isin(x)]
    title="LIVE COURSE-3 Min Alert"
    pn="qk1.pkl"
    m,mess,mess2=formatter(dfd11,pn)
    sender(mess,m,url,title,color)
    sender(mess2,m,url,title,color)
    dfd11=dfd1[dfd1['td'].astype(int).isin(y)]
    title="LIVE COURSE-6 Min Alert"
    pn="qk1c.pkl"
    m,mess,mess2=formatter(dfd11,pn)
    sender(mess,m,url,title,color)
    sender(mess2,m,url,title,color)
    dfd11=dfd1[dfd1['td'].astype(int).isin(z)]
    title="LIVE COURSE-10 Min Alert"
    pn="qk1cc.pkl"
    m,mess,mess2=formatter(dfd11,pn)
    sender(mess,m,url,title,color)
    sender(mess2,m,url,title,color)
    #cat2
    dfd1=dfd.loc[(dfd['user_count']==0) & (dfd['has_attended']==':+1:')]
    color="#FFFF00"
    dfd11=dfd1[dfd1['td'].astype(int).isin(x)]
    title="LIVE COURSE-3 Min Alert"
    pn="qk2.pkl"
    m,mess,mess2=formatter(dfd11,pn)
    sender(mess,m,url,title,color)
    sender(mess2,m,url,title,color)
    dfd11=dfd1[dfd1['td'].astype(int).isin(y)]
    title="LIVE COURSE-6 Min Alert"
    pn="qk2c.pkl"
    m,mess,mess2=formatter(dfd11,pn)
    sender(mess,m,url,title,color)
    sender(mess2,m,url,title,color)
    dfd11=dfd1[dfd1['td'].astype(int).isin(z)]
    title="LIVE COURSE-10 Min Alert"
    pn="qk2cc.pkl"
    m,mess,mess2=formatter(dfd11,pn)
    sender(mess,m,url,title,color)
    sender(mess2,m,url,title,color)
    #cat3
    dfd1=dfd.loc[(dfd['user_count']>0) & (dfd['has_attended']==':x:')]
    url="https://hooks.slack.com/services/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"
    color="#A020F0"
    dfd11=dfd1[dfd1['td'].astype(int).isin(x)]
    title="LIVE COURSE-3 Min Alert"
    pn="qk3.pkl"
    m,mess,mess2=formatter(dfd11,pn)
    sender(mess,m,url,title,color)
    sender(mess2,m,url,title,color)
    dfd11=dfd1[dfd1['td'].astype(int).isin(y)]
    title="LIVE COURSE-6 Min Alert"
    pn="qk3c.pkl"
    m,mess,mess2=formatter(dfd11,pn)
    sender(mess,m,url,title,color)
    sender(mess2,m,url,title,color)
    dfd11=dfd1[dfd1['td'].astype(int).isin(z)]
    title="LIVE COURSE-10 Min Alert"
    pn="qk3cc.pkl"
    m,mess,mess2=formatter(dfd11,pn)
    sender(mess,m,url,title,color)
    sender(mess2,m,url,title,color)
    #dropoff
    url="https://hooks.slack.com/services/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"
    dfd1=dfd.loc[(dfd['td'].astype(int)<=20) | ((dfd['user_count']>0) & (dfd['td'].astype(int)<90))]
    dfd11=dfd1.loc[(dfd1['left_at'].astype(str)!='None') & (dfd1['has_attended']==':+1:') & (dfd1['td']>=1)]
    color="#0000FF"
    title="LIVE COURSE-Dropoff Alert"
    pn="qkd.pkl"
    m,mess,mess2=formatter(dfd11,pn)
    sender(mess,m,url,title,color)
    sender(mess2,m,url,title,color)
    #rejoin
    dfd11=dfd[dfd['dropoff_count']>0]
    color="#00FF00"
    title="LIVE COURSE-Rejoin Alert"
    pn="qkr.pkl"
    m,mess,mess2=formatter(dfd11,pn)
    sender(mess,m,url,title,color)
    sender(mess2,m,url,title,color)



    # %%
    #workshop module
    df_sa=xn9
    df_sa=df_sa[df_sa['course_type']=='WORKSHOP']
    df_sk=df_sa
    print(df_sa)
    dt=datetime.now()
    df_sa['curr_dt']=dt
    st=df_sa['class_start_time'].tolist()
    ja=df_sa['joined_at'].tolist()
    i_n=df_sa['instructor_name'].tolist()
    cbi=df_sa['batch_id'].tolist()
    ct=df_sa['course_type'].tolist()
    df_sa['td']=(df_sa['curr_dt']-df_sa['class_start_time']).astype('timedelta64[m]')
    df_s=df_sa
    df_sa=df_sa[df_sa['has_attended']=="NO"]
    df_sa=df_sa[df_sa['td']<=5]
    df_sa=df_sa[df_sa['td']>=3]
    df_sa=df_sa[df_sa['joined_at'].isna()]
    dfpn=pd.read_csv(pwd + "/ci.csv")
    df_sa=pd.merge(df_sa, dfpn, how='left', left_on=['course_id'], right_on=['course_id'])
    df_sa_copy=df_sa
    of=open("ia3.pkl","rb")
    lst=pickle.load(of)
    of.close()
    df_sa=df_sa[~df_sa['batch_id'].isin(lst)]
    cip=df_sa_copy['batch_id'].tolist()
    ofn=open("ia3.pkl","wb")
    pickle.dump(cip,ofn)
    ofn.close()
    st=df_sa['class_start_time'].tolist()
    ja=df_sa['joined_at'].tolist()
    i_n=df_sa['instructor_name'].tolist()
    cbi=df_sa['batch_id'].tolist()
    i_d=df_sa['instructor_id'].tolist()
    c_n=df_sa['course_name'].tolist()
    c_t=df_sa['course_type'].tolist()
    s_c=df_sa['Slack Codes'].tolist()
    msg=""
    for kk in range(len(cbi)):
        p0='Start Time: '+str(st[kk])
        p1='course_name: '+str(c_n[kk])
        p2='instructor_id: '+str(i_d[kk])
        p3="Instructor Name: "+str(i_n[kk])
        p4="Batch ID: "+str(cbi[kk])
        p5="Course Type: "+str(c_t[kk])
        msg=msg+p0+'\n'+p1+'\n'+p2+'\n'+p3+'\n'+p4+'\n'+p5+'\n'+"-----------------------------"+'\n'

        logging.basicConfig(level=logging.DEBUG)

        slack_token = "xoxb-882099602902-3377088964865-zeCsUYj0nu0YffEkpHZ3tw1t"
        client = WebClient(token=slack_token)
        if(msg!=""):
            try:
                response = client.chat_postMessage(
                    channel=str(s_c[kk]),
                    text=msg,
                )
            except SlackApiError as e:
                assert e.response["error"]
    print("msg=",msg)
    if(msg!=""):
        if __name__ == '__main__':
            url = "https://hooks.slack.com/services/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"
            message = (msg)
            title = (f"3 MINUTES LATE ALERT :zap:")
            slack_data = {
                "username": "NotificationBot",
                "icon_emoji": ":satellite:",
                "attachments": [
                    {
                        "color": "#FFFF00",
                        "fields": [
                            {
                                "title": title,
                                "value": message,
                                "short": "false",
                            }
                        ]
                    }
                ]
            }
            byte_length = str(sys.getsizeof(slack_data))
            headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
            response = requests.post(url, data=json.dumps(slack_data), headers=headers)
            if response.status_code != 200:
                raise Exception(response.status_code, response.text)
    df_f=df_s
    df_f=df_f[df_f['has_attended']=="NO"]
    df_f=df_f[df_f['td']<=30]
    df_f=df_f[df_f['td']>=5]
    df_f=df_f[df_f['joined_at'].isna()]
    df_f=pd.merge(df_f, dfpn, how='left', left_on=['course_id'], right_on=['course_id'])
    df_sx=df_f
    of1=open("ia4.pkl","rb")
    lst1=pickle.load(of1)
    of1.close()
    df_f=df_f[~df_f['batch_id'].isin(lst1)]
    cip1=df_sx['batch_id'].tolist()
    ofn1=open("ia4.pkl","wb")
    pickle.dump(cip1,ofn1)
    ofn1.close()
    st1=df_f['class_start_time'].tolist()
    ja1=df_f['joined_at'].tolist()
    i_n1=df_f['instructor_name'].tolist()
    i_d1=df_f['instructor_id'].tolist()
    c_n1=df_f['course_name'].tolist()
    cbi1=df_f['batch_id'].tolist()
    c_t1=df_f['course_type'].tolist()
    s_c1=df_f['Slack Codes'].tolist()
    msg2=""
    for kk1 in range(len(cbi1)):
        p00='Start Time: '+str(st1[kk1])
        p11='course_name: '+str(c_n1[kk1])
        p22='instructor_id: '+str(i_d1[kk1])
        p33="Instructor Name: "+str(i_n1[kk1])
        p44="Batch ID: "+str(cbi1[kk1])
        p55="course type: "+str(c_t1[kk1])
        msg2=msg2+p00+'\n'+p11+'\n'+p22+'\n'+p33+'\n'+p44+'\n'+p55+'\n'"-----------------------------"+'\n'

        logging.basicConfig(level=logging.DEBUG)

        slack_token = "xoxb-882099602902-3377088964865-zeCsUYj0nu0YffEkpHZ3tw1t"
        client = WebClient(token=slack_token)
        if(msg2!=""):
            try:
                response = client.chat_postMessage(
                    channel=str(s_c1[kk1]),
                    text=msg2
                )
            except SlackApiError as e:
                assert e.response["error"]
        
    print(msg2)
    if(msg2!=""):
        if __name__ == '__main__':
            url = "https://hooks.slack.com/services/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"
            message = (msg2)
            title = (f"5 MINUTES LATE ALERT :zap:")
            slack_data = {
                "username": "NotificationBot",
                "icon_emoji": ":satellite:",
                "attachments": [
                    {
                        "color": "#FF0000",
                        "fields": [
                            {
                                "title": title,
                                "value": message,
                                "short": "false",
                            }
                        ]
                    }
                ]
            }
            byte_length = str(sys.getsizeof(slack_data))
            headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
            response = requests.post(url, data=json.dumps(slack_data), headers=headers)
            if response.status_code != 200:
                raise Exception(response.status_code, response.text)
    df_sk=df_sk[df_sk['is_cancelled']!=True]
    df_sk['lesson_id']=df_sk['lesson_id'].astype(int)
    df_sk['class_start_time']=pd.to_datetime(df_sk['class_start_time']).dt.tz_localize(None)
    df_sk['joined_at']=pd.to_datetime(df_sk['joined_at']).dt.tz_localize(None)
    df_sk['class_end_time']=pd.to_datetime(df_sk['class_end_time']).dt.tz_localize(None)
    dt=datetime.now()
    df_sk['curr_dt']=dt
    st=df_sk['class_start_time'].tolist()
    ja=df_sk['joined_at'].tolist()
    i_n=df_sk['name'].tolist()
    cbi=df_sk['batch_id'].tolist()
    df_sk['td']=(df_sk['curr_dt']-df_sk['class_start_time']).astype('timedelta64[m]')
    df_sk['td2']=(df_sk['class_end_time']-df_sk['class_start_time']).astype('timedelta64[m]')
    #df_sa=df_sa[df_sa['has_attended']=="NO"]
    df_sk=df_sk[df_sk['td'].astype(int)<df_sk['td2'].astype(int)]
    df_sk=df_sk[~df_sk['left_at'].isna()]
    df_sk['left_at']=pd.to_datetime(df_sk['left_at'])
    df_sk['anchor']=df_sk['lesson_id'].astype(str)+ " " + df_sk['left_at'].astype(str)
    df_sk_copy=df_sk
    of=open("bqc.pkl","rb")
    lst=pickle.load(of)
    of.close()
    df_sk=df_sk[~df_sk['anchor'].isin(lst)]
    cip=df_sk_copy['anchor'].tolist()
    ofn=open("bqc.pkl","wb")
    pickle.dump(cip,ofn)
    ofn.close()
    st=df_sk['class_start_time'].tolist()
    ja=df_sk['joined_at'].tolist()
    i_n=df_sk['name'].tolist()
    cbi=df_sk['batch_id'].tolist()
    i_d=df_sk['instructor_id'].tolist()
    c_n=df_sk['course_name'].tolist()
    l_a=df_sk['left_at'].tolist()
    msg=""
    msgx=""
    msgl=""
    ckc=0
    for kk in range(len(cbi)):
        ckc=ckc+1
        p0='Start Time: '+str(st[kk])
        p1='course_name: '+str(c_n[kk])
        p2='instructor_id: '+str(i_d[kk])
        p3="Instructor Name: "+str(i_n[kk])
        p4="Batch ID: "+str(cbi[kk])
        p7="Drop Time: "+str(l_a[kk])
        msg=msg+p0+'\n'+p1+'\n'+p2+'\n'+p3+'\n'+p4+'\n'+p7+'\n'+"-----------------------------"+'\n'
    if(msg!=""):
        if __name__ == '__main__':
            url = "https://hooks.slack.com/services/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"
            message = (msg)
            title = (f"Instructor Drop-off Alert :zap:")
            slack_data = {
                "username": "NotificationBot",
                "icon_emoji": ":satellite:",
                #"channel" : "#somerandomcahnnel",
                "attachments": [
                    {
                        "color": "#FF0000",
                        "fields": [
                            {
                                "title": title,
                                "value": message,
                                "short": "false",
                            }
                        ]
                    }
                ]
            }
            byte_length = str(sys.getsizeof(slack_data))
            headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
            response = requests.post(url, data=json.dumps(slack_data), headers=headers)
            if response.status_code != 200:
                raise Exception(response.status_code, response.text)
if __name__ == '__main__':
    # Start foo as a process
    p = multiprocessing.Process(target=foo, name="Foo")
    p.start()
    p.join(220)

# If thread is active
    if p.is_alive():
        print("foo is running... let's kill it...")

        # Terminate foo
        p.terminate()
        p.join()
