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
>             self.data['a_position'] = 0.99*self.data['a_position']  #0.15 * np.random.randn(                                                                                 self.n, 3)
>             self.program.bind(gloo.VertexBuffer(self.data))
>         if event.text == 'b':
>             self.data['a_position'] = 1.01*self.data['a_position']  #0.15 * np.random.randn(                                                                                 self.n, 3)
>             self.program.bind(gloo.VertexBuffer(self.data))
>
```

2) we measure 'frames per second" (this way you can see what is the cost of changing data outside shaders by pressing and holding either 'a' or 'b' and seeing how it affects the frame rate): 

```
297a310
>     c.measure_fps()
```
