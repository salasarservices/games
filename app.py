import random
import streamlit as st

st.title("🎲 Insure or Risk It?")

initial_budget = 10000

assets = {
    "Car": {"insurance_cost": 2000, "loss": 20000},
    "House": {"insurance_cost": 3500, "loss": 40000},
    "Health": {"insurance_cost": 3000, "loss": 30000},
    "Phone": {"insurance_cost": 1000, "loss": 10000},
    "Inventory": {"insurance_cost": 4000, "loss": 50000}
}

disasters = {
    "Fire": "House",
    "Theft": "Phone",
    "Illness": "Health",
    "Accident": "Car",
    "No Event": None
}

st.markdown("## Instructions:")
st.markdown("You have ₹10,000. Select which assets you want to insure. The game will run for 3 rounds, each with a random disaster event.")

st.markdown("### Available Assets:")
for asset, data in assets.items():
    st.markdown(f"- **{asset}** → Insurance: ₹{data['insurance_cost']} | Potential Loss: ₹{data['loss']}")

selected_assets = st.multiselect("Select the assets you want to insure:", options=list(assets.keys()))

if st.button("Play Game"):
    budget = initial_budget
    total_insurance_cost = sum(assets[asset]["insurance_cost"] for asset in selected_assets)
    budget -= total_insurance_cost

    st.success(f"Insurance cost deducted: ₹{total_insurance_cost}. Remaining budget: ₹{budget}")

    for i in range(1, 4):
        st.markdown(f"### Round {i}")
        event = random.choice(list(disasters.keys()))
        affected_asset = disasters[event]
        st.write(f"🌀 Disaster Event: **{event}**")

        if affected_asset:
            if affected_asset in selected_assets:
                st.success(f"You had insured {affected_asset}. No loss this round!")
            else:
                loss = assets[affected_asset]["loss"]
                budget -= loss
                st.error(f"You did not insure {affected_asset}. You lost ₹{loss}")
        else:
            st.info("No disaster this round. You're safe!")

    st.markdown("---")
    st.subheader(f"🏁 Final Budget: ₹{budget}")
