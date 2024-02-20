import json
import random
import time
from util.common_utils import CommonUtils
from util.qna3_utils import Qna3Utils
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def perform_claim_verification(wallet_address, private_key, qna3_util):
    # 发送签到交易
    tx_hash = qna3_util.send_claim_tx(
        to="0xB342e7D33b806544609370271A8D074313B7bc30",
        from_=wallet_address,
        data='0xe95a644f0000000000000000000000000000000000000000000000000000000000000001',
        gas_price=int(qna3_util.web3.eth.gas_price * 1.2),
        gas_limit=50000 + random.randint(1, 10000),
        chain_id=204,
        private_key=private_key
    )

    logging.info(tx_hash)

    try:
        if tx_hash:
            resp_text = qna3_util.send_claim_verify('opbnb', token)
            if resp_text is None:
                logging.error("请求失败: 无法解析响应文本")
                time.sleep(random.randint(1, 3))
            elif resp_text == '{"statusCode":422,"message":"user already signed in today"}':
                logging.info(f"已签到: {wallet_address}")
            elif json.loads(resp_text)['statusCode'] != 200:
                logging.error(f"签到失败，错误信息: {resp_text}")
            else:
                logging.info(f"成功签到: {wallet_address}")

        else:
            logging.info("签到失败")
    except Exception as e:
        logging.info(f"签到时发生异常: {str(e)}")


# 示例用法
if __name__ == "__main__":

    invite_code = ''

    qna3_util = Qna3Utils()
    # 将钱包地址和私钥存入 Redis，设置过期时间为一天
    wallets = CommonUtils.read_wallets_from_file('./wallets.txt')
    for wallet in wallets:
        wallet_address = wallet['address']
        private_key = wallet['private_key']

        # 从 Redis 中获取所有钱包地址和私钥

        # 依次进行交互

        # 待签名msg
        message_to_sign = "AI + DYOR = Ultimate Answer to Unlock Web3 Universe"
        # 获取签名
        signature = qna3_util.signature_opbnb_chain(private_key, wallet_address, message_to_sign)
        # 进行登录
        token = qna3_util.login(wallet_address, signature,invite_code)
        if token is not None:
            # 检验当天是否签到
            state = qna3_util.check_sign_state(token)
            if state:
                logging.info(f"{CommonUtils.print_wallet_address(wallet_address)}: 当天地址已签到")
            else:
                logging.info(f"{(wallet_address)}: 未签到，准备签到")
                perform_claim_verification(wallet_address, private_key, qna3_util)
        else:
            logging.info(f"{(wallet_address)}: 获取token异常")

        time.sleep(random.randint(7, 10))
