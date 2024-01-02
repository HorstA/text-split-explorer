import streamlit as st
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
    Language,
)
import code_snippets as code_snippets
import tiktoken


# Streamlit UI
st.title("Text Splitter Playground")
st.info(
    """Splittet Text in Chunks, verwendet **Langchain Textsplitter**. Parameter:

- `chunk_size`: Maximale Größe der resultierenden Abschnitte (je nach Wahl in Zeichen oder Token)
- `chunk_overlap`: Überschneidung zwischen den resultierenden Chunks (je nach Wahl in Zeichen oder Token)
- `length_function`: Wie man die Länge von Chunks gemessen werden soll, entweder Zeichen oder Token
- Der Typ des Textsplitters, der im Wesentlichen die Trennzeichen steuert, die für die Aufteilung verwendet werden
"""
)
col1, col2, col3, col4 = st.columns([1, 1, 1, 2])

with col1:
    chunk_size = st.number_input(min_value=1, label="Chunk Size", value=1000)

with col2:
    # Setting the max value of chunk_overlap based on chunk_size
    chunk_overlap = st.number_input(
        min_value=1,
        max_value=chunk_size - 1,
        label="Chunk Overlap",
        value=int(chunk_size * 0.2),
    )

    # Display a warning if chunk_overlap is not less than chunk_size
    if chunk_overlap >= chunk_size:
        st.warning("Chunk Overlap muss kleiner Chunk Length sein!")

with col3:
    length_function = st.selectbox("Length Function", ["Characters", "Tokens"])

splitter_choices = ["RecursiveCharacter", "Character"] + [str(v) for v in Language]

with col4:
    splitter_choice = st.selectbox("Select a Text Splitter", splitter_choices)

if length_function == "Characters":
    length_function = len
    length_function_str = code_snippets.CHARACTER_LENGTH
elif length_function == "Tokens":
    enc = tiktoken.get_encoding("cl100k_base")

    def length_function(text: str) -> int:
        return len(enc.encode(text))

    length_function_str = code_snippets.TOKEN_LENGTH
else:
    raise ValueError

if splitter_choice == "Character":
    import_text = code_snippets.CHARACTER.format(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=length_function_str,
    )

elif splitter_choice == "RecursiveCharacter":
    import_text = code_snippets.RECURSIVE_CHARACTER.format(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=length_function_str,
    )

elif "Language." in splitter_choice:
    import_text = code_snippets.LANGUAGE.format(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        language=splitter_choice,
        length_function=length_function_str,
    )
else:
    raise ValueError

# st.info(import_text)

# Box for pasting text
doc = st.text_area("Fügen Sie Ihren Text hier ein:", height=500)

# Split text button
if st.button("Split Text"):
    # Choose splitter
    if splitter_choice == "Character":
        splitter = CharacterTextSplitter(
            separator="\n\n",
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=length_function,
        )
    elif splitter_choice == "RecursiveCharacter":
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=length_function,
        )
    elif "Language." in splitter_choice:
        language = splitter_choice.split(".")[1].lower()
        splitter = RecursiveCharacterTextSplitter.from_language(
            language,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=length_function,
        )
    else:
        raise ValueError
    # Split the text
    splits = splitter.split_text(doc)

    # Display the splits
    for idx, split in enumerate(splits, start=1):
        st.text_area(f"Split {idx}", split, height=200)
