
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
from streamlit_option_menu import option_menu

from database import (
    add_patient,
    get_patients,
    update_patient,
    delete_patient,
    get_patient_by_id
)

from prediction import generate_prediction

st.set_page_config(
    page_title="AI Health Prediction System",
    page_icon="🏥",
    layout="wide"
)
st.markdown("""
<style>

/* Main Background */
.stApp{
    background: #F4F7FC;
}

/* Headers */
h1,h2,h3,h4,h5,h6{
    color:#0F172A !important;
}

/* Normal Text */
p,label,span{
    color:#1E293B !important;
}

/* Dashboard Cards */
.card{
    background:linear-gradient(135deg,#2563EB,#7C3AED);
    padding:20px;
    border-radius:18px;
    box-shadow:0px 6px 18px rgba(0,0,0,0.15);
    text-align:center;
}

.metric{
    font-size:34px;
    font-weight:bold;
    color:white;
}

.title{
    font-size:15px;
    color:#E2E8F0;
    font-weight:600;
}

/* Input Labels */
.stTextInput label,
.stNumberInput label,
.stDateInput label,
.stSelectbox label,
.stTextArea label{
    color:#0F172A !important;
    font-weight:600 !important;
}

/* Input Boxes */
.stTextInput input,
.stNumberInput input{
    background:white !important;
    color:black !important;
}

/* Tabs */
button[data-baseweb="tab"]{
    color:#0F172A !important;
    font-weight:600 !important;
}

button[data-baseweb="tab"][aria-selected="true"]{
    background:#2563EB !important;
    color:white !important;
    border-radius:10px;
}

/* Dataframe */
[data-testid="stDataFrame"]{
    background:white;
    border-radius:15px;
    padding:10px;
}

/* Analytics Charts Container */
.element-container{
    color:black !important;
}

/* Buttons */
.stButton button{
    background:#2563EB;
    color:white;
    border:none;
    border-radius:10px;
    height:48px;
    font-weight:600;
}

.stButton button:hover{
    background:#1D4ED8;
}

/* Success */
.stSuccess{
    background:#DCFCE7 !important;
    color:#166534 !important;
}

/* Error */
.stError{
    background:#FEE2E2 !important;
    color:#991B1B !important;
}

/* Warning */
.stWarning{
    background:#FEF3C7 !important;
    color:#92400E !important;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background:#0F172A;
}

section[data-testid="stSidebar"] *{
    color:white !important;
}

</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("🏥 Health AI")
    selected = option_menu(
        menu_title=None,
        options=["Dashboard","Patient Management","Analytics"],
        icons=["house","person","bar-chart"]
    )

st.title("🏥 AI Health Prediction System")
st.caption("Patient Management & Disease Risk Assessment Platform")

try:
    patient_df = get_patients()
except:
    patient_df = pd.DataFrame()

if selected == "Dashboard":

    total = len(patient_df)

    high = len(patient_df[patient_df["remarks"].astype(str).str.contains("High", na=False)]) if not patient_df.empty else 0
    healthy = len(patient_df[patient_df["remarks"]=="Healthy"]) if not patient_df.empty else 0
    other = max(total-high-healthy,0)

    c1,c2,c3,c4 = st.columns(4)

    for col,title,val in [
        (c1,"Total Patients",total),
        (c2,"High Risk",high),
        (c3,"Healthy",healthy),
        (c4,"Others",other)
    ]:
        with col:
            st.markdown(f"""
            <div class='card'>
            <div class='title'>{title}</div>
            <div class='metric'>{val}</div>
            </div>
            """, unsafe_allow_html=True)

    if not patient_df.empty:
        col1,col2 = st.columns(2)

        with col1:
            risk = patient_df["remarks"].value_counts().reset_index()
            risk.columns=["Risk","Count"]
            fig = px.pie(risk,names="Risk",values="Count",hole=.5,title="Risk Distribution")
            st.plotly_chart(fig,use_container_width=True)

        with col2:
            fig2 = px.histogram(
                patient_df,
                x="cholesterol",
                title="Cholesterol Analysis"
            )
            st.plotly_chart(fig2,use_container_width=True)

elif selected == "Patient Management":

    tab1,tab2,tab3,tab4 = st.tabs(
        ["➕ Add","📋 View","✏️ Update","🗑️ Delete"]
    )

    with tab1:

        col1,col2 = st.columns(2)

        with col1:
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            dob = st.date_input("Date of Birth")

        with col2:
            glucose = st.number_input("Glucose",0.0)
            hb = st.number_input("Haemoglobin",0.0)
            chol = st.number_input("Cholesterol",0.0)

        if st.button("🧠 Predict Risk"):

            remarks = generate_prediction(glucose,hb,chol)

            if "Healthy" in remarks:
                st.success(remarks)
            elif "High" in remarks:
                st.error(remarks)
            else:
                st.warning(remarks)

        if st.button("💾 Save Patient"):

            remarks = generate_prediction(glucose,hb,chol)

            add_patient((
                name,dob,email,
                glucose,hb,chol,remarks
            ))

            st.success("Patient Saved Successfully")

    with tab2:

        if not patient_df.empty:

            search = st.text_input("Search Patient")

            df = patient_df

            if search:
                df = df[
                    df["full_name"].astype(str)
                    .str.contains(search,case=False,na=False)
                ]

            st.dataframe(df,use_container_width=True)

            csv = df.to_csv(index=False)

            st.download_button(
                "📥 Download CSV",
                csv,
                "patients.csv",
                "text/csv"
            )

    with tab3:

        pid = st.number_input(
            "Patient ID",
            min_value=1,
            step=1
        )

        name = st.text_input("Name",key="u1")
        email = st.text_input("Email",key="u2")
        glucose = st.number_input("Glucose",0.0,key="u3")
        hb = st.number_input("Haemoglobin",0.0,key="u4")
        chol = st.number_input("Cholesterol",0.0,key="u5")

        if st.button("Update Patient"):

            remarks = generate_prediction(
                glucose,hb,chol
            )

            update_patient(
                pid,
                (
                    name,
                    date.today(),
                    email,
                    glucose,
                    hb,
                    chol,
                    remarks
                )
            )

            st.success("Patient Updated")

    with tab4:

        pid = st.number_input(
            "Patient ID to Delete",
            min_value=1,
            step=1,
            key="del"
        )

        if st.button("Delete Patient"):
            delete_patient(pid)
            st.success("Patient Deleted")

elif selected == "Analytics":

    st.subheader("Analytics Dashboard")

    if not patient_df.empty:

        col1,col2 = st.columns(2)

        with col1:
            fig = px.pie(
                patient_df,
                names="remarks",
                title="Health Status Distribution"
            )
            st.plotly_chart(fig,use_container_width=True)

        with col2:
            fig = px.scatter(
                patient_df,
                x="glucose",
                y="cholesterol",
                color="remarks",
                title="Glucose vs Cholesterol"
            )
            st.plotly_chart(fig,use_container_width=True)

        st.dataframe(patient_df,use_container_width=True)
    else:
        st.info("No patient records found.")
