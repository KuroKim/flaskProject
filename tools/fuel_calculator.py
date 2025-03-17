from flask import Blueprint, render_template

fuel_calculator_bp = Blueprint('fuel_calculator', __name__)


@fuel_calculator_bp.route('/fuel-calculator')
def fuel_calculator():
    return render_template('fuel_calculator.html')
