# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 13:53:36 2024

@author: Oyku
"""
import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import streamlit as st
import plotly.express as px
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import streamlit_js_eval
import numpy as np
# Setting Streamlit page configuration
st.set_page_config(
    page_title="UrClimate",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Hiding Streamlit default styles and buttons
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
            header {visibility: hidden;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton { visibility:hidden;}
button[title="View fullscreen"]{
    visibility: hidden;}
 [data-testid="stSidebar"]{
        visibility: hidden;
    }
 [data-testid="collapsedControl"] {
       display: none
   }
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

#Veri input

ortalama_sıcaklık = pd.read_csv('data_manipulation/HES/temperature_mean.csv')
minimum_sıcaklık = pd.read_csv('data_manipulation/HES/temperature_min.csv')
maksimum_sıcaklık= pd.read_csv('data_manipulation/HES/temperature_max.csv')
yagis= pd.read_csv('data_manipulation/HES/precipitation_sum.csv')
kar= pd.read_csv('data_manipulation/HES/snowfall_sum.csv')
buharlasma=pd.read_csv('data_manipulation/HES/et0_fao_evapotranspiration_sum.csv')
soil_m=pd.read_csv('data_manipulation/HES/soil_moisture_0_to_10cm_mean.csv')
#Başlık
st.title("HES")
if st.button("Anasayfaya Geri Dön"):
        # Tarayıcıda sayfanın URL'sini değiştirerek Anasayfa.py sayfasına geri dönme
        st.experimental_set_query_params()
#Artış Azalışlar
col1, col2, col3 = st.columns(3)


ortalama_sıcaklık['date'] = pd.to_datetime(ortalama_sıcaklık['date'])
yıllık_ortalamalar = ortalama_sıcaklık.groupby(ortalama_sıcaklık['date'].dt.year)['temperature_2m_mean'].mean().reset_index()
yıllık_ortalamalar.set_index('date', inplace=True)

# İlgili yıllara göre filtrele
yıl_2020_2023 = yıllık_ortalamalar.loc['1950':'2023'].mean()
yıl_2046_2049 = yıllık_ortalamalar.loc['2024':'2049'].mean()

# Farkı hesapla
fark = yıl_2046_2049 - yıl_2020_2023

col1.metric("Yıllık Ort. Sıcaklık", f"{yıl_2046_2049[0].round(2)} °C", fark[0].round(2))

yagis['date'] = pd.to_datetime(yagis['date'])
yıllık_ortalama_yagis = yagis.groupby(yagis['date'].dt.year)['precipitation_sum'].mean().reset_index()
yıllık_ortalama_yagis.set_index('date', inplace=True)

# İlgili yıllara göre filtrele
yagis_yıl_2020_2023 = yıllık_ortalama_yagis.loc['1950':'2023'].mean()
yagis_yıl_2046_2049 = yıllık_ortalama_yagis.loc['2024':'2049'].mean()

# Farkı hesapla
yagis_fark = yagis_yıl_2046_2049 - yagis_yıl_2020_2023


col2.metric("Yıllık Ort. Yağış", f"{yagis_yıl_2046_2049[0].round(2)} mm", yagis_fark[0].round(2))

kar['date'] = pd.to_datetime(kar['date'])
yıllık_ortalama_kar = kar.groupby(kar['date'].dt.year)['snowfall_sum'].mean().reset_index()
yıllık_ortalama_kar.set_index('date', inplace=True)

# İlgili yıllara göre filtrele
kar_yıl_2020_2023 = yıllık_ortalama_kar.loc['1950':'2023'].mean()
kar_yıl_2046_2049 = yıllık_ortalama_kar.loc['2024':'2049'].mean()

# Farkı hesapla
kar_fark = kar_yıl_2046_2049 - kar_yıl_2020_2023

col3.metric("Yıllık Ort. Kar Yağışı", f"{kar_yıl_2046_2049[0].round(2)} cm", kar_fark[0].round(2))
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Sıcaklık", "Yağış", "Kar Yağışı","Debi Tahmini","Kuraklık"])

with tab1:
   
   col1, col2 = st.columns([1,1],gap="medium")
   
   
   with col1:
        # Tarih sütununu datetime türüne çevir
       ortalama_sıcaklık['date'] = pd.to_datetime(ortalama_sıcaklık['date'])
       minimum_sıcaklık['date'] = pd.to_datetime(minimum_sıcaklık['date'])
       maksimum_sıcaklık['date'] = pd.to_datetime(maksimum_sıcaklık['date'])
        
        # Yıllık ortalama, maksimum ve minimum sıcaklık hesapla
       ortalama_sıcaklık['yil'] = ortalama_sıcaklık['date'].dt.year
       minimum_sıcaklık['yil'] = minimum_sıcaklık['date'].dt.year
       maksimum_sıcaklık['yil'] = maksimum_sıcaklık['date'].dt.year
       yillik_ortalama = ortalama_sıcaklık.groupby('yil')['temperature_2m_mean'].mean().reset_index()
       yillik_min = minimum_sıcaklık.groupby('yil')['temperature_2m_min'].mean().reset_index()
       yillik_max = maksimum_sıcaklık.groupby('yil')['temperature_2m_max'].mean().reset_index()
        
        # Plotly figürü oluştur
       fig = go.Figure()
        
        # Yıllık ortalama, maksimum ve minimum sıcaklık izlerini ekle
       fig.add_trace(go.Scatter(x=yillik_ortalama['yil'], y=yillik_ortalama['temperature_2m_mean'], mode='lines', name='Yıllık Ortalama Sıcaklık'))
       fig.add_trace(go.Scatter(x=yillik_min['yil'], y=yillik_min['temperature_2m_min'], mode='lines', name='Yıllık Min Sıcaklık'))
       fig.add_trace(go.Scatter(x=yillik_max['yil'], y=yillik_max['temperature_2m_max'], mode='lines', name='Yıllık Max Sıcaklık'))
        
        # Layout'u güncelle
       fig.update_layout(title='Yıllık Ortalama, Min ve Max Sıcaklık',
                          xaxis_title='Yıl',
                          yaxis_title='Sıcaklık (°C)')
        
        # Grafiği göster
       st.plotly_chart(fig)
       container = st.container(border=True)
       container.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
   with col2:
        # Tarih sütununu datetime türüne çevir
       sorted_data = maksimum_sıcaklık.sort_values(by='temperature_2m_max', ascending=False)
       num_rows = len(sorted_data)
       top_1_percent_index = int(num_rows * 0.01)
       top_1_percent_slice = sorted_data.head(top_1_percent_index)
       belirli_deger=top_1_percent_slice["temperature_2m_max"].min()
       filtrelenmis_df = maksimum_sıcaklık[maksimum_sıcaklık['temperature_2m_max'] >= belirli_deger]
       yillik_sayilar = filtrelenmis_df.groupby(filtrelenmis_df['date'].dt.year).size().reset_index(name='sayi')
       fig = px.bar(yillik_sayilar, x='date', y='sayi', title="Sıcak Hava Dalgası Sıklığı")
       fig.update_layout(xaxis_title='Yıl', yaxis_title='Sayı')
        
        # Eğilim çizgisini ekleyin
       z = np.polyfit(yillik_sayilar['date'], yillik_sayilar['sayi'], 1)
       p = np.poly1d(z)

       # Eğilim çizgisini grafiğe ekle
       fig.add_scatter(x=yillik_sayilar['date'], y=p(yillik_sayilar['date']), mode='lines',line=dict(color='red'),name='Eğilim Çizgisi')
       st.plotly_chart(fig,use_container_width=True)
       container2 = st.container(border=True)
       container2.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
with tab2:
   
   col1, col2 = st.columns([1,1],gap="medium")
   
   
   with col1:
       
       
        # Tarih sütununu datetime türüne çevir
       yagis['date'] = pd.to_datetime(yagis['date'])
        
         
         # Yıllık ortalama, maksimum ve minimum sıcaklık hesapla
       yagis['yil'] = yagis['date'].dt.year
        
       yillik_ortalama = yagis.groupby('yil')['precipitation_sum'].mean().reset_index()
           
         
         # Plotly figürü oluştur
       fig = go.Figure()
         
         # Yıllık ortalama, maksimum ve minimum sıcaklık izlerini ekle
       fig.add_trace(go.Scatter(x=yillik_ortalama['yil'], y=yillik_ortalama['precipitation_sum'], mode='lines', name='Yıllık Ortalama Yağış'))
           
         
         # Layout'u güncelle
       fig.update_layout(title='Yıllık Ortalama Yağış',
                           xaxis_title='Yıl',
                           yaxis_title='Yağış(mm)')
       z = np.polyfit(yillik_ortalama['yil'], yillik_ortalama['precipitation_sum'], 1)
       p = np.poly1d(z)
         
        # Eğilim çizgisini grafiğe ekle
       fig.add_scatter(x=yillik_ortalama['yil'], y=p(yillik_ortalama['yil']), mode='lines',line=dict(color='red'),name='Eğilim Çizgisi') 
         # Grafiği göster
       st.plotly_chart(fig)
       
       container = st.container(border=True)
       container.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
   with col2:
        # Tarih sütununu datetime türüne çevir
       selection = st.selectbox("Yağış Açısından Günleri Kıyaslayın", ["Az Yağışlı ve Kurak Günler(<1 mm / gün)", "Yağışlı Günler(>1 mm / gün)", "Şiddetli Yağışlı Günler(>10 mm / gün)", "Çok Şiddetli Yağışlı Günler(>20 mm / gün)","Sel Riski Barındıran Günler(>50 mm / gün)"]) 
       if selection == "Az Yağışlı ve Kurak Günler(<1 mm / gün)":
          secenek = yagis['precipitation_sum'] < 1
       elif selection == "Yağışlı Günler(>1 mm / gün)":
           secenek= yagis['precipitation_sum'] > 1
       elif selection == "Şiddetli Yağışlı Günler(>10 mm / gün)":
           secenek= yagis['precipitation_sum'] > 10
       elif selection == "Çok Şiddetli Yağışlı Günler(>20 mm / gün)":
           secenek= yagis['precipitation_sum'] > 20
       elif selection == "Sel Riski Barındıran Günler(>50 mm / gün)":
           secenek= yagis['precipitation_sum'] > 50
       rain_above = yagis[secenek]
       rain_days_by_year = rain_above.groupby('yil').size().reset_index(name='gun')
       fig = px.bar(rain_days_by_year, x='yil', y='gun', title=f'Yıl Bazında {selection} Sayısı')
       z = np.polyfit(rain_days_by_year['yil'], rain_days_by_year['gun'], 1)
       p = np.poly1d(z)

       # Eğilim çizgisini grafiğe ekle
       fig.add_scatter(x=yillik_ortalama['yil'], y=p(yillik_ortalama['yil']), mode='lines',line=dict(color='red'),name='Eğilim Çizgisi') 
       
       fig.update_layout(xaxis_title='Yıl', yaxis_title='Gün')
       st.plotly_chart(fig)
       container2 = st.container(border=True)
       container2.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")

with tab3:

   col1, col2 = st.columns([1,1],gap="medium")
   
   
   with col1:
       tab1, tab2= st.tabs(["Yıllık Ortalama Kar Yağışı", "Aylık Ortalama Kar Yağışı"])
       with tab1:
        # Tarih sütununu datetime türüne çevir
           kar['date'] = pd.to_datetime(kar['date'])
       
            
            # Yıllık ortalama, maksimum ve minimum sıcaklık hesapla
           kar['yil'] = kar['date'].dt.year
           
           yillik_ortalama = kar.groupby('yil')['snowfall_sum'].mean().reset_index()
          
            
            # Plotly figürü oluştur
           fig = go.Figure()
            
            # Yıllık ortalama, maksimum ve minimum sıcaklık izlerini ekle
           fig.add_trace(go.Scatter(x=yillik_ortalama['yil'], y=yillik_ortalama['snowfall_sum'], mode='lines', name='Yıllık Ortalama Kar Yağışı'))
          
            
            # Layout'u güncelle
           fig.update_layout(title='Yıllık Ortalama Kar Yağışı',
                              xaxis_title='Yıl',
                              yaxis_title='Kar Yağışı(cm)')
           z = np.polyfit(yillik_ortalama['yil'], yillik_ortalama['snowfall_sum'], 1)
           p = np.poly1d(z)
    
           # Eğilim çizgisini grafiğe ekle
           fig.add_scatter(x=yillik_ortalama['yil'], y=p(yillik_ortalama['yil']), mode='lines',line=dict(color='red'),name='Eğilim Çizgisi') 
            # Grafiği göster
           st.plotly_chart(fig)
       
       with tab2:
               kar["ay"]=kar["date"].dt.month
               selected_month = st.selectbox("Bir ay seçin", range(1, 13), format_func=lambda x: pd.to_datetime(str(x), format='%m').strftime('%m'))
               filtered_df = kar[kar['ay'] == selected_month]
    

               average_snowfall_by_year = filtered_df.groupby(filtered_df['date'].dt.year)['snowfall_sum'].mean().reset_index()
    

               fig = px.bar(average_snowfall_by_year, x='date', y='snowfall_sum', labels={'date': 'Yıl', 'snowfall_sum': 'Ortalama Kar Yağışı (cm)'})
               fig.update_layout(title=f"{selected_month}.Aya Göre Ortalama Kar Yağışı",
                      xaxis_title='Yıl',
                      yaxis_title='Ortalama Kar Yağışı (cm)')
    

               z = np.polyfit(average_snowfall_by_year['date'], average_snowfall_by_year['snowfall_sum'], 1)
               p = np.poly1d(z)
               fig.add_scatter(x=average_snowfall_by_year['date'], y=p(average_snowfall_by_year['date']), mode='lines', line=dict(color='red'), name='Eğilim Çizgisi')           
               st.plotly_chart(fig)
       container = st.container(border=True)
       container.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")        
    
   with col2:
       tab1, tab2= st.tabs(["Yıllara Göre Kar Yağan Gün Sayısı", "Yıllara Göre Günlük Maksimum Kar Miktarı"])
        # Tarih sütununu datetime türüne çevir
       with tab1:
           kar['kar_yagdi_mi'] = kar['snowfall_sum'] > 0 
          
           kar_yagdi_sayisi = kar.groupby(kar['date'].dt.year)['kar_yagdi_mi'].sum().reset_index()
    
    
           fig = px.bar(kar_yagdi_sayisi, x='date', y='kar_yagdi_mi', labels={'date': 'Yıl', 'kar_yagdi_mi': 'Kar Yağan Gün Sayısı'})
           fig.update_layout(title='Yıllara Göre Kar Yağan Gün Sayısı',
                          xaxis_title='Yıl',
                          yaxis_title='Kar Yağan Gün Sayısı')
           z = np.polyfit(kar_yagdi_sayisi['date'], kar_yagdi_sayisi['kar_yagdi_mi'], 1)
           p = np.poly1d(z)
            
            # Eğilim çizgisini grafiğe ekleme
           fig.add_trace(go.Scatter(x=kar_yagdi_sayisi['date'], y=p(kar_yagdi_sayisi['date']), mode='lines', line=dict(color='red'), name='Eğilim Çizgisi'))
           st.plotly_chart(fig)
       with tab2:
           gunluk_kar = kar.groupby('date')['snowfall_sum'].sum().reset_index()


           gunluk_max_kar = gunluk_kar.groupby(gunluk_kar['date'].dt.year)['snowfall_sum'].max().reset_index()


           fig = px.bar(gunluk_max_kar, x='date', y='snowfall_sum', labels={'date': 'Yıl', 'snowfall_sum': 'Günlük Maksimum Kar (cm)'})
           fig.update_layout(title='Yıllara Göre Günlük Maksimum Kar Miktarı',
                      xaxis_title='Yıl',
                      yaxis_title='Günlük Maksimum Kar (cm)')
           z = np.polyfit(gunluk_max_kar['date'], gunluk_max_kar['snowfall_sum'], 1)
           p = np.poly1d(z)

# Eğilim çizgisini grafiğe ekleme
           fig.add_trace(go.Scatter(x=gunluk_max_kar['date'], y=p(gunluk_max_kar['date']), mode='lines', line=dict(color='red'), name='Eğilim Çizgisi'))
           st.plotly_chart(fig)   

       container3 = st.container(border=True)
       container3.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
with tab4 :
    buharlasma['date'] = pd.to_datetime(buharlasma['date'])
    yillik_ortalama_buharlasma = buharlasma.groupby(buharlasma['date'].dt.year)['et0_fao_evapotranspiration_sum'].mean().reset_index()
    yillik_ortalama_buharlasma.set_index('date', inplace=True)

    min_deger = yillik_ortalama_buharlasma['et0_fao_evapotranspiration_sum'].min()
    max_deger = yillik_ortalama_buharlasma['et0_fao_evapotranspiration_sum'].max()
    
    yillik_ortalama_buharlasma['normalized_et0'] = ((yillik_ortalama_buharlasma['et0_fao_evapotranspiration_sum'] - min_deger) / (max_deger - min_deger)) * 100
    
    min_deger = yıllık_ortalama_yagis['precipitation_sum'].min()
    max_deger = yıllık_ortalama_yagis['precipitation_sum'].max()
    
    yıllık_ortalama_yagis['normalized_precipitation'] = ((yıllık_ortalama_yagis['precipitation_sum'] - min_deger) / (max_deger - min_deger)) * 100
    fark= pd.DataFrame()
    # Normalleştirilmiş veriyi gösterelim
    fark["debi"] =yıllık_ortalama_yagis['normalized_precipitation'].astype(float) - yillik_ortalama_buharlasma['normalized_et0'].astype(float)
    fark["debi"]  = fark["debi"].rolling(window=10, min_periods=3).mean()
# Plotly grafiğini oluşturalım
    fig = go.Figure()

# Farkın çizgi grafiği
    fig.add_trace(go.Scatter(x=fark.index, y=fark["debi"], mode='lines', name='Yağış - Buharlaşma Farkı'))

# Grafik düzenlemeleri
    fig.update_layout(
        title='Yağış ve Buharlaşma Dengesinin Olası Debi Potansiyeline Etkisi',
        xaxis_title='Yıl',
        yaxis_title='Etki Puanı',
        legend_title='Değişkenler',
        # Arka plan rengi yeşil (RGB değeri)
        yaxis=dict(
            zeroline=True,  # Sıfır çizgisini kaldır
            tickmode='linear',  # Tick modunu lineer olarak belirle
            tick0=0,  # Başlangıç noktası sıfır
            dtick=10,  # Ticklerin aralığı
            ticklen=10,  # Tick uzunluğu
            tickwidth=2,  # Tick kalınlığı
            tickcolor='rgba(0,0,0,0.3)',  # Tick rengi
            range=[-50, 50],  # Y ekseninin aralığı
            showline=True,  # Eksen çizgisini göster
            showgrid=False,  # Izgara çizgisini kaldır
            linecolor='black',  # Eksen çizgisi rengi
            linewidth=2,  # Eksen çizgisi kalınlığı
            mirror=True,  # Eksen çizgisini eksenin diğer tarafına yansıt
            showticklabels=True,  # Tick etiketlerini göster
            tickfont=dict(size=12),  # Tick etiket fontu
            overlaying='y',
            side='right',  # Eksenin pozisyonu
            showspikes=True,  # Spike'ları göster
            spikesnap='cursor',  # Spike'ların imleç konumunda olmasını sağla
            spikedash='solid',  # Spike çizgi stili
            spikecolor='black',  # Spike rengi
            spikethickness=1  # Spike kalınlığı
        ),
        shapes=[
            dict(
                type='rect',
                xref='paper',
                yref='y',
                x0=0,
                y0=50,
                x1=1,
                y1=0,
                fillcolor='green',
                opacity=0.2,
                layer='below',
                line_width=0,
                name='Pozitif Etki'
            ),
            dict(
                type='rect',
                xref='paper',
                yref='y',
                x0=0,
                y0=-50,
                x1=1,
                y1=0,
                fillcolor='red',
                opacity=0.2,
                layer='below',
                line_width=0,
                name='Negatif Etki'
            )
        ],
        legend=dict(
            x=1.05,
            y=1,
            traceorder='normal',
            font=dict(
                family='Arial',
                size=12,
                color='black'
            ),
            bgcolor='LightSteelBlue',
            bordercolor='black',
            borderwidth=1
        )
    )
    
    fig.update_traces(
        line=dict(
            color='black',
            width=2
        )
    )

 # Grafiği gösterelim
    st.plotly_chart(fig)   

with tab5 :
    soil_m['date'] = pd.to_datetime(soil_m['date'])
    yillik_ortalama_soil_m = soil_m.groupby(soil_m['date'].dt.year)['soil_moisture_0_to_10cm_mean'].mean().reset_index()
    yillik_ortalama_soil_m .set_index('date', inplace=True)

    min_deger = yillik_ortalama_soil_m['soil_moisture_0_to_10cm_mean'].min()
    max_deger = yillik_ortalama_soil_m['soil_moisture_0_to_10cm_mean'].max()
    
    yillik_ortalama_soil_m['normalized_soil'] = ((yillik_ortalama_soil_m['soil_moisture_0_to_10cm_mean'] - min_deger) / (max_deger - min_deger)) * 100
    min_deger = yıllık_ortalamalar['temperature_2m_mean'].min()
    max_deger = yıllık_ortalamalar['temperature_2m_mean'].max()
    
    yıllık_ortalamalar['normalized_t2m'] = ((yıllık_ortalamalar['temperature_2m_mean'] - min_deger) / (max_deger - min_deger)) * 100
    kuraklık = pd.DataFrame()
    kuraklık["kuraklık"]= yillik_ortalama_buharlasma['normalized_et0']-yillik_ortalama_soil_m['normalized_soil'] -  yıllık_ortalama_yagis['normalized_precipitation'] + yıllık_ortalamalar['normalized_t2m'] 
    
    kuraklık['kuraklık'] = kuraklık['kuraklık'].rolling(window=30, min_periods=3).mean()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=kuraklık.index, y=kuraklık['kuraklık'], mode='lines', name='Kuraklık İndeksi'))
    fig.update_layout(title='Yıllık Kuraklık İndeksi', xaxis_title='Yıl', yaxis_title='Kuraklık İndeksi')
    st.plotly_chart(fig)   
