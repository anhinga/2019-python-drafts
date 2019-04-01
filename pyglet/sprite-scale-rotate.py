import time
import pyglet

class Workaround(object):

    def __init__(self):
        self.total_time = 0
	
workaround = Workaround()

workaround.total_time = 0.0
print("init: ", workaround.total_time)

#time.sleep(5)

image = pyglet.image.load('Before elections 015.JPG')
sprite = pyglet.sprite.Sprite(image)

config = pyglet.gl.Config(sample_buffers=1, samples=4)

window = pyglet.window.Window(config=config, resizable=True)

fps_display = pyglet.clock.ClockDisplay()

def update(dt):
    #sprite.scale *= 0.999
    #print("continue: ", workaround.total_time) 
    workaround.total_time += dt
    sprite.scale = 10.0/workaround.total_time
    sprite.rotation -= 1.0
    print("%6.2f %6.2f %f %f" % (workaround.total_time, pyglet.clock.get_fps(), sprite.scale, sprite.rotation))

pyglet.clock.schedule_interval(update, 0.01)

@window.event
def on_draw():
    sprite.draw()
    fps_display.draw()   

pyglet.app.run()