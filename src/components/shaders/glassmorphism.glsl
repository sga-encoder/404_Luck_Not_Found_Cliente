$HEADER$

// Propiedades uniformes que podemos controlar desde Python
uniform float blur_radius;
uniform float opacity;
uniform vec4 tint_color;
uniform vec2 resolution;
uniform float time;

// Función optimizada para desenfoque gaussiano de dos pasadas
vec4 gaussianBlur(sampler2D image, vec2 uv, vec2 pixelSize, float radius) {
    // Primera pasada: desenfoque horizontal
    vec4 hBlur = vec4(0.0);
    float hTotalWeight = 0.0;
    float sigma = radius;
    float blurSize = sigma * 2.5; // Reducido para mejor rendimiento
    
    // Desenfoque horizontal optimizado
    for (float x = -blurSize; x <= blurSize; x += 1.0) {
        float weight = exp(-(x*x) / (2.0 * sigma * sigma));
        hBlur += texture2D(image, uv + vec2(x * pixelSize.x, 0.0)) * weight;
        hTotalWeight += weight;
    }
    hBlur /= hTotalWeight;
    
    // Segunda pasada: desenfoque vertical
    vec4 vBlur = vec4(0.0);
    float vTotalWeight = 0.0;
    
    for (float y = -blurSize; y <= blurSize; y += 1.0) {
        float weight = exp(-(y*y) / (2.0 * sigma * sigma));
        vBlur += texture2D(image, uv + vec2(0.0, y * pixelSize.y)) * weight;
        vTotalWeight += weight;
    }
    vBlur /= vTotalWeight;
    
    // Mezclar los dos desenfoques
    return mix(hBlur, vBlur, 0.5);
}

void main(void)
{
    // Coordenadas de textura normalizadas
    vec2 uv = tex_coord0.xy;
    vec2 pixelSize = 1.0 / resolution;
    
    // Aplicar desenfoque gaussiano optimizado
    vec4 blurredColor = gaussianBlur(texture0, uv, pixelSize, blur_radius);
    
    // Efecto de aberración cromática sutil
    float aberrationStrength = 0.001 + sin(time * 0.2) * 0.0005; // Efecto sutil que varía con el tiempo
    vec4 aberrationR = gaussianBlur(texture0, uv + vec2(aberrationStrength, 0.0), pixelSize, blur_radius);
    vec4 aberrationB = gaussianBlur(texture0, uv - vec2(aberrationStrength, 0.0), pixelSize, blur_radius);
    
    // Crear el efecto de aberración cromática
    blurredColor.r = mix(blurredColor.r, aberrationR.r, 0.15);
    blurredColor.b = mix(blurredColor.b, aberrationB.b, 0.15);
    
    // Aplicar tinte y transparencia con un cálculo mejorado para mayor realismo
    vec3 glassColor = mix(blurredColor.rgb, tint_color.rgb, tint_color.a * 0.8);
    
    // Añadir un sutil efecto de foco (hotspot) en el centro
    vec2 center = vec2(0.5, 0.5);
    float dist = distance(uv, center) * 2.0;
    float hotspot = 1.0 - smoothstep(0.0, 1.0, dist);
    glassColor += vec3(0.1) * hotspot * hotspot * 0.3;
    
    // Efecto de refracción mejorado
    vec2 distortion = vec2(
        sin(uv.y * 15.0 + time * 0.3) * 0.0015,
        cos(uv.x * 15.0 + time * 0.3) * 0.0015
    );
    vec4 refractedColor = texture2D(texture0, uv + distortion);
    
    // Efecto de borde luminoso mejorado (más suave y realista)
    float edgeDistance = min(min(uv.x, 1.0-uv.x), min(uv.y, 1.0-uv.y)) * 12.0;
    float edgeGlow = smoothstep(0.0, 0.8, edgeDistance);
    vec3 edgeColor = mix(vec3(1.0), vec3(0.95, 0.98, 1.0), 0.7); // Color ligeramente azulado
    glassColor += edgeColor * (1.0 - edgeGlow) * 0.25;
    
    // Añadir un ligero ruido para simular imperfecciones del vidrio
    float noise = fract(sin(dot(uv, vec2(12.9898, 78.233)) * 43758.5453 + time * 0.1) * 43758.5453);
    glassColor += (noise - 0.5) * 0.02;
    
    // Ajustar la opacidad final
    vec4 finalColor = vec4(glassColor, opacity);
    
    // Combinar con refracción para un efecto más realista
    gl_FragColor = finalColor * 0.85 + refractedColor * 0.15;
}