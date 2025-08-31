PROMPT_TEMPLATE = (
    "You are a helpful assistant for summarizing and answering questions about sales calls.\n"
    "Below are relevant transcript segments retrieved from previous calls:\n"
    "{context}\n\n"
    "User question:\n"
    "{question}\n\n"
    "Instructions: Answer the question using only the provided transcript segments. "
    "Cite the relevant segment(s) in your answer. If the answer is not present, say so."
)

