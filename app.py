import streamlit as st
import random

# Set Streamlit page configuration
st.set_page_config(page_title="Life Happens - Insurance Game", layout="centered")

# Initialize game state
if "balance" not in st.session_state:
    st.session_state.balance = 50000
    st.session_state.coverage = {"Car": None, "House": None, "Life": None, "Health": None}
    st.session_state.history = []
    st.session_state.round = 0
    st.session_state.game_over = False

# Define game scenarios
scenarios = [
    {
        "title": "You're buying your first car!",
        "type": "Car",
        "options": {
            "No Cover": 0,
            "Basic Cover (₹3,000)": 3000,
            "Comprehensive Cover (₹6,000)": 6000
        },
        "events": [
            {"event": "Minor Accident", "loss": 15000, "covered": {"Basic": 10000, "Comprehensive": 5000}},
            {"event": "Car Theft", "loss": 30000, "covered": {"Basic": 30000, "Comprehensive": 10000}}
        ]
    },
    {
        "title": "You've bought a new house!",
        "type": "House",
        "options": {
            "No Cover": 0,
            "Fire-only Cover (₹4,000)": 4000,
            "Full Cover (₹8,000)": 8000
        },
        "events": [
            {"event": "Fire Damage", "loss": 40000, "covered": {"Fire-only": 10000, "Full": 5000}},
            {"event": "Earthquake", "loss": 60000, "covered": {"Fire-only": 60000, "Full": 10000}}
        ]
    },
    {
        "title": "You’ve started earning well—planning for family security?",
        "type": "Life",
        "options": {
            "No Cover": 0,
            "₹1 Cr Term Plan (₹5,000)": 5000,
            "₹2 Cr Term Plan (₹9,000)": 9000
        },
        "events": [
            {"event": "Sudden Illness", "loss": 0, "covered": {"₹1 Cr Term": 0, "₹2 Cr Term": 0}},
            {"event": "Fatal Accident", "loss": 0, "covered": {"₹1 Cr Term": -10000000, "₹2 Cr Term": -20000000}}
        ]
    },
    {
        "title": "Health alert! Time to prepare?",
        "type": "Health",
        "options": {
            "No Cover": 0,
            "Basic Health Plan (₹6,000)": 6000,
            "Super Top-up Plan (₹10,000)": 10000
        },
        "events": [
            {"event": "Hospitalization", "loss": 25000, "covered": {"Basic": 10000, "Super": 2000}},
            {"event": "Critical Illness", "loss": 50000, "covered": {"Basic": 30000, "Super": 10000}}
        ]
    }
]

# Function to play one round
def play_round():
    if st.session_state.round >= len(scenarios):
        st.session_state.game_over = True
        return

    scenario = scenarios[st.session_state.round]
    st.header(f"Round {st.session_state.round + 1}: {scenario['title']}")

    choice = st.radio("Choose your coverage:", list(scenario["options"].keys()), key=f"choice_{st.session_state.round}")

    if st.button("Confirm Choice & See What Happens", key=f"confirm_{st.session_state.round}"):
        cost = scenario["options"][choice]
        st.session_state.balance -= cost

        st.session_state.coverage[scenario["type"]] = choice

        # Random event from scenario
        event = random.choice(scenario["events"])
        st.subheader(f"Event: {event['event']}")

        # Determine out-of-pocket cost
        coverage_key = None
        for cov in event["covered"].keys():
            if cov in choice:
                coverage_key = cov
                break

        if coverage_key:
            out_of_pocket = event["covered"][coverage_key]
        else:
            out_of_pocket = event["loss"]

        st.session_state.balance -= out_of_pocket

        # Record the result
        st.session_state.history.append({
            "Scenario": scenario["title"],
            "Choice": choice,
            "Event": event["event"],
            "Out-of-pocket": out_of_pocket,
            "Remaining": st.session_state.balance
        })

        st.success(f"You paid ₹{out_of_pocket} out-of-pocket.")
        st.session_state.round += 1

# Function to show game summary
def show_summary():
    st.title("🏁 Game Over: Your Summary")

    st.write(f"💰 Final Balance: ₹{st.session_state.balance}")

    for record in st.session_state.history:
        st.markdown(f"""
        **{record['Scenario']}**
        - Choice: {record['Choice']}
        - Event: {record['Event']}
        - Out-of-pocket: ₹{record['Out-of-pocket']}
        - Balance after round: ₹{record['Remaining']}
        """)

    # Final grade
    final = st.session_state.balance
    if final > 45000:
        grade = "A+ – Risk Managed Like a Pro!"
    elif final > 35000:
        grade = "B – You did pretty well!"
    elif final > 20000:
        grade = "C – Some risky gaps."
    else:
        grade = "D – Ouch! Time to learn insurance basics."

    st.subheader(f"🎓 Grade: {grade}")

    if st.button("🔁 Play Again"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]

# Game loop
if not st.session_state.game_over:
    play_round()
else:
    show_summary()
