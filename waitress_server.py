from waitress import serve
import app #main은 flask app을 작성한 py파일입니다.
print('running art api server')
serve(app.app, host='0.0.0.0', port=5555,threads= 4)