# WhisperChainAI MVP - Streamlit Web UI Version (with Export to JSON + Real OpenAI Support)

import streamlit as st
import json
import os
from typing import List

# Optional: Use OpenAI if key is set
def ask_whisperchainai(question: str) -> str:
    try:
        import openai
        openai.api_key = os.getenv("OPENAI_API_KEY")
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are WhisperChainAI, an assistant that helps teams recall past decisions, reasoning, and tribal knowledge."},
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message.content
    except Exception:
        # Fallback simulated response
        if "stockout" in question.lower():
            return "You usually delay reorders by 14 days post-sale dip."
        elif "october" in question.lower():
            return "A 15% markdown is applied by the third week of October."
        elif "sla" in question.lower() or "vendor" in question.lower():
            return "Escalation occurs if the delay exceeds 4 days."
        elif "black friday" in question.lower():
            return "Reorders typically increase by 30% two weeks prior to Black Friday."
        else:
            return "Sorry, I couldn't find a relevant memory. Try rephrasing your question."

# Initialize session state for memory cards
if "example_cards" not in st.session_state:
    st.session_state.example_cards = [
        {"title": "Stockout Policy - Q3", "summary": "Delay reorders by 14 days post-sale dip.", "tags": ["#inventory", "#q3"]},
        {"title": "Markdown Strategy October", "summary": "Applied 15% discount by week 3.", "tags": ["#sales", "#promo"]},
        {"title": "Vendor SLA Escalation Rule", "summary": "Escalate to ops if delay > 4 days.", "tags": ["#supplychain", "#sla"]}
    ]

st.title("🧠 WhisperChainAI")
st.subheader("Unlock your team's tribal knowledge using AI")

query = st.text_input("Ask WhisperChainAI a question")

if query:
    answer = ask_whisperchainai(query)
    st.markdown("### 💬 Memory Recall")
    st.success(answer)

    if st.checkbox("Save this as a Memory Card"):
        title = st.text_input("Memory Card Title")
        tags_input = st.text_input("Tags (comma-separated)")
        if st.button("Save Memory Card") and title:
            tags = [f"#{tag.strip()}" for tag in tags_input.split(',') if tag.strip()]
            st.session_state.example_cards.append({"title": title, "summary": answer, "tags": tags})
            st.success("Memory Card saved!")

# Export Memory Cards
st.markdown("## 📁 Export Memory Cards")
if st.button("Download as JSON"):
    json_data = json.dumps(st.session_state.example_cards, indent=2)
    st.download_button(
        label="Download Memory Cards",
        data=json_data,
        file_name="whisperchainai_memory_cards.json",
        mime="application/json"
    )

# Display Memory Cards
st.markdown("## 📚 Memory Cards")
for card in st.session_state.example_cards:
    st.markdown(f"### {card['title']}")
    st.markdown(card['summary'])
    st.markdown("Tags: " + " ".join(card['tags']))
    st.markdown("---")
