import re

from flask import Flask, render_template, request

app = Flask(__name__)

positive_words = {
    "good", "great", "love", "loved", "amazing", "best",
    "excellent", "fantastic", "wonderful", "awesome", "happy",
    "enjoy", "enjoyed", "nice", "perfect", "impressive",
    "pleasant", "delicious", "satisfied",
}

negative_words = {
    "bad", "awful", "hate", "hated", "worst", "sad",
    "terrible", "horrible", "poor", "boring", "disappointing",
    "disappointed", "unpleasant", "frustrating", "frustrated",
    "angry", "unhappy", "annoying", "uncomfortable", "disgusting",
}


@app.route("/", methods=["GET", "POST"])
def index():
    text = ""
    result = None
    positive_count = 0
    negative_count = 0
    positive_percent = None
    negative_percent = None

    if request.method == "POST":
        text = request.form.get("review", "").strip()

        if text:
            for negation, word in re.findall(
                r"\b(?:(not)\s+(?:very\s+)?)?([a-z]+)\b", text.lower()
            ):
                if word in positive_words:
                    is_positive = not negation
                elif word in negative_words:
                    is_positive = bool(negation)
                else:
                    continue

                if is_positive:
                    positive_count += 1
                else:
                    negative_count += 1

            if positive_count > negative_count:
                result = "POSITIVE"
            elif negative_count > positive_count:
                result = "NEGATIVE"
            else:
                result = "UNKNOWN"

            matched_count = positive_count + negative_count
            if matched_count:
                positive_percent = round(100 * positive_count / matched_count, 1)
                negative_percent = round(100 - positive_percent, 1)

    return render_template(
        "index.html",
        text=text,
        result=result,
        positive_count=positive_count,
        negative_count=negative_count,
        positive_percent=positive_percent,
        negative_percent=negative_percent,
    )


if __name__ == "__main__":
    app.run()