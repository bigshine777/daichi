import streamlit as st
import pandas as pd
import yfinance as yf
import altair as alt
def get_data(days,tickers):
    df=pd.DataFrame()
    for company in tickers.keys():
        tkl=yf.Ticker(tickers[company])
        hist=tkl.history(period=f'{days}d')
        hist.index=hist.index.strftime('%d %B %Y')
        hist=hist[['Close']]
        hist.columns=[company]
        hist=hist.T
        hist.index.name='Name'
        df=pd.concat([df,hist])
    return df
try:
    st.title('株価可視化アプリ')
    st.sidebar.write("""
    こちらは株価可視化ツールだよ！以下のオプションから表示日数を変更してね
    """)
    st.sidebar.write("""
    ## 表示日数選択
    """)
    days=st.sidebar.slider('日数',1,50,25)
    st.write(f"""
    ### 過去＊＊{days}日間＊＊のGAFA株価
    """)
    st.sidebar.write("""
    ## 株価の範囲指定
    """)
    ymin,ymax=st.sidebar.slider(
        '範囲を指定',
        0.0,800.0,(0.0,800.0)
    )
    tickers={
        'apple':'AAPL',
        'facebook':'META',
        'google':'GOOGL',
        'microsoft':'MSFT',
        'netflix':'NFLX',
        'amazon':'AMZN'
    }
    df=get_data(days,tickers)
    campany=st.multiselect(
        '会社名を選択してください',
        list(df.index)
    )
    if not campany:
        st.error('少なくとも一社は選んでください')
    else:
        data=df.loc[campany]
        st.write('### 株価(USD)',data.sort_index())
        data=pd.melt(data.reset_index(),id_vars=['Name']).rename(
            columns={'value':'Stock Prices(USD)'}
        )
        chart=(
            alt.Chart(data)
            .mark_line(opacity=0.8,clip=True)
            .encode(
                x='Date:T',
                y=alt.Y('Stock Prices(USD):Q',stack=None,scale=alt.Scale(domain=[ymin,ymax])),
                color='Name:N'
            )
        )
        st.altair_chart(chart,use_container_width=True)
except:
    st.error('エラーが発生しました。リロードを行ってください')


