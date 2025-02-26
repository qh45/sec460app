import streamlit as st
import random

# List of random messages
messages = [
    "Good news will come to you by mail.",
    "A fresh start will put you on your way.",
    "A friend asks only for your time not your money.",
    "A golden opportunity is heading your way.",
    "A smile is your personal welcome mat.",
    "All your hard work will soon pay off.",
    "An important person will offer you support.",
    "Believe in yourself and others will too.",
    "Change is happening in your life, so go with the flow!",
    "Distance yourself from the negativity of others.",
    "Embrace change and make it work in your favor.",
    "Expect great things and great things will come to you.",
    "Great things are coming your way.",
    "Happiness will soon knock on your door.",
    "Keep your goals in sight and go for it.",
    "Look forward to a new adventure.",
    "Seize every opportunity that comes your way.",
    "Success is on your horizon.",
    "You will make a new friend soon.",
    "Your future is bright and full of possibilities."
]

def main():
    st.title("Fortune Teller")
    
    if st.button("Click to see your fortune"):
        message = random.choice(messages)
        st.write(message)
        
if __name__ == "__main__":
    main()
