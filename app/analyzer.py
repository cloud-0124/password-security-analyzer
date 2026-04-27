import re

def analyze_password(password: str):
    score = 0
    feedback = []

    # 길이 체크
    if len(password) >= 8:
        score += 25
    else:
        feedback.append("비밀번호 길이가 8자 이상이어야 합니다.")

    # 대문자
    if re.search(r"[A-Z]", password):
        score += 25
    else:
        feedback.append("대문자를 포함하세요.")

    # 숫자
    if re.search(r"[0-9]", password):
        score += 25
    else:
        feedback.append("숫자를 포함하세요.")

    # 특수문자
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 25
    else:
        feedback.append("특수문자를 포함하세요.")

    # 등급
    if score >= 75:
        level = "strong"
    elif score >= 50:
        level = "medium"
    else:
        level = "weak"

    return {
        "score": score,
        "level": level,
        "feedback": feedback
    }
