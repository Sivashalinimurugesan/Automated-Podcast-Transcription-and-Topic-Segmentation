!pip install pandas gTTS
import pandas as pd
from gtts import gTTS

df = pd.read_csv("cs_students.csv")

for _, row in df.iterrows():
    text = (
        f"For {row['Name']}, with interest in {row['Interested Domain']} "
        f"and GPA {row['GPA']}, the future career is {row['Future Career']}."
    )
    tts = gTTS(text=text, lang='en')
    filename = f"student_{row['Student ID']}.mp3"
    tts.save(filename)

print("Audio files generated successfully!")
