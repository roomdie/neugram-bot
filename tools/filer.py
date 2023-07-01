
def read_txt(path: str, encoding="utf-8"):
    with open("bot/data/text/{}.txt".format(path), "r", encoding=encoding) as file:
        text = file.read()
    return text
