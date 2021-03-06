# -*- coding: utf-8 -*-
"""
PyThaiNLP Demo Online
V 0.1
พัฒนาโดย นาย วรรณพงษ์  ภัททิยไพบูลย์
"""
import logging
from flask import Flask, render_template, abort, request,jsonify
from pythainlp.tokenize import word_tokenize
from pythainlp.tokenize import tcc
#from pythainlp.word_vector import thai2vec
from pythainlp.tag import pos_tag
from pythainlp.sentiment import sentiment
from pythainlp.soundex import LK82,Udom83
import json
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', name='Home')

@app.route('/word_tokenizer')
def word_tokenizer_web():
    return render_template('word_tokenizer.html', name='Word tokenizer')

@app.route('/pos_tag')
def pos_tag_web():
    return render_template('pos_tag.html', name='POS Tag')

@app.route('/thai2vec')
def thai2vec_web():
    return render_template('thai2vec.html', name='Thai2Vec')

@app.route('/soundex')
def soundex_web():
    return render_template('soundex.html', name='Soundex')

@app.route('/tcc')
def tcc_web():
    return render_template('tcc.html', name='TCC')

@app.route('/about')
def about_web():
    return render_template('about.html', name='About')

@app.route('/api/word_tokenizer', methods=["GET"])
def word_tokenizer_api():
	txt=""
	try:
		sent = request.args.get('sent', 0, type=str)
		engine = request.args.get('engine', 0, type=str)
		txt='|'.join(word_tokenize(sent,engine)).replace('|<|br|>|','<br>').replace('<|br|>','<br>')
	except:
		txt="Error"
	return jsonify(result=txt)

@app.route('/api/tcc', methods=["GET"])
def tcc_api():
	sent = request.args.get('sent', 0, type=str)
	txt=""
	for i in sent.split('<br>'):
		txt+=tcc.tcc(i)+"<br>"
	return jsonify(result=txt)

@app.route('/api/pos_tag', methods=["GET"])
def pos_tag_api():
	sent = request.args.get('sent', 0, type=str)
	txt=""
	for i in sent.split('<br>'):
		txt+=" ".join("%s/%s" % tup for tup in pos_tag(word_tokenize(i),engine='artagger'))+"<br>"
	return jsonify(result=txt)

@app.route('/api/soundex', methods=["GET"])
def soundex_api():
	sent = request.args.get('sent', 0, type=str)
	txt=""
	for i in sent.split('<br>'):
		txt+="<b>Word : </b>"+i+"<br><p>กฎการเข้ารหัสซาวน์เด็กซ์ของ วิชิตหล่อจีระชุณห์กุล และ เจริญ คุวินทร์พันธุ์ - LK82 : "+LK82(i)+"<br>กฎการเข้ารหัสซาวน์เด็กซ์ของ วรรณี อุดมพาณิชย์ - Udom83 : "+Udom83(i)+"</p><br>"
	return jsonify(result=txt)

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500

@app.errorhandler(404)
def not_found(e):
	return "404 NOT FOUND"


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)