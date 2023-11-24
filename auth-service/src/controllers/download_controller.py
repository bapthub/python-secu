import flask from Blueprint

download_routes = Blueprint('download_routes', __name__)

### DOWNLOAD CERTIFICATE PAGE
@download_routes.route('/download_certificate/<serial>', methods=['GET'])
def download_certificate(serial):
    file_path = f'certificates_ca/{serial}.pem'
    return send_file(file_path, as_attachment=True)
