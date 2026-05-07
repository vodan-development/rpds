import streamlit as st
from datetime import date, datetime
import pandas as pd
import requests  # for SPARQL HTTP requests
import plotly.express as px 
import os 
from dotenv import load_dotenv; load_dotenv()
from db import get_connection, init_db
from schema import LOCATION_REGISTRY, EVENT_TYPES, AFFECTED_STATUSES, LABELS, SUBEVENT_TYPES, AFFECTED_TARGET,AFFILIATION,GENDER,INVOLVED_CATEGORY    # SUBEVENT_TYPES Part of schema New Addded 
from etl import (
    dataframe_to_rdf,
    upload_to_allegrograph,
    SPARQL_ENDPOINT,
    AG_USERNAME,
    AG_PASSWORD,
)

# ---------------------------------------------------------
# BASIC APP CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(page_title="Secure Refugee Data System (RPDS)", layout="wide")

# Ensure DB and table exist
init_db()

# 2. GLOBAL HELPER FUNCTIONS (Moved here to fix NameError)
# ---------------------------------------------------------
# TRANSLATION HELPERS
# ---------------------------------------------------------
def tr(key: str, default_en: str) -> str:
    # Translation helper for multilingual labels.
    # Supports English, Amharic (am), and Tigrigna (ti).
    if language.startswith("Amharic"):
        if key in LABELS and "am" in LABELS[key]:
            return f"{LABELS[key]['en']} / {LABELS[key]['am']}"
        return default_en
    elif language.startswith("Tigrigna"):
        if key in LABELS and "ti" in LABELS[key]:
            return f"{LABELS[key]['en']} / {LABELS[key]['ti']}"
        return default_en
    else:
        if key in LABELS and "en" in LABELS[key]:
            return LABELS[key]["en"]
        return default_en


def section_header(title_en: str, title_am: str = "", title_ti: str = ""):
    # Section header that supports English, Amharic, and Tigrigna.
    if language.startswith("Amharic") and title_am:
        st.subheader(f"{title_en} / {title_am}")
    elif language.startswith("Tigrigna") and title_ti:
        st.subheader(f"{title_en} / {title_ti}")
    else:
        st.subheader(title_en)

# ---------------------------------------------------------
# AUTHENTICATION LOGIC (FAIR Access Control)
# ---------------------------------------------------------
def check_password():
    # Returns True if the user has provided correct credentials.
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        # Use columns to center the login container
        empty_left, center_col, empty_right = st.columns([1, 2, 1])
        
        with center_col:
            # Define the Logo image path relative to this script
            img_path = os.path.join(os.path.dirname(__file__), "logo.png")

            # Using a container to ensure everything stays grouped
            with st.container():
                if os.path.exists(img_path):
                     st.image(img_path, width=300) # Adjust width as needed
                    # st.sidebar.image(img_path, use_container_width="stretch")
                else:
                    # This prevents the MediaFileStorageError by checking existence first
                    st.sidebar.error("⚠️ logo.png not found in directory")
          
                st.markdown("<h2 style='text-align: center;'>🔐 Secure Refugee Data System (RPDS) Login </h2>", unsafe_allow_html=True)
                
                with st.container(border=True):
                    user_input = st.text_input("Username")
                    pw_input = st.text_input("Password", type="password")
                    
                    if st.button("Sign In", use_container_width="stretch"):
                        users = {
                            os.getenv("ADMIN_USER"): {
                                "pwd": os.getenv("ADMIN_PASSWORD"), 
                                "role": "Admin"
                            },
                            os.getenv("SECTOR_OFFICER_USER"): {
                                "pwd": os.getenv("SECTOR_OFFICER_PASSWORD"), 
                                "role": "Sector Officer"
                            },
                            os.getenv("FIELD_OFFICER_USER"): {
                                "pwd": os.getenv("FIELD_OFFICER_PASSWORD"), 
                                "role": "Field Worker"
                            }
                        }
                        
                        if user_input in users and pw_input == users[user_input]["pwd"]:
                            st.session_state["authenticated"] = True
                            st.session_state["user_role"] = users[user_input]["role"]
                            st.session_state["username"] = user_input
                            st.rerun()
                        else:
                            st.error("Invalid username or password.")
        return False
    return True

# ---------------------------------------------------------
# TRANSLATION HELPERS
# ---------------------------------------------------------
def tr(key: str, default_en: str) -> str:
    # Translation helper for multilingual labels.
    if language.startswith("Amharic"):
        return f"{LABELS[key]['en']} / {LABELS[key]['am']}" if key in LABELS and "am" in LABELS[key] else default_en
    elif language.startswith("Tigrigna"):
        return f"{LABELS[key]['en']} / {LABELS[key]['ti']}" if key in LABELS and "ti" in LABELS[key] else default_en
    return LABELS[key]["en"] if key in LABELS and "en" in LABELS[key] else default_en

# ---------------------------------------------------------
# PROTECTED APP CONTENT (April 2026 Update)
# ---------------------------------------------------------
if check_password():
    # 1. SIDEBAR CONFIGURATION (Locked to Session)
    st.sidebar.title("FieldLab1 Navigation")
    
    current_role = st.session_state["user_role"]
    current_user = st.session_state["username"]
    
    language = st.sidebar.selectbox("Language / ቋንቋ", ["English", "Amharic / አማርኛ", "Tigrigna / ትግርኛ"])
    page = st.sidebar.radio("Main Menu", ["Submit report", "View cases", "SPARQL dashboard"])
    
    st.sidebar.divider()
    st.sidebar.write(f"👤 **User:** `{current_user}`")
    st.sidebar.write(f"🛡️ **Role:** `{current_role}`")
    
    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()

    # ---------------------------------------------------------
    # PAGE 1: SUBMIT 
    # This page has been updated to align with the new DIS
    # April 2026 Update
    # ---------------------------------------------------------
    if page == "Submit report":
        st.title("Incident / Event Reporting Form")

        with st.form("event_report_form"):
            # 1. Reporting Information
            # Added Tigrigna title: "ሓበሬታ ጸብጻብ"
            section_header("1. Reporting Information", "የሪፖርት መረጃ", "ሓበሬታ ጸብጻብ")

            col_r1, col_r2, col_r3, col_r4 = st.columns(4)

            with col_r1:
                organisation_id = st.number_input(
                    tr("organisation_id", "Organisation ID"),
                    min_value=0,
                    step=1,
                    help="Internal code of the organisation collecting this report.",
                )
            with col_r2:
                input_by = st.text_input(
                    tr("input_by", "Input by (user name / ID)"),
                    help="Person or account entering this data.",
                )
            with col_r3: # New Added 
                date_received = st.date_input(
                    tr("date_received", "Date report received"),
                    value=date.today(),
                    help="Date at which the incident was reported to the source organisation.",
                )
            with col_r4:
                date_recorded = st.date_input(
                    tr("date_recorded", "Date report recorded"),
                    value=date.today(),
                )
            # 2. Camp / Location
            # Added Tigrigna title: "ሓበሬታ መዓስከር"
            section_header("2. Camp Information", "የካምፕ መረጃ", "ሓበሬታ መዓስከር")
            col_r1, col_r2 = st.columns(2) 
            with col_r1: # New col and input schema 
                camp_name = st.text_input(
                    tr("camp_name", "Camp Name"),
                    help="Name of the refugee or IDP camp",
                ) 
            with col_r2: # New col and input schema 
                camp_id = st.number_input(
                    tr("camp_id", "Camp ID"),
                    min_value=0,
                    step=1,
                    help="ID of the refugee or IDP camp.",
                )
            st.subheader("Location")#,"የተጎዱ","ዝተሃሰዩ ወገናት")
            col_r1, col_r2, col_r3, col_r4 = st.columns(4) 
            with col_r1:   # New Added
                all_countries = sorted({loc["country"] for loc in LOCATION_REGISTRY})
                selected_country = st.selectbox(
                    tr("country", "Country"),
                    options=all_countries,
                )
            with col_r2:   # New Added
                regions_for_country = sorted(
                    {loc["region"] for loc in LOCATION_REGISTRY if loc["country"] == selected_country}
                )
                selected_region = st.selectbox(
                    tr("region", "Region / State"),
                    options=regions_for_country,
                )
            with col_r3:   # New Added
                camps_for_region = sorted(
                    {
                        loc["camp"]
                        for loc in LOCATION_REGISTRY
                        if loc["country"] == selected_country and loc["region"] == selected_region
                    }
                )
                camp_options = camps_for_region + ["Other (specify)"]
                selected_camp = st.selectbox(
                    tr("town", "Town"),
                    options=camp_options,
                    help="The town in which the camp is located",
                )
                camp_other = ""
                if selected_camp == "Other (specify)":
                    camp_other = st.text_input(
                        tr("camp_other", "If other, please specify camp / town name")
                    )
            with col_r4: # New col and input schema 
                village_name = st.text_input(
                    tr("village_name", "Village Name"),
                    help="The village in which the camp is located",
                ) 
            col_c1, col_c2 = st.columns(2)
            with col_c1:
                camp_lat = st.number_input(
                    tr("latitude", "Latitude (optional)"),
                    value=0.0,
                    format="%.6f",
                )
            with col_c2:
                camp_lon = st.number_input(
                    tr("longitude", "Longitude (optional)"),
                    value=0.0,
                    format="%.6f",
                )

            # 3. Event Information
            # Added Tigrigna title: "ሓበሬታ ፍጻሜ"
            section_header("3. Event Information", "የክስተት መረጃ", "ሓበሬታ ፍጻሜ")

            col_e1, col_e2, col_e3 = st.columns(3)
            with col_e1:
                event_date = st.date_input(
                    tr("event_date", "Date of event"),
                    value=date.today(),
                )
            with col_e2:
                time_range = st.text_input(
                    tr("time_range", "Time range (e.g. 10:00–12:00)"),
                    help="Period of the event",
                )
            with col_e3:
                event_location_detail = st.text_input(
                    tr("event_location_detail", "Specific place (neighbourhood / site)"),
                    help="More detailed description of where in the camp or town.",
                )

            col_e4, col_e5 = st.columns(2)
            with col_e4:
                event_type = st.selectbox(
                    tr("event_type", "Type of event that took place"),
                    EVENT_TYPES,
                    help="The type of event that took place",
                )
            with col_e5:
                # event_subtype = st.text_input(
                #     tr("event_subtype", "Subtype (optional)"),
                #     help="More specific description, e.g. shelling, looting, GBV, checkpoint violence, etc.",
                # )
                # New modified to dropdown 
                event_subtype = st.selectbox(
                    tr("event_subtype", "The subtype of event that took place"),
                    SUBEVENT_TYPES,
                    help="The type of event that took place"
                )

            # 4. Involved Parties
            # Added Tigrigna title: "ዝምልከቶም ወገናት"
            section_header("4. Involved Parties", "ተዋናይ ወገኖች", "ዝምልከቶም ወገናት")
            st.subheader("Affected")#,"የተጎዱ","ዝተሃሰዩ ወገናት")
            col_a1, col_a2, col_a3 = st.columns(3)
            with col_a1:
                affected_status = st.selectbox(
                    tr("affected_status", "Status of affected group"),
                    AFFECTED_STATUSES,
                )
            with col_a2:
                affected_number = st.number_input(
                    tr("affected_number", "Estimated number affected"),
                    min_value=0,
                    step=1,
                )
            with col_a3: 
                ethnicity = st.text_input(
                    tr("ethnicity", "Ethnicity"),
                    help="The ethnicity of the affected group or individual",
                )
            affected_target = st.selectbox(
                    tr("affected_target", "Affected Target"),
                    AFFECTED_TARGET,
                    help="The group that was targeted by the event"
            )      
            impact_description = st.text_area(
                    tr("impact_description", "Impact description"),
                    height=150,
                    help="Describe what happened, who was affected, and how.",
            )

            st.subheader("Perpetrator(s)")#,"የተጎዱ","ዝተሃሰዩ ወገናት")
            col_p1, col_p2, col_p3 = st.columns(3)
            with col_p1:
                affiliation = st.selectbox(
                    tr("affiliation", "Affiliation"),
                    AFFILIATION,
                    help="The group or individual that is responsible for the event",
                )
            with col_p2:
                age = st.number_input(
                    tr("age", "Age"),
                    min_value=0,
                    step=1,
                    help="The age of the perpetrator(s)",
                )
            with col_p3:
                gender = st.selectbox(
                        tr("gender", "Gender"),
                        GENDER,
                        help="The gender of the perpetrator(s)"
                )      
            perpetrator_description = st.text_area(
                    tr("perpetrator_description", "Perpetrator Descriptionn"),
                    height=150,
                    help="The description of the perpetrator(s)",
            )

            st.subheader("Involved")#,"የተጎዱ","ዝተሃሰዩ ወገናት") 
            #col_a1, col_a2 = st.columns(2)
            #with col_a1:
            involved_category = st.selectbox(
                    tr("involved_category", "Involved Category"),
                    INVOLVED_CATEGORY,
                    help="The category of the party involved in the event",
            )
            #with col_a2:
            involvement_description = st.text_area(
                    tr("involvement_description", "Involvement description"),
                    height=150,
                    help="Description of the involvement of the party in the event.",
            )

            # 5. Sensitivity Flags
            # Added Tigrigna title: "ደረጃ ምስጢራዊነት"
            section_header("6. Sensitivity", "የግላዊነት ደረጃ", "ደረጃ ምስጢራዊነት")

            col_flags1, col_flags2 = st.columns(2)
            with col_flags1:
                is_sensitive = st.checkbox(
                    tr("is_sensitive", "Mark as sensitive protection case"),
                    help="Restrict detailed access to authorised protection staff.",
                )
            with col_flags2:
                is_anonymous = st.checkbox(
                    tr("is_anonymous", "Anonymous report (no personal identifiers)"),
                    help="Do not store names or direct identifiers.",
                )

            submitted = st.form_submit_button("Submit report")

        #-----------------------------------------#
        # Handle submission
        #-----------------------------------------#
        if submitted:
            # 1. Define mandatory fields for validation
            # You can add or remove fields from this list based on your requirements
            errors = []
            if not organisation_id: errors.append("Organisation ID")
            if not input_by.strip(): errors.append("Input By")
            if not event_type: errors.append("Event Type")

            # 2. Check for errors
            if errors:
                st.error(f"❌ Submission failed. Please fill in the following required fields: {', '.join(errors)}")
            else:
                # 3. Proceed with submission if validation passes
                camp_final = selected_camp if selected_camp != "Other (specify)" else camp_other
                sensitive_flag = 1 if is_sensitive else 0
                anonymous_flag = 1 if is_anonymous else 0

                conn = get_connection()
                cur = conn.cursor()
                cur.execute(
                    """
                    INSERT INTO cases (
                        role, organisation_id, input_by, date_received, date_recorded, 
                        camp_name, camp_id, country, region, town, village_name, 
                        latitude, longitude, event_date, time_range, 
                        event_location_detail, event_type, event_subtype,
                        affected_status, affected_number, ethnicity, affected_target, 
                        impact_description, affiliation, age, gender, 
                        perpetrator_description, involved_category, involvement_description,
                        is_sensitive, is_anonymous, created_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        current_role, 
                        int(organisation_id), 
                        input_by, 
                        str(date_received), 
                        str(date_recorded),
                        camp_name, 
                        int(camp_id), 
                        selected_country, 
                        selected_region, 
                        camp_final, 
                        village_name,
                        float(camp_lat), 
                        float(camp_lon), 
                        str(event_date), 
                        time_range,
                        event_location_detail, 
                        event_type, 
                        event_subtype,
                        affected_status, 
                        int(affected_number), 
                        ethnicity, 
                        affected_target, 
                        impact_description, 
                        affiliation, 
                        int(age), 
                        gender, 
                        perpetrator_description, 
                        involved_category, 
                        involvement_description,
                        sensitive_flag, 
                        anonymous_flag, 
                        datetime.utcnow().isoformat()
                    ),
                )
                conn.commit()
                conn.close()
                st.success("Report saved successfully to local database (rpds.db).")


    # ---------------------------------------------------------
    # PAGE 2: VIEW CASES
    # ---------------------------------------------------------
    def view_cases_page():
        st.title(tr("view_cases", "View Cases & Analytics"))
        st.markdown("---")

        # 1. FETCH DATA FROM SQLITE
        conn = get_connection()
        df = pd.read_sql_query("SELECT * FROM cases", conn)
        conn.close()

        if df.empty:
            st.warning("No data found in the local database. Please submit a new case first.")
            return

        # 2. DATA PRE-PROCESSING
        df['event_date'] = pd.to_datetime(df['event_date'], errors='coerce')
        df['affected_number'] = pd.to_numeric(df['affected_number'], errors='coerce').fillna(0)
        df['is_sensitive'] = pd.to_numeric(df['is_sensitive'], errors='coerce').fillna(0)

        # 3. TOP-LEVEL RISK INDICATORS
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Total Cases", len(df))
        with m2:
            sens_count = int(df['is_sensitive'].sum())
            sens_percent = (sens_count / len(df)) * 100 if len(df) > 0 else 0
            st.metric("Sensitive Records", f"{sens_count}", f"{sens_percent:.1f}% Risk")
        with m3:
            total_impact = int(df['affected_number'].sum())
            st.metric("Total Affected", f"{total_impact:,}")
        with m4:
            # Highlight high-intensity violence events
            violence_cases = len(df[df['event_type'].str.contains("Violence", na=False)])
            st.metric("Violence Reports", violence_cases, delta_color="inverse")

        st.markdown("---")

        # 4. ANALYTICS TABS
        tab_map, tab_time, tab_risk = st.tabs(["🌍 Incident Map", "📅 Timeline", "📊 Risk Analysis"])

        with tab_map:
            st.subheader("Geospatial Distribution")
            map_df = df.dropna(subset=['latitude', 'longitude'])
            if not map_df.empty:
                fig_map = px.scatter_mapbox(
                    map_df, lat="latitude", lon="longitude", color="event_type", 
                    size="affected_number", hover_name="village_name", zoom=5, height=500
                )
                fig_map.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":0,"l":0,"b":0})
                st.plotly_chart(fig_map, use_container_width="stretch")
            else:
                st.info("No GPS coordinates found to map.")

        with tab_time:
            st.subheader("Incident Trends")
            timeline_df = df.groupby('event_date').size().reset_index(name='count')
            fig_line = px.line(timeline_df, x='event_date', y='count', markers=True, title="Incident Volume")
            st.plotly_chart(fig_line, use_container_width="stretch")

        with tab_risk:
            col_l, col_r = st.columns(2)
            with col_l:
                st.subheader("Severity by Event Type")
                fig_sun = px.sunburst(df, path=['event_type', 'event_subtype'], values='affected_number')
                st.plotly_chart(fig_sun, use_container_width="stretch")
            with col_r:
                st.subheader("Impact by Ethnicity")
                fig_bar = px.bar(df, x="ethnicity", y="affected_number", color="affected_status", barmode="group")
                st.plotly_chart(fig_bar, use_container_width="stretch")
        # 5. DATA TABLE
        with st.expander("🔍 Detailed Case Ledger"):
            st.dataframe(df.sort_values(by='created_at', ascending=False), use_container_width="stretch")


    if page == "View cases":
        st.title("View reported cases")

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT 
                id, role, organisation_id, input_by, date_received, date_recorded,
                camp_name, camp_id, country, region, town, village_name,
                latitude, longitude, event_date, time_range, event_location_detail,
                event_type, event_subtype, affected_status, affected_number,
                ethnicity, affected_target, impact_description, affiliation,
                age, gender, perpetrator_description, involved_category,
                involvement_description, is_sensitive, is_anonymous, created_at
            FROM cases
            ORDER BY datetime(created_at) DESC
            """
        )
        rows = cur.fetchall()
        conn.close()

        if not rows:
            st.info("No cases saved yet. Submit a report first on the 'Submit report' page.")
        else:
            df = pd.DataFrame(
                rows,
                columns=[
                    "ID", "Role", "Organisation ID", "Input By", "Date Received", "Date Recorded",
                    "Camp Name", "Camp ID", "Country", "Region", "Town", "Village Name",
                    "Latitude", "Longitude", "Event Date", "Time Range", "Event Location Detail",
                    "Event Type", "Event Subtype", "Affected Status", "Affected Number",
                    "Ethnicity", "Affected Target", "Impact Description", "Affiliation",
                    "Age", "Gender", "Perpetrator Description", "Involved Category",
                    "Involvement_Description", "Sensitive", "Anonymous", "Created At",
                ],
            )

            df["Sensitive"] = df["Sensitive"].map({0: "No", 1: "Yes"})
            df["Anonymous"] = df["Anonymous"].map({0: "No", 1: "Yes"})

            st.markdown(f"Total cases in database: **{len(df)}**")

            col_f1, col_f2, col_f3 = st.columns(3)

            with col_f1:
                countries = ["All"] + sorted(df["Country"].dropna().unique().tolist())
                selected_country_filter = st.selectbox("Filter by country", countries, index=0)

            with col_f2:
                event_types = ["All"] + sorted(df["Event Type"].dropna().unique().tolist())
                selected_event_type_filter = st.selectbox("Filter by event type", event_types, index=0)

            with col_f3:
                hide_sensitive = st.checkbox("Hide sensitive cases", value=False)

            filtered_df = df.copy()

            if selected_country_filter != "All":
                filtered_df = filtered_df[filtered_df["Country"] == selected_country_filter]

            if selected_event_type_filter != "All":
                filtered_df = filtered_df[filtered_df["Event Type"] == selected_event_type_filter]

            if current_role == "Field Worker":
                filtered_df = filtered_df[filtered_df["Sensitive"] == "No"]
                st.info("Sensitive cases are hidden for Field Workers (Do No Harm).")
            else:
                if hide_sensitive:
                    filtered_df = filtered_df[filtered_df["Sensitive"] == "No"]

            st.markdown(f"Showing **{len(filtered_df)}** case(s) after filters.")
            st.dataframe(filtered_df, use_container_width="stretch")

            if not filtered_df.empty:
                st.markdown("### Case details")
                selected_case_id = st.selectbox(
                    "Select a case ID to view full details",
                    options=filtered_df["ID"].tolist(),
                )

                if selected_case_id is not None:
                    conn = get_connection()
                    cur = conn.cursor()
                    cur.execute("SELECT * FROM cases WHERE id = ?", (int(selected_case_id),))
                    detail_row = cur.fetchone()
                    conn.close()

                    if detail_row:
                        # In a real app, you'd map these indices to the columns correctly
                        st.write(detail_row)
                    #----------- DELETE Action start  here -------------#    
                    #---- Functional code - uncomment when necessary ---#
                    #-----April 17 , 2026-------------------------------#
                    #     conn = get_connection()
                    #     # Fetch full record as a DataFrame for easy editing
                    #     df_edit = pd.read_sql_query("SELECT * FROM cases WHERE id = ?", conn, params=(int(selected_case_id),))
                    #     conn.close()

                    # if not df_edit.empty:
                    #     record = df_edit.iloc[0]

                    #     # --- ACTION BUTTON for DELETE ---
                    #     col_edit, col_del = st.columns(2)
                                               
                    #     with col_del:
                    #         if st.button("🗑️ Delete Record", type="primary"):
                    #            st.session_state[f"confirm_delete_{selected_case_id}"] = True
                        
                    #         if st.session_state.get(f"confirm_delete_{selected_case_id}", False):
                    #             st.warning(f"Are you sure you want to permanently delete Case #{selected_case_id}?")
                    #             if st.button("✅ Yes, Confirm Delete"):
                    #                 from db import delete_case
                    #                 delete_case(selected_case_id)
                    #                 del st.session_state[f"confirm_delete_{selected_case_id}"]
                    #                 st.success("Record deleted.")
                    #                 st.rerun()
                    #             if st.button("❌ Cancel"):
                    #                 del st.session_state[f"confirm_delete_{selected_case_id}"]
                    #                 st.rerun()    

                    #-------------  DELETE Action end here ----------#   

            # View Case Based on Analytics (April 19,2026 Update)
            view_cases_page()
            st.markdown("### Export / upload filtered cases")
            if current_role == "Admin":
                export_df = filtered_df.copy()
            else:
                export_df = filtered_df[filtered_df["Sensitive"] == "No"].copy()

            if not export_df.empty:
                csv_data = export_df.to_csv(index=False).encode("utf-8")
                st.download_button("Download CSV", data=csv_data, file_name="export.csv", mime="text/csv")
                
                rdf_data = dataframe_to_rdf(export_df)
                st.download_button("Download RDF (Turtle)", data=rdf_data, file_name="exportRDF.ttl", mime="text/turtle")

                if current_role == "Admin":
                    if st.button("Upload RDF to AllegroGraph"):
                        success, msg = upload_to_allegrograph(rdf_data)
                        if success: st.success(msg)
                        else: st.error(msg)

    # ---------------------------------------------------------
    # PAGE 3: FAIR SPARQL DASHBOARD (CONDITIONAL UI)
    # ---------------------------------------------------------
    if page == "SPARQL dashboard":
        st.title("🛡️ FAIR SPARQL Explorer")
        st.caption("AllegroGraph Knowledge Graph Interface | Aligned with HDS CDM")

        with st.expander("📂 Core Class Ontology (HDS CDM)", expanded=False):
            st.markdown("""
            **Namespace:** `hds: http://example.org/hds#`
            * **hds:Incident**: The central event.
            * **hds:Camp**: Spatial entities linked via `hds:fromLocation`.
            * **hds:Victim**: Linked via `hds:hasVictim`.
            * **hds:Record**: Provenance metadata linked via `hds:reportsOn`.
            """)

        interface_mode = st.radio("Select Discovery Mode", ["Graphical User Interface", "Expert SPARQL Console"], horizontal=True)
        st.divider()

        # Aligned with etl.py namespaces
        PREFIXES = """PREFIX hds: <http://example.org/hds#>
                    PREFIX res: <https://fieldlab1.example.org/resource/>
                    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                    PREFIX dct: <http://purl.org/dc/terms/>
                    PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
                    """

        if interface_mode == "Graphical User Interface":
            st.markdown("### 🌍 Geographic Scope")
            geo_col1, geo_col2 = st.columns(2)
          
            with geo_col1:
                countries = sorted(list(set([l["country"] for l in LOCATION_REGISTRY])))
                sel_country = st.selectbox("Select Country", ["All"] + countries)
            with geo_col2:
                regions = sorted(list(set([l["region"] for l in LOCATION_REGISTRY if sel_country == "All" or l["country"] == sel_country])))
                sel_region = st.selectbox("Select Region", ["All"] + regions)   

            st.markdown("### 📅 Temporal Scope")
            time_col1, time_col2 = st.columns(2)
            with time_col1:
                start_dt = st.date_input("Start Date", value=date(2023, 1, 1))
            with time_col2:
                end_dt = st.date_input("End Date", value=date.today())

            st.markdown("### 🛠️ Data Relationships")
            col_g1, col_g2 = st.columns(2)
            with col_g1:
                included_classes = st.multiselect(
                    "Link Incident with Entities:",
                    ["Location", "Victim", "Perpetrator", "Record"],
                    default=["Location", "Victim"]
                )
            with col_g2:
                limit_val = st.slider("Result Limit", 1, 500, 50)

            # --- DYNAMIC QUERY GENERATION ---
            select_vars = ["?incident", "?eventType", "?date"]
            where_clauses = [
                "  ?incident rdf:type hds:Incident .",
                "  ?incident dct:type ?eventType .",
                "  ?incident dct:date ?date ."
            ]
            
            filter_clauses = [f"  FILTER (?date >= '{start_dt}'^^xsd:date && ?date <= '{end_dt}'^^xsd:date)"]

            if "Location" in included_classes:
                select_vars.append("?campName")
                where_clauses.append("  ?incident hds:fromLocation ?loc .")
                where_clauses.append("  ?loc rdfs:label ?campName .")
                if sel_region != "All":
                    filter_clauses.append(f"  FILTER (?campName = '{sel_region}')")

            if "Victim" in included_classes:
                select_vars.append("?victimDesc")
                where_clauses.append("  OPTIONAL { ?incident hds:hasVictim ?v . ?v hds:description ?victimDesc . }")

            if "Perpetrator" in included_classes:
                select_vars.append("?perpAffiliation")
                where_clauses.append("  OPTIONAL { ?incident hds:hasPerpetrator ?p . ?p hds:description ?perpAffiliation . }")

            if "Record" in included_classes:
                select_vars.append("?recordedAt")
                where_clauses.append("  OPTIONAL { ?rec hds:reportsOn ?incident ; hds:recordedAt ?recordedAt . }")

            query_to_run = (
                f"{PREFIXES}\nSELECT DISTINCT " + " ".join(select_vars) + 
                "\nWHERE {\n" + "\n".join(where_clauses) + "\n" + 
                "\n".join(filter_clauses) + 
                f"\n}}\nORDER BY DESC(?date)\nLIMIT {limit_val}"
            )

            with st.expander("🔍 Inspect FAIR SPARQL (HDS Aligned)"):
                st.code(query_to_run, language="sparql")  

        else:
            st.markdown("### 💻 Expert SPARQL Console")
            default_expert_query = f"""{PREFIXES}
            SELECT ?incident ?eventType ?date ?camp
            WHERE {{
            ?incident rdf:type hds:Incident ;
                        dct:type ?eventType ;
                        dct:date ?date ;
                        hds:fromLocation ?loc .
            ?loc rdfs:label ?camp .
            }}
            ORDER BY DESC(?date)
            LIMIT 25"""
            query_to_run = st.text_area("SPARQL Editor", value=default_expert_query, height=300)
            
        if st.button("▶️ Execute SPARQL Query"):
            try:
                with st.spinner("Querying AllegroGraph..."):
                    resp = requests.get(
                        SPARQL_ENDPOINT,
                        params={"query": query_to_run},
                        auth=(AG_USERNAME, AG_PASSWORD),
                        headers={"Accept": "application/sparql-results+json"},
                        timeout=30
                    )
                
                if resp.status_code == 200:
                    data = resp.json()
                    bindings = data.get("results", {}).get("bindings", [])
                    
                    if not bindings:
                        st.warning("No data found. Ensure you have uploaded RDF data via the 'View Cases' page.")
                    else:
                        cols = list(bindings[0].keys())
                        formatted_rows = [{c: b[c]["value"] for c in cols if c in b} for b in bindings]
                        res_df = pd.DataFrame(formatted_rows)
                        st.subheader(f"Results ({len(res_df)})")
                        st.dataframe(res_df, use_container_width="stretch")
                else:
                    st.error(f"SPARQL Error: {resp.text}")
            except Exception as e:
                st.error(f"Connection Error: {str(e)}")