import os
import requests
import streamlit as st

st.set_page_config(page_title="Tableau + AML POC", layout="wide")

st.title("Tableau Dashboard + AML Pipeline Trigger")

TABLEAU_EMBED_URL = os.getenv("TABLEAU_EMBED_URL", "https://public.tableau.com/views/RegionalSampleWorkbook/Stocks")
BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000")

st.subheader("Dashboard")
st.components.v1.iframe(TABLEAU_EMBED_URL, height=700, scrolling=True)

st.divider()
st.subheader("Upload Dataset")

uploaded_file = st.file_uploader("Choose input dataset", type=["csv", "parquet", "xlsx", "json", "txt"])

if st.button("Upload And Trigger AML Pipeline", type="primary"):
    if not uploaded_file:
        st.error("Please choose a file first.")
    else:
        try:
            files = {
                "file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type or "application/octet-stream")
            }
            response = requests.post(f"{BACKEND_API_URL}/upload-trigger", files=files, timeout=120)
            response.raise_for_status()
            payload = response.json()

            st.success("Pipeline submitted successfully.")
            st.write(f"Job name: `{payload.get('job_name')}`")
            if payload.get("ml_studio_job_url"):
                st.markdown(f"[Open Job In Azure ML Studio]({payload['ml_studio_job_url']})")
        except requests.HTTPError:
            message = response.text if response is not None else "Unknown HTTP error"
            st.error(f"Backend request failed: {message}")
        except Exception as exc:
            st.error(f"Unexpected error: {exc}")

with st.expander("Current config"):
    st.code(
        "\n".join(
            [
                f"TABLEAU_EMBED_URL={TABLEAU_EMBED_URL}",
                f"BACKEND_API_URL={BACKEND_API_URL}",
            ]
        )
    )
