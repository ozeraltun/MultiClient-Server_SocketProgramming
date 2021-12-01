class Message:
    def __init__(self, str_data):
        self.val = str_data

    def get_message(self):
        return self.val

    def set_message(self, new_val):
        self.val = new_val
