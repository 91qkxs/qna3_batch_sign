import time

from loguru import logger


class CommonUtils:
    @staticmethod
    def countdown_timer(seconds):
        for remaining in range(seconds, 0, -1):
            print(f"\r当前线程休眠，剩余: {remaining} 秒", end='', flush=True)
            time.sleep(1)
        print("\r线程休眠结束，准备下一步操作            ")
    @staticmethod
    def print_masked_wallet_address(wallet_address):
        masked_address = wallet_address[:4] + "****" + wallet_address[-5:]
        return masked_address

    @staticmethod
    def read_wallets_from_file(file_path):
        wallets = []
        with open(file_path, 'r') as file:
            for line in file:
                address, private_key = line.strip().split(',')
                wallets.append({'address': address, 'private_key': private_key})
        return wallets
    @staticmethod
    def print_wallet_address(input_string):
        if len(input_string) <= 7:
            return input_string
        else:
            visible_prefix = input_string[:3]
            visible_suffix = input_string[-4:]
            masked_middle = '*' * (len(input_string) - 7)
            masked_string = visible_prefix + masked_middle + visible_suffix
            return masked_string