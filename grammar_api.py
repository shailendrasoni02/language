from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import language_tool_python

app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load LanguageTool for English
tool = language_tool_python.LanguageTool('en-US')

@app.get("/check")
def check_grammar(text: str):
    matches = tool.check(text)
    corrected_text = text
    for match in reversed(matches):  # Reverse so replacements don't shift indices
        corrected_text = (
            corrected_text[: match.offset]
            + match.replacements[0] if match.replacements else match.context
            + corrected_text[match.offset + match.errorLength :]
        )
    return {"original": text, "corrected": corrected_text}

# Run the server with: uvicorn grammar_api:app --reload
