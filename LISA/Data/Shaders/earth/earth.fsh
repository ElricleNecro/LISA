#version 130

out vec4 vfragColor;

uniform sampler2D map;

in vec3 texcoord;

void main()
{
    vec2 longitudeLatitude = vec2(
        (atan(texcoord.y, texcoord.x) / 3.1415926 + 1.0) * 0.5,
        (asin(texcoord.z) / 3.1415926 + 0.5)
    );
    vfragColor = vec4(texture2D(map, longitudeLatitude).rgb, 1.);
}
