from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/', methods=['GET'])
def copy_site():
    target_url = request.args.get('url')
    if not target_url:
        return jsonify({'error': 'Missing "url" parameter'}), 400

    api_url = 'https://copier.saveweb2zip.com/api/copySite'
    payload = {
        'url': target_url,
        'renameAssets': False,
        'saveStructure': False,
        'alternativeAlgorithm': False,
        'mobileVersion': False
    }

    headers = {
        'Content-Type': 'application/json',
        'Origin': 'https://saveweb2zip.com',
        'Referer': 'https://saveweb2zip.com/',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36'
    }

    response = requests.post(api_url, json=payload, headers=headers)
    data = response.json()

    if not data or 'md5' not in data:
        return jsonify({'error': 'Failed to get md5', 'response': data}), 500

    md5 = data['md5']
    download_url = f"https://copier.saveweb2zip.com/api/downloadArchive/{md5}"

    return jsonify({
        'success': True,
        'download': download_url
    })

# For local run
if __name__ == '__main__':
    app.run(debug=True)
