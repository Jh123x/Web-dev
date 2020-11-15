
class WebParser(object):
    def __init__(self):
        self.parsers = {
            "generic" : self.handle_generic,
            "name" : self.handle_name,
        }
        self.data = {}
    

    def handle_post(self, data:dict):
        pass

    def handle_get(self, data:dict):
        pass

    def handle_name(self, data:dict):
        firstname = data['fname']
        lastname = data['lname']
        return \
        f"""<b>Hello {firstname} {lastname}</b>"""

    def handle_generic(self, data:dict):
        """Handle the generic case"""

        return f"""<b>Error Protocol not found</b>"""

    def parse(self, data:dict) -> str:
        """Parse the data to json"""
        handler_type = data.get("type", "").lower()
        handler = self.parsers.get(handler_type, self.parsers["generic"])
        result = handler(data)
        # print(result)
        return result
