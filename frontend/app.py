import streamlit as st
import requests

st.set_page_config(
    page_title="University Student Support Assistant",
    page_icon="./udsm_logo.jpeg",
    layout="centered"
)

#UDSM THEME
# Secondary blue      : #0864AF
# Accent green        : #2e7d32 (success / confirmations, ARIS-style)
# Light green tint    : #eaf6ec
# Background          : white / very light grey


st.markdown("""
<style>

/* Main page */
.stApp{
    background-color:#f5f7fa;
}

/* Top banner */
.udsm-banner{
    background:linear-gradient(90deg, #0864AF 0%, #00509e 100%);
    padding:22px 20px;
    border-radius:10px;
    margin-bottom:18px;
    box-shadow:0 2px 8px rgba(0,51,102,0.25);
}
.udsm-banner h1{
    color:#ffffff !important;
    text-align:center;
    font-weight:800;
    margin:0;
    letter-spacing:0.3px;
}
.udsm-banner p{
    text-align:center;
    color:#d7e6f5;
    margin:4px 0 0 0;
    font-size:15px;
}
 
/* Sub headings */
h2,h3{
    color:#003366;
}
 
/* Card-style container for the assistant intro */
.udsm-card{
    background:#ffffff;
    border:1px solid #dbe4ee;
    border-left:5px solid #2e7d32;
    border-radius:10px;
    padding:18px 20px;
    margin-bottom:16px;
    box-shadow:0 1px 4px rgba(0,0,0,0.05);
}
 
/* Answer box */
.udsm-answer{
    background:#eaf6ec;
    border:1px solid #bfe3c4;
    border-left:5px solid #2e7d32;
    border-radius:10px;
    padding:16px 18px;
    margin-top:10px;
    color:#0f3d1a;
}

/* Main title */
h1{
    color:#003366;
    text-align:center;
    font-weight:bold;
}


/* Buttons */
.stButton>button{
    background-color:#003366;
    color:white;
    border-radius:8px;
    border:none;
    padding:10px 18px;
    font-weight:bold;
    transition:0.2s ease-in-out;
}

.stButton>button:hover{
    background-color:#2e7d32;
    color:white;
}

/* Text inputs */
.stTextInput input{
    border-radius:8px;
    border:1px solid #003366;
}
.stTextInput input:focus{
    border:1px solid #2e7d32;
    box-shadow:0 0 0 1px #2e7d32;
}
 
/* Radio buttons */
div[role="radiogroup"]{
    padding:10px;
    border-radius:8px;
    background:#ffffff;
    border:1px solid #dbe4ee;
}

/* Radio buttons */
div[role="radiogroup"]{
    padding:10px;
    border-radius:8px;
    background:#ffffff;
}

/* Success / warning / error boxes */
.stSuccess{
    border-radius:8px;
    background-color:#eaf6ec !important;
}
.stWarning{
    border-radius:8px;
}
.stError{
    border-radius:8px;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background:#003366;
    color:white;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="udsm-banner">
    <h1>🎓 University Student Support Assistant</h1>
    <p>University of Dar es Salaam &nbsp;|&nbsp; AI-powered Student Support</p>
</div>
""", unsafe_allow_html=True)
 
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "last_question" not in st.session_state:
    st.session_state.last_question = ""
if "last_answer" not in st.session_state:
    st.session_state.last_answer = ""
if "feedback_given" not in st.session_state:
    st.session_state.feedback_given = False
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    choice = st.radio("Choose action", ["Login", "Register"])

    if choice == "Register":
        st.subheader("Create your account")

        username = st.text_input("Choose username")
        password = st.text_input("Choose password", type="password")

        if st.button("Register"):
            response = requests.post(
                "http://localhost:8000/register",
                json={
                    "username": username,
                    "password": password
                }
            )

            if response.status_code == 200:
                st.success("Account successfully created! You can now login.")
            else:
                st.error(
                    response.json()["detail"])
    elif choice == "Login":
        st.subheader("Login to access system")

        username = st.text_input("Enter username")
        password = st.text_input("Enter password", type="password")

        if st.button("Login"):
            if not username.strip() or not password.strip():
                st.error("Please enter both username and password to log in")
            else:
                response = requests.post(
                    "http://localhost:8000/login",
                    json={
                        "username": username,
                        "password": password
                    }
                )

                if response.status_code == 200:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success("You are successfully logged in!")
                    st.rerun()
                else:
                    st.error(response.json()["detail"])
else:
    st.markdown(f"""
    <div class="udsm-card">
    Hi <b>{st.session_state.username}</b>! I'm your virtual assistant. How can I help you?<br>
    Ask me about student support services such as:
    <ul>
        <li>Course registration</li>
        <li>Accommodation &amp; housing application</li>
        <li>Fees payments</li>
        <li>Exams information</li>
        <li>Academic calendar</li>
        <li>ICT support services</li>
        <li>Library services</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    
    
    #st.title("University Student Support Assistant")
    
    #st.write(""" Hi! I'm your virtual assistant. How can I help you? 
         #Ask me about student support services such as:\n 
         #- Course registration\n 
         #- Accomodation & housing application\n 
         #- Fees payments\n
         #- Exams information\n
         #- Academic calendar\n
         #- ICT support services\n
         #- Library services 
         #""")

    question = st.text_input("Ask me: ")

    if st.button("Submit"):
        if not question.strip():
            st.warning("Please enter a question before submitting")
        else:
            with st.spinner("Getting answer..."):
                response = requests.post("http://localhost:8000/ask", json={"question": question})
                answer = response.json().get("answer")

                st.session_state.last_question = question
                st.session_state.last_answer = answer
                st.session_state.feedback_given = False
                
    if st.session_state.last_answer:
        st.markdown(f"""
        <div class="udsm-answer">
        <b>Answer:</b><br>{st.session_state.last_answer}
        </div>
        """, unsafe_allow_html=True)
        
        rating = st.radio("Was this response helpful? Rate:", ["Good", "Average", "Poor"], horizontal=True)
        
        if st.session_state.feedback_given:
            st.success("Thank you for the feedback!")
        else:
            if st.button("Give feedback"):
                requests.post(
                    "http://localhost:8000/feedback",
                    json={
                        "username": st.session_state.username,
                        "question": st.session_state.last_question,
                        "rating": rating
                    }
                )
                st.session_state.feedback_given = True
                st.rerun()

            
