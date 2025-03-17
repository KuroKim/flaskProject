from flask import Blueprint, render_template

timer_bp = Blueprint('timer', __name__)


@timer_bp.route('/timer')
def timer():
    return render_template('timer.html')
