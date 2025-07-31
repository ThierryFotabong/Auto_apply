import groq
from config import GROQ_API_KEY

client = groq.Groq(api_key=GROQ_API_KEY)

def tailor_resume_for_job(base_resume: str, job_description: str) -> str:
    prompt = (
        "You are a world class professional resume writer with experts in ATS resume creatiom. "
        "Rewrite the following base resume to best match the job description provided. "
        "Highlight the skills and experiences from the resume that are most relevant to the job. "
        "\n\nBase Resume:\n" + base_resume +
        "\n\nJob Description:\n" + job_description +
        "\n\nRewritten Resume:"
    )
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1024,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"