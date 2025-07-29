import streamlit as st
import random

# Page config
st.set_page_config(page_title="Suraksha Sathi – Life in 5 Cards", layout="centered")

# Theme colors
PRIMARY = "#2d448d"
SUCCESS = "#a6ce39"
INFO = "#459fda"

# Initialize session state
if "started" not in st.session_state:
    st.session_state.started = False
    st.session_state.balance = 100000  # Starting balance
    st.session_state.card_index = 0
    st.session_state.results = []

# Define 5 real-life Indian middle-class scenarios
scenarios = [
    {
        "title": "🩺 Health Scare: Emergency Hospitalization",
        "cost": 60000,
        "insurance": {
            "Mediclaim (₹5,000 premium)": {"premium": 5000, "out_of_pocket": 10000},
            "Super Top-Up (₹8,000 premium)": {"premium": 8000, "out_of_pocket": 2000},
            "No Insurance": {"premium": 0, "out_of_pocket": 60000},
        }
    },
    {
        "title": "🚗 Car Accident: Bumper Repair & Liability",
        "cost": 40000,
        "insurance": {
            "Third-Party Only (₹2,000)": {"premium": 2000, "out_of_pocket": 30000},
            "Comprehensive (₹6,000)": {"premium": 6000, "out_of_pocket": 5000},
            "No Insurance": {"premium": 0, "out_of_pocket": 40000},
        }
    },
    {
        "title": "🏠 Fire at Home: Kitchen Damage",
        "cost": 70000,
        "insurance": {
            "Fire-Only Cover (₹3,000)": {"premium": 3000, "out_of_pocket": 20000},
            "Home Insurance (₹7,000)": {"premium": 7000, "out_of_pocket": 5000},
            "No Insurance": {"premium": 0, "out_of_pocket": 70000},
        }
    },
    {
        "title": "💼 Job Loss: Income Halt for 3 Months",
        "cost": 90000,
        "insurance": {
            "Income Protection (₹4,000)": {"premium": 4000, "out_of_pocket": 30000},
            "EMI Waiver Policy (₹5,000)": {"premium": 5000, "out_of_pocket": 20000},
            "No Insurance": {"premium": 0, "out_of_pocket": 90000},
        }
    },
    {
        "title": "⚰️ Sudden Death in Family: Funeral & Legal Costs",
        "cost": 100000,
        "insurance": {
            "Term Life Cover (₹6,000)": {"premium": 6000, "out_of_pocket": 10000},
            "Term + Accidental Rider (₹8,000)": {"premium": 8000, "out_of_pocket": 5000},
            "No Insurance": {"premium": 0, "out_of_pocket": 100000},
        }
    }
]

# Start Game
def start_game():
    st.session_state.started = True
    st.session_state.balance = 100000
    st.session_state.card_index = 0
    st.session_state.results = []

# Game UI
def play_game():
    index = st.session_state.card_index
    if index < len(scenarios):
        scenario = scenarios[index]
        st.markdown(f"### {scenario['title']}")
        st.write(f"**Estimated Loss:** ₹{scenario['cost']}")

        choice = st.radio("Choose your insurance option:",
                          options=list(scenario["insurance"].keys()),
                          key=f"choice_{index}")

        if st.button("Confirm Choice", key=f"confirm_{index}"):
            selected = scenario["insurance"][choice]
            total_loss = selected["premium"] + selected["out_of_pocket"]
            st.session_state.balance -= total_loss
            st.session_state.results.append({
                "title": scenario["title"],
                "choice": choice,
                "premium": selected["premium"],
                "out_of_pocket": selected["out_of_pocket"],
                "remaining": st.session_state.balance
            })
            st.session_state.card_index += 1
            st.experimental_rerun()
    else:
        show_summary()

# Final Summary
def show_summary():
    st.markdown("## 🧾 Game Summary")
    for res in st.session_state.results:
        with st.container():
            st.markdown(f"**{res['title']}**")
            st.markdown(f"- Insurance Chosen: `{res['choice']}`")
            st.markdown(f"- Premium Paid: ₹{res['premium']}")
            st.markdown(f"- Out-of-pocket Cost: ₹{res['out_of_pocket']}")
            st.markdown(f"- Remaining Balance: ₹{res['remaining']}")
            st.markdown("---")

    final = st.session_state.balance
    st.subheader(f"🏁 Final Balance: ₹{final}")
    if final > 80000:
        grade = "A+ – Excellent risk manager! 🎉"
    elif final > 60000:
        grade = "B – Pretty good decisions!"
    elif final > 30000:
        grade = "C – Took some risk, but survived!"
    else:
        grade = "D – Oops! Insurance matters."

    st.markdown(f"### 🎓 Grade: **{grade}**")

    if st.button("🔁 Play Again"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.session_state.refresh = True
st.session_state.run_id = random.randint(0, 999999)  # force re-render


# Title and Start
st.markdown(f"<h1 style='color:{PRIMARY};'>Suraksha Sathi – Your Life in 5 Cards</h1>", unsafe_allow_html=True)

if not st.session_state.started:
    st.markdown("💡 Make insurance choices for 5 real-life events. Your goal: retain as much of your ₹1,00,000 as possible.")
    if st.button("Start Game"):
        start_game()
if "refresh" not in st.session_state:
    st.session_state.refresh = False
else:
    play_game()
    if st.session_state.refresh:
    st.session_state.refresh = False
    st.experimental_rerun()

