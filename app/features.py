import math
import re
from collections import Counter


SPECIAL_PATTERN = re.compile(r"[^A-Za-z0-9]")


FEATURE_NAMES = [
    "length",
    "lowercase_count",
    "uppercase_count",
    "digit_count",
    "special_count",
    "unique_char_count",
    "entropy",
]


def password_features(password: str) -> list[float]:
    length = len(password)
    counts = Counter(password)
    entropy = 0.0

    if length:
        for count in counts.values():
            probability = count / length
            entropy -= probability * math.log2(probability)

    return [
        float(length),
        float(sum(char.islower() for char in password)),
        float(sum(char.isupper() for char in password)),
        float(sum(char.isdigit() for char in password)),
        float(len(SPECIAL_PATTERN.findall(password))),
        float(len(counts)),
        float(entropy),
    ]
