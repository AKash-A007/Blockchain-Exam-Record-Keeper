from block import Block
import os
import json
import time
import shutil

CHAIN_FILE = os.environ.get('CHAIN_FILE', 'chain.json')

class Blockchain:
    def __init__(self):
        self._ensure_chain_file_is_file()  # Check if it's a directory first
        self.chain = []
        
        if os.path.exists(CHAIN_FILE) and os.path.isfile(CHAIN_FILE):
            try:
                with open(CHAIN_FILE, 'r') as f:
                    raw = json.load(f)
                for b in raw:
                    block = Block(b['index'], b['timestamp'], b['data'], b['previous_hash'])
                    block.hash = b.get('hash', block.compute_hash())
                    self.chain.append(block)
                print(f"Loaded {len(self.chain)} blocks from file")
            except Exception as e:
                print(f'Failed to load chain from file: {e}, creating genesis block')
                self.create_genesis_block()
        else:
            print('Chain file does not exist, creating genesis block')
            self.create_genesis_block()

    def _ensure_chain_file_is_file(self):
        """Make sure CHAIN_FILE is a file, not a directory"""
        if os.path.exists(CHAIN_FILE) and os.path.isdir(CHAIN_FILE):
            print(f"Warning: {CHAIN_FILE} is a directory. Removing it.")
            shutil.rmtree(CHAIN_FILE, ignore_errors=True)

    def create_genesis_block(self):
        # FIXED: Use dictionary {'info': 'genesis'} not set {'info','genesis'}
        genesis = Block(0, time.time(), {'info': 'genesis'}, '0')  # FIXED: '0' as string
        self.chain = [genesis]
        self._persist()

    @property
    def last_block(self):
        return self.chain[-1]

    def add_block(self, data):
        index = self.last_block.index + 1
        timestamp = time.time()
        previous_hash = self.last_block.hash
        new_block = Block(index, timestamp, data, previous_hash)
        self.chain.append(new_block)
        self._persist()
        return new_block

    def _persist(self):
        try:
            # Write to temporary file first to avoid corruption
            temp_file = CHAIN_FILE + '.tmp'
            with open(temp_file, 'w') as f:
                json.dump([b.to_dict() for b in self.chain], f, indent=2)
            
            # Replace original file
            os.replace(temp_file, CHAIN_FILE)
            print(f"Persisted {len(self.chain)} blocks to {CHAIN_FILE}")
        except Exception as e:
            print('Persist failed:', e)

    def to_list(self):
        return [b.to_dict() for b in self.chain]

    def get_student_records(self, student_id):
        records = []
        for b in self.chain:
            if (hasattr(b.data, 'get') and 
                isinstance(b.data, dict) and 
                b.data.get('student_id') == student_id):
                records.append(b.data)
        return records

    def is_valid(self):
        if len(self.chain) == 0:
            return False
            
        # Check genesis block
        genesis = self.chain[0]
        if genesis.index != 0 or genesis.previous_hash != '0':
            return False
            
        # Check subsequent blocks
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            prev = self.chain[i-1]
            
            if current.previous_hash != prev.hash:
                return False
                
            if current.hash != current.compute_hash():
                return False
                
            if current.index != prev.index + 1:
                return False
                
        return True