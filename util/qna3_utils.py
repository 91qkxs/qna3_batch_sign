import json
import random

import requests
from web3 import Web3
from eth_account import Account, messages
import logging
from faker import Faker


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Qna3Utils(object):
    def __init__(self, http_provider='https://opbnb.publicnode.com'):
        self.session = requests.Session()
        self.web3 = Web3(Web3.HTTPProvider(http_provider))
        self.fake = Faker()


    def get_wallet_balance(self, wallet_address):
        """
        获取余额
        """
        balance_wei = self.web3.eth.get_balance(wallet_address)
        balance_eth = self.web3.from_wei(balance_wei, 'ether')
        return balance_eth

    def signature_opbnb_chain(self, private_key, wallet_address, message_to_sign):
        """
        OPBNB链上签名
        """
        # 转换为Checksum地址
        wallet_address_checksum = self.web3.to_checksum_address(wallet_address)
        # 创建可签名消息
        signable_message = messages.encode_defunct(text=message_to_sign)
        # 使用私钥进行签名
        signed_message = Account.sign_message(signable_message, private_key=private_key)
        # 验证签名
        recovered_address = Account.recover_message(signable_message, signature=signed_message.signature)
        # 如果Recovered Address与提供的钱包地址不匹配，则签名无效
        if recovered_address.lower() != wallet_address_checksum.lower():
            raise ValueError("签名错误，秘钥钱包不匹配")
        # 在这里可以执行与OPBNB链的其他交互逻辑，例如发送交易等
        # 返回签名
        return signed_message.signature.hex()

    def send_claim_tx(self, to, from_, data, gas_price, gas_limit, chain_id, private_key):
        """
        发送交易
        """
        nonce = self.web3.eth.get_transaction_count(from_)

        transaction = {
            'to': to,
            'from': from_,
            'data': data,
            'gasPrice': gas_price,
            'gas': gas_limit,
            'nonce': nonce,
            'chainId': chain_id,
        }

        signed_transaction = self.web3.eth.account.sign_transaction(transaction, private_key=private_key)
        # 发送交易
        transaction_hash = self.web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
        return transaction_hash.hex()

    def read_wallets_from_file(self, file_path):
        wallets = []
        with open(file_path, 'r') as file:
            for line in file:
                address, private_key = line.strip().split(',')
                wallets.append({'address': address, 'private_key': private_key})
        return wallets

    def login(self, wallet_address, signature,invite_code="3EwnfTtN"):
        try:
            # proxy = "you proxy"
            user_agent = self.fake.chrome()
            response = self.session.post(
                url="https://api.qna3.ai/api/v2/auth/login",
                params={"via": "wallet"},
                headers={
                    "User-Agent": user_agent,
                    "Content-Type": "application/json",
                    "Accept": "application/json, text/plain, */*",
                    "Origin": "https://qna3.ai",
                    "x-lang": "chinese"
                },
                data=json.dumps({"wallet_address": wallet_address, "signature": signature ,"invite_code":invite_code}),
                # proxies
                # proxies=proxy,
                timeout=30  # 设置超时时间为30秒

            )

            response.raise_for_status()

            if "data" in response.json():
                return response.json()["data"]["accessToken"]
            else:
                logging.info("登录失败，返回数据不包含 'data' 字段")
                return None
        except requests.exceptions.RequestException as e:
            logging.info(f'HTTP Request failed: {e}')
            return None

    def check_sign_state(self, access_token):
        try:

            # proxy = "you proxy"
            user_agent = self.fake.chrome()
            response = self.session.post(
                url="https://api.qna3.ai/api/v2/graphql",
                headers={
                    "User-Agent": user_agent,
                    "Content-Type": "application/json",
                    "Accept": "application/json, text/plain, */*",
                    "Origin": "https://qna3.ai",
                    "Authorization": "Bearer " + access_token
                },
                data=json.dumps({
                    "query": "query loadUserDetail($cursored: CursoredRequestInput!) {\n  userDetail {\n    "
                             "checkInStatus {\n      checkInDays\n      todayCount\n      checked\n    }\n    "
                             "credit\n    creditHistories(cursored: $cursored) {\n      cursorInfo {\n        "
                             "endCursor\n        hasNextPage\n      }\n      items {\n        claimed\n        "
                             "extra\n        id\n        score\n        signDay\n        signInId\n        txHash\n   "
                             "     typ\n      }\n      total\n    }\n    invitation {\n      code\n      "
                             "inviteeCount\n      leftCount\n    }\n    origin {\n      email\n      id\n      "
                             "internalAddress\n      userWalletAddress\n    }\n    voteHistoryOfCurrentActivity {\n   "
                             "   created_at\n      query\n    }\n    ambassadorProgram {\n      bonus\n      "
                             "claimed\n      family {\n        checkedInUsers\n        totalUsers\n      }\n    }\n  "
                             "}\n}",
                    "variables": {
                        "cursored": {"after": "", "first": 20}
                    }
                }),
                # proxies=proxy,
                timeout=30  # 设置超时时间为30秒

            )

            response.raise_for_status()

            response_json = response.json()
            check_in_status = response_json.get("data", {}).get("userDetail", {}).get("checkInStatus", {})
            checked = check_in_status.get("checked", False)
            return checked
        except requests.exceptions.RequestException as e:
            logging.info(f'HTTP Request failed: {e}')
            return None

    def send_claim_hash(self, hash, via, access_token):
        try:
            # proxy = "you proxy"
            params = {'hash': hash, 'via': via}
            response = self.session.post(
                url='https://api.qna3.ai/api/v2/my/check-in',
                json=params,
                headers={
                    "User-Agent": self.fake.chrome(),
                    "Content-Type": "application/json",
                    "Accept": "application/json, text/plain, */*",
                    "Origin": "https://qna3.ai",
                    "Authorization": "Bearer " + access_token
                },
                # proxies=proxy,
                timeout=90  # 设置超时时间为30秒

            )
            logging.info(response)
            logging.info(response.text)
            logging.info(response.status_code)
            response.raise_for_status()

            resp_text = response.text
            return resp_text
        except requests.exceptions.RequestException as e:
            #  logging.info(f'请求失败: {e}')
            return None

    def send_claim_verify(self, via, access_token):
        try:
            # proxy = "you proxy"
            params = {'via': via}
            response = self.session.post(
                url='https://api.qna3.ai/api/v2/my/check-in/verify',
                json=params,
                headers={
                    "User-Agent": self.fake.chrome(),
                    "Content-Type": "application/json",
                    "Accept": "application/json, text/plain, */*",
                    "Origin": "https://qna3.ai",
                    "Authorization": "Bearer " + access_token
                },
                # proxies=proxy,
                timeout=90  # 设置超时时间为30秒

            )
            logging.info(response)
            logging.info(response.text)
            logging.info(response.status_code)
            response.raise_for_status()

            resp_text = response.text
            return resp_text
        except requests.exceptions.RequestException as e:
            #  logging.info(f'请求失败: {e}')
            return None



    def transfer_balance(self, sender_address, recipient_address, private_key):
        """
        转账余额1% opbnb到任意钱包
        """
        # 获取发送者地址的余额
        balance_wei = self.web3.eth.get_balance(sender_address)
        balance_eth = self.web3.from_wei(balance_wei, 'ether')

        # 计算要转账的金额（当前余额的十分之一）
        amount_to_transfer = balance_wei / 100

        # 获取当前钱包地址的 nonce 值
        nonce = self.web3.eth.get_transaction_count(sender_address)

        # 获取当前 gas price
        gas_price = self.web3.eth.gas_price

        # 构建转账交易
        tx = {
            'nonce': nonce,
            'to': recipient_address,
            'value': int(amount_to_transfer),
            'gas': 50000 + random.randint(1, 10000),  # 设置 gas 限额
            'gasPrice': int(self.web3.eth.gas_price * 1.15),  # 使用动态获取的 gas price
            'chainId': 204,
        }

        # 对交易进行签名
        signed_tx = self.web3.eth.account.sign_transaction(tx, private_key)
        logging.info(f"signed_tx: {signed_tx.rawTransaction.hex()}")

        # 发送已签名的交易
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        logging.info(f"tx_hash: {tx_hash.hex()}")

        # 等待交易被确认
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        logging.info(f"tx_receipt: {tx_receipt.status}")
        # 获取交易的状态
        if tx_receipt.status == 1:
            logging.info("转账成功")
            return True
        else:
            logging.info("转账失败")
            return False