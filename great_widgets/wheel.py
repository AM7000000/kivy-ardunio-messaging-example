import math

from kivy.uix.widget import Widget

from kivy.graphics import Color, Rectangle

from kivy.logger import Logger

from kivy.properties import NumericProperty, OptionProperty, BooleanProperty, BoundedNumericProperty

class Wheel(Widget):
    orientation       = OptionProperty('vertical', options=('vertical', 'horizontal'))
    mode              = OptionProperty('absolute', options=('absolute', 'relative'))
    fixed             = BooleanProperty(False) 
    sharp             = BooleanProperty(True)
    
    color_other       = Color(0.1843137254901961, 0.6549019607843137, 0.8313725490196079) ## default color of solid line
    color_value       = Color(1, 0, 0)
    
    line_size         = NumericProperty( 5)
    seperation_size   = NumericProperty(20)
    
    value_visible     = BooleanProperty(True)
    value_locked      = BooleanProperty(True)
    value_lock        = NumericProperty(0)
    value_lock_type   = OptionProperty('range', options=('range', 'pixel'))
    value             = NumericProperty(0.)
    value_px          = NumericProperty(0)
    
    distance          = BoundedNumericProperty(.8, min=0, max=1) #radians
    
    def __init__(self, **kwargs):
        super(Wheel, self).__init__(**kwargs)
        
        self.bind(orientation  = self.on_widget_change)
        
        self.bind(pos          = self.on_widget_change)
        
        self.bind(size         = self.prep_value_locked)
        self.bind(size         = self.on_widget_change)
        
        self.bind(value        = self.on_value)
        self.bind(value_lock   = self.prep_value_locked)
        self.bind(value_locked = self.prep_value_locked)
        
        self.bind(value_px     = self._calc_px2dec)
        self.bind(value_px     = self.on_value_px)
        self.bind(value_px     = self.on_widget_change)
        
    def on_value(self, widget, value):
        return
    
    def on_value_px(self, widget, value):
        return
    
    def prep_value_locked(self, widget, lock):
        if self.value_locked:
            self.value_px = self._calc_lock()
    
    def on_widget_change(self, widget, value):
        self.canvas.clear() # clear wheels canvas
                    
        # wheel lines
        self.canvas.add(self.color_other)
        with self.canvas: # drawing wheel_lines above know_main
            if self.value_visible:
                self._draw_line(self._calc_pos(self.value_px))
            
            for prefix in [1, -1]: # TODO: replace "prefix" with the right translation for "Vorzeichen"
                x = self._calc_pos(self.value_px)
                x += prefix * (self._calc_seperation(x) + self._calc_line_size(x))
                while abs(x) <= [self.height/2, self.width/2][self.orientation != "vertical"]:
                    line_size = self._draw_line(x)
                    x += prefix * (self._calc_seperation(x) + line_size)
                    if int(self.height-x) == 0:
                        break
        # value line in right color
        if self.value_visible:
            self.canvas.add(self.color_value)
            with self.canvas: # drawing wheel_main
                self._draw_line(self.value_px)
        
    def _calc_lock(self):
        if self.value_lock_type == "pixel":
            return self.value_lock
        else:
            return self.value_lock * (self.height/2)
        
    def _calc_px2dec(self, widget, value):
        self.value = [1./(self.height/2)*value, 1./(self.width/2)*value][self.orientation != "vertical"] ## TODO: Needs correction , so self.value is exactly between -1 and 1
    
    def _calc_pos(self, pos):
        while pos > [self.height/2, self.width/2][self.orientation != "vertical"]:
            pos -= [self.height/2, self.width/2][self.orientation != "vertical"]
        while pos < [-self.height/2, -self.width/2][self.orientation != "vertical"]:
            pos += [self.height/2, self.width/2][self.orientation != "vertical"]
        return pos
    
    def _calc_cos(self, size, x, maxi):
        return (size*math.cos (((1/(float(maxi)*2))*x)*math.pi/(1/self.distance))/(1/self.distance))*(1/self.distance)
    
    def _calc_size2x(self, x, size):
        if self.orientation == "vertical":
            return self._calc_cos( size,x-self.y, self.height/2)
        else:
            return self._calc_cos( size,x-self.x, self.width/2)
        
    def _calc_line_size(self, x):
        return self._calc_size2x( x, self.line_size)
    
    def _calc_seperation(self, x):
        return self._calc_size2x( x, self.seperation_size)
    
    def _draw_line(self, x):
        line_size = self._calc_line_size(x)
        self._draw(line_size, x)
        return line_size
    
    def _draw(self, line_size, x): # maybe later needed to draw shadows
        if self.sharp:
            line_size = math.floor(line_size)
        if  self.orientation == "vertical" and (x > -(self.height/2) and x < (self.height/2)):
            return Rectangle(size=(self.width,line_size), pos=(self.x,x+(self.height/2)-(self.line_size/2)))
        elif self.orientation == "horizontal" and (x > -(self.width/2) and x < (self.width/2)):
            return Rectangle(size=(line_size,self.height), pos=(x+(self.width/2)-(self.line_size/2), self.y))
        
    def on_touch(self, touch):
        ## TODO: Adding check here as used in Button()
        if touch.pos[0] >= self.pos[0] and touch.pos[1] >= self.pos[1] and touch.pos[0] <= (self.pos[0]+self.size[0]) and touch.pos[1] <= (self.pos[1]+self.size[1]):
            if self.mode == "absolute":
                self.value_px = [touch.x-(self.width/2),touch.y-(self.height/2)][self.orientation == "vertical"]
            else:
                self.value_px += [touch.dx,touch.dy][self.orientation == "vertical"]
        return
    
    def on_touch_down(self, touch):
        if not touch.is_mouse_scrolling:
            self.on_touch(touch)
        return Widget.on_touch_move(self, touch)
    
    def on_touch_move(self, touch):
        if not touch.is_mouse_scrolling:
            self.on_touch(touch)
        return Widget.on_touch_move(self, touch)
    
    def on_touch_up(self, touch):
        if self.value_locked:
            self.value_px = self._calc_lock()
            #self.on_widget_change(self, None)
        else:
            if not touch.is_mouse_scrolling:
                self.on_touch(touch)
        return Widget.on_touch_up(self, touch)
    
if __name__ == '__main__':
    from kivy.app import App
    
    class WheelApp(App):
        def build(self):
            w = Wheel()
            return w
    WheelApp().run()