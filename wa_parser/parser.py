from datetime import datetime

class WhatsappMessage:
    date: str
    time: str
    sender: str
    message: str
    datetime_obj: None
    is_system_message: bool

    def __init__(self,date,time,sender,message,is_system_message=False):
        self.date = date
        self.time = time
        self.sender = sender
        self.message = message
        self.datetime_obj = None
        self.is_system_message = is_system_message
        self.__post_init__()
    
    def __post_init__(self):
        try:
            self.datetime_obj = datetime.strptime(f"{self.date} {self.time}", "%d/%m/%y %H:%M")
        except ValueError:
            self.datetime_obj = None
    
    def to_dict(self):
        return {
            'date': self.date,
            'time': self.time,
            'sender': self.sender,
            'message': self.message,
            'is_system_message': self.is_system_message
        }

class WhatsappParser:
    def __init__(self,format="android"):
        self.format = format.lower()
        if self.format not in ("android","ios"):
            raise ValueError("supported format type are 'android' or 'ios'")
        
    def is_header(self,line):
        if self.format == "android":
            return self._is_header_android(line)
    
    def _is_header_android(self,line):
        line = line.split(" ")
        if len(line) > 3:
            if line[2] == '-':
                return True
        return False
    
    def is_real_message(self, line):
        if self.format == "android":
            return self._is_real_message_android(line)

    def _is_real_message_android(self,line):
        parts = line.split(" - ",1)
        name_message_part = parts[1]
        if ':' in name_message_part:
            return True
        else:
            return False
    
    def _is_real_message_ios(self,line):
        parts = line.split(" ",1)
        name_message_part = parts[1]
        if ':' in name_message_part:
            return True
        else:
            return False
    
    def parse_header(self,line):
        if self.format == "android":
            return self._parse_header_android(line)
    
    def _parse_header_android(self,line):
        parts = line.split(" - ",1)
        datetime = parts[0].split(" ")
        name_message_part = parts[1]
        date = datetime[0].replace(",","")
        time = datetime[1]
        if ':' in name_message_part:
            name_message = name_message_part.split(':')
            name = name_message[0]
            message = name_message[1]
        else:
            name = name_message_part
            message = ""
        
        return date,time,name,message

    def parse_wa_chat(self,file):
        messages = []
        current_message = ""
        current_header = None

        with open(file,"r") as raw:
            for line in raw.readlines():
                line = line.rstrip('\n')
                if self.is_header(line):
                    if current_header is not None:
                        date, time, sender, _, is_system = current_header
                        messages.append(WhatsappMessage(
                            date=date,
                            time=time,
                            sender=sender,
                            message=current_message.strip(),
                            is_system_message=is_system
                        ))
                    date, time, sender, message_content = self.parse_header(line)
                    is_system = not self.is_real_message(line)
                    current_header = (date, time, sender, message_content, is_system)
                    current_message = message_content
                else:
                    if current_message:
                        current_message += "\n" + line
                    else:
                        current_message = line
            if current_header is not None:
                date, time, sender, _, is_system= current_header
                messages.append(WhatsappMessage(
                    date = date,
                    time = time,
                    sender = sender,
                    message = current_message.strip(),
                    is_system_message=is_system
                ))
        return messages
