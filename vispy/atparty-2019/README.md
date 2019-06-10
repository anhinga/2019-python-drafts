Materials related to my June 8, 2019 compo entry for @party, http://atparty-demoscene.net/. The code traces its origins to the random number generator from Chapter 10 of "The Book of Shaders": https://thebookofshaders.com/10/

```c
float random (vec2 st) {
    return fract(sin(dot(st.xy,
                         vec2(12.9898,78.233)))*
        43758.5453123);
}
```

It is possible to edit the code on the book site and observe the changes. One can note that when one gradually replaces `43758.5453123` by 4375., 437., 43., and 4., the image acquires more and more non-random structure.

