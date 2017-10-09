import phonenumbers
import re

from dateutil.parser import parse


class ParseXML():

    def print_all(self, root):
        for message in root:
            self.print_message(message)

    @staticmethod
    def print_message(message):
        for attrib in message.attrib:
            print("{a}: {v}".format(a=attrib.upper(), v=message.attrib[attrib]))
        print("\n")

    @staticmethod
    def standardize_number(number):
        try:
            if len(re.sub('[()\-+ "]', '', number)) == 10:
                # Assume USA is the country code. Sorry rest of the world. :/
                lookup = phonenumbers.parse('+1{n}'.format(n=number))
            else:
                lookup = phonenumbers.parse('+{n}'.format(n=number))
            fixed_number = phonenumbers.format_number(lookup, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            return fixed_number
        except phonenumbers.NumberParseException as npe:
            print(npe)

    @staticmethod
    def standardize_date(_date):
        """ Return the date in yyyy/mm/dd HH:MM:SS format """
        _date = parse(_date)
        return _date.strftime('%Y/%m/%d %H:%M:%S')

    def human_readable(self, message):
        """ Return the data in a more human readable way """
        try:
            if message.attrib["type"] == "1":
                message.set("type", "received")
            elif message.attrib["type"] == "2":
                message.set("type", "sent")
            elif message.attrib["type"] == "3":
                message.set("type", "draft")
            elif message.attrib["type"] == "5":
                message.set("type", "failed")
            if message.attrib["read"] == "1":
                message.set("read", "read")
            elif message.attrib["read"] == "0":
                message.set("read", "unread")
        except KeyError:
            try:
                if message.attrib["text_only"]:
                    try:
                        message.set("attachment", message[0][0].attrib["text"])
                        message.set("text", message[0][1].attrib["text"])
                    except IndexError as err:
                        print("ERROR!! {e}".format(e=err))
                        print(message.attrib)
            except KeyError as err:
                print("ERROR!! {e} attribute not in -".format(e=err))
                print(message.attrib)
                print("\n")
                return
        # try/pass here in case the mms doesn't have a number attached (it happens).
        try:
            pretty_number = self.standardize_number(message.attrib["address"])
            message.set("address", pretty_number)
        except KeyError as err:
            print("ERROR!! {e}".format(e=err))
            print(message.attrib)
        pretty_date = self.standardize_date(message.attrib["readable_date"])
        message.set("readable_date", pretty_date)
        return message
