import serial

from kivy.event      import EventDispatcher
from kivy.properties import NumericProperty, StringProperty

class Connector(EventDispatcher):
    connect_to = StringProperty(None)
    baudrate   = NumericProperty(115200)
    timeout    = NumericProperty(.2)
    
    read       = StringProperty("")
    write      = StringProperty("")
    
    def __init__(self, *args, **kwargs):
        super(Connector, self).__init__(*args, **kwargs)
        
        self.bind(baudrate = self._on_baudrate )
        self.bind(write    = self._on_write    )
        
        self.connection = serial.Serial(self.connect_to)
        #self.connection.open(self.connect_to)
        self.connection.setBaudrate(self.baudrate)
        self.connection.setTimeout(self.timeout)
        
    def _on_baudrate(self, widget, baud):
        self.connection.setBaudrate(baud)
    
    def _on_write(self, widget, value):
        self.connection.write(value)
    def _on_timeout(self, widget, value):
        self.connection.setTimeout(value)
    
    def read(self):
        self.read = self.connection.read()
    
    def readall(self):
        rchar   = self.connection.read()
        rstring = rchar
        while rchar != '':
            rchar = self.connection.read()
            rstring += rchar
        self.read = rstring