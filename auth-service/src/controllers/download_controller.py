from flask import Blueprint,send_file

download_controller = Blueprint('download_controller', __name__)

### DOWNLOAD CERTIFICATE PAGE
@download_controller.route('/download_certificate/<serial>', methods=['GET'])
def download_certificate(serial):
    file_path = f'certificates_ca/{serial}.pem'
    return send_file(file_path, as_attachment=True)
