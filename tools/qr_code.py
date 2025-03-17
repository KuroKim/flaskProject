from flask import Blueprint, render_template, request, send_file
import qrcode
import io

qr_code_bp = Blueprint('qr_code', __name__)


@qr_code_bp.route('/qr-code', methods=['GET', 'POST'])
def qr_code():
    qr_image = None
    if request.method == 'POST':
        text = request.form.get('text', '')
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(text)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        return send_file(img_byte_arr, mimetype='image/png', as_attachment=True, download_name='qr_code.png')
    return render_template('qr_code.html', qr_image=qr_image)
