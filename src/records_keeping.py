import json
import pandas as pd
import os
import shutil
from src.get_base_dir_path import GetBaseDirPath


class Records:
    def __init__(self):
        self.base_path = GetBaseDirPath().__call__()

    def clear_records(self):
        path = "{}/resources/records.json".format(self.base_path)
        out_file = open(path, "w")
        json.dump([], out_file, indent=1)
        out_file.close()

    def clear_balance(self):
        path1 = "{}/resources/limits".format(self.base_path)
        path2 = "{}/resources/balance.json".format(self.base_path)
        initial_balance = pd.read_csv(path1)
        initial_balance.to_json(path2)

    def clear_results(self):
        directory_name = "tests/results"
        parent_dir = os.path.dirname(self.base_path)
        path = os.path.join(parent_dir, directory_name)
        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path)

    def charge(self, amount, token="NaN", owner=""):
        path = "{}/resources/balance.json".format(self.base_path)
        balances = pd.read_json(path)
        index = balances.loc[(balances["card_token"] == token) | (balances["owner"] == owner)].index.tolist()[0]
        balances.at[index, "Limit"] -= amount
        balances.to_json(path)
        return balances.at[index, "Limit"]

    def update_records(self, token, day, amount, owner, result, reason, limit):
        path = "{}/resources/records.json".format(self.base_path)
        records = pd.read_json(path)
        new_entry = pd.DataFrame({"card_token": [token],
                                  "day": [day],
                                  "amount": [amount],
                                  "Charged Owner": [owner],
                                  "Result": [result],
                                  "Reason": [reason],
                                  "Limit": [limit]})

        records = pd.concat([records, new_entry], ignore_index=True, axis=0)
        records.to_json(path)

    def get_limit(self, token="1234567890", owner=""):
        path = "{}/resources/balance.json".format(self.base_path)
        try:
            balances = pd.read_json(path)
            limit = balances.loc[(balances["card_token"] == int(token)) | (balances["owner"] == owner)].iloc[0].at[
                "Limit"]
        except IndexError:
            limit = 0
        return limit

    def transaction_today(self, token, day):
        try:
            path = "{}/resources/records.json".format(self.base_path)
            records = pd.read_json(path)
            filtered_records = records.loc[(records["card_token"] == int(token)) & (records["day"] == day)]
            accepted_records = filtered_records.loc[filtered_records["Result"] == "Accepted"]
            transactions = len(accepted_records.index)
        except KeyError:
            transactions = 0
        return transactions
