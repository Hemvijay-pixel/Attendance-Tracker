import streamlit as st
import pandas as pd
from collections import defaultdict
import json
import os

DATA_FILE = "attendance.json"

# ---------------- STORAGE ----------------

def load_attendance():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_attendance(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ---------------- SUBJECT SLOTS ----------------

slots_per_day = {
    "Monday":        {"DBMS": 2, "Interpretable ML": 1, "OS": 1, "Neural Networks": 1},
    "Tuesday":       {"CBCS": 1, "OS": 1, "Design Thinking": 1, "DBMS": 1, "Neural Networks": 1},
    "Wednesday":     {"CBCS": 1, "Neural Networks": 2, "Probability": 1, "DBMS": 1},
    "Thursday":      {"CBCS": 1, "OS": 1, "Probability": 1, "DBMS": 1, "Interpretable ML": 1},
    "Friday":        {"OS": 1, "Probability": 2, "Design Thinking": 1, "Interpretable ML": 1},
    "Monday_Sat":    {"DBMS": 2, "Interpretable ML": 1, "OS": 1, "Neural Networks": 1},
    "Wednesday_Sat": {"CBCS": 1, "Neural Networks": 2, "Probability": 1, "DBMS": 1},
}

# ---------------- CAE-1 SKIPPED SLOTS ----------------

cae1_skipped_slots = {
    "10/02/2026": {"CBCS": 1, "OS": 1},
    "11/02/2026": {"CBCS": 1, "Neural Networks": 1},
    "12/02/2026": {"CBCS": 1, "OS": 1},
    "13/02/2026": {"OS": 1, "Probability": 1},
    "16/02/2026": {"DBMS": 2},
    "17/02/2026": {"CBCS": 1, "OS": 1},
#---------------- CAE-2 Skipped slots/hours ------------
    "23/03/2026": {"DBMS": 2},
    "24/03/2026": {"CBCS": 1, "OS": 1},
    "25/03/2026": {"CBCS": 1, "Neural Networks": 1},
    "26/03/2026": {"CBCS": 1, "OS": 1},
    "27/03/2026": {"OS": 1, "Probability": 1},
    "30/03/2026": {"DBMS": 2},
}

# ---------------- WORKING DAYS ----------------
# (date, timetable_key, status, day_type)

working_days = [
    ("24/11/2025", "Monday",    "Present",  "Normal"),
    ("25/11/2025", "Tuesday",   "Present",  "Normal"),
    ("26/11/2025", "Wednesday", "Present",  "Normal"),
    ("27/11/2025", "Thursday",  "Present",  "Normal"),
    ("28/11/2025", "Friday",      "Present",  "Normal"),
    ("01/12/2025", "Monday",    "Present",  "Normal"),
    ("04/12/2025", "Thursday",  "Present",  "Normal"),
    ("05/12/2025", "Friday",    "Present",  "Normal"),
    ("08/12/2025", "Monday",    "Present",  "Normal"),
    ("09/12/2025", "Full",      "Present",  "Holiday"),
    ("10/12/2025", "Wednesday", "Present",  "Normal"),
    ("11/12/2025", "Thursday",  "Present",  "Normal"),
    ("12/12/2025", "Friday",    "Present",  "Normal"),
    ("15/12/2025", "Monday",    "Absent",  "Normal"),
    ("16/12/2025", "Tuesday",   "Absent",  "Normal"),
    ("17/12/2025", "Wednesday", "Absent",  "Normal"),
    ("18/12/2025", "Thursday",  "Absent",  "Normal"),
    ("19/12/2025", "Friday",    "Absent",  "Normal"),
    ("05/01/2026", "Monday",    "Present",  "Normal"),
    ("06/01/2026", "Tuesday",   "Present",  "Normal"),
    ("07/01/2026", "Wednesday", "Present",  "Normal"),
    ("08/01/2026", "Thursday",  "Present",  "Normal"),
    ("09/01/2026", "Friday",    "Present",  "Normal"),
    ("12/01/2026", "Monday",    "Present",  "Normal"),
    ("13/01/2026", "Full",      "Present",  "Holiday"),
    ("19/01/2026", "Monday",    "Present",  "Normal"),
    ("20/01/2026", "Tuesday",   "Present",   "Normal"),
    ("21/01/2026", "Wednesday", "Present",  "Normal"),
    ("22/01/2026", "Thursday",  "Present",  "Normal"),
    ("23/01/2026", "Friday",    "Present",  "Normal"),
    ("27/01/2026", "Tuesday",   "Present",  "Normal"),
    ("28/01/2026", "Wednesday", "Present",  "Normal"),
    ("29/01/2026", "Thursday",  "Present",  "Normal"),
    ("30/01/2026", "Friday",    "Present",  "Normal"),
    ("02/02/2026", "Monday",    "Present",  "Normal"),
    ("03/02/2026", "Tuesday",   "Present",  "Normal"),
    ("04/02/2026", "Wednesday", "Present",  "Normal"),
    ("05/02/2026", "Full",      "Present",  "Culturals"),
    ("06/02/2026", "Full",      "Present",  "Culturals"),
    ("09/02/2026", "Monday",    "Present",  "Normal"),
    ("10/02/2026", "Tuesday",   "Present",  "CAE"),
    ("11/02/2026", "Wednesday", "Present",  "CAE"),
    ("12/02/2026", "Thursday",  "Present",  "CAE"),
    ("13/02/2026", "Friday",    "Present",  "CAE"),
    ("14/02/2026", "Monday_Sat","Present",  "Normal"),
    ("16/02/2026", "Monday",    "Present",  "CAE"),
    ("17/02/2026", "Tuesday",   "Present",  "CAE"),
    ("18/02/2026", "Wednesday", "Present",   "Normal"),
    ("19/02/2026", "Full",      "Present",  "Placement"),
    ("20/02/2026", "Friday",    "Present",  "Normal"),
    ("23/02/2026", "Monday",    "Present",  "Normal"),
    ("24/02/2026", "Full",      "Present",  "Placement"),
    ("25/02/2026", "Wednesday", "Present",  "Normal"),
    ("26/02/2026", "Thursday",  "Present",  "Normal"),
    ("27/02/2026", "Friday",    "Present",  "Normal"),
    ("28/02/2026", "Wednesday", "Present", "Normal"),
    ("02/03/2026", "Monday",    "Present",   "Normal"),
    ("03/03/2026", "Tuesday",   "Present",  "Normal"),
    ("04/03/2026", "Wednesday", "Present",  "Normal"),
    ("05/03/2026", "Thursday",  "Present",  "Normal"),
    ("06/03/2026", "Friday",    "Present",  "Normal"),
    ("16/03/2026", "Monday",    "Present",  "Normal"),
    ("17/03/2026", "Tuesday",   "Present",  "Normal"),
    ("18/03/2026", "Wednesday", "Present",  "Normal"), 
    ("20/03/2026", "Friday",    "Present", "Normal"),
    ("23/03/2026", "Monday",    "Present", "CAE"),
    ("24/03/2026", "Tuesday",   "Present", "CAE"),
    ("25/03/2026", "Wednesday", "Present", "CAE"),
    ("26/03/2026", "Thursday",  "Present", "CAE"),
    ("27/03/2026", "Friday",    "Present", "CAE"),
    ("30/03/2026", "Monday",    "Present", "CAE"),
    ("01/04/2026", "Wednesday", "Present", "Normal"),
    ("02/04/2026", "Thursday",  "Present", "Normal"),
    ("06/04/2026", "Monday",    "Present", "Normal"),
    ("07/04/2026", "Tuesday",   "Present", "Normal"),
    ("08/04/2026", "Wednesday", "Present", "Normal"),
    ("09/04/2026", "Thursday",  "Present", "Normal"),
    ("10/04/2026", "Friday",    "Upcoming", "Normal"),
    ("13/04/2026", "Monday",   "Upcoming", "Normal"),
    ("15/04/2026", "Wednesday", "Upcoming", "Normal"),
    ("16/04/2026", "Thursday", "Upcoming", "Normal"),
    ("17/04/2026", "Friday", "Upcoming", "Normal"),
]

# ---------------- SLOT RESOLVER ----------------

def resolve_slots(timetable_key, date):
    if timetable_key == "Full":
        return {}

    base = dict(slots_per_day.get(timetable_key, {}))

    # FIX: Remove first 2 hours for CAE days (instead of subject-specific removal)
    if date in cae1_skipped_slots:
        remove_hours = 2
        updated = {}

        for subject, count in base.items():
            if remove_hours <= 0:
                updated[subject] = count
                continue

            if count <= remove_hours:
                remove_hours -= count
                # skip entire subject slot
            else:
                updated[subject] = count - remove_hours
                remove_hours = 0

        base = updated

    return base

# ---------------- ATTENDANCE CALCULATION ----------------

def calculate_attendance(data):
    attended = defaultdict(int)
    total    = defaultdict(int)

    for date, timetable_key, default_status, day_type in working_days:
        status = data.get(date, default_status)
        if status == "Upcoming":
            continue
        slots = resolve_slots(timetable_key, date)
        for subject, count in slots.items():
            total[subject] += count
            if status == "Present":
                attended[subject] += count

    rows = []
    for subject in total:
        A = attended[subject]
        T = total[subject]
        percent = (A / T) * 100 if T > 0 else 0
        rows.append({
            "Subject":    subject,
            "Attended":   A,
            "Total":      T,
            "Missed":     T - A,
            "Percentage": round(percent, 2)
        })

    return pd.DataFrame(rows)

# (Rest of the code remains unchanged)



# ---------------- STREAMLIT UI ----------------

st.set_page_config(page_title="Smart Attendance Analytics", layout="wide")
st.title("📊 Smart Attendance Analytics System")

attendance_data = load_attendance()

# ---------------- ATTENDANCE MANAGEMENT ----------------

st.header("✏️ Update Attendance")

date_list = [d for d, _, _, _ in working_days]
selected_date = st.selectbox("Select Date", date_list)

status_options = ["Present", "Absent", "Upcoming"]
current_status = attendance_data.get(selected_date, "Present")

selected_status = st.selectbox(
    "Select Status",
    status_options,
    index=status_options.index(current_status) if current_status in status_options else 0
)

if st.button("Update Attendance"):
    attendance_data[selected_date] = selected_status
    save_attendance(attendance_data)
    st.success(f"{selected_date} updated to {selected_status}")

st.divider()

# ---------------- ATTENDANCE TABLE ----------------

st.header("📋 Attendance Table")

rows = []
for date, timetable_key, default_status, day_type in working_days:
    status = attendance_data.get(date, default_status)
    rows.append({
        "Date":      date,
        "Timetable": timetable_key,
        "Status":    status,
        "Type":      day_type
    })

edited_df = st.data_editor(
    pd.DataFrame(rows),
    column_config={
        "Status": st.column_config.SelectboxColumn(
            "Status",
            options=["Present", "Absent", "Upcoming"],
            required=True
        ),
        "Date":      st.column_config.TextColumn("Date",      disabled=True),
        "Timetable": st.column_config.TextColumn("Timetable", disabled=True),
        "Type":      st.column_config.TextColumn("Type",      disabled=True),
    },
    use_container_width=True,
    hide_index=True,
    key="attendance_editor"
)

# Save any changes made in the table
if st.button("💾 Save Table Changes"):
    for _, row in edited_df.iterrows():
        attendance_data[row["Date"]] = row["Status"]
    save_attendance(attendance_data)
    st.success("Table changes saved!")
    st.rerun()

st.divider()

# ---------------- SYSTEM OVERVIEW ----------------

attendance_df = calculate_attendance(attendance_data)

st.header("📌 System Overview")

present  = sum(1 for d, t, s, dt in working_days if attendance_data.get(d, s) == "Present" and dt != "Holiday")
absent   = sum(1 for d, t, s, dt in working_days if attendance_data.get(d, s) == "Absent" and dt != "Holiday")
upcoming = sum(1 for d, t, s, dt in working_days if attendance_data.get(d, s) == "Upcoming" and dt != "Holiday")

# Overall % is day-wise (matches college portal calculation)
total_working = present + absent
overall = (present / total_working) * 100 if total_working > 0 else 0

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Subjects",      len(attendance_df))
c2.metric("Present Days",  present)
c3.metric("Absent Days",   absent)
c4.metric("Upcoming Days", upcoming)
c5.metric("Attendance %",  f"{overall:.2f}%")

st.dataframe(attendance_df, use_container_width=True)

# ---------------- HEALTH MONITOR ----------------

st.divider()
st.header("📈 Attendance Health Monitor")

for _, row in attendance_df.iterrows():
    st.subheader(row["Subject"])
    st.progress(
        min(row["Percentage"] / 100, 1.0),
        text=f"{row['Percentage']}%  ({row['Attended']}/{row['Total']})"
    )

# ---------------- LEAVE SIMULATION ----------------

st.divider()
st.header("🧪 Leave Simulation")

upcoming_days = [d for d, t, s, dt in working_days if attendance_data.get(d, s) == "Upcoming"]
leave_days = st.multiselect("Select leave days", upcoming_days)

simulation = attendance_data.copy()
for d in leave_days:
    simulation[d] = "Absent"

if leave_days:
    st.write("### Selected Leave Days")
    for d in leave_days:
        st.write(f"❌ {d}")

sim_df = calculate_attendance(simulation)
st.dataframe(sim_df)

# ---------------- SMART LEAVE PLANNER ----------------

st.divider()
st.header("📅 Smart Leave Planner")

for date, timetable_key, status, day_type in working_days:
    if attendance_data.get(date, status) != "Upcoming":
        continue
    sim = attendance_data.copy()
    sim[date] = "Absent"
    result = calculate_attendance(sim)
    risk = result[result["Percentage"] < 80]["Subject"].tolist()
    if len(risk) == 0:
        st.success(f"{date} → Safe Leave")
    else:
        st.warning(f"{date} → Risk for {', '.join(risk)}")

# ---------------- SEMESTER PREDICTION ----------------

st.divider()
st.header("🔮 Semester Prediction")

prediction_rows = []
for _, row in attendance_df.iterrows():
    subject = row["Subject"]
    att     = row["Attended"]
    tot     = row["Total"]

    upcoming_slots = 0
    for date, timetable_key, status, day_type in working_days:
        if attendance_data.get(date, status) == "Upcoming":
            slots = resolve_slots(timetable_key, date)
            upcoming_slots += slots.get(subject, 0)

    future_total    = tot + upcoming_slots
    future_attended = att + upcoming_slots
    final_percent   = (future_attended / future_total) * 100 if future_total > 0 else 0

    prediction_rows.append({
        "Subject":           subject,
        "Current %":         row["Percentage"],
        "Predicted Final %": round(final_percent, 2)
    })

st.dataframe(pd.DataFrame(prediction_rows))

# ---------------- RECOVERY PLANNER ----------------

st.divider()
st.header("🎯 Recovery Planner")

for _, row in attendance_df.iterrows():
    subject = row["Subject"]
    A = row["Attended"]
    T = row["Total"]

    if T > 0 and (A / T) >= 0.8:
        st.success(f"{subject}: Attendance already safe ✅")
        continue

    needed = 0
    while (A + needed) / (T + needed) < 0.8:
        needed += 1

    st.warning(f"{subject}: Attend next {needed} classes to reach 80%")

# ---------------- EXPORT REPORT ----------------

st.divider()
st.header("📄 Export Attendance Report")

csv = attendance_df.to_csv(index=False)
st.download_button(
    label="Download Report",
    data=csv,
    file_name="attendance_report.csv",
    mime="text/csv"
)