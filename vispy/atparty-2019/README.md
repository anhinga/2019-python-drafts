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

Then, if one replaces `vec2(12.9898,78.233)` with the current mouse position, one obtains an interactive animation controlled by mouse. 

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

At this stage, I ported this shader into VisPy (I describe this port next). The VisPy-based Python code was used in the interactive presentation during @party compoes.

I have now made the Shadertoy version available on the Shadertoy site: https://www.shadertoy.com/view/WlSGzK

(The difference is, the `vec2(sin(4.*uv.x), sin(10.*uv.y))` is now the starting version on the Shadertoy site (this version is committed here as **demo.glsl**), and I added 1 pixel to the mouse position, `0.1*iMouse.xy+vec2(1.0,1.0)`, so that the initial state is not blank.)

***

I took the https://github.com/vispy/vispy/blob/master/examples/demo/gloo/shadertoy.py example, and replaced the shader there with my shader (the resulting file is committed as **second-demo-shadertoy.py**).

The following differences were necessary during this port: I had to replace `void mainImage( out vec4 fragColor, in vec2 fragCoord )` by `void main( void )`. I had to use `gl_FragCoord.xy` instead of `fragCoord`, and `gl_FragColor` instead of `fragColor`.

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


**IN PROGRESS...**
