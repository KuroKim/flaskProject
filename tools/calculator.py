from flask import Blueprint, render_template

calculator_bp = Blueprint('calculator', __name__)


@calculator_bp.route('/calculator')
def calculator():
    return render_template('calculator.html')
