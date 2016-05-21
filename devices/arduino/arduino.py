
from . import RobotDevice
from messages import RobotMessage
import serial, re

class CmdMessage:
    """
    Basic interface to an arduino using the CmdMessenger library.
    """
    
    def __init__(self,device,baud_rate=115200,
                 field_separator=",",
                 command_separator=";",
                 escape_character="\\"):
        """
        Input:
            device: device location (e.g. /dev/ttyACM0)

            The baud_rate, separators, and escape_character should match what's
            in the arduino code that initializes the CmdMessenger.  The default
            values match the default values as of CmdMessenger 3.6. 
        """

        self.device = device
        self.baud_rate = baud_rate
        self.field_separator = field_separator
        self.command_separator = command_separator
        self.escape_character = escape_character

        self._esc_pattern = re.compile(r"([{}{}])".format(self.field_separator,
                                                          self.command_separator))
        self._esc_sub_str = r"{}\\1".format(self.escape_character)

        self.serial_handle = serial.Serial(device,baud_rate)

    
    def send(self,*args):
        """
        Send a command (which may or may not have associated arguments) to an 
        arduino using the CmdMessage protocol.  The command and any parameters
        should be passed as direct arguments to send.  The function will convert
        python data types to strings, as well as escaping problem characters.
        """

        if len(args) < 1:
            err = "You must specify a command (and maybe parameters).\n"
            raise ValueError(err)

        # Turn arguments into strings, replacing separators with escaped separators
        strings = [self._esc_pattern.sub(self._esc_sub_str,"{}".format(a)) for a in args]

        # compile the final string
        compiled_string = "{};".format(",".join(strings))

        # Send the message
        self.serial_handle.write(compiled_string)

    def recieve(self,convert_strings=True):
        """
        Read a serial message sent by CmdMessage library.  

        Inputs:
            convert_strings: try to convert read parameter strings into integers
                             or floats. [default: True]

        Possible outputs:

            None (no message)

            OR

            ((cmd1,[param1,param2,...,paramN]),
             (cmd2,[param1,param2,...,paramN]),
              ...
             (cmdM,[param1,param2,...,paramN]))

            If params are empty, they will be returned as an emtpy list.  If 
            only one command comes through, it will still be in a tuple like:

            ((cmd1,[param1,param2,...,paramN]))
        """

        # Read raw serial
        message = self.serial_handle.read()

        # No message
        if message == "":
            return None

        # Split message by command separator, ignoring escaped command separators
        message_list = re.split(r'(?<!\\){}'.format(self.command_separator),message)

        # Go through each command message
        final_out = []
        for m in message_list:
            
            # Split message on field separator, ignoring escaped separtaors
            fields = re.split(r'(?<!\\){}'.format(self.field_separator),m)
            fields = m.split(self.field_separator)
            command = fields[0]

            # Parse all of the fields
            field_out = []
            for f in fields[1:]:

                if f.isdigit():
                    # is it an integer?
                    field_out.append(int(f))
                else: 

                    try:
                        # is it a float?
                        field_out.append(float(f))
                    except ValueError:
                        # keep as a string
                        field_out.append(f)

            final_out.append((command,field_out))

        return final_out 
        
class ArduinoRobotDevice(RobotDevice):
    """
    """

    def __init__(self,device_name=None,baud_rate=115200,device_tty=None,name=None):
        """
        """

        RobotDevice.__init__(self,name)

        self._device_name = device_name
        self._device_tty = device_tty

        self.baud_rate = baud_rate
        self.found_device = False

        # Try to connect to specified device
        if self._device_tty != None:
            try:       
                self._device_handle = serial.Serial(self._device_tty,self.baud_rate)
                self.found_device = True
            except:
                pass

        # Or look for the device
        else:
            self._find_serial()

        # Send message that we've found device (or not)
        if self.found_device:
            message="{} connected on {} at {} baud.".format(self._device_name,
                                                            self._device_tty,
                                                            self.baud_rate))
            msg = RobotMessage(source_device=self.name,
                               message=message)
            self._messages.append(msg)

        else:
            message="Could not find usb device identifying as {}".format(self._device_name)

            msg = RobotMessage(destination="warn",
                               source_device=self.name,
                               message=message)

            self._messages.append(msg)  
 
        
    def _find_serial(self):
        """
        Search through attached serial devices until one reports the specified
        device_name when probed by "who_are_you".
        """

        tty_devices = [d for d in os.listdir("/dev") if d.startswith("ttyA")]

        self.found_device = False
        for d in tty_devices:

            try:
                
                tmp_tty = os.path.join("/dev",d)
                tmp_msg = CmdMessage(tmp_tty,self.baud_rate)
                tmp_msg.write("who_are_you") 
               
                reported_device_name = tmp_msg.read()

                if reported_device_name[0][1] == self._device_name:
                    self._device_tty = tmp_tty
                    self._device_msg = tmp_msg
                    self.found_device = True
                    break

            except (FileNotFoundError,PermissionError,TypeError):
                pass


def ArduinoDrivetrain(ArduinoRobotDevice):
    """
    """

    def __init__(self,device_name=None,baud_rate=115200,device_tty=None,name=None):
        """
        """

        super(ArduinoDrivetrain, self).__init__(device_name,baud_rate,device_tty,name)

        self._control_dict = {"forward":self._forward,
                              "reverse":self._reverse,
                              "brake":self._brake,
                              "coast":self._coast,
                              "left":self._left,
                              "right":self._right,
                              "setspeed":self._set_speed}

    def _forward(self,owner):

        pass

    def _reverse(self,owner):

        pass
        
    def _left(self,owner):
     
        pass 

    def _right(self,owner):

        pass
        
    def _brake(self,owner):

        pass
        
    def _coast(self,owner):

        pass

    def _set_speed(self,speed,owner):
        """
        Set the speed of the motors.
        """
    
        # Make sure the speed set makes sense. 
        if speed > self._max_speed or speed < 0:
            err = "speed {:.3f} is invalid".format(speed)

            self._append_message(RobotMessage(destination_device="warn",
                                              source_device=self.name,
                                              message=err))

            # Be conservative.  Since we recieved a mangled speed command, set
            # speed to 0.
            self._append_message(RobotMessage(destination="robot",
                                              destination_device=self.name,
                                              source="robot",
                                              source_device=self.name,
                                              message=["setspeed",{"speed":0}]))
        else:
            self._drive_speed = speed

        
    def shutdown(self,owner):

        pass 
