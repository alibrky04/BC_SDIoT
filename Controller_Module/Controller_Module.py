from pox.core import core
from pox.lib.revent.revent import EventMixin
from pox.lib.util import dpidToStr
from pox.lib.addresses import IPAddr

from flask import Flask, jsonify, request
from urllib.parse import urlparse
import json
import hashlib
from uuid import uuid4
import requests
import datetime
import  threading
import time
import random

log = core.getLogger()

StartTime = time.time()

P_Slots = [0] * 10

ReqNumCount = 1
TNum = 5

def GetUpTime():
    global StartTime
    Uptime = time.time() - StartTime
    return int(Uptime)

def SetTimeSlot():
    TimeSlot = random.randint(5, 10)
    return TimeSlot

def SetRemoveTime(TimeSlot, Uptime):
    RemoveTime = TimeSlot + Uptime
    return RemoveTime

def SetHostNumber():
    return random.randint(1, 15)

class BlockChainComponent(EventMixin):

    def __init__(self, flask_port = 8888):
        self.__name__ = 'BlockChainComponent'
        self.chain = []
        self.chain_started = False
        self.waiting_blocks = []
        self.transactions = []
        self.nodes = set()
        self.app = None
        self.flask_port = flask_port
        
    def start_chain(self):
        """starts the chain.
        -> If there is any node in system generates genesis block
        -> If there is other nodes in the system replicates other nodes chain
        -> Also sets chain_started = True. Other chain functions shouldn't be used if chain_started is false
        """

        # If there is nodes in the set
        if len(self.nodes) > 0:
            # Then replace the chain from other nodes
            self.replace_chain()
        else:
            # If there is no node in network than create genesis block
            self.create_block(nonce=1, previous_hash='0')

        self.chain_started = True
        return True

    def create_block(self, nonce, previous_hash):
        block_transactions = self.transactions.copy()
        m_root = self.calculateMerkleRoot()

        self.transactions = []
        
        block = {'index': len((self.chain)) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'nonce': nonce,
                 'previous_hash': previous_hash,
                 'merkle_root': m_root,
                 'transactions': block_transactions
                 }

        self.chain.append(block)
        return block

    def add_transaction(self, requestNo, host, spot, reservation_start_time, reservation_end_time):

        # this adds new transaction object to transaction list in blockchain
        self.transactions.append({
            'Request No': requestNo,
            'host': host,
            'spot': spot,
            'reservation_start_time': reservation_start_time,
            'reservation_end_time': reservation_end_time
        })

        previous_block = self.get_previous_block()
        return previous_block['index'] + 1

    def get_previous_block(self):
        """returns the last element in the chain """
        return self.chain[-1]

    def proof_of_work(self, previous_nonce):
        # sets new nonce to one
        new_nonce = 0

        # Nonce check setted to false
        check_nonce = False

        # while there is no proof of work (a nonce ending with 4 zero)
        while check_nonce is False:

            # Calculate hash
            hash_ops = hashlib.sha256(str(new_nonce ** 2 - previous_nonce ** 2).encode()).hexdigest()

            ## if the calculated hash is ending with 4 zero set check nonce to true end loop
            if hash_ops[:4] == '0000':
                check_nonce = True
            else:
                # else keep calculating the nonces
                new_nonce += 1

        ## when you find a valid nonce return the finded nonce
        return new_nonce

    def calculateHash(self, block):
        # json dumps serializes object to json format sort keys mean that argument should be sorted
        # first function takes a single block as a arguemnt then jsonifies the block
        encoded_block = json.dumps(block, sort_keys=True).encode()

        # after jsonofying the block it converts string to encyripted hash with sha256
        return hashlib.sha256(encoded_block).hexdigest()

    def calculateMerkleRoot(self):
        # This method calculates the merkle root of the block
        transactions = self.transactions

        # If there are no transactions, return None
        if len(transactions) == 0:
            return None

        merkle_tree = [hashlib.sha256(str(tx).encode()).hexdigest() for tx in transactions]

        while len(merkle_tree) > 1:
            # Duplicate the last transaction if the number of transactions is odd
            if len(merkle_tree) % 2 != 0:
                merkle_tree.append(merkle_tree[-1])
                
            merkle_tree = [hashlib.sha256((merkle_tree[i] + merkle_tree[i + 1]).encode()).hexdigest()
                           for i in range(0, len(merkle_tree), 2)]

        merkle_root = merkle_tree[0]

        return merkle_root

    # This function adds a new node to node set inside blockchain
    def add_node(self, adress):
        parsed_url = urlparse(adress)
        self.nodes.add(parsed_url.netloc)

    def add_waiting_block(self, block):
        self.waiting_blocks.append(block)

    def update_chain(self):
        """Adds blocks mined from other blocks to waiting blocks if its valid"""

        # While there is waiting blocks in waiting_blocks list
        while self.waiting_blocks:

            # Get the latest block mined by other nodes
            current_block = self.waiting_blocks.pop(0)

            # Create temporary chain for last two blocks
            test_chain = [self.get_previous_block(), current_block]

            # If the temporary chain is valid add new block to block_chain
            if self.isChainValid(test_chain):
                self.chain.append(current_block)


    def replace_chain(self):

        # this denotes to all nodes in the network
        network = self.nodes

        longest_chain = None

        # Set max lenght as self chain as trial then look for ching logner than this
        max_length = len(self.chain)

        # Check all the nodes in the network
        for node in network:

            # use http response to obtain chain
            response = requests.get(f'http://{node}/get_chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                if length > max_length:
                    max_length = length
                    longest_chain = chain

        if longest_chain:
            self.chain = longest_chain
            return True
        return False

    def isChainValid(self, chain):
        """
        This functions checks if the blockchain is valid or not
        :param chain: is a chain to control
        :return: Boolean if blockchain is valid
        """

        # If the length of chain is one then return true
        if len(chain) == 1:
            return True

        # Get last two block and perform calculations
        previous_block = chain[len(chain) - 2]
        block = chain[len(chain) - 1]

        if block['previous_hash'] != hashlib.sha256(
                json.dumps(previous_block, sort_keys=True).encode()).hexdigest():
            return False

        previous_nonce = previous_block['nonce']
        nonce = block['nonce']

        hash_operation = hashlib.sha256(str(nonce ** 2 - previous_nonce ** 2).encode()).hexdigest()
        if hash_operation[:4] != '0000':
            return False

        return True

    def getChain(self):
        return self.chain

    def launch(self):
        core.openflow.addListeners(self)
        self.app = Flask(__name__)

        @self.app.route('/mine_block', methods=['GET'])
        def mine_block():
            # Method implementation for mining a new block
            previous_block = self.get_previous_block()
            previous_nonce = previous_block['nonce']
            nonce = self.proof_of_work(previous_nonce)
            previous_hash = hashlib.sha256(json.dumps(previous_block, sort_keys=True).encode()).hexdigest()

            block = self.create_block(nonce, previous_hash)
            block_json = {
                'index': block['index'],
                'timestamp': block['timestamp'],
                'nonce': block['nonce'],
                'previous_hash': block['previous_hash'],
                'merkle_root': block['merkle_root'],
                'transactions': block['transactions']
            }

            for node in self.nodes:
                dumped_json_block = json.dumps(block_json)
                headers = {'Content-Type': 'application/json'}
                requests.post(f'http://{node}/share_block', data=dumped_json_block)

            return jsonify(block_json), 200

        @self.app.route('/get_chain', methods=['GET'])
        def get_chain():
            response = {
                'chain': self.chain,
                'length': len(self.chain)
            }
            return jsonify(response), 200

        @self.app.route('/is_valid', methods=['GET'])
        def is_valid():
            is_valid = self.isChainValid(self.chain)
            response = {'message': 'BlockChain is valid'} if is_valid else {'message': 'BlockChain is invalid'}
            return jsonify(response), 200

        @self.app.route('/add_transaction', methods=['POST'])
        def add_transaction():
            global ReqNumCount
            UpTime = GetUpTime()

            requestNo = ReqNumCount
            host = SetHostNumber()
            spot = random.randint(0, 9)
            reservation_start_time = UpTime
            reservation_end_time = SetRemoveTime(SetTimeSlot(), UpTime)

            index = self.add_transaction(requestNo, host, spot + 1, reservation_start_time, reservation_end_time)

            ReqNumCount += 1

            # Prepare a response message
            response = {'message': f'A transaction has been added to block {index}'}

            return jsonify(response), 201

        @self.app.route('/connect_nodes', methods=['POST'])
        def connect_nodes():
            json = request.get_json()
            nodes = json.get('nodes')
            if nodes is None:
                return 'No node', 400
            for node in nodes:
                self.add_node(node)
            response = {'message': 'All the nodes are now connected', 'total_nodes': list(self.nodes)}
            return jsonify(response), 200

        @self.app.route('/replace_chain', methods=['GET'])
        def replace_chain():
            is_chain_replaced = self.replace_chain()
            if is_chain_replaced:
                response = {'message': 'The other nodes were containing more blocks so the chain is replaced',
                            'chain': self.chain}
            else:
                response = {'message': 'BlockChain has not been replaced',
                            'chain': self.chain}
            return jsonify(response), 200

        @self.app.route('/start_chain', methods=['GET'])
        def start_chain():
            response_chain = self.start_chain()
            return {"response": f'Blockchain started {response_chain}'}, 200

        @self.app.route('/share_block', methods=['POST'])
        def share_block():
            block_object = request.get_json()
            self.add_waiting_block(block_object)
            self.update_chain()
            return {"response": f'Node received successfully {self.waiting_blocks}'}, 200

        log.info("Blockchain component launched")
        self.app.run(host='0.0.0.0', port=self.flask_port)  # Adjust the port as needed

def launch(flask_port=8888):
    blockchain_component = BlockChainComponent(flask_port)
    core.registerNew(BlockChainComponent)
    blockchain_thread = threading.Thread(target=blockchain_component.launch)
    blockchain_thread.daemon = True
    blockchain_thread.start()

if __name__ == '__main__':
    launch()
