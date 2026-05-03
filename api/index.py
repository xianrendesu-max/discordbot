import json
from flask import Flask, jsonify, request
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

app = Flask(__name__)

# Discord Developer Portalの「General Information」にある「PUBLIC KEY」をここに入れる
PUBLIC_KEY = 'de10cfc414839d0915d74c7d1b7ecc3de10104b1dc703a74b6829c5006a9a12e'

def verify_signature(request):
    signature = request.headers.get('X-Signature-Ed25519')
    timestamp = request.headers.get('X-Signature-Timestamp')
    body = request.data.decode('utf-8')

    if not signature or not timestamp:
        return False

    verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))
    try:
        verify_key.verify(f'{timestamp}{body}'.encode(), bytes.fromhex(signature))
        return True
    except BadSignatureError:
        return False

@app.route('/', methods=['POST'])
def interactions():
    # 署名検証
    if not verify_signature(request):
        return 'Invalid request signature', 401

    data = request.json
    
    # 1. PING (Discordとの接続確認)
    if data.get('type') == 1:
        return jsonify({'type': 1})

    # 2. APPLICATION_COMMAND (スラッシュコマンド)
    if data.get('type') == 2:
        command_name = data.get('data', {}).get('name')

        if command_name == 'hello':
            return jsonify({
                'type': 4,
                'data': {
                    'content': 'こんにちは仙人botです。色々なことができます'
                }
            })

    return jsonify({'type': 1})

# Vercel用
def handler(request):
    return app(request)
