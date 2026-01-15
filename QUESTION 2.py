import streamlit as st

st.title("Smart Home Air Conditioner Controller")

temperature = st.number_input("Temperature (°C)", value=22)
humidity = st.number_input("Humidity (%)", value=46)
occupancy = st.selectbox("Occupancy", ["OCCUPIED", "EMPTY"])
time_of_day = st.selectbox("Time of Day", ["MORNING", "AFTERNOON", "EVENING", "NIGHT"])
windows_open = st.checkbox("Windows Open")

def decide_ac(temp, hum, occ, time, win):
    if win:
        return "AC OFF | Windows are open"
    if temp <= 22:
        return "AC OFF | Too cold"
    if occ == "EMPTY" and temp >= 24:
        return "ECO MODE | Setpoint 27°C"
    if occ == "OCCUPIED" and temp >= 30 and hum >= 70:
        return "COOL HIGH | Setpoint 23°C"
    if occ == "OCCUPIED" and temp >= 28:
        return "COOL MEDIUM | Setpoint 24°C"
    if occ == "OCCUPIED" and time == "NIGHT" and temp >= 26:
        return "SLEEP MODE | Setpoint 26°C"
    return "COOL LOW | Setpoint 25°C"

if st.button("Decide AC Setting"):
    result = decide_ac(temperature, humidity, occupancy, time_of_day, windows_open)
    st.success(result)
