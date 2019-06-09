#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vispy: gallery 2, testskip
# Copyright (c) Vispy Development Team. All Rights Reserved.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.

"""
Shadertoy demo. You can copy-paste shader code from an example on
www.shadertoy.com and get the demo.

TODO: support cubes and videos as channel inputs (currently, only images
are supported).

"""

# NOTE: This example throws warnings about variables not being used;
# this is normal because only some shadertoy examples make use of all
# variables, and the GPU may compile some of them away.

import sys
from datetime import datetime, time
import numpy as np
from vispy import gloo
from vispy import app


vertex = """
#version 120

attribute vec2 position;
void main()
{
    gl_Position = vec4(position, 0.0, 1.0);
}
"""

fragment = """
#version 120

uniform vec3      iResolution;           // viewport resolution (in pixels)
uniform float     iGlobalTime;           // shader playback time (in seconds)
uniform vec4      iMouse;                // mouse pixel coords
uniform vec4      iDate;                 // (year, month, day, time in seconds)
uniform float     iSampleRate;           // sound sample rate (i.e., 44100)
uniform sampler2D iChannel0;             // input channel. XX = 2D/Cube
uniform sampler2D iChannel1;             // input channel. XX = 2D/Cube
uniform sampler2D iChannel2;             // input channel. XX = 2D/Cube
uniform sampler2D iChannel3;             // input channel. XX = 2D/Cube
uniform vec3      iChannelResolution[4]; // channel resolution (in pixels)
uniform float     iChannelTime[4];       // channel playback time (in sec)

uniform float     iControl; // custom control
uniform float     iControl1; // second custom control

%s
"""


def get_idate():
    now = datetime.now()
    utcnow = datetime.utcnow()
    midnight_utc = datetime.combine(utcnow.date(), time(0))
    delta = utcnow - midnight_utc
    return (now.year, now.month, now.day, delta.seconds)


def noise(resolution=64, nchannels=1):
    # Random texture.
    return np.random.randint(low=0, high=256,
                             size=(resolution, resolution, nchannels)
                             ).astype(np.uint8)


class Canvas(app.Canvas):

    def __init__(self, shadertoy=None):
        app.Canvas.__init__(self, keys='interactive', size=(1600, 900))
        if shadertoy is None:
            shadertoy = """
            void main(void)
            {
                vec2 uv = gl_FragCoord.xy / iResolution.xy;
                gl_FragColor = vec4(uv,0.5+0.5*sin(iGlobalTime),1.0);
            }"""
        self.program = gloo.Program(vertex, fragment % shadertoy)

        self.program["position"] = [(-1, -1), (-1, 1), (1, 1),
                                    (-1, -1), (1, 1), (1, -1)]
        self.program['iMouse'] = 0, 0, 0, 0
        
        self.program['iControl'] = 0.0
        
        self.program['iControl1'] = 0.0

        self.program['iSampleRate'] = 44100.
        for i in range(4):
            self.program['iChannelTime[%d]' % i] = 0.
        self.program['iGlobalTime'] = 0.

        self.activate_zoom()

        self._timer = app.Timer('auto', connect=self.on_timer, start=True)

        self.show()

    def set_channel_input(self, img, i=0):
        tex = gloo.Texture2D(img)
        tex.interpolation = 'linear'
        tex.wrapping = 'repeat'
        self.program['iChannel%d' % i] = tex
        self.program['iChannelResolution[%d]' % i] = img.shape

    def on_draw(self, event):
        self.program.draw()

    def on_mouse_click(self, event):
        # BUG: DOES NOT WORK YET, NO CLICK EVENT IN VISPY FOR NOW...
        imouse = event.pos + event.pos
        self.program['iMouse'] = imouse

    def on_mouse_move(self, event):
        if event.is_dragging:
            x, y = event.pos
            px, py = event.press_event.pos
            imouse = (x, self.size[1] - y, px, self.size[1] - py)
            self.program['iMouse'] = imouse
            
    def on_key_press(self, event):
        if event.key == 'a' or event.key == 'A':
            self.program['iControl'] = 1 # self.program['iControl']+0.5
        if event.key == 'l' or event.key == 'L':
            self.program['iControl'] = 0 # self.program['iControl']-0.5 
        if event.key == 'q' or event.key == 'Q':
            self.program['iControl1'] = 1 
        if event.key == 'p' or event.key == 'P':
            self.program['iControl1'] = 0 
        if event.key == '1':
            self.program['iControl'] = 0
            self.program['iControl1'] = 0
        if event.key == '2':
            self.program['iControl'] = 0
            self.program['iControl1'] = 1
        if event.key == '3':
            self.program['iControl'] = 1
            self.program['iControl1'] = 1            

    def on_timer(self, event):
        self.program['iGlobalTime'] = event.elapsed
        self.program['iDate'] = get_idate()  # used in some shadertoy exs
        self.update()

    def on_resize(self, event):
        self.activate_zoom()

    def activate_zoom(self):
        gloo.set_viewport(0, 0, *self.physical_size)
        self.program['iResolution'] = (self.physical_size[0],
                                       self.physical_size[1], 0.)

# -------------------------------------------------------------------------
# COPY-PASTE SHADERTOY CODE BELOW
# -------------------------------------------------------------------------
SHADERTOY = """
float fract_sin_dot (vec2 uv) {
    return fract(sin(dot(
                         mix(uv.xy,
                             mix(vec2(sin(4.*uv.x), sin(10.*uv.y)),
                                 vec2(sin(4.*uv.x), uv.y),
                                 iControl),
                             iControl1),
                         0.1*iMouse.xy))*
        4. + 0.5*iGlobalTime);
}

void main( void )
{
    vec2 uv = gl_FragCoord.xy/iResolution.xy;

    float value = fract_sin_dot( uv );

    gl_FragColor = vec4(vec3(value),1.0);
}
"""
# -------------------------------------------------------------------------

canvas = Canvas(SHADERTOY)
# Input data.
canvas.set_channel_input(noise(resolution=256, nchannels=1), i=0)

if __name__ == '__main__':

    canvas.show()
    if sys.flags.interactive == 0:
        canvas.app.run()
