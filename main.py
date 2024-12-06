from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import json

app = Flask(__name__)
CORS(app)

@app.route('/apis', methods=['GET'])
def get_video_data_apisan():
    # クエリパラメータからvideoidを取得
    videoid = request.args.get('v')
    if not videoid:
        return jsonify({'error': 'Video ID is required'}), 400
    
    try:
        # curlコマンドを使って、外部APIからデータを取得
        url = f"https://thingproxy.freeboard.io/fetch/https://inv.nadeko.net/api/v1/videos/{videoid}"
        result = subprocess.run(["curl", url], capture_output=True, text=True)
        
        if result.returncode == 0:
            # JSONデータを解析
            data = json.loads(result.stdout)

            # formatStreamsの中にあるリンクだけを抽出
            if 'formatStreams' in data:
                links = [stream.get('url') for stream in data['formatStreams'] if 'url' in stream]
                
                # リンクを改行で区切って表示
                return '\n'.join(links)
            else:
                return jsonify({'error': "No formatStreams found in the response"}), 500
        else:
            # curlコマンドのエラー
            return jsonify({'error': f"Failed to fetch data: {result.stderr}"}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api', methods=['GET'])
def get_video_data_api():
    # クエリパラメータからvideoidを取得
    videoid = request.args.get('v')
    if not videoid:
        return jsonify({'error': 'Video ID is required'}), 400
    
    try:
        # curlコマンドを使って、外部APIからデータを取得
        url = f"https://thingproxy.freeboard.io/fetch/https://inv.nadeko.net/api/v1/videos/{videoid}"
        result = subprocess.run(["curl", url], capture_output=True, text=True)
        
        if result.returncode == 0:
            # 取得したJSONデータをレスポンスとして返す
            return jsonify(json.loads(result.stdout))
        else:
            # curlコマンドのエラー
            return jsonify({'error': f"Failed to fetch data: {result.stderr}"}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

