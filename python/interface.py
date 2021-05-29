import BT
import maze
import score

# *hint: You may design additional functions to execute the input command, which will be helpful when debugging :)


class interface:
    def __init__(self):
        print("")
        print("Arduino Bluetooth Connect Program.")
        print("")
        self.ser = BT.bluetooth()
        port = "COM4"
        while(not self.ser.do_connect(port)):
            if(port == "quit"):
                self.ser.disconnect()
                quit()
            port = "COM4"
        input("Press enter to start.")
        # self.ser.SerialWrite('s')

    def get_UID(self, time=2.5):
        return self.ser.SerialReadByte(time)

    def send_action(self, action):
        # TODO : send the action to car
        self.ser.SerialWrite(str(int(action)))
        return

    def end_process(self):
        self.ser.SerialWrite('e')
        self.ser.disconnect()

    def get_command(self):
        return self.ser.SerialReadString()
