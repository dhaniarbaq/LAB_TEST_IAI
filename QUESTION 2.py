# -*- coding: utf-8 -*-
# app.py
import json
from typing import List, Dict, Any, Tuple
import operator
import streamlit as st

# ----------------------------
# 1) Rule Engine (UNCHANGED)
# ----------------------------
OPS = {
    "==": operator.eq,
    "!=": operator.ne,
    ">": operator.gt,
    ">=": operator.ge,
    "<": operator.lt,
    "<=": operator.le,
}

DEFAULT_RULES: List[Dict[str, Any]] = [
    {
        "name": "Windows open → AC OFF",
        "priority": 110,
        "conditions": [["windows_open", "==", True]],
        "action": {
            "mode": "OFF",
            "fan_speed": "AUTO",
            "setpoint": None,
            "reason": "Cooling disabled because windows are open"
        }
    },
    {
        "name": "Empty house → Eco mode",
        "priority": 95,
        "conditions": [
            ["occupancy", "==", "EMPTY"],
            ["temperature", ">=", 24]
        ],
        "action": {
            "mode": "ECO",
            "fan_speed": "LOW",
            "setpoint": 27,
            "reason": "No occupants, energy saving activated"
        }
    },
    {
        "name": "Hot & humid while occupied",
        "priority": 85,
        "conditions": [
            ["occupancy", "==", "OCCUPIED"],
            ["temperature", ">=", 30],
            ["humidity", ">=", 70]
        ],
        "action": {
            "mode": "COOL",
            "fan_speed": "HIGH",
            "setpoint": 23,
            "reason": "High temperature and humidity detected"
        }
    },
    {
        "name": "Hot while occupied",
        "priority": 75,
        "conditions": [
            ["occupancy", "==", "OCCUPIED"],
            ["temperature", ">=", 28]
        ],
        "action": {
            "mode": "COOL",
            "fan_speed": "MEDIUM",
            "setpoint": 24,
            "reason": "High temperature detected"
        }
    },
    {
        "name": "Warm while occupied",
        "priority": 65,
        "conditions": [
            ["occupancy", "==", "OCCUPIED"],
            ["temperature", ">=", 26],
            ["temperature", "<", 28]
        ],
        "action": {
            "mode": "COOL",
            "fan_speed": "LOW",
            "setpoint": 25,
            "reason": "Moderately warm environment"
        }
    },
    {
        "name": "Night comfort mode",
        "priority": 80,
        "conditions": [
            ["occupancy", "==", "OCCUPIED"],
            ["time_of_day", "==", "NIGHT"],
            ["temperature", ">=", 26]
        ],
        "action": {
            "mode": "SLEEP",
            "fan_speed": "LOW",
            "setpoint": 26,
            "reason": "Night-time comfort optimization"
        }
    },
    {
        "name": "Too cold → system OFF",
        "priority": 90,
        "conditions": [["temperature", "<=", 22]],
        "action": {
            "mode": "OFF",
            "fan_speed": "AUTO",
            "setpoint": None,
            "reason": "Temperature already low"
        }
    }
]

def evaluate_condition(facts: Dict[str, Any], cond: List[Any]) -> bool:
    field, op, value = cond
    if field not in facts or op not in OPS:
        return False
    return OPS[op](facts[field], value)

def rule_matches(facts: Dict[str, Any], rule: Dict[str, Any]) -> bool:
    return all(evaluate_condition(facts, condition) for condition in rule["conditions"])

def run_rules(
    facts: Dict[str, Any],
    rules: List[Dict[str, Any]]
) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:

    matched_rules = [r for r in rules if rule_matches(facts, r)]

    if not matched_rules:
        return {
            "mode": "OFF",
            "fan_speed": "AUTO",
            "setpoint": None,
            "reason": "No rule satisfied"
        }, []

    matched_rules.sort(key=lambda r: r["priority"], reverse=True)
    return matched_rules[0]["action"], matched_rules


# ----------------------------
# 2) Streamlit UI (REDESIGNED)
# ----------------------------
st.set_page_config(page_title="Smart AC Rule-Based System", layout="wide")

st.markdown(
    "<h1 style='text-align:center;'>❄️ Smart Air Conditioner Control Dashboard</h1>",
    unsafe_allow_html=True
)
st.markdown("<p style='text-align:center;'>Rule-Based Expert System for AC Automation</p>", unsafe_allow_html=True)
st.markdown("---")

# ---- Input Panel (Top Section) ----
st.subheader("🏠 Home Environment Inputs")

col1, col2, col3 = st.columns(3)

with col1:
    temperature = st.number_input("🌡️ Temperature (°C)", value=23, step=1)
    humidity = st.number_input("💧 Humidity (%)", value=50, step=1)

with col2:
    occupancy = st.selectbox("👥 Occupancy Status", ["OCCUPIED", "EMPTY"])
    time_of_day = st.radio("🕒 Time of Day", ["DAY", "NIGHT"], horizontal=True)

with col3:
    windows_open = st.checkbox("🪟 Windows are open", value=False)
    st.markdown("")
    run = st.button("🚀 Run Rule Engine", type="primary", use_container_width=True)

facts = {
    "temperature": temperature,
    "humidity": humidity,
    "occupancy": occupancy,
    "time_of_day": time_of_day,
    "windows_open": windows_open
}

# ---- Display Facts and Results in Two Columns ----
st.markdown("---")
left, right = st.columns([1, 2])

with left:
    st.subheader("📌 Current Facts")
    st.json(facts)

with right:
    st.subheader("🤖 System Decision")

    if run:
        action, fired_rules = run_rules(facts, DEFAULT_RULES)

        # Action summary using metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Mode", action["mode"])
        m2.metric("Fan Speed", action["fan_speed"])
        m3.metric("Setpoint", "None" if action["setpoint"] is None else f"{action['setpoint']} °C")

        st.success(f"📝 **Reason:** {action['reason']}")

        # Rules Fired
        st.subheader("📜 Rules That Matched (by Priority)")
        if fired_rules:
            for r in fired_rules:
                st.write(f"🔹 **{r['name']}**  |  Priority: `{r['priority']}`")
        else:
            st.warning("No rules matched the current conditions.")

    else:
        st.info("Click **Run Rule Engine** to evaluate the current home conditions.")

# ---- Optional Expandable Rule Base Viewer ----
with st.expander("📚 View All Rules in the Knowledge Base"):
    st.json(DEFAULT_RULES)
