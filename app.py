import streamlit as st
import os
import pandas as pd
import plotly.express as px
from textblob import TextBlob

from src.preprocess_audio import preprocess_audio
from src.transcript import transcribe_audio
from src.segmentation import segment_transcript

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Podcast Intelligence Dashboard",
    layout="wide"
)

st.title("🎙️ Podcast Intelligence Dashboard")

# ---------------- TABS ----------------
tab_upload, tab_sentiment, tab_keywords = st.tabs(
    ["🎧 Audio Upload", "📊 Sentiment", "🔎 Keyword Explorer"]
)

# ---------------- SESSION STATE INIT ----------------
for key in ["cleaned_audio", "transcript_data", "segments"]:
    if key not in st.session_state:
        st.session_state[key] = None

# ================= TAB 1: AUDIO UPLOAD =================
with tab_upload:
    uploaded = st.file_uploader(
        "Upload podcast audio",
        type=["wav", "mp3", "m4a"]
    )

    use_preprocessed = st.checkbox(
        "This audio is already preprocessed (clean, silence removed)"
    )

    if uploaded:
        os.makedirs("audio_raw", exist_ok=True)
        raw_path = f"audio_raw/{uploaded.name}"

        with open(raw_path, "wb") as f:
            f.write(uploaded.getbuffer())

        col1, col2 = st.columns(2)

        # ---------- TRANSCRIPT ----------
        with col1:
            if st.button("📝 Transcript"):
                if use_preprocessed:
                    st.session_state.cleaned_audio = raw_path
                else:
                    with st.spinner("Preprocessing audio..."):
                        st.session_state.cleaned_audio = preprocess_audio(raw_path)

                with st.spinner("Transcribing audio..."):
                    st.session_state.transcript_data = transcribe_audio(
                        st.session_state.cleaned_audio
                    )

                st.success("Transcript generated successfully")

        # ---------- SEGMENTS ----------
        with col2:
            if st.button("🧩 Segments"):
                if st.session_state.transcript_data is None:
                    st.warning("Please generate the transcript first")
                else:
                    with st.spinner("Segmenting transcript..."):
                        st.session_state.segments = segment_transcript(
                            st.session_state.transcript_data
                        )
                    st.success("Segments generated successfully")

    # ---------- DISPLAY AUDIO & TRANSCRIPT ----------
    if st.session_state.cleaned_audio:
        st.subheader("🎧 Preprocessed Audio (Full Length)")
        st.audio(st.session_state.cleaned_audio)

    if st.session_state.transcript_data:
        st.subheader("🧠 Summary")
        st.write(st.session_state.transcript_data["summary"])

        st.subheader("📜 Full Transcript")
        st.text_area(
            "Transcript",
            st.session_state.transcript_data["full_text"],
            height=300
        )

    # ---------- SEGMENTS + KEYWORD SEARCH ----------
    if st.session_state.segments:
        st.subheader("🔍 Search Segments by Keyword")

        search_query = st.text_input(
            "Type a keyword to filter segments"
        ).lower().strip()

        for seg in st.session_state.segments:
            searchable = (
                " ".join(seg["keywords"]) + " " + seg["text"]
            ).lower()

            if not search_query or search_query in searchable:
                with st.expander(
                    f"{seg['topic']} ({int(seg['start'])}s – {int(seg['end'])}s)"
                ):
                    st.markdown("**Keywords:**")
                    st.write(", ".join(seg["keywords"]))

                    st.markdown("**Segment Text:**")
                    st.write(seg["text"])

# ================= TAB 2: SENTIMENT =================
with tab_sentiment:
    if not st.session_state.segments:
        st.info("Generate segments to view sentiment analysis")
    else:
        st.subheader("📊 Segment Sentiment Analysis")

        for seg in st.session_state.segments:
            polarity = TextBlob(seg["text"]).sentiment.polarity

            if polarity > 0.1:
                dot = "🟢"
            elif polarity < -0.1:
                dot = "🔴"
            else:
                dot = "🟡"

            with st.expander(
                f"{seg['topic']} ({int(seg['start'])}s – {int(seg['end'])}s) {dot}"
            ):
                st.markdown("**Keywords:**")
                st.write(", ".join(seg["keywords"]))

                st.markdown("**Segment Text:**")
                st.write(seg["text"])

# ================= TAB 3: KEYWORD EXPLORER =================
with tab_keywords:
    if not st.session_state.segments:
        st.info("Generate segments to explore keywords")
    else:
        st.subheader("🔎 Keyword Explorer")

        # Aggregate keyword frequencies across segments
        keyword_counts = {}
        for seg in st.session_state.segments:
            for kw in seg["keywords"]:
                keyword_counts[kw] = keyword_counts.get(kw, 0) + 1

        df = pd.DataFrame(
            [{"keyword": k, "count": v} for k, v in keyword_counts.items()]
        ).sort_values("count", ascending=False)

        # ---- BAR CHART (FINAL CHOICE) ----
        fig = px.bar(
            df,
            x="count",
            y="keyword",
            orientation="h",
            title="Keyword Frequency Across Segments"
        )

        fig.update_layout(
            xaxis_title="Number of Segments",
            yaxis_title="Keyword",
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)
