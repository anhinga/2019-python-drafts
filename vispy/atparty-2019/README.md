### Materials related to my June 8, 2019 compo entry for @party, http://atparty-demoscene.net/. 

The code traces its origins to the random number generator from Chapter 10 of "The Book of Shaders": https://thebookofshaders.com/10/

```c
float random (vec2 st) {
    return fract(sin(dot(st.xy,
                         vec2(12.9898,78.233)))*
        43758.5453123);
}
```

It is possible to edit the code on the book site and observe the changes. One can note that when one gradually replaces `43758.5453123` by `4375.`, `437.`, `43.`, and `4.`, the image acquires more and more non-random structure.

Then, if one replaces `vec2(12.9898,78.233)` with the current mouse position, one obtains an interactive shader controlled by mouse. 

```c
float fract_sin_dot (vec2 uv) {
    return fract(sin(dot(uv.xy,
                         iMouse.xy))*
        4.);
}
```

It turned out that images tend to be more interesting when the mouse coordinates are low, so I rescaled the mouse vector multiplying it by `0.1`.

Then I added time to the argument of `fract`, and this way the shader became animated. I thought it is better to slow the animation down somewhat by multiplying time by 0.5, resulting in this code fragment:

```c
float fract_sin_dot (vec2 uv) {
    return fract(sin(dot(
                         uv.xy,
                         0.1*iMouse.xy))*
        4. + 0.5*iTime);
}
```

Finally, I added the alternatives, `vec2(sin(4.*uv.x), sin(10.*uv.y))` and `vec2(sin(4.*uv.x), uv.y)`. One can use them instead of `uv.xy` in the dot product for more interesting patterns.

***

At this stage, I ported this shader into VisPy (I describe this port next). The VisPy-based Python code was used in the interactive presentation during @party compos.

I have now made the Shadertoy version available on the Shadertoy site: https://www.shadertoy.com/view/WlSGzK

(The difference is, the `vec2(sin(4.*uv.x), sin(10.*uv.y))` is now the starting version on the Shadertoy site (this version is committed here as **demo.glsl**), and I added 1 pixel to the mouse position, `0.1*iMouse.xy+vec2(1.0,1.0)`, so that the initial state is not blank.)

![Image](https://www.shadertoy.com/media/shaders/WlSGzK.jpg "a shader")

***

I took the https://github.com/vispy/vispy/blob/master/examples/demo/gloo/shadertoy.py example, and replaced the shader there with my shader (the resulting file is committed as **second-demo-shadertoy.py**).

The following differences were necessary during this port: I had to replace `void mainImage( out vec4 fragColor, in vec2 fragCoord )` with `void main( void )`. I had to use `gl_FragCoord.xy` instead of `fragCoord`, and `gl_FragColor` instead of `fragColor`.

I added the ability to switch between
  * `uv.xy`
  * `vec2(sin(4.*uv.x), sin(10.*uv.y))`
  * `vec2(sin(4.*uv.x), uv.y)`
  
by pressing numeric keys `1`, `2`, `3`. To accomplish that I had to change the shader somewhat and to add following function to the OpenGL part:

```python
    def on_key_press(self, event):
        if event.key == '1':
            self.program['iControl'] = 0
            self.program['iControl1'] = 0
        if event.key == '2':
            self.program['iControl'] = 0
            self.program['iControl1'] = 1
        if event.key == '3':
            self.program['iControl'] = 1
            self.program['iControl1'] = 1   
```

I have also added some control by letters with a somewhat different logic, but that was probably a mistake.

If one were to add keyboard control on the Shadertoy site, the code doing that would be quite different (they have a dedicated "texture keyboard" for this).

Another difference with the Shadertoy site is that mouse click event does not work in VisPy right now, **one has to drag the mouse to communicate with the program**:

```python
    def on_mouse_click(self, event):
        # BUG: DOES NOT WORK YET, NO CLICK EVENT IN VISPY FOR NOW...
        imouse = event.pos + event.pos
        self.program['iMouse'] = imouse
```

On the positive side, it is much easier to generate negative values for the mouse pointer in VisPy by dragging the mouse below or to the left of the image (the coordinate origin is at the lower left corner in this program), and those negative values produce interesting effects.

I was advised to add mouse position logging to **second-demo-shadertoy.py** to file (or to console) to aid reproducibility of the observed patterns. Some simple-minded code which prints on console can be achieved by additing one more line to `on_mouse_move` function, for example:

```python
    def on_mouse_move(self, event):
        if event.is_dragging:
            x, y = event.pos
            px, py = event.press_event.pos
            imouse = (x, self.size[1] - y, px, self.size[1] - py)
            self.program['iMouse'] = imouse
            print("x,y: ", x, y, " px,py: ", px, py, " imouse: ", imouse)
```

***

Performance recording: https://scenesat.com/videoarchive/118 preparations starting at 11:38:07 and the demo at 11:40:55 time mark (11 hours 40 min 55 sec, in case the URL changes, that is "2019-06-09 @-party 2019 - Day 2 (12h55m4s hours)").

(I did forget to bring the mouse which I had with me to the scene, so the interactive control was somewhat less fluent than what I can achieve with an external mouse. The compos started at 2:15am (rather than at planned time of 10:30pm), and were running till about 4am.)

***

### Post-@party

A colorized shader (all 3 modes at different color channels): https://www.shadertoy.com/view/WlS3RV

![Image](https://www.shadertoy.com/media/shaders/WlS3RV.jpg "a shader")

One of the possible double warps here: https://www.shadertoy.com/view/3tSGzV

![Image](https://www.shadertoy.com/media/shaders/3tSGzV.jpg "a shader")
