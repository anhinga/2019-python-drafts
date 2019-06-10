Materials related to my June 8, 2019 compo entry for @party, http://atparty-demoscene.net/. The code traces its origins to the random number generator from Chapter 10 of "The Book of Shaders": https://thebookofshaders.com/10/

```c
float random (vec2 st) {
    return fract(sin(dot(st.xy,
                         vec2(12.9898,78.233)))*
        43758.5453123);
}
```

It is possible to edit the code on the book site and observe the changes. One can note that when one gradually replaces `43758.5453123` by `4375.`, `437.`, `43.`, and `4.`, the image acquires more and more non-random structure.

Then, if one replaces `vec2(12.9898,78.233)` with the current mouse position, one can create an interactive animation. 

```c
float fract_sin_dot (vec2 uv) {
    return fract(sin(dot(uv.xy,
                         iMouse.xy))*
        4.);
}
```

It turns out that images tend to be more interesting when the mouse coordinates are low, so we rescale the mouse vector multiplying it by `0.1`.

Then we add time to the argument of `fract`, and this way the shader becomes animated. We thought it is better to slow the animation down somewhat by multiplying time by 0.5, resulting in this code fragment:

```c
float fract_sin_dot (vec2 uv) {
    return fract(sin(dot(
                         uv.xy,
                         0.1*iMouse.xy))*
        4. + 0.5*iTime);
}
```

Finally, we add the alternatives, `vec2(sin(4.*uv.x), sin(10.*uv.y))` and `vec2(sin(4.*uv.x), uv.y)`. One can use them instead of `uv.xy` in the dot product for more interesting patterns.

***

**IN PROGRESS...**
