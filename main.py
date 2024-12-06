from flask import Flask, request, jsonify
import subprocess
import json

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def get_video_data():
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
            # エラーが発生した場合
            return jsonify({'error': f"Failed to fetch data: {result.stderr}"}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
