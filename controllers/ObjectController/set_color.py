def getIfromRGB(rgb):
    red = rgb[0]
    green = rgb[1]
    blue = rgb[2]
    RGBint = (red<<16) + (green<<8) + blue
    return RGBint

def set_color(self, color, alpha):
    self.color = color
    
    self.display.setColor(getIfromRGB(color))
    self.display.setAlpha(alpha)
    self.display.fillOval(int(self.display.getWidth()/2), int(self.display.getHeight()/2), 200, 200)