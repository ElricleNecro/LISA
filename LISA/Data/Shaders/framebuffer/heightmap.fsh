#version 330

in vec3 worldPosition;
in vec3 modelPosition;

uniform sampler2D image;
uniform mat4 model;
uniform mat4 rotate;
uniform vec3 camera;
uniform float materialShininess;
uniform vec3 materialSpecularColor;

uniform struct Light {
    vec4 position;
    vec3 intensities;
    float attenuation;
    float ambientCoefficient;
    // float coneAngle;
    // vec3 coneDirection;
} light;

out vec4 finalColor;

vec3 ApplyLight(Light light, vec3 surfaceColor, vec3 normal, vec3 surfacePos, vec3 surfaceToCamera) {
    vec3 surfaceToLight;
    float attenuation = 1.0;
    if(light.position.w == 0.0) {
        //directional light
        surfaceToLight = normalize(light.position.xyz);
        attenuation = 1.0; //no attenuation for directional lights
    } else {
        //point light
        surfaceToLight = normalize(light.position.xyz - surfacePos);
        float distanceToLight = length(light.position.xyz - surfacePos);
        attenuation = 1.0 / (1.0 + light.attenuation * pow(distanceToLight, 2));

        //cone restrictions (affects attenuation)
        // float lightToSurfaceAngle = degrees(acos(dot(-surfaceToLight, normalize(light.coneDirection))));
        // if(lightToSurfaceAngle > light.coneAngle){
        //     attenuation = 0.0;
        // }
    }

    //ambient
    vec3 ambient = light.ambientCoefficient * surfaceColor.rgb * light.intensities;

    //diffuse
    float diffuseCoefficient = max(0.0, dot(normal, surfaceToLight));
    vec3 diffuse = diffuseCoefficient * surfaceColor.rgb * light.intensities;

    //specular
    float specularCoefficient = 0.0;
    if(diffuseCoefficient > 0.0)
        specularCoefficient = pow(max(0.0, dot(surfaceToCamera, reflect(-surfaceToLight, normal))), materialShininess);
    vec3 specular = specularCoefficient * materialSpecularColor * light.intensities;

    //linear color (color before gamma correction)
    return ambient + attenuation*(diffuse + specular);
}

void main()
{
    /* vec4 surfaceColor = vec4(1.0, 1.0, 1.0, 1.0); */
    vec4 surfaceColor = texture(image, (modelPosition.xy+1)/2);

    vec3 surfaceToLight = vec3(light.position) - worldPosition;

    vec3 camera_rotated = transpose(mat3(rotate)) * camera;

    // not working I don't know why
    vec3 fragNormal = normalize(cross(dFdx(worldPosition), dFdy(worldPosition)));
    /* vec3 fragNormal = vec3(0, 0, 1); */

    finalColor = vec4(ApplyLight(light, surfaceColor.rgb, fragNormal, worldPosition, normalize(camera_rotated-worldPosition)), 1);
}
