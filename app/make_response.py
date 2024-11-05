from app import app
import json
def make_response(text):
    if isinstance(text, (str, int, float)):
        text = {"responce": text}

    json_text = json.dumps(text,
                           sort_keys=True, indent=4,  ensure_ascii=False)

    # Подготовить ответ
    result = app.response_class(
        response=f"{json_text}",
        status=200,
        mimetype="application/json; charset=utf-8"
    )

    return result


def make_error(text, error: int):
    if isinstance(text, (str, int, float)):
        text = {"error": text}

    json_text = json.dumps(text,
                           sort_keys=True, indent=4,  ensure_ascii=False)

    # Подготовить ответ
    result = app.response_class(
        response=f"{json_text}",
        status=error,
        mimetype="application/json; charset=utf-8"
    )

    return result
