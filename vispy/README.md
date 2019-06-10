A modification of https://github.com/vispy/vispy/blob/master/examples/demo/gloo/cloud.py

To install [VisPy](http://vispy.org/), `pip install --upgrade vispy` (or other variants mentioned in VisPy documentation)

To run example, `python vispy_example.py`

The main differences from the original:

1) we establish that we can change data outside shaders (by pressing 'a' and 'b' keys):

```
248a249,251
>         self.n = n
>         self.data = data
>
263a267,273
>         if event.text == 'a':
>             self.data['a_position'] = 0.99*self.data['a_position']  #0.15 * np.random.randn(self.n, 3)
>             self.program.bind(gloo.VertexBuffer(self.data))
>         if event.text == 'b':
>             self.data['a_position'] = 1.01*self.data['a_position']  #0.15 * np.random.randn(self.n, 3)
>             self.program.bind(gloo.VertexBuffer(self.data))
>
```

2) we measure 'frames per second" (this way you can see what is the cost of changing data outside shaders by pressing and holding either 'a' or 'b' and seeing how it affects the frame rate): 

```
297a310
>     c.measure_fps()
```

***

Among the key features of VisPy is that one can include _vertex shaders_ and _fragment shaders_ (also known as _pixel shaders_)  written in GLSL (OpenGL Shading Language) and represented as strings into Python code. 

In the `vispy_example.py` in this directory, the vertex shader program is at lines 16-50 and the fragment shader program is at lines 54-210, so this is an example of a really shader-heavy code (35+155=190 lines are in shaders, that's out of the 311 lines of the overall length of `vispy_example.py`).

[The Book of Shaders](https://thebookofshaders.com/) is a nice tutorial book on fragment shaders.

***

And, more specifically, [the chapter on Fractal Brownian Motion](https://thebookofshaders.com/13/) references the website of Íñigo Quílez, and, in particular, his articles on [advanced value noise](http://www.iquilezles.org/www/articles/morenoise/morenoise.htm) and [domain warping](http://www.iquilezles.org/www/articles/warp/warp.htm).

The first of these articles provides information on how his famous [Elevated](http://www.iquilezles.org/prods/index.htm#elevated) 4 kb intro is made. I wanted to understand that one since I first seen it a few years ago.

To link this back to VisPy examples, the Shadertoy program https://www.shadertoy.com/view/MdX3Rr is implemented by https://github.com/vispy/vispy/blob/master/examples/demo/gloo/shadertoy.py (if you have VisPy installed, just run `python shadertoy.py` to reproduce this Shadertoy animation).

***

The materials for my @party 2019 compo entry related to VisPy and shaders are in `atparty-2019` subdirectory.
