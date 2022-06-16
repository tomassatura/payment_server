import xml.etree.ElementTree as ET
from src.records_keeping import Records
import xmltodict
from src.actions import GetWeatherInformation


class PaymentServer:
    transaction_limit = 150
    temperature_limit = 10
    count_limit = 1

    def __init__(self, payment_message_request_xml):
        self.records = Records()
        self.input_dict = xmltodict.parse(payment_message_request_xml)["Body"]["Transaction"]
        self.day = self.input_dict["Transaction_Time"].split("T")[0]
        self.city = self.input_dict["Merchant"]["Merchant_City"]
        self.amount = int(self.input_dict["Amount"])
        self.weather_information = self.get_weather_information()
        self.owner = "customer"
        self.reason = "None"
        self.result = "Declined"
        # weather factors
        self.weather_factor = 1
        self.sunny_factor = 1
        self.update_factors()
        # token check
        try:
            self.token = self.input_dict["Token"]
        except KeyError:
            self.token = "0000"
        self.limit = self.records.get_limit(self.token)
        self.update_owner()
        self.output_string = ""

    def handle(self):
        # perform checks
        self.checks()
        # assign result
        self.update_result()
        # output xml-like string
        self.output_string = self.format_xml()
        # perform charge and update of records
        new_limit = self.limit
        if self.result == "Accepted":
            if self.owner == "bank":
                self.records.charge(self.amount, owner="bank")
            else:
                new_limit = self.records.charge(self.amount, token=int(self.token))
        self.records.update_records(self.token, self.day, self.amount, self.owner, self.result, self.reason, new_limit)

    def checks(self):
        # CHECKS
        # check no. 1 - insufficient funds
        if self.amount > self.limit:
            self.reason = "InsufficientFunds"
            return "InsufficientFunds"
        # check no. 2 + check no. 6
        transactions_today = self.records.transaction_today(self.token, self.day)
        if transactions_today >= (self.count_limit * self.sunny_factor):
            self.reason = "TransactionCountOverLimit"
            return "TransactionCountOverLimit"
        # check no. 3 + check no. 5
        if self.amount > (self.transaction_limit * self.weather_factor):
            self.reason = "TransactionAmountOverLimit"
            return "TransactionAmountOverLimit"
        # check no. 4
        if self.weather_information["clouds"] == "RAINING":
            self.reason = "ItsRaining"
            return "ItsRaining"

    def update_factors(self):
        if self.weather_information['temperature'] < self.temperature_limit:
            self.weather_factor = 0.5
        if self.weather_information["clouds"] == "SUNNY":
            self.sunny_factor = 2

    def update_owner(self):
        if self.weather_information["wind_direction"] == "N":
            self.owner = "bank"
            self.limit = self.records.get_limit(owner=self.owner)
        else:
            self.limit = self.records.get_limit(self.token)

    def get_weather_information(self):
        action = GetWeatherInformation()
        action_run_result = action.run_with_data(date=self.day, city=self.city)
        return action_run_result.get("weather_information")

    def update_result(self):
        if (self.reason == "None") & (self.token != "0000"):
            self.result = "Accepted"
        else:
            self.result = "Declined"

    def format_xml(self):
        root = ET.Element("Body")
        doc = ET.SubElement(root, "TransactionResponse")
        ET.SubElement(doc, "Result").text = self.result
        ET.SubElement(doc, "Reason").text = self.reason
        tree = ET.ElementTree(root)
        ET.indent(tree, space="\t", level=0)
        return tree
