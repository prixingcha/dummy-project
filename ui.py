import streamlit as st

# Define the JSON data
data = [
    {
        "thumbnail": "https://img.youtube.com/vi/liR6t8n11i8/maxresdefault.jpg",
        "📚": "RJ PRAVEEN >>> Boss Pe Kiya Bada Prank 😂 | RJ Praveen | Prank Call | Online Shopping Scam 😅 | Comedy Video",
        "🔗": "https://www.youtube.com/watch?v=liR6t8n11i8",
        "status": "👍 1,422  👎 0👁  21,108",
        "others": "🕑  00:03:23  📢737,000🌍IN"
    },
    {
        "thumbnail": "https://img.youtube.com/vi/Wtt9tuO8UPY/maxresdefault.jpg",
        "📚": "Mervin Praison >>> Anthropic Claude API: Supercharge Your AI App with Large Context",
        "🔗": "https://www.youtube.com/watch?v=Wtt9tuO8UPY",
        "status": "👍 23  👎 0👁  209",
        "others": "🕑  00:05:50  📢15,800🌍GB"
    },
    {
        "thumbnail": "https://img.youtube.com/vi/m0AACKdFnO8/maxresdefault.jpg",
        "📚": "Rainbow Balloonicorn >>> Satisfying Stubborn Balloon Took 3 Tries to Pop It #balloon_popping  #funny #buttons_popping",
        "🔗": "https://www.youtube.com/watch?v=m0AACKdFnO8",
        "status": "👍 18  👎 0👁  454",
        "others": "🕑  00:00:56  📢2,390🌍US"
    }
]

# Create Streamlit UI
st.title("YouTube Extracted Data")
for video in data:
    st.markdown(f"[![Thumbnail]({video['thumbnail']})]({video['🔗']})")
    st.write(video["📚"])
    st.write(video["status"])
    st.write(video["others"])
    st.write("---")
    
    
st.image(video["thumbnail"], width=100, output_format="JPEG")
