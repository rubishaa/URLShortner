from datetime import datetime
from livecode.models import *
from livecode import app, models
from random import choice
import string
from flask import render_template, request, flash, redirect, url_for


shortid = ""
def generate_short_id(num_of_chars: int):
    """Function to generate short_id of specified number of characters"""
    return ''.join(choice(string.ascii_letters+string.digits) for _ in range(num_of_chars))


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        short_id = request.form['custom_id']
        shortid = short_id
        if short_id and ShortUrls.query.filter_by(short_id=short_id).first() is not None:
            flash('Please enter different custom id!')
            return redirect(url_for('index'))

        if not url:
            flash('The URL is required!')
            return redirect(url_for('index'))

        if not short_id:
            short_id = generate_short_id(8)
        models.insert_shorturl(url, short_id)
        short_url = request.host_url + short_id
        return render_template('index.html', short_url=short_url)

    return render_template('index.html')

@app.route('/<short_id>')
def redirect_url(short_id):
    link = models.get_url(str(short_id))
    if link:
        return redirect(link.longurl)
    else:
        flash('Invalid URL')
        return redirect(url_for('index'))