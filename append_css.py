css = '''
/* Dynamic Service Icons Animations */
.anim-spin-slow { animation: spinSlow 8s linear infinite; transform-origin: center; }
@keyframes spinSlow { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
.anim-float-up { animation: floatUp 2s ease-in-out infinite; }
@keyframes floatUp { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-4px); } }
.anim-float-down { animation: floatDown 2s ease-in-out infinite; }
@keyframes floatDown { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(4px); } }
.anim-bar-1 { animation: barGrow 1.5s ease-in-out infinite alternate; transform-origin: left bottom; }
.anim-bar-2 { animation: barGrow 1.5s ease-in-out infinite alternate 0.5s; transform-origin: left bottom; }
.anim-bar-3 { animation: barGrow 1.5s ease-in-out infinite alternate 1s; transform-origin: left bottom; }
@keyframes barGrow { 0% { transform: scaleY(0.3); opacity: 0.5; } 100% { transform: scaleY(1); opacity: 1; } }
.anim-pulse-line { stroke-dasharray: 60; stroke-dashoffset: 60; animation: lineDash 2.5s ease-in-out infinite alternate; }
@keyframes lineDash { 0% { stroke-dashoffset: 60; } 100% { stroke-dashoffset: 0; } }
.anim-fade { animation: fadeInOut 2.5s ease-in-out infinite alternate; }
@keyframes fadeInOut { 0% { opacity: 0; transform: scale(0.5); transform-origin: center; } 100% { opacity: 1; transform: scale(1.2); transform-origin: center; } }
.service-icon-svg { filter: drop-shadow(0 0 10px rgba(249, 217, 118, 0.4)); transition: transform 0.3s ease, filter 0.3s ease; }
.card:hover .service-icon-svg { transform: scale(1.15) translateY(-5px); filter: drop-shadow(0 0 15px rgba(249, 217, 118, 0.8)); }
'''
with open('/Users/xingxiu/Desktop/Fluxium网站/css/main.css', 'a') as f:
    f.write(css)
