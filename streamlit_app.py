import streamlit as st
from views import FeedView, AddPostView
from services import get_feed, add_post
AddPostView(add_post)
st.write("___")
FeedView(get_feed)