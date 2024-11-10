import google.generativeai as genai
from groq import Groq


def translate_text_Gemini(text, target_language):
    """
    Translates the given text to the specified target language using Google's Gemini model.

    Parameters:
    - text (str): The text to translate.
    - target_language (str): The target language for translation.

    Returns:
    - str: The translated text.
    """
    # Initialize the Gemini API with the API key
    genai.configure(api_key="API KEY")  # Your actual API key
    
    # Create a GenerativeModel instance with the specified model
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Prepare the prompt for translation
    prompt = f"Translate the following text to {target_language}: '{text}'"

    # Generate content using the Gemini model
    response = model.generate_content(prompt)

    # Print the translated text
    #print("Response from Gemini:", response.text)

    # Return the translated text
    return response.text

def translate_text_Llama3(text, target_language):
    """
    Translates the given text to the specified target language using Groq's model.

    Parameters:
    - text (str): The text to translate.
    - target_language (str): The target language for translation.

    Returns:
    - str: The translated text.
    """
    client = Groq(api_key="API KEY")
    # Prepare the prompt for translation
    prompt = f"Translate the following text to {target_language}: '{text}' and do not explain your translation, just give the translated text."

    # Create a completion using Groq's chat model (assuming `llama3-8b-8192` can perform translation tasks)
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    # Collect the translated text from the response stream
    translated_text = ""
    for chunk in completion:
        translated_text += chunk.choices[0].delta.content or ""

    return translated_text


#translated = translate_text_Llama3("Hello, how are you?", "German")
#print("Translated text:", translated)

# Example usage: Pass the text you want to translate
#transcription_text = "Hello, how are you?"
#translated_text = translate_text(transcription_text, target_language="German")
#print("Translated Text:", translated_text)

