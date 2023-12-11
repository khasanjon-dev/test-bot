def keys_serializer(text: str):
    if text.isalnum():
        res = ''
        for letter in text:
            if letter.isalpha():
                res += letter
        return res
    return text
