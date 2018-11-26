from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

import spacy

nlp = spacy.load('en_core_web_sm')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/parse')
def parse():
    query = request.args.get('query')
    doc = nlp(query)

    noun_chunk_tokens = [chunk.root for chunk in doc.noun_chunks]
    js_tokens = []
    for token in doc:
        js_tokens  += [{
            'id': token.i,
            'text': token.text,
            'pos': token.pos_,
            'headId': token.head.i,
            'dep': token.dep_,
            'nounChunkHead': token in noun_chunk_tokens,
            'collapsedText': ' '.join([token.text for token in token.subtree]),
            'childIds': [child.i for child in token.children]
        }]
    return jsonify(js_tokens)

if __name__ == "__main__":
    app.run()
