from flask import Blueprint, render_template

pressure_converter_bp = Blueprint('pressure_converter', __name__)


@pressure_converter_bp.route('/pressure_converter')
def pressure_converter():
    return render_template('pressure_converter.html')
