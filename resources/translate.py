from flask_restful import Resource
from googletrans import Translator, constants

class translate_util:
    def get_code_list(self):
        return constants.LANGUAGES

class Translate(Resource):

  def get(self, word, language):

    if len(language) > 2:
        for l in constants.LANGUAGES:
            if constants.LANGUAGES[l] == language:
                language = l
                break


    translator = Translator()
    detection = translator.detect(word)
    language_code = detection.lang
    try:
        translation = translator.translate(word,dest=language)
    except:
        return "Cannot translate",200
    return {
            "original word: " : word,
            "translated word: " : translation.text,
            "original language: " : constants.LANGUAGES[language_code],
            "translated language: " : constants.LANGUAGES[language]
            }, 200