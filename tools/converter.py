from flask import Blueprint, render_template

converter_bp = Blueprint('converter', __name__)


@converter_bp.route('/converter')
def converter():
    return render_template('converter.html')
