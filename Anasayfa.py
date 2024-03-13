import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import streamlit_js_eval
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

def main():
    # Setting up the layout
    col1, mid, col2 = st.columns([1, 1,1])

    with col1:
        st.image('https://urclimate.com/wp-content/uploads/2023/12/LOGO_UrClimate_4-1.png', width=180)
    
    with col2:
        st.title('UrClimate İklim Risk Demo Dashboard', anchor=False)
    
    # Create a wide map object
    folium_map = folium.Map(location=[39, 35.5], zoom_start=6)

    # Define locations, labels, and page URLs
    locations = [
        (41.269758, 28.74381, 'Havalimanı',  '/HAVALIMANI', 'airport.png'),
        (39.433, 29.9878, 'Fabrika','/FABRIKA', 'factory.png'),
        (37.887, 36.962, 'HES',  '/HES','hydro-power.png'),
        # Add more locations with respective icons
    ]

    # Add markers to the map
    for lat, lon, label, page_url, icon in locations:
        icon_path = f"icons/{icon}"  # Assuming icons are stored in a folder named 'icons'
        popup_content =  f"""
    <div style="text-align: center;">
        <h4 style="font-weight: bold;">{label}</h4>
         <a href="#" onclick="window.open('{page_url}'); return false;" style="text-decoration: none;">
            <button style="background-color: #abdbe3;
                            border: none;
                            color: black;
                            padding: 5px 12px;
                            text-align: center;
                            text-decoration: none;
                            display: inline-block;
                            font-size: 10px;
                            margin: 4px 2px;
                            transition-duration: 0.4s;
                            cursor: pointer;
                            border-radius: 8px;
                            box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2), 0 6px 20px 0 rgba(0,0,0,0.19);">
                Analize Git
            </button>
        </a>
    </div>
"""
        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_content, max_width=300),
            tooltip=f"{label}",
            icon=folium.CustomIcon(icon_path, icon_size=(30, 30))  # Adjust icon size as needed
        ).add_to(folium_map)

    # Stream the map
    st_folium(folium_map, use_container_width=True)

if __name__ == "__main__":
    main()
