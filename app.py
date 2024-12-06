from flask import Flask, request
import subprocess
import json

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def get_video_data():
    # クエリパラメータからvideoidを取得
    videoid = request.args.get('v')
    if not videoid:
        return "Video ID is required", 400
    
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
                return "No formatStreams found in the response", 500
        else:
            # curlコマンドのエラー
            return f"Failed to fetch data: {result.stderr}", 500
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True)
