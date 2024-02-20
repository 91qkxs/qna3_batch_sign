import random

from util.common_utils import CommonUtils
from util.qna3_utils import Qna3Utils
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
def read_lines(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines


def write_line(file_path, line):
    with open(file_path, 'a') as file:
        file.write(line)


def transfer_from_new_to_wallet(wallet_file, new_file, t_file):

    qna3_util = Qna3Utils()

    # 读取钱包文件和新账户文件的内容
    wallet_accounts = read_lines(wallet_file)
    new_accounts = read_lines(new_file)

    # 如果新账户列表为空，直接返回
    if not new_accounts:
        return

    # 遍历 new_accounts 中的每个账户
    for new_account in new_accounts:
        recipient_address, recipient_key = new_account.strip().split(',')

        # 如果新账户已经在钱包中，则跳过该账户
        if recipient_address in [line.split(',')[0].strip() for line in wallet_accounts]:
            continue

        # 随机选择一个发送账户
        sender_address, sender_key = random.choice(wallet_accounts).strip().split(',')

        # 假设有一个名为 transfer_balance 的方法可以进行转账，返回转账是否成功的布尔值
        transfer_success = qna3_util.transfer_balance(sender_address, recipient_address, sender_key)

        # 如果转账成功，则将新账户信息写入 t.txt 文件
        if transfer_success:
            write_line(t_file, f"{recipient_address},{recipient_key}\n")
        CommonUtils.countdown_timer(2)  # 休眠30秒

    # 如果所有的新账户都被转账完毕，则可以在这里处理
    logging.info("所有新账户转账完成")



# 示例调用
wallet_file = "from_wallets.txt"
new_file = "to_wallets.txt"
t_file = "success_wallets.txt"
transfer_from_new_to_wallet(wallet_file, new_file, t_file)
