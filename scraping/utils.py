import ahocorasick


def build_automation(words: list[str]) -> ahocorasick.Automaton:
    """
    Создает и возвращает автомат для поиска списка слов в тексте
    """
    automation = ahocorasick.Automaton()
    for word in words:
        automation.add_word(word.lower(), word.lower())
    automation.make_automaton()
    return automation