from typing import List


def create_tags(file_name: str) -> List[str]:
    """Возвращает список тегов на основе наименования файла.
    Разделяет теги по пробелу и нижнему подчеркиванию.
    """
    tags = []
    for by_space in file_name.split(" "):
        for by_underline in by_space.split("_"):
            tags.append(by_underline)

    tags = format_tags(tags)

    return tags


def format_tags(tags: List[str]) -> List[str]:
    """Форматирует теги, сливая значение и величину"""
    enriched_tags = []

    for i in range(len(tags)):
        if tags[i].lower() == "ггц" and i != 0 and is_float(tags[i - 1]):
            enriched_tags.pop()
            enriched_tags.append(f"#{tags[i - 1]}_{tags[i]}")
        elif tags[i].lower() == "гц" and i != 0 and is_float(tags[i - 1]):
            enriched_tags.pop()
            enriched_tags.append(f"#{tags[i - 1]}_{tags[i]}")
        elif tags[i].lower() == "дб" and i != 0 and is_float(tags[i - 1]):
            enriched_tags.pop()
            enriched_tags.append(f"#{tags[i - 1]}_{tags[i]}")
        else:
            enriched_tags.append(f"#{tags[i]}")

    return enriched_tags


def is_float(s: str) -> bool:
    """Проверяет переводимости строки в число"""
    try:
        float(s)
        return True
    except ValueError:
        return False
