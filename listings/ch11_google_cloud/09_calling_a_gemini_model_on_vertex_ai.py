from google import genai   # pip install google-genai

client = genai.Client(vertexai=True, project="your-project-id",
                      location="us-central1")

MODEL = "gemini-2.5-flash"   # replace with a current model name from the docs

response = client.models.generate_content(
    model=MODEL,
    contents=("Extract the dataset name, sample size, and evaluation metrics "
              "from this abstract. Answer NOT STATED for anything missing.\n\n"
              + open("abstract.txt").read()),
)
print(response.text)
