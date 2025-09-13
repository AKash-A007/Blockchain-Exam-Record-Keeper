from blockchain import Blockchain
import hashlib
import json
import time
from flask import Flask, request, jsonify
import os
USE_REDIS = os.environ.get('USE_REDIS', 'false').lower() in ('1', 'true', 'yes')
if USE_REDIS:
    try:
        from redis import Redis
        redis_host = os.environ.get('REDIS_HOST', 'redis')
        redis_port = int(os.environ.get('REDIS_PORT', 6379))
        redis_client = Redis(host=redis_host, port=redis_port, decode_responses=True)
    except Exception as e:
        print('Redis import/connection failed:', e)
        USE_REDIS = False

blockchain = Blockchain()
app = Flask(__name__)


@app.route('/')
def home():
    return "Blockchain Student Record Keeper is running!"


@app.route('/chain', methods=['GET'])
def get_chain():
    # caching example
    if USE_REDIS:
        cached = redis_client.get('full_chain')
        if cached:
            return jsonify({'chain': json.loads(cached), 'cached': True})
    data = blockchain.to_list()
    if USE_REDIS:
        redis_client.set('full_chain', json.dumps(data), ex=10)
    return jsonify({'chain': data, 'length': len(data)})


@app.route('/add_mark', methods=['POST'])
def add_mark():
    payload = request.get_json()
    if not payload:
        return jsonify({'error': 'JSON payload required'}), 400
    required = ('student_id', 'name', 'subject', 'marks')
    if not all(k in payload for k in required):
        return jsonify({'error': f'required fields: {required}'}), 400
    record = {
        'student_id': payload['student_id'],
        'name': payload['name'],
        'subject': payload['subject'],
        'marks': int(payload['marks'])
    }
    new_block = blockchain.add_block(record)
    # invalidate cache
    if USE_REDIS:
        redis_client.delete('full_chain')
        redis_client.delete(f'student:{record["student_id"]}')
    return jsonify({'status': 'ok', 'block': new_block.to_dict()}), 201


@app.route('/student/<student_id>', methods=['GET'])
def get_student(student_id):
    if USE_REDIS:
        cached = redis_client.get(f'student:{student_id}')
        if cached:
            return jsonify({'records': json.loads(cached), 'cached': True})
    recs = blockchain.get_student_records(student_id)
    if USE_REDIS:
        redis_client.set(f'student:{student_id}', json.dumps(recs), ex=30)
    return jsonify({'records': recs})


@app.route('/verify', methods=['GET'])
def verify():
    valid = blockchain.is_valid()
    return jsonify({'valid': valid})


@app.route('/block/<int:index>', methods=['GET'])
def get_block(index):
    if 0 <= index < len(blockchain.chain):
        return jsonify(blockchain.chain[index].to_dict())
    return jsonify({'error': 'block not found'}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)