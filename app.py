"""D.Sh. — BMI Calculator (Streamlit Cloud + MongoDB)."""

from datetime import datetime, timezone

import streamlit as st
from pymongo import MongoClient
from pymongo.errors import PyMongoError

st.set_page_config(page_title="BMI Calculator", page_icon="⚖️")


# ---------- MongoDB ----------
@st.cache_resource
def get_collection():
    """Connect once per session; reads the URI from Streamlit secrets."""
    client = MongoClient(st.secrets["mongo"]["uri"], serverSelectionTimeoutMS=5000)
    return client["bmi_app"]["records"]


def bmi_category(bmi: float) -> str:
    if bmi < 18.5:
        return "Underweight"
    if bmi < 25:
        return "Normal weight"
    if bmi < 30:
        return "Overweight"
    return "Obese"


# ---------- UI ----------
st.title("⚖️ BMI Calculator")
st.caption("Enter your data — the result is shown below and saved to MongoDB.")

with st.form("bmi_form"):
    name = st.text_input("Name")
    height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=170.0, step=0.5)
    weight = st.number_input("Weight (kg)", min_value=10.0, max_value=300.0, value=70.0, step=0.5)
    submitted = st.form_submit_button("Calculate BMI")

if submitted:
    if not name.strip():
        st.error("Please enter your name.")
    else:
        bmi = round(weight / (height / 100) ** 2, 2)
        category = bmi_category(bmi)

        # ----- Outputs -----
        st.subheader("Results")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Name", name.strip())
        col2.metric("Height", f"{height:g} cm")
        col3.metric("Weight", f"{weight:g} kg")
        col4.metric("BMI", bmi)
        st.info(f"Category: **{category}**")

        # ----- Register in MongoDB -----
        record = {
            "name": name.strip(),
            "height_cm": height,
            "weight_kg": weight,
            "bmi": bmi,
            "category": category,
            "created_at": datetime.now(timezone.utc),
        }
        try:
            get_collection().insert_one(record)
            st.success("Record saved to MongoDB ✅")
        except (PyMongoError, KeyError) as e:
            st.warning(f"Could not save to MongoDB: {e}")

# ---------- History ----------
st.divider()
if st.checkbox("Show saved records"):
    try:
        rows = list(
            get_collection()
            .find({}, {"_id": 0})
            .sort("created_at", -1)
            .limit(20)
        )
        if rows:
            st.dataframe(rows, use_container_width=True)
        else:
            st.info("No records yet.")
    except (PyMongoError, KeyError) as e:
        st.warning(f"Could not load records: {e}")
