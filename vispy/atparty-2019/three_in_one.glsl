float fract_sin_dot (vec2 uv) {
        return fract(sin(dot(
                         uv.xy,
                         // vec2(sin(4.*uv.x), sin(10.*uv.y)),
                         // vec2(sin(4.*uv.x), uv.y),
                         0.1*iMouse.xy+vec2(1.0,1.0)))*
        4. + 0.5*iTime);
}

void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
    vec2 uv = fragCoord/iResolution.xy;

    vec3 color = vec3(fract_sin_dot( uv ),
                      fract_sin_dot( vec2(sin(4.*uv.x), sin(10.*uv.y)) ),
                      fract_sin_dot( vec2(sin(4.*uv.x), uv.y) ));

    fragColor = vec4(color,1.0);
}
