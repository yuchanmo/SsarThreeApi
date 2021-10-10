import pandas as pd
from constant import *
from datetime import datetime
import datetime
from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy as np

def index(df):
    #평균 낙찰가
    df['auction_date'] = pd.to_datetime(df['auction_date'])
    avg_money = df.groupby(['artist_name_kor_born'])[['money']].mean()
    avg_money['avg_rank'] = avg_money['money'].rank(method = 'dense', ascending=False)
    avg_money = avg_money.sort_values(by=['avg_rank'], ascending=True)

    #호당 낙찰가
    canvas_avg_money = df.groupby(['artist_name_kor_born'])[['canvas_size_money']].mean()
    canvas_avg_money['canvas_avg_rank'] = canvas_avg_money['canvas_size_money'].rank(method = 'dense', ascending=False)
    canvas_avg_money = canvas_avg_money.sort_values(by=['canvas_avg_rank'], ascending=True)

    #최고 낙찰가
    max_money = df.groupby(['artist_name_kor_born'])[['money']].max()
    max_money['max_rank'] = max_money['money'].rank(method = 'dense', ascending=False)
    max_money = max_money.sort_values(by=['max_rank'], ascending=True)

    #총 판매가
    sum_money = df.groupby(['artist_name_kor_born'])[['money']].sum()
    sum_money['sum_rank'] = sum_money['money'].rank(method = 'dense', ascending=False)
    sum_money = sum_money.sort_values(by=['sum_rank'], ascending=True)

    #출품수
    count_money = df.groupby(['artist_name_kor_born'])[['artist_name_kor_born']].count()
    count_money['count_rank'] = count_money['artist_name_kor_born'].rank(method = 'dense', ascending=False)
    count_money = count_money.sort_values(by=['count_rank'], ascending=True)
    count_money.columns = ['count','count_rank']
    #최근 6개월 상승율
    df_6month = df[(df['auction_date'] < datetime.today().strftime('%Y-%m-%d')) & (df['auction_date'] >= (datetime.today() - relativedelta(months=+6)).strftime('%Y-%m-%d'))]
    df_12month = df[(df['auction_date'] < (datetime.today() - relativedelta(months=+6)).strftime('%Y-%m-%d')) & (df['auction_date'] >= (datetime.today() - relativedelta(months=+12)).strftime('%Y-%m-%d'))]

    df_6month_avg_money = df_6month.groupby(['artist_name_kor_born'])[['money']].mean()
    df_12month_avg_money = df_12month.groupby(['artist_name_kor_born'])[['money']].mean()

    recent_increased_rate = pd.merge(df_6month_avg_money, df_12month_avg_money, left_index = True, right_index = True, how = 'inner')
    recent_increased_rate = recent_increased_rate.dropna(axis = 0)

    recent_increased_rate['increased_rate'] = (recent_increased_rate['money_x'] - recent_increased_rate['money_y'])/recent_increased_rate['money_y']*100
    recent_increased_rate = recent_increased_rate[['increased_rate']]
    recent_increased_rate['increased_rate'] = round(recent_increased_rate['increased_rate'],1).astype(str) + '%'

    #전체 랭크
    total_index = pd.merge(avg_money, canvas_avg_money, left_index = True, right_index = True, how = 'left')
    total_index = pd.merge(total_index, max_money, left_index = True, right_index = True, how = 'left')
    total_index = pd.merge(total_index, sum_money, left_index = True, right_index = True, how = 'left')
    total_index = pd.merge(total_index, count_money, left_index = True, right_index = True, how = 'left')
    total_index = pd.merge(total_index, recent_increased_rate, left_index = True, right_index = True, how = 'left')

    total_index = total_index[['increased_rate','avg_rank','canvas_avg_rank','max_rank','sum_rank','count_rank']]
    total_index['total_sum'] = total_index['avg_rank']+ total_index['canvas_avg_rank']+total_index['max_rank']+total_index['sum_rank']+total_index['count_rank']
    total_index['total_rank'] = total_index['total_sum'].rank(method = 'dense', ascending=True)
    total_index = total_index.sort_values(by=['total_rank'], ascending=True)
        
    return avg_money, canvas_avg_money, max_money, sum_money, count_money, recent_increased_rate, total_index

start = datetime.now()
df = pd.read_sql('exec getArtistRanking',sqlserver)
end = datetime.now()
print(end-start)
df.head()
df['artist_name_kor_born'] = df['artist_name_kor'] + '('+ df['birth'] + ')'


df['auction_date'] = pd.to_datetime(df['auction_date'])
avg_money = df.groupby(['artist_name_kor_born','artist_id'])[['money']].mean()
avg_money['avg_rank'] = avg_money['money'].rank(method = 'dense', ascending=False)
avg_money = avg_money.sort_values(by=['avg_rank'], ascending=True)

#호당 낙찰가
canvas_avg_money = df.groupby(['artist_name_kor_born','artist_id'])[['canvas_size_money']].mean()
canvas_avg_money['canvas_avg_rank'] = canvas_avg_money['canvas_size_money'].rank(method = 'dense', ascending=False)
canvas_avg_money = canvas_avg_money.sort_values(by=['canvas_avg_rank'], ascending=True)

#최고 낙찰가
max_money = df.groupby(['artist_name_kor_born','artist_id'])[['money']].max()
max_money['max_rank'] = max_money['money'].rank(method = 'dense', ascending=False)
max_money = max_money.sort_values(by=['max_rank'], ascending=True)

#총 판매가
sum_money = df.groupby(['artist_name_kor_born','artist_id'])[['money']].sum()
sum_money['sum_rank'] = sum_money['money'].rank(method = 'dense', ascending=False)
sum_money = sum_money.sort_values(by=['sum_rank'], ascending=True)

#출품수
count_money = df.groupby(['artist_name_kor_born','artist_id'])[['artist_name_kor_born']].count()
count_money['count_rank'] = count_money['artist_name_kor_born'].rank(method = 'dense', ascending=False)
count_money = count_money.sort_values(by=['count_rank'], ascending=True)
count_money.columns = ['count','count_rank']
#최근 6개월 상승율
df_6month = df[(df['auction_date'] < datetime.today().strftime('%Y-%m-%d')) & (df['auction_date'] >= (datetime.today() - relativedelta(months=+6)).strftime('%Y-%m-%d'))]
df_12month = df[(df['auction_date'] < (datetime.today() - relativedelta(months=+6)).strftime('%Y-%m-%d')) & (df['auction_date'] >= (datetime.today() - relativedelta(months=+12)).strftime('%Y-%m-%d'))]

df_6month_avg_money = df_6month.groupby(['artist_name_kor_born','artist_id'])[['money']].mean()
df_12month_avg_money = df_12month.groupby(['artist_name_kor_born','artist_id'])[['money']].mean()

recent_increased_rate = pd.merge(df_6month_avg_money, df_12month_avg_money, left_index = True, right_index = True, how = 'inner')
recent_increased_rate = recent_increased_rate.dropna(axis = 0)

recent_increased_rate['increased_rate'] = (recent_increased_rate['money_x'] - recent_increased_rate['money_y'])/recent_increased_rate['money_y']*100
recent_increased_rate = recent_increased_rate[['increased_rate']]
recent_increased_rate['increased_rate'] = round(recent_increased_rate['increased_rate'],1).astype(str) + '%'

#전체 랭크
total_index = pd.merge(avg_money, canvas_avg_money, left_index = True, right_index = True, how = 'left')
total_index = pd.merge(total_index, max_money, left_index = True, right_index = True, how = 'left')
total_index = pd.merge(total_index, sum_money, left_index = True, right_index = True, how = 'left')
total_index = pd.merge(total_index, count_money, left_index = True, right_index = True, how = 'left')
total_index = pd.merge(total_index, recent_increased_rate, left_index = True, right_index = True, how = 'left')

total_index = total_index[['increased_rate','avg_rank','canvas_avg_rank','max_rank','sum_rank','count_rank']]
total_index['total_sum'] = total_index['avg_rank']+ total_index['canvas_avg_rank']+total_index['max_rank']+total_index['sum_rank']+total_index['count_rank']
total_index['total_rank'] = total_index['total_sum'].rank(method = 'dense', ascending=True)
total_index = total_index.sort_values(by=['total_rank'], ascending=True)

avg_money = avg_money.join(recent_increased_rate,how='left').reset_index().fillna('')
avg_money.columns = ['artist_name_kor_born','artist_id','money','rank','increased_rate']
canvas_avg_money = canvas_avg_money.join(recent_increased_rate,how='left').reset_index().fillna('')
canvas_avg_money.columns = ['artist_name_kor_born','money','rank','increased_rate']
max_money = max_money.join(recent_increased_rate,how='left').reset_index().fillna('')
max_money.columns = ['artist_name_kor_born','money','rank','increased_rate']
sum_money = sum_money.join(recent_increased_rate,how='left').reset_index().fillna('')
sum_money.columns = ['artist_name_kor_born','money','rank','increased_rate']
count_money = count_money.join(recent_increased_rate,how='left').reset_index().fillna('')
count_money.columns = ['artist_name_kor_born','count','rank','increased_rate']
total_index = total_index.reset_index().fillna('')
recent_increased_rate = recent_increased_rate.reset_index().fillna('')

a = total_index[total_index['artist_id']==6987]
a.sample(frac=1)[:6]

df = pd.read_sql('exec getArtistRanking',sqlserver)
df['artist_name_kor_born'] = df['artist_name_kor'] + '('+ df['birth'] + ')'
avg,canvas,max,sum,count,recent,total = index(df)

a,c,m,s,co,r,t = index(df)
end = datetime.now()
print(end-start)

len(a)
len(r)
r.head()

a.head()
c.head()
m.head()
s.head()
co.head()
r.head()

co.columns = ['count','count_rank']

a.join(r,how='left').reset_index()
c.join(r,how='left').reset_index()
m.join(r,how='left').reset_index()
s.join(r,how='left').reset_index()
co.join(r,how='left').reset_index()
co.head()



artist_id = 6987


auction_art_df = pd.read_sql(f"exec getAuctionArtDetail {art_info_id}",sqlserver)
auction_art_row = auction_art_df.iloc[0]
auction_art_history_df = pd.read_sql(f"exec getAuctionPriceHistory {art_info_id}",sqlserver)

auction_art_row.to_dict()

auction_art_df.dtypes
df = pd.read_sql(f'exec getArtistDetailRankingEtl',sqlserver)

df['artist_name_kor_born'] = df['artist_name_kor'] + '('+ df['birth'] + ')'
df['auction_date'] = pd.to_datetime(df['auction_date'])
df[['estimate_high','estimate_low','canvas_size']] = df[['estimate_high','estimate_low','canvas_size']].apply(pd.to_numeric).apply(pd.Series)
conditions = [
    (df['size_length'] > df['size_width']),
    (df['size_length'] < df['size_width']),
    (df['size_length'] == df['size_width']),
    ]
choices = [df['size_length'], df['size_width'], df['size_width']]
df['max_size'] = np.select(conditions, choices, default='0')
df['max_size'] = pd.to_numeric(df['max_size'])

df = df[df['auction_date'].notna()]
df['auction_year'] = (df['auction_date'].dt.year).astype('int')
df['auction_year'] = df['auction_year'].astype('str') + '_' + df['half_year'].astype(str)
df['canvas_estimate_high'] = np.where((df['artwork_type'] == 'work on paper')|(df['artwork_type'] == 'paintings'), df['estimate_high']/df['canvas_size'], np.nan)
df['canvas_estimate_high'] = df['canvas_estimate_high'].astype(float)
df['canvas_estimate_low'] = np.where((df['artwork_type'] == 'work on paper')|(df['artwork_type'] == 'paintings'), df['estimate_low']/df['canvas_size'], np.nan)
df['canvas_estimate_low'] = df['canvas_estimate_low'].astype(float)


#Lots Performance Against Estimate
conditions = [ 
(df['money'] == np.nan),
(df['money']<df['canvas_estimate_low']),
(df['max_size']>=df['canvas_estimate_low']) & (df['max_size']<=df['canvas_estimate_high']), 
(df['money']>df['canvas_estimate_high'])
]

choices = ['Drop','Below Estimate','Within Estimate','Above Estimate']
df['aganist_estimate'] = np.select(conditions, choices, default=np.nan).astype(str)
potion_count = df.groupby(['artist_id','artist_name_kor_born','auction_year','aganist_estimate'])[['aganist_estimate']].count()



#Lots Performance Against Estimate

conditions = [ 
(df['money'] < 10000000),
(df['money'] >= 10000000) & (df['money'] < 50000000),
(df['money'] >= 50000000) & (df['money'] < 100000000),
(df['money'] >= 100000000) & (df['money'] < 1000000000),
(df['money'] >= 1000000000)
]

choices = ['1000만원 미만','1000만원이상 5000만원이하','5000만원이상 1억원이하','1억원이상 10억원이하','10억원이상']
df['potion_price'] = np.select(conditions, choices, default=np.nan).astype(str)
potion_price = df.groupby(['artist_id','artist_name_kor_born','auction_year','potion_price'])[['potion_price']].count()


#평균 낙찰가
avg_money = df.groupby(['artist_id','artist_name_kor_born','auction_year'])[['money','estimate_high','estimate_low']].mean()
avg_money.reset_index(inplace = True)
avg_money['a_rank'] = avg_money.groupby(['auction_year'])['money'].rank(method = 'dense', ascending=False)



#호당 낙찰가
canvas_avg_money = df.groupby(['artist_id','artist_name_kor_born','auction_year'])[['canvas_size_money','canvas_estimate_high','canvas_estimate_low']].mean()
canvas_avg_money.reset_index(inplace = True)
canvas_avg_money['canvas_rank'] = canvas_avg_money.groupby(['auction_year'])['canvas_size_money'].rank(method = 'dense', ascending=False)

#최고 낙찰가
max_money = df.groupby(['artist_id','artist_name_kor_born','auction_year'])[['money']].max()
max_money.reset_index(inplace = True)
max_money['m_rank'] = max_money.groupby(['auction_year'])['money'].rank(method = 'dense', ascending=False)


#총 판매가
sum_money = df.groupby(['artist_id','artist_name_kor_born','auction_year'])[['money']].sum()
sum_money.reset_index(inplace = True)
sum_money['s_rank'] = sum_money.groupby(['auction_year'])['money'].rank(method = 'dense', ascending=False)

#출품수
count_money = df.groupby(['artist_id','artist_name_kor_born','auction_year'])[['money']].count()
count_money.reset_index(inplace = True)
count_money['c_rank'] = count_money.groupby(['auction_year'])['money'].rank(method = 'dense', ascending=False)

#전체 랭크
total_index = pd.merge(avg_money, canvas_avg_money, left_on = ['artist_id','artist_name_kor_born','auction_year'], right_on = ['artist_id','artist_name_kor_born','auction_year'], how = 'left')
total_index = pd.merge(total_index, max_money, left_on = ['artist_id','artist_name_kor_born','auction_year'], right_on = ['artist_id','artist_name_kor_born','auction_year'], how = 'left')
total_index = pd.merge(total_index, sum_money, left_on = ['artist_id','artist_name_kor_born','auction_year'], right_on = ['artist_id','artist_name_kor_born','auction_year'], how = 'left')
total_index = pd.merge(total_index, count_money, left_on = ['artist_id','artist_name_kor_born','auction_year'], right_on = ['artist_id','artist_name_kor_born','auction_year'], how = 'left')
detail_chart = pd.merge(avg_money, canvas_avg_money, left_on = ['artist_id','artist_name_kor_born','auction_year'], right_on = ['artist_id','artist_name_kor_born','auction_year'], how = 'left')
detail_chart = detail_chart[['artist_id','artist_name_kor_born','auction_year','money','estimate_high','estimate_low','canvas_size_money','canvas_estimate_high','canvas_estimate_low']] 

total_index = total_index[['artist_id','artist_name_kor_born','auction_year','a_rank','canvas_rank','m_rank','s_rank','c_rank']]
total_index['total_sum'] = total_index['a_rank']+ total_index['canvas_rank']+total_index['m_rank']+total_index['s_rank']+total_index['c_rank']
total_index['rank'] = total_index.groupby(['auction_year'])['total_sum'].rank(method = 'dense', ascending=False)
total_index = total_index.sort_values(by=['rank'], ascending=True)
total_index = total_index[['artist_id','artist_name_kor_born','auction_year','rank']]
avg_money, canvas_avg_money, max_money, sum_money, count_money, total_index, detail_chart, potion_count, potion_price


potion_count, potion_price

avg_money.to_sql('avg_money',sqlserver,'dbo',if_exists='append',index=False)
canvas_avg_money.to_sql('canvas_avg_money',sqlserver,'dbo',if_exists='append',index=False)
max_money.to_sql('max_money',sqlserver,'dbo',if_exists='append',index=False)
sum_money.to_sql('sum_money',sqlserver,'dbo',if_exists='append',index=False)
count_money.to_sql('count_money',sqlserver,'dbo',if_exists='append',index=False)
total_index.to_sql('total_index',sqlserver,'dbo',if_exists='append',index=False)
detail_chart.to_sql('detail_chart',sqlserver,'dbo',if_exists='append',index=False)
potion_count.to_sql('potion_count',sqlserver,'dbo',if_exists='append',index=False)
potion_price.to_sql('potion_price',sqlserver,'dbo',if_exists='append',index=False)

df['auction_year'].to_list()
artist_id = 6987
df = pd.read_sql('exec [getArtistDetailRanking] 6987',sqlserver)
df = pd.read_sql(f'exec [getArtistDetailMoneyChart] {artist_id}',sqlserver)
df[['money','estimate_high','estimate_low']] = df[['money','estimate_high','estimate_low']].fillna(0).apply(lambda x : round(x,0))

res = dict()
groups = df.groupby('cate')
for gn,g in groups:    
    x = g['auction_year'].to_list()
    y1 = g['money'].to_list()
    y2 = g['estimate_high'].to_list()
    y3 = g['estimate_low'].to_list()
    res[gn] = {'x':x,'y':[{'data':y1},{'data':y2},{'data':y3}]}