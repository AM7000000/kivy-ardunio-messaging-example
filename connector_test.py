from great_widgets.wheel import Wheel
from connector import Connector

class SerialWheel(Wheel):
    connector = Connector(connect_to= "/dev/ttyACM0",
                          baudrate = 115200)
    
    def __init__(self, **kwargs):
        Wheel.__init__(self, **kwargs)
        self.bind(value = self.serial_value)
    
    def serial_value(self, widget, value):
        self.connector.write = "w a 11 %s\r" %((255/2)*(value+1))

if __name__ == '__main__':
    from kivy.app import App
    
    class WheelApp(App):
        def build(self):
            w = SerialWheel(value_locked = False)
            return w
    WheelApp().run()