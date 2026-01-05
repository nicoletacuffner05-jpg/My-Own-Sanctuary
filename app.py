import streamlit as st
import requests
import random
from datetime import date, datetime

# --- 1. CORE ENGINE: Liturgy & Theme ---
@st.cache_data(ttl=3600)
def fetch_liturgy():
    try:
        r = requests.get("http://calapi.inadiutorium.cz/api/v1/calendars/general-en/today", timeout=5).json()
        c = r['celebrations'][0]
        return c['title'], c['colour'], c['rank']
    except:
        return "Ordinary Time", "green", "ferial"

saint, color_name, rank = fetch_liturgy()
color_map = {"green": "#1E5631", "purple": "#4B0082", "red": "#8B0000", "white": "#B8860B", "violet": "#4B0082"}
app_color = color_map.get(color_name.lower(), "#1E5631")

st.set_page_config(page_title="Catholic Sanctuary Master", page_icon="🇻🇦", layout="wide")

# Styling
st.markdown(f"""
    <style>
    .stApp {{ background-color: #FDFCF0; }}
    [data-testid="stSidebar"] {{ background-color: {app_color} !important; }}
    .stSidebar * {{ color: white !important; }}
    .stButton>button {{ background-color: {app_color}; color: white; border-radius: 12px; font-weight: bold; }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA: Quotes & Prayers ---
quotes = [
    "“Pray, hope, and don’t worry.” – St. Padre Pio",
    "“The world offers you comfort. But you were not made for comfort. You were made for greatness.” – Pope Benedict XVI",
    "“Spread love everywhere you go. Let no one ever come to you without leaving happier.” – St. Mother Teresa",
    "“To fall in love with God is the greatest romance; to seek him the greatest adventure.” – St. Augustine",
    "“Be who God meant you to be and you will set the world on fire.” – St. Catherine of Siena"
]

# --- 3. STATE MANAGEMENT ---
if 'virtue_points' not in st.session_state:
    st.session_state.virtue_points = 0

# --- 4. NAVIGATION ---
page = st.sidebar.radio("Sanctuary Navigation", 
    ["🏠 Home", "📖 Daily Lectures & Bible Search", "📿 Complete Prayer Library", "✝️ Stations of the Cross", "🛡️ Virtue Tracker", "🕊️ Confessional", "🎵 Sacred Audio"])

# --- 5. PAGES ---

if page == "🏠 Home":
    st.title("Daily Sanctuary")
    st.success(f"**Feast:** {saint}")
    st.metric("Liturgical Color", color_name.capitalize())
    st.markdown("---")
    st.subheader("Saint's Quote of the Day")
    st.info(random.choice(quotes))

elif page == "📖 Daily Lectures & Bible Search":
    tab1, tab2 = st.tabs(["Today's Gospel", "Search the Bible"])
    with tab1:
        try:
            b = requests.get("https://bible-api.com/verse_of_the_day?translation=dra").json()
            st.subheader(f"{b['verse']['name']}")
            st.write(f"### {b['verse']['text']}")
        except: st.error("Bible server offline.")
    with tab2:
        query = st.text_input("Look up a verse (e.g., John 3:16)")
        if query:
            s = requests.get(f"https://bible-api.com/{query}?translation=dra").json()
            if 'text' in s: st.write(f"### {s['reference']}\n{s['text']}")

elif page == "📿 Complete Prayer Library":
    st.title("The Great Library of Prayers")
    cat = st.selectbox("Category:", ["All Psalms", "Daily Prayers", "Marian Devotions", "Latin Hymns"])
    
    if cat == "All Psalms":
        p_name = st.selectbox("Select Psalm:", ["Psalm 23", "Psalm 51", "Psalm 91", "Psalm 130", "Psalm 150"])
        texts = {
            "Psalm 23": "The Lord is my shepherd; I shall not want...",
            "Psalm 51": "Have mercy on me, O God, according to thy great mercy...",
            "Psalm 91": "He that dwelleth in the aid of the most High shall abide under the shadow of the God of heaven...",
            "Psalm 130": "Out of the depths I have cried to thee, O Lord: Lord, hear my voice...",
            "Psalm 150": "Praise ye the Lord in his holy places: praise ye him in the firmament of his power..."
        }
        st.write(texts.get(p_name))
    
    elif cat == "Marian Devotions":
        st.write("**The Angelus:** The Angel of the Lord declared unto Mary. R. And she conceived of the Holy Spirit...")
        st.write("**Salve Regina:** Hail, holy Queen, Mother of mercy, our life, our sweetness, and our hope...")

elif page == "✝️ Stations of the Cross":
    st.title("✝️ Way of the Cross")
    s_idx = st.select_slider("Station", options=range(1, 15))
    stations = {
        1: ("Jesus is Condemned", "Jesus is unjustly condemned by Pilate to die on the Cross."),
        2: ("Jesus Carries His Cross", "Jesus accepts the heavy weight of the Cross for our sins."),
        3: ("Jesus Falls the First Time", "Our Lord falls under the weight of the wood."),
        4: ("Jesus Meets His Mother", "A sorrowful meeting between Son and Mother."),
        5: ("Simon Helps Jesus", "Simon the Cyrenian is forced to help carry the Cross."),
        6: ("Veronica Wipes His Face", "Veronica offers her cloth to wipe the sweat and blood."),
        7: ("Jesus Falls a Second Time", "The pain of the wounds is renewed in this second fall."),
        8: ("Jesus Meets the Women", "Jesus tells the women to weep not for Him, but for themselves."),
        9: ("Jesus Falls a Third Time", "Extreme weakness leads to a final fall before Calvary."),
        10: ("Jesus is Stripped", "His garments are torn away, adhering to His wounds."),
        11: ("Jesus is Nailed", "Jesus offers His life as the nails pierce His hands and feet."),
        12: ("Jesus Dies", "After three hours of agony, our Savior expires."),
        13: ("Jesus is Taken Down", "The body of Jesus is placed in the arms of His Mother."),
        14: ("Jesus is Buried", "The disciples lay the body of Jesus in the tomb.")
    }
    st.subheader(f"Station {s_idx}: {stations[s_idx][0]}")
    st.write(f"*{stations[s_idx][1]}*")
    st.markdown("**V.** We adore Thee, O Christ, and we praise Thee.  \n**R.** Because by Thy holy cross, Thou hast redeemed the world.")

elif page == "🛡️ Virtue Tracker":
    st.title("🛡️ Virtue Tracker")
    v1 = st.checkbox("Humility")
    v2 = st.checkbox("Patience")
    v3 = st.checkbox("Charity")
    if st.button("Log Daily Virtues"):
        st.session_state.virtue_points += (v1 + v2 + v3)
        st.balloons()
    st.progress(min(st.session_state.virtue_points / 100, 1.0))
    st.write(f"Current Holiness Score: {st.session_state.virtue_points}")

elif page == "🎵 Sacred Audio":
    st.title("🎵 Sacred Audio")
    st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
  
