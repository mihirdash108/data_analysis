# %%


import requests
res = requests.post('http://metabase.frontrow.co.in/api/session', 
                    headers = {"Content-Type": "application/json"},
                    json =  {"username": "mihir.dash@frontrow.co.in", 
                             "password": "Balio@123"}
                   )
assert res.ok == True
token = res.json()['id']



# %%


import pandas as pd
res = requests.get('http://metabase.frontrow.co.in/api/card', 
              headers = {'Content-Type': 'application/json',
                        'X-Metabase-Session': token
                        }
            )
res.json()



# %%


res = requests.post('http://metabase.frontrow.co.in/api/card/367/query/json', 
              headers = {'Content-Type': 'application/json',
                        'X-Metabase-Session': token
                        }
            )
df_counseling_booking=pd.DataFrame(res.json())



# %%


res = requests.post('http://metabase.frontrow.co.in/api/card/464/query/json', 
              headers = {'Content-Type': 'application/json',
                        'X-Metabase-Session': token
                        }
            )
df_counseling_attendance=pd.DataFrame(res.json())



# %%


df_counseling_attendance['no_of_dropoffs']



# %%


res = requests.post('http://metabase.frontrow.co.in/api/card/3/query/json', 
              headers = {'Content-Type': 'application/json',
                        'X-Metabase-Session': token
                        }
            )
df_order=pd.DataFrame(res.json())



# %%


course_id = [116,184,185,117,193,334,379,332,333,378]
df_order_filtered = df_order[df_order['course_id'].isin(course_id)]
df_order_not_renew =df_order_filtered.loc[df_order_filtered['is_renewal'] != 'YES']
df_order_not_renew_free = df_order_not_renew .loc[df_order_not_renew ['payment_gateway'] != 'FREE']
df_order_not_renew_free 



# %%


df_counseling_booking =df_counseling_booking[df_counseling_booking['booking_type'] == 'COUNSELLING']



# %%


counseling_booking_dump = df_counseling_booking[['user_id', 'instructor_id' , 'instructor_name' , 'booked_at', 'start_date', 'end_date' , 'booking_type', 'is_booked_by_user']].reset_index()



# %%


counseling_booking_dump['booked_at'] =  pd.to_datetime(counseling_booking_dump['booked_at'])
counseling_booking_dump['booked_at'] = counseling_booking_dump['booked_at'].dt.strftime('%Y/%m/%d')



# %%


df_order_not_renew_free['order_at'] =  pd.to_datetime(df_order_not_renew_free['order_at'])
df_order_not_renew_free['order_at'] = df_order_not_renew_free['order_at'].dt.strftime('%Y/%m/%d')



# %%


counseling_booking_dump["userdate"] = counseling_booking_dump["user_id"].astype(str) + counseling_booking_dump["booked_at"].astype(str)



# %%


df_order_not_renew_free["userdate"] = df_order_not_renew_free["user_id"].astype(str) + df_order_not_renew_free["order_at"].astype(str)



# %%


df_order_counselling_booking = pd.merge(df_order_not_renew_free, 
                      counseling_booking_dump, 
                      on ='userdate', 
                      how ='inner')



# %%


df_orders_by_date =  df_order_not_renew_free.groupby(['order_at']).user_id.nunique().reset_index()



# %%


df_orders_by_date = df_orders_by_date.sort_values(by='order_at', ascending=False)
df_orders_by_date.rename(columns = {'user_id':'no of orders'}, inplace = True)
df_orders_by_date.rename(columns = {'order_at':'date'}, inplace = True)
df_orders_by_date



# %%


df_order_day_counselling_booked = df_order_counselling_booking.groupby(['booked_at']).user_id_x.nunique().reset_index()
df_order_day_counselling_booked.rename(columns = {'user_id_x':'counselling booked'}, inplace = True)
df_order_day_counselling_booked.rename(columns = {'booked_at':'date'}, inplace = True)
df_order_day_counselling_booked



# %%


df_order_day_counselling_booked = df_order_counselling_booking.pivot_table(values='user_id_x', index='booked_at', columns='is_booked_by_user', aggfunc='nunique', margins = False).reset_index()
df_order_day_counselling_booked = df_order_day_counselling_booked.sort_values(by='booked_at', ascending=False)
df_order_day_counselling_booked.rename(columns = {'YES':'Booked by user'}, inplace = True)
df_order_day_counselling_booked.rename(columns = {'NO':'Booked by admin'}, inplace = True)
df_order_day_counselling_booked.rename(columns = {'booked_at':'date'}, inplace = True)
df_order_day_counselling_booked  = df_order_day_counselling_booked.fillna('0')
df_order_day_counselling_booked['Booked by user'] = df_order_day_counselling_booked['Booked by user'].astype(int)
df_order_day_counselling_booked['Booked by admin'] = df_order_day_counselling_booked['Booked by admin'].astype(int)
df_order_day_counselling_booked['Total bookings'] = df_order_day_counselling_booked['Booked by admin'] + df_order_day_counselling_booked['Booked by user']
df_order_day_counselling_booked



# %%


df_counseling_attendance['class_start_time'] =  pd.to_datetime(df_counseling_attendance['class_start_time'])
df_counseling_attendance['class_start_time'] = df_counseling_attendance['class_start_time'].dt.strftime('%Y/%m/%d')



# %%


df_counseling_attendance_music = df_counseling_attendance.loc[df_counseling_attendance['parent_category_name'] == 'Music']



# %%


df_counseling_attendance_user = df_counseling_attendance_music.loc[df_counseling_attendance_music['is_booking_user'] == 'YES']
df_counseling_attendance_user_duration = df_counseling_attendance_user.loc[df_counseling_attendance_user['duration_mins'] > 0]
df_counseling_attendance_user_course_book = df_counseling_attendance_user.loc[(df_counseling_attendance_user['counselling_time_course_booked'] > 0) & (df_counseling_attendance_user['has_joined'] == 'YES')]
df_counseling_attendance__course_book_thatday = df_counseling_attendance_user.loc[(df_counseling_attendance_user['counselling_time_course_booked'] == 0) & (df_counseling_attendance_user['has_joined'] == 'YES') & (df_counseling_attendance_user['counselling_day_course_booked'] > 0)]
df_counseling_attendance__course_book_nextday = df_counseling_attendance_user.loc[(df_counseling_attendance_user['counselling_day_course_booked'] == 0) & (df_counseling_attendance_user['has_joined'] == 'YES') & (df_counseling_attendance_user['counselling_subsequent_day_course_booked'] > 0)]



# %%


df_counseling_attendance_user_pivot = df_counseling_attendance_user.pivot_table(values='session_id', index='class_start_time', columns='has_joined', aggfunc='count', margins = False).reset_index()



# %%


df_counseling_attendance_user_pivot
df_counseling_attendance_user_pivot = df_counseling_attendance_user_pivot.fillna('0')



# %%


df_counseling_attendance_user_pivot = df_counseling_attendance_user_pivot.sort_values(by='class_start_time', ascending=False)
df_counseling_attendance_user_pivot['NO'] = df_counseling_attendance_user_pivot['NO'].astype(int)
df_counseling_attendance_user_pivot['YES'] = df_counseling_attendance_user_pivot['YES'].astype(int)



# %%


df_counseling_attendance_user_pivot['Total'] = df_counseling_attendance_user_pivot['NO'] + df_counseling_attendance_user_pivot['YES']
df_counseling_attendance_user_pivot['Attendance %'] = (df_counseling_attendance_user_pivot['YES']*100)/df_counseling_attendance_user_pivot['Total']
df_counseling_attendance_user_pivot['Attendance %'] = df_counseling_attendance_user_pivot['Attendance %'].round(2)
df_counseling_attendance_user_pivot.rename(columns = {'class_start_time':'date'}, inplace = True)
df_counseling_attendance_user_pivot.rename(columns = {'NO':'counselling_missed'}, inplace = True)
df_counseling_attendance_user_pivot.rename(columns = {'YES':'counselling_attended'}, inplace = True)
df_counseling_attendance_user_pivot



# %%


df_counseling_attendance_user_duration_avg = df_counseling_attendance_user_duration.groupby(['class_start_time']).duration_mins.mean().reset_index()
df_counseling_attendance_user_duration_avg = df_counseling_attendance_user_duration_avg.sort_values(by='class_start_time', ascending=False)
df_counseling_attendance_user_duration_avg.rename(columns = {'duration_mins':'avg_duration_mins'}, inplace = True)
df_counseling_attendance_user_duration_avg.rename(columns = {'class_start_time':'date'}, inplace = True)
df_counseling_attendance_user_duration_avg['avg_duration_mins'] = df_counseling_attendance_user_duration_avg['avg_duration_mins'].round(2)
df_counseling_attendance_user_duration_avg



# %%


df_counseling_attendance_user_course_book_count = df_counseling_attendance_user_course_book.groupby(['class_start_time']).user_id.count().reset_index()
df_counseling_attendance_user_course_book_count= df_counseling_attendance_user_course_book_count.sort_values(by='class_start_time', ascending=False)
df_counseling_attendance_user_course_book_count.rename(columns = {'user_id':'course_booked_during_counselling'}, inplace = True)
df_counseling_attendance_user_course_book_count.rename(columns = {'class_start_time':'date'}, inplace = True)
df_counseling_attendance_user_course_book_count
df_counseling_attendance__course_book_count_thatday = df_counseling_attendance__course_book_thatday.groupby(['class_start_time']).user_id.count().reset_index()
df_counseling_attendance__course_book_count_thatday= df_counseling_attendance__course_book_count_thatday.sort_values(by='class_start_time', ascending=False)
df_counseling_attendance__course_book_count_thatday.rename(columns = {'user_id':'course_booked_during_counselling_day'}, inplace = True)
df_counseling_attendance__course_book_count_thatday.rename(columns = {'class_start_time':'date'}, inplace = True)
df_counseling_attendance__course_book_count_thatday
df_counseling_attendance__course_book_count_nextday = df_counseling_attendance__course_book_nextday.groupby(['class_start_time']).user_id.count().reset_index()
df_counseling_attendance__course_book_count_nextday= df_counseling_attendance__course_book_count_nextday.sort_values(by='class_start_time', ascending=False)
df_counseling_attendance__course_book_count_nextday.rename(columns = {'user_id':'course_booked_during_next_day'}, inplace = True)
df_counseling_attendance__course_book_count_nextday.rename(columns = {'class_start_time':'date'}, inplace = True)
df_counseling_attendance__course_book_count_nextday



# %%


df_counseling_user_attended = df_counseling_attendance_user.loc[df_counseling_attendance_user['has_joined'] == 'YES']
df_counseling_user_attended_sessions = df_counseling_user_attended[['session_id','has_joined','is_booking_user']]



# %%


df_counselling_user_instructor_sessions = pd.merge(df_counseling_attendance_music, 
                      df_counseling_user_attended_sessions, 
                      on ='session_id', 
                      how ='inner')



# %%


df_counselling_user_instructor_sessions



# %%


df_counselling_instructor_attended_sessions = df_counselling_user_instructor_sessions.loc[df_counselling_user_instructor_sessions['is_instructor'] == 'YES']
df_counselling_user_instructor_attneded_sessions_daywise = df_counselling_instructor_attended_sessions.groupby(['class_start_time']).session_id.nunique().reset_index()



# %%


df_counselling_user_instructor_attneded_sessions_daywise = df_counselling_user_instructor_attneded_sessions_daywise.sort_values(by='class_start_time', ascending=False)
df_counselling_user_instructor_attneded_sessions_daywise.rename(columns = {'class_start_time':'date'}, inplace = True)
df_counselling_user_instructor_attneded_sessions_daywise



# %%


df_counseling_attendance_user_pivot_attended = df_counseling_attendance_user_pivot[['date', 'counselling_attended']]
df_counselling_user_instructor_attendance_percentage = pd.merge(df_counseling_attendance_user_pivot_attended , 
                      df_counselling_user_instructor_attneded_sessions_daywise, 
                      on ='date', 
                      how ='inner')
df_counselling_user_instructor_attendance_percentage['instructor_attendance_%'] = (df_counselling_user_instructor_attendance_percentage['session_id']*100)/df_counselling_user_instructor_attendance_percentage['counselling_attended']



# %%


df_counselling_attendance_course_book_percentage = pd.merge(df_counseling_attendance_user_pivot_attended, 
                      df_counseling_attendance_user_course_book_count, 
                      on ='date', 
                      how ='inner')

df_counselling_attendance_course_book_percentage['course_book_during_counselling_%'] = (df_counselling_attendance_course_book_percentage['course_booked_during_counselling']*100)/df_counselling_attendance_course_book_percentage['counselling_attended']
df_counselling_attendance_course_book_percentage



# %%


df_counseling_attendance_user_pivot_final = df_counseling_attendance_user_pivot[['date', 'counselling_missed', 'counselling_attended', 'Total','Attendance %']]
df_counseling_attendance_user_pivot_final 



# %%


df_counselling_user_instructor_attendance_percentage_final = df_counselling_user_instructor_attendance_percentage[['date', 'instructor_attendance_%']]
df_counselling_user_instructor_attendance_percentage_final['instructor_attendance_%'] = df_counselling_user_instructor_attendance_percentage_final['instructor_attendance_%'].round(2)
df_counselling_user_instructor_attendance_percentage_final 



# %%


df_counselling_attendance_course_book_percentage_final = df_counselling_attendance_course_book_percentage[['date','course_booked_during_counselling' ,'course_book_during_counselling_%']]
df_counselling_attendance_course_book_percentage_final['course_book_during_counselling_%'] = df_counselling_attendance_course_book_percentage_final['course_book_during_counselling_%'].round(2)
df_counselling_attendance_course_book_percentage_final



# %%


order_counselling = df_orders_by_date.merge(df_order_day_counselling_booked, on='date')
order_counselling['booked_by_user_%'] = (order_counselling['Booked by user']*100)/order_counselling['Total bookings']
order_counselling['booked_by_user_%'] = order_counselling['booked_by_user_%'].round(2)
order_counselling['booked_by_admin_%'] = (order_counselling['Booked by admin']*100)/order_counselling['Total bookings']
order_counselling['booked_by_admin_%'] = order_counselling['booked_by_admin_%'].round(2)
order_counselling['total_booking_%'] = (order_counselling['Total bookings']*100)/order_counselling['no of orders']
order_counselling['total_booking_%'] = order_counselling['total_booking_%'].round(2)
order_counselling 



# %%


import numpy as np
summary = df_counseling_attendance_user_pivot_final.merge(df_counselling_user_instructor_attendance_percentage_final, on = 'date' , how = 'left').merge(df_counselling_attendance_course_book_percentage_final, on = 'date', how = 'left').merge(df_counseling_attendance_user_duration_avg, on = 'date' , how = 'left').merge(df_counseling_attendance__course_book_count_thatday , on = 'date', how = 'left').merge(df_counseling_attendance__course_book_count_nextday , on = 'date', how = 'left')
summary = summary[['date', 'counselling_missed', 'counselling_attended', 'Total', 'course_booked_during_counselling', 'course_booked_during_counselling_day' ,'course_booked_during_next_day', 'Attendance %', 'instructor_attendance_%', 'course_book_during_counselling_%', 'avg_duration_mins' ]]
summary = summary.replace(np.inf, np.nan)
summary = summary.fillna('0') 
summary



# %%


import datetime
import calendar
import numpy as np
order_counselling_weekwise = order_counselling[['date', 'no of orders', 'Booked by user', 'Booked by admin', 'Total bookings' ]].copy()
order_counselling_weekwise['date'] = pd.to_datetime(order_counselling_weekwise['date'])
order_counselling_weekwise['day'] =order_counselling_weekwise['date'].dt.day
order_counselling_weekwise['month'] =order_counselling_weekwise['date'].dt.month
order_counselling_weekwise['year'] =order_counselling_weekwise['date'].dt.year
order_counselling_weekwise['week'] = np.where(order_counselling_weekwise['day'] < 9,1, np.where(order_counselling_weekwise['day'] < 16,2, np.where(order_counselling_weekwise['day'] < 23, 3 , np.where(order_counselling_weekwise['day'] <32,4,0 ))))
order_counselling_weekwise_pivot = order_counselling_weekwise.groupby(['year', 'month', 'week'])['no of orders', 'Booked by user', 'Booked by admin', 'Total bookings'].agg('sum').reset_index()
order_counselling_weekwise_pivot['booked_by_user_%'] = (order_counselling_weekwise_pivot['Booked by user']*100)/order_counselling_weekwise_pivot['Total bookings']
order_counselling_weekwise_pivot['booked_by_user_%'] = order_counselling_weekwise_pivot['booked_by_user_%'].round(2)
order_counselling_weekwise_pivot['booked_by_admin_%'] = (order_counselling_weekwise_pivot['Booked by admin']*100)/order_counselling_weekwise_pivot['Total bookings']
order_counselling_weekwise_pivot['booked_by_admin_%'] = order_counselling_weekwise_pivot['booked_by_admin_%'].round(2)
order_counselling_weekwise_pivot['total_booking_%'] = (order_counselling_weekwise_pivot['Total bookings']*100)/order_counselling_weekwise_pivot['no of orders']
order_counselling_weekwise_pivot['total_booking_%'] = order_counselling_weekwise_pivot['total_booking_%'].round(2)
order_counselling_weekwise_pivot = order_counselling_weekwise_pivot.sort_values(by=['year', 'month', 'week'], ascending=False)
order_counselling_weekwise_pivot



# %%


counselling_summary = summary[['date', 'counselling_missed', 'counselling_attended', 'course_booked_during_counselling', 'course_booked_during_counselling_day' , 'course_booked_during_next_day', 'Total']].copy()
counselling_summary['date'] = pd.to_datetime(counselling_summary['date'])
counselling_summary['day'] =counselling_summary['date'].dt.day
counselling_summary['month'] =counselling_summary['date'].dt.month
counselling_summary['year'] =counselling_summary['date'].dt.year
counselling_summary['week'] = np.where(counselling_summary['day'] < 9,1, np.where(counselling_summary['day'] < 16,2, np.where(counselling_summary['day'] < 23, 3 , np.where(counselling_summary['day'] <32,4,0 ))))
counselling_summary['course_booked_during_counselling'] = counselling_summary['course_booked_during_counselling'].astype(int)
counselling_summary['course_booked_during_counselling_day'] = counselling_summary['course_booked_during_counselling_day'].astype(int)
counselling_summary['course_booked_during_next_day'] = counselling_summary['course_booked_during_next_day'].astype(int)
counselling_summary_pivot = counselling_summary.groupby(['year', 'month', 'week'])['counselling_missed', 'counselling_attended', 'Total', 'course_booked_during_counselling', 'course_booked_during_counselling_day', 'course_booked_during_next_day'].agg('sum').reset_index()
counselling_summary_pivot['Attendance %'] = (counselling_summary_pivot['counselling_attended']*100)/counselling_summary_pivot['Total']
counselling_summary_pivot['Attendance %'] = counselling_summary_pivot['Attendance %'].round(2)
counselling_summary_pivot['course_book_during_counselling_%'] = (counselling_summary_pivot['course_booked_during_counselling']*100)/counselling_summary_pivot['counselling_attended']
counselling_summary_pivot['course_book_during_counselling_%'] = counselling_summary_pivot['course_book_during_counselling_%'].round(2)
counselling_summary_pivot = counselling_summary_pivot.sort_values(by=['year', 'month', 'week'], ascending=False)
counselling_summary_pivot = counselling_summary_pivot.fillna(0)
counselling_summary_pivot



# %%


counseling_booking_dump['start_date'] =  pd.to_datetime(counseling_booking_dump['start_date'])
counseling_booking_dump['start_date'] = counseling_booking_dump['start_date'].dt.strftime('%Y/%m/%d')
counseling_booking_dump["userstartdate"] = counseling_booking_dump["user_id"].astype(str) + counseling_booking_dump["start_date"].astype(str)
counseling_booking_dump



# %%


df_counseling_attendance["userstartdate"] = df_counseling_attendance["user_id"].astype(str) + df_counseling_attendance["class_start_time"].astype(str)
df_counseling_booking_attendance = counseling_booking_dump.merge(df_counseling_attendance[['session_id','userstartdate', 'has_joined']] , on = 'userstartdate' , how = 'left')
df_counseling_booking_attendance_pivot = df_counseling_booking_attendance.pivot_table(values = 'session_id', index = 'booked_at', columns = 'has_joined', aggfunc = 'count', margins= False).reset_index()
df_counseling_booking_attendance_pivot = df_counseling_booking_attendance_pivot.fillna('0')
df_counseling_booking_attendance_pivot['Total'] = df_counseling_booking_attendance_pivot['NO'].astype(int) + df_counseling_booking_attendance_pivot['YES'].astype(int)
df_counseling_booking_attendance_pivot['attendance %'] = (df_counseling_booking_attendance_pivot['YES']*100).astype(int)/df_counseling_booking_attendance_pivot['Total']
df_counseling_booking_attendance_pivot  = df_counseling_booking_attendance_pivot.sort_values(by='booked_at', ascending=False)
df_counseling_booking_attendance_pivot



# %%


df_counseling_booking_attendance



# %%


df_counseling_booking_attendance
df_counselling_att_daily_instr = df_counseling_booking_attendance.pivot_table(values = 'session_id', index = ['booked_at', 'instructor_id' ,  'instructor_name'], columns = 'has_joined', aggfunc = 'count', margins= False).reset_index()
df_counselling_att_daily_instr = df_counselling_att_daily_instr.fillna('0')
df_counselling_att_daily_instr['Total'] = df_counselling_att_daily_instr['NO'].astype(int) + df_counselling_att_daily_instr['YES'].astype(int)
df_counselling_att_daily_instr['att %'] = (df_counselling_att_daily_instr['YES'].astype(int)*100)/df_counselling_att_daily_instr['Total']
df_counselling_att_daily_instr = df_counselling_att_daily_instr.sort_values(by='booked_at', ascending=False)
df_counselling_att_overll_instr = df_counseling_booking_attendance.pivot_table(values = 'session_id', index =  'instructor_name', columns = 'has_joined', aggfunc = 'count', margins= False).reset_index()
df_counselling_att_overll_instr = df_counselling_att_overll_instr.fillna('0')
df_counselling_att_overll_instr['Total'] = df_counselling_att_overll_instr['NO'].astype(int) + df_counselling_att_overll_instr['YES'].astype(int)
df_counselling_att_overll_instr['att %'] = (df_counselling_att_overll_instr['YES'].astype(int)*100)/df_counselling_att_overll_instr['Total']
df_counselling_att_daily_instr



# %%


df_counseling_attendance_instr = df_counseling_attendance_music[['session_id', 'user_id' , 'instructor_id', 'instructor_name', 'has_joined', 'booked_at', 'class_start_time', 'duration_mins', 'no_of_dropoffs','user_waiting_time', 'platform' , 'is_admin', 'is_instructor', 'is_booking_user']].copy()
df_counseling_attendance_instr_user = df_counseling_attendance_instr.loc[(df_counseling_attendance_instr['is_booking_user'] == 'YES') & (df_counseling_attendance_instr['duration_mins'] > 0)].copy()
df_counseling_attendance_instr_user
df_counseling_attendance_instr_user['duration bkt'] = np.where(df_counseling_attendance_instr_user['duration_mins'].astype(int) <15, 'less than 15 mins' , 
                                                          np.where(df_counseling_attendance_instr_user['duration_mins'].astype(int) >=15 , 'More than 15 mins', 
                                                           'else' ))
df_counseling_attendance_instr_pivot = df_counseling_attendance_instr_user.pivot_table(values='session_id', index=[ 'class_start_time', 'instructor_id', 'instructor_name'], columns='duration bkt', aggfunc='count', margins = False).reset_index()
df_counseling_attendance_instr_pivot = df_counseling_attendance_instr_pivot.fillna('0')
df_counseling_attendance_instr_pivot = df_counseling_attendance_instr_pivot.sort_values(by='class_start_time', ascending=False)
df_counseling_attendance_instr_pivot['Total sessions'] = df_counseling_attendance_instr_pivot['More than 15 mins'].astype(int) + df_counseling_attendance_instr_pivot['less than 15 mins'].astype(int)
df_counseling_attendance_instr_pivot['% less than 15 mins'] = (df_counseling_attendance_instr_pivot['less than 15 mins'].astype(int)*100)/df_counseling_attendance_instr_pivot['Total sessions']
df_counseling_attendance_instr_pivot



# %%


df_counseling_attendance_usr_low_durtn = df_counseling_attendance_instr.loc[(df_counseling_attendance_instr['is_booking_user'] == 'YES') & (df_counseling_attendance_instr['duration_mins'] <15) & (df_counseling_attendance_instr['duration_mins'] > 0)].copy()
df_counseling_attendance_low_durtn_rca = df_counseling_attendance_usr_low_durtn[['session_id' , 'class_start_time', 'user_id' , 'instructor_id' , 'instructor_name', 'platform' ,  'duration_mins' , 'no_of_dropoffs', 'user_waiting_time']].copy()
df_counseling_attendance_low_durtn_rca.rename(columns = {'no_of_dropoffs':'no_of_dropoffs_users'}, inplace = True)
df_counseling_attendance_instr_low_durtn = df_counseling_attendance_instr[['session_id', 'platform', 'no_of_dropoffs', 'user_waiting_time']].loc[(df_counseling_attendance_instr['is_instructor'] == 'YES')].copy()
df_counseling_attendance_instr_low_durtn.rename(columns = {'no_of_dropoffs':'no_of_dropoffs_instr'}, inplace = True)
df_counseling_attendance_instr_low_durtn.rename(columns = {'user_waiting_time':'instr_waiting_time'}, inplace = True)
df_counseling_attendance_instr_low_durtn.rename(columns = {'platform':'instr_platform'}, inplace = True)
df_counseling_attendance_low_durtn_rca = df_counseling_attendance_low_durtn_rca.merge(df_counseling_attendance_instr_low_durtn, on = 'session_id' , how = 'left').reset_index()
df_counseling_attendance_low_durtn_rca = df_counseling_attendance_low_durtn_rca.fillna(' ')
df_counseling_attendance_low_durtn_rca



# %%


import gspread 
from oauth2client.service_account import ServiceAccountCredentials



# %%
import os
pwd=os.getcwd()

# define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name(pwd+'/credentials.json', scope)

# authorize the clientsheet 
client = gspread.authorize(creds)



# %%


# get the instance of the Spreadsheet
sheet = client.open('Counselling automation')

# get the first sheet of the Spreadsheet
booking = sheet.get_worksheet(0)
attendance= sheet.get_worksheet(1)
weekwise_booking = sheet.get_worksheet(2)
weekwise_attendance = sheet.get_worksheet(3)
booking_attendance = sheet.get_worksheet(4)
inst_daily = sheet.get_worksheet(5)
inst_ovrall = sheet.get_worksheet(6)
instr_duration =  sheet.get_worksheet(7)
instr_duration_rca =  sheet.get_worksheet(8)



# %%


booking.update('A:Z', [order_counselling.columns.values.tolist()]+ order_counselling.values.tolist())



# %%


attendance.update('A:Z', [summary.columns.values.tolist()]+ summary.values.tolist())



# %%


weekwise_booking.update('A:Z', [order_counselling_weekwise_pivot.columns.values.tolist()]+ order_counselling_weekwise_pivot.values.tolist())



# %%


weekwise_attendance.update('A:Z', [counselling_summary_pivot.columns.values.tolist()]+ counselling_summary_pivot.values.tolist())



# %%


booking_attendance.update('A:Z', [df_counseling_booking_attendance_pivot.columns.values.tolist()]+ df_counseling_booking_attendance_pivot.values.tolist())



# %%


inst_daily.update('A:ZZ', [df_counselling_att_daily_instr.columns.values.tolist()]+ df_counselling_att_daily_instr.values.tolist())



# %%


inst_ovrall.update('A:Z', [df_counselling_att_overll_instr.columns.values.tolist()]+ df_counselling_att_overll_instr.values.tolist())



# %%


instr_duration.update('A:Z', [df_counseling_attendance_instr_pivot.columns.values.tolist()]+ df_counseling_attendance_instr_pivot.values.tolist())



# %%


instr_duration_rca.update('A:Z', [df_counseling_attendance_low_durtn_rca.columns.values.tolist()]+ df_counseling_attendance_low_durtn_rca.values.tolist())



# %%



import pandas as pd
import gspread
from gspread_dataframe import get_as_dataframe, set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials
import json
import random
import sys
import os
import numpy as np
from datetime import datetime,date,timedelta
from math import ceil
import requests
pwd=os.getcwd()
scope =["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds =ServiceAccountCredentials.from_json_keyfile_name(pwd+"/credentials.json", scope)
client = gspread.authorize(creds)
spreadsheet = client.open("Counselling automation")
kmk="Booking summary"
wks1=spreadsheet.worksheet(kmk)
print()
dfs1=pd.DataFrame(wks1.get_all_records())
kmk="attendance summary"
wks1=spreadsheet.worksheet(kmk)
print()
dfs2=pd.DataFrame(wks1.get_all_records())




dfs1
dfs1['date']=pd.to_datetime(dfs1['date']).dt.date
dfs2['date']=pd.to_datetime(dfs2['date']).dt.date
d=date.today()-timedelta(1)
dfs1=dfs1[dfs1['date']==d]
dfs2=dfs2[dfs2['date']==d]
dfs2
a=dfs1['no of orders'].tolist()
b=dfs1['Total bookings'].tolist()
c=dfs1['total_booking_%'].tolist()
d=dfs2['counselling_attended'].tolist()
e=dfs2['counselling_missed'].tolist()
f=dfs2['Total'].tolist()
g=dfs2['Attendance %'].tolist()
h=dfs2['instructor_attendance_%'].tolist()
i=dfs2['course_book_during_counselling_%'].tolist()
j=dfs2['avg_duration_mins'].tolist()
k=dfs2['date'].tolist()

dd=str(k[0])
dd
if(len(a)>0):
    msg=""
    p0="No of Orders: "+str(a[0])
    p1="Total Bookings: "+str(b[0])
    p2="Total Booking(%): "+str(c[0])+'%'
    p3="Counselling Attended: "+str(d[0])
    p4="Counselling Missed: "+str(e[0])
    p5="Total Counselling: "+str(f[0])
    p6="Attendance(%): "+str(g[0])+'%'
    p7="Instructor Attendance: "+str(h[0])+'%'
    p8="Course Book(%): "+str(i[0])+'%'
    p9="Avg. Duration(mins): "+str(j[0])
    msg=msg+p0+'\n'+p1+'\n'+p2+'\n'+'\n'+p3+'\n'+p4+'\n'+p5+'\n'+p6+'\n'+'\n'+p7+'\n'+p8+'\n'+p9
    url = "https://hooks.slack.com/services/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"
    message = (msg)
    title = (f"Counselling Summary For "+dd)
    slack_data = {
        "username": "NotificationBot",
        "icon_emoji": ":satellite:",
        #"channel" : "#somerandomcahnnel",
        "attachments": [
            {
                "color": "#008080",
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



# %%






# %%







