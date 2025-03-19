import streamlit as st
import json
from datetime import datetime
from pytz import timezone

# Function to convert UTC timestamp to PDT
def convert_to_pdt(timestamp):
    try:
        utc_time = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f%z")
        pdt_time = utc_time.astimezone(timezone('US/Pacific'))
        return pdt_time.strftime("%-m/%-d/%y %H:%M %Z")
    except ValueError:
        return "Invalid Timestamp"

# Function to convert bytes to readable formats (Bytes, KB, or MB)
def convert_bytes(value):
    try:
        if value < 1024:
            return f"{value} B"
        kb_value = value // 1024
        if kb_value > 9999:  # Convert to MB if KB > 9999
            return f"{kb_value // 1024} MB"
        else:
            return f"{kb_value} KB"
    except (TypeError, ValueError):
        return "N/A"

# Function to check if the user agent is a web browser
def is_browser_user_agent(user_agent):
    browser_keywords = ["Mozilla", "Chrome", "Safari", "Firefox", "Edge"]
    return any(keyword in user_agent for keyword in browser_keywords)

# Streamlit app
st.title("Interactive JSON Viewer")

# Text area for JSON input with auto-processing
st.subheader("Input JSON Data")
json_input = st.text_area("Paste your JSON data here:", height=200)

# Parse and process JSON data
if json_input:
    try:
        # Parse the input JSON
        data = json.loads(json_input)

        # Convert the timestamp to PDT
        formatted_timestamp = convert_to_pdt(data.get('timestamp', 'N/A'))

        # Prepare fields
        all_fields = {
            "Hostname": data.get('http', {}).get('hostname', 'N/A'),
            "HTTP User Agent": None if is_browser_user_agent(data.get('http', {}).get('http_user_agent', '')) else data.get('http', {}).get('http_user_agent', 'N/A'),
            "URL": None if data.get('http', {}).get('url', '/') == "/" else data.get('http', {}).get('url', 'N/A'),
            "Source IP": data.get('src_ip', 'N/A'),
            "Dest IP": data.get('dest_ip', 'N/A'),
            "Source Port": data.get('src_port', 'N/A'),
            "Dest Port": data.get('dest_port', 'N/A'),
            "Bytes to Client": convert_bytes(data.get('flow', {}).get('bytes_toclient', 0)),
            "Bytes to Server": convert_bytes(data.get('flow', {}).get('bytes_toserver', 0)),
            "Signature": data.get('alert', {}).get('signature', 'N/A'),
            "Category": data.get('alert', {}).get('category', 'N/A'),
            "MITRE Technique Name": data.get('alert', {}).get('metadata', {}).get('mitre_technique_name', ['N/A'])[0],
            "Application Protocol": None if data.get('app_proto', 'http') == "http" else data.get('app_proto', 'N/A')
        }

        # Automatically select only fields with valid values (not None or N/A)
        default_fields = [field for field, value in all_fields.items() if value not in (None, 'N/A')]

        # Display field selection
        st.subheader("Choose Additional Fields to Display")
        fields_to_display = st.multiselect(
            "Select fields:",
            list(all_fields.keys()),
            default=default_fields
        )

        # Display values
        st.subheader("Field Values")
        st.markdown(f"- **Agent Host:** ____")  # Placeholder for actual data
        st.markdown(f"- **Timestamp:** {formatted_timestamp}")

        # Render selected fields in order
        for field in fields_to_display:
            st.markdown(f"- **{field}:** {all_fields[field]}")

    except json.JSONDecodeError:
        st.error("Invalid JSON! Please check your input.")
else:
    st.info("Awaiting JSON input...")