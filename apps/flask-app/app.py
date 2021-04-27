from flask import Flask, render_template
import random

app = Flask(__name__)

# list of cat images
images = [
    "https://media.giphy.com/media/BzyTuYCmvSORqs1ABM/giphy.gif",
    "https://media.giphy.com/media/3o6Zt481isNVuQI1l6/giphy.gif",
    "https://media.giphy.com/media/mlvseq9yvZhba/giphy.gif",
    "https://media.giphy.com/media/jpbnoe3UIa8TU8LM13/giphy.gif",
    "https://media.giphy.com/media/13CoXDiaCcCoyk/giphy.gif",
    "https://media.giphy.com/media/8vQSQ3cNXuDGo/giphy.gif",
    "https://media.giphy.com/media/q1MeAPDDMb43K/giphy.gif",
    "https://media.giphy.com/media/tBxyh2hbwMiqc/giphy.gif",
    "https://media.giphy.com/media/33OrjzUFwkwEg/giphy.gif",
    "https://media.giphy.com/media/jTnGaiuxvvDNK/giphy.gif",
    "https://media.giphy.com/media/Z1kpfgtHmpWHS/giphy.gif",
    "https://media.giphy.com/media/cW64pEEZe0YZa/giphy.gif",
    "https://media.giphy.com/media/MxAGWdkQlQdFZbLRTA/giphy.gif",
    "https://media.giphy.com/media/SVYrs1hU0SiAf1nw1n/giphy.gif",
    "https://media.giphy.com/media/QObPo575HQHlGMhbae/giphy.gif"
]

@app.route('/')
def index():
    url = random.choice(images)
    return render_template('index.html', url=url)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
