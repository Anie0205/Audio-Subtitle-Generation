from deep_translator import GoogleTranslator

def translate_text(text, target_language):
    translated = GoogleTranslator(source='auto', target=target_language).translate(text)
    return translated

# Example usage
#print(translate_text("Hello, how are you?", target_language="fr"))
