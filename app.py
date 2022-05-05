import json
import os
import random

from flask import Flask, send_from_directory, request
from run_case import run_case

app = Flask(__name__)

app.static_folder = './cases/'


@app.route('/case')
def case():
    case_name = '{:04d}.json'.format(int(random.random() * 86))

    return send_from_directory(app.static_folder, case_name, cache_timeout=0)


@app.route('/solve', methods=['GET', 'POST'])
def solve():
    # need posted data here
    res = run_case(os.environ["USV_EXECUTABLE"], request.json)
    return json.dumps(res)
