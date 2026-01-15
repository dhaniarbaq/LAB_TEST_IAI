import json
import operator
import streamlit as st

with open("json_q2.txt", "r") as f:
    RULES = json.load(f)

OPS = {
    "==": operator.eq,
    "!=": operator.ne,
    ">": operator.gt,
    ">=": operator.ge,
    "<": operator.lt,
    "<=": operator.le,
}

def check_condition(facts, condition):
    field, op, value = condition
    return OPS[op](facts[field], value)

def rule_match(facts, rule):
    return all(check_condition(facts, c) for c in rule["conditions"])

def infer_action(facts):
    matched_rules = [r for r in RULES if rule_match(facts, r)]
    if not matched_rules:
        return None, []
    matched_rules.sort(key=lambda r: r["priority"], reverse=True)
    return matched_rules[0], matched_rules

st.set_page_config(page_title="Smart AC Controller", layout="centered")

st.title("Smart Home Air Conditioner Controller")
st.caption("Rule-Based Expert System using JSON Knowledge Base")

temperature = st.number_input("Temperature (°C)", value=22)
humidity = st.number_input("Humidity (%)", value=46)
occupancy = st.selectbox("Occupancy", ["OCCUPIED", "EMPTY"])
time_of_day = st.selectbox("Time of Day", ["MORNING", "AFTERNOON", "EVENING", "NIGHT"])
windows_open = st.checkbox("Windows Open")

facts = {
    "temperature": temperature,
    "humidity": humidity,
    "occupancy": occupancy,
    "time_of_day": time_of_day,
    "windows_open": windows_open
}

st.subheader("Current Facts")
st.json(facts)

if st.button("Run Rule Engine"):
    selected_rule, matched = infer_action(facts)

    if selected_rule:
        action = selected_rule["action"]

        st.subheader("System Decision")
        st.metric("AC Mode", action["ac_mode"])
        st.metric("Fan Speed", action["fan_speed"])
        st.metric(
            "Setpoint",
            "None" if action["setpoint"] is None else f"{action['setpoint']} °C"
        )
        st.success(f"Reason: {action['reason']}")

        st.subheader("Matched Rules (by priority)")
        for r in matched:
            st.write(f"• {r['name']} (Priority {r['priority']})")
    else:
        st.warning("No rule matched. AC remains OFF.")
