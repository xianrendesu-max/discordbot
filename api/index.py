from flask import Flask, jsonify, request
from discord_interactions import verify_key_signature, InteractionType, InteractionResponseType

app = Flask(__name__)

# Discord Developer Portalで取得する
PUBLIC_KEY = 'YOUR_DISCORD_PUBLIC_KEY' 

@app.route('/', methods=['POST'])
def interactions():
    # 署名の検証（Discordからの正規のリクエストか確認）
    signature = request.headers.get('X-Signature-Ed25519')
    timestamp = request.headers.get('X-Signature-Timestamp')
    if signature is None or timestamp is None or not verify_key_signature(PUBLIC_KEY, request.data, signature, timestamp):
        return 'Invalid request signature', 401

    # リクエストデータの解析
    interaction = request.json

    # 1. PING (Discord側との接続確認用)
    if interaction.get('type') == InteractionType.PING:
        return jsonify({
            'type': InteractionResponseType.PONG
        })

    # 2. APPLICATION_COMMAND (スラッシュコマンドなど)
    if interaction.get('type') == InteractionType.APPLICATION_COMMAND:
        command_name = interaction.get('data').get('name')

        if command_name == 'hello':
            return jsonify({
                'type': InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                'data': {
                    'content': 'こんにちは！Vercelから返信しています。'
                }
            })

    return jsonify({'type': InteractionResponseType.PONG})

# Vercel用ハンドラー
def handler(request):
    return app(request)
