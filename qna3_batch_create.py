from eth_account import Account
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_wallet():
    """
    创建钱包

    Returns:
        dict: 包含地址和私钥的字典
    """
    account = Account.create()
    wallet_data = {
        'address': account.address,
        'private_key': account.key.hex()
    }
    logging.debug(f"Wallet created - Address: {wallet_data['address']}")
    return wallet_data


def generate_and_save_wallets( file_path, num_wallets):
    """
    生成并保存多个钱包信息到文件

    Args:
        file_path (str): 文件路径
        num_wallets (int): 要生成的钱包数量
    """
    wallets = []
    for _ in range(num_wallets):
        wallet_data = create_wallet()
        wallets.append(wallet_data)
        logging.debug(f"Wallet created - Address: {wallet_data['address']}")

    with open(file_path, 'w') as file:
        for wallet_data in wallets:
            file.write(f"{wallet_data['address']},{wallet_data['private_key']}\n")

    logging.debug(f"Wallet information written to {file_path}")

if __name__ == '__main__':
    generate_and_save_wallets('generate_wallets.txt', 100)