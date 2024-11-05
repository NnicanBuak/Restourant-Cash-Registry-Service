from flask import jsonify


def make_response(text):
    from . import app

    if isinstance(text, (str, int, float)):
        text = {"responce": text}

    json_text = jsonify(text)

    # Подготовить ответ
    result = app.response_class(
        response=f"{json_text.json}", status=200, mimetype="application/json; charset=utf-8"
    )

    return result


def make_error(text, error: int):
    from . import app
    if isinstance(text, (str, int, float)):
        text = {"error": text}

    json_text = jsonify(text)

    # Подготовить ответ
    result = app.response_class(
        response=f"{json_text.json}",
        status=error,
        mimetype="application/json; charset=utf-8",
    )

    return result
