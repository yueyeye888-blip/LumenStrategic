const canvas = document.getElementById('world-canvas');
const ctx = canvas.getContext('2d');

let width, height;
let nodes = [];
const numNodes = 120; // Lower density for a cleaner look
let animationFrameId;

// Initialize canvas
function initCanvas() {
    width = window.innerWidth;
    height = window.innerHeight;
    canvas.width = width;
    canvas.height = height;
    createNodes();
}

// Node class representing the network points
class Node {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.vx = (Math.random() - 0.5) * 0.4;
        this.vy = (Math.random() - 0.5) * 0.4;
        this.baseRadius = Math.random() * 2 + 1;
        this.radius = this.baseRadius;
        this.isHub = Math.random() > 0.9; // 10% chance to be a golden hub
        if (this.isHub) {
            this.baseRadius = Math.random() * 3 + 2;
            this.radius = this.baseRadius;
        }
        this.angle = Math.random() * Math.PI * 2;
    }

    update() {
        this.x += this.vx;
        this.y += this.vy;

        // Bounce off walls
        if (this.x < 0 || this.x > width) this.vx *= -1;
        if (this.y < 0 || this.y > height) this.vy *= -1;

        // Pulsing effect
        this.angle += 0.05;
        this.radius = this.baseRadius + Math.sin(this.angle) * 0.5;
    }

    draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        
        if (this.isHub) {
            ctx.fillStyle = 'rgba(212, 175, 55, 0.8)'; // Golden hub
            ctx.shadowBlur = 15;
            ctx.shadowColor = 'rgba(212, 175, 55, 0.6)';
        } else {
            ctx.fillStyle = 'rgba(0, 229, 255, 0.5)'; // Cyan nodes
            ctx.shadowBlur = 0;
        }
        ctx.fill();
        ctx.shadowBlur = 0; // reset
    }
}

// Create nodes clustered roughly like continents (optional, random for now)
function createNodes() {
    nodes = [];
    for (let i = 0; i < numNodes; i++) {
        // Biased distribution toward center-ish
        const x = width * 0.1 + Math.random() * width * 0.8;
        const y = height * 0.1 + Math.random() * height * 0.8;
        nodes.push(new Node(x, y));
    }
}

// Draw connections between nodes
function drawLines() {
    for (let i = 0; i < nodes.length; i++) {
        for (let j = i + 1; j < nodes.length; j++) {
            const dx = nodes[i].x - nodes[j].x;
            const dy = nodes[i].y - nodes[j].y;
            const distance = Math.sqrt(dx * dx + dy * dy);

            if (distance < 160) {
                ctx.beginPath();
                ctx.moveTo(nodes[i].x, nodes[i].y);
                ctx.lineTo(nodes[j].x, nodes[j].y);

                // Line opacity based on distance
                const opacity = 1 - (distance / 160);
                
                // Color based on whether nodes are golden hubs
                if (nodes[i].isHub || nodes[j].isHub) {
                    ctx.strokeStyle = `rgba(212, 175, 55, ${opacity * 0.4})`;
                } else {
                    ctx.strokeStyle = `rgba(0, 229, 255, ${opacity * 0.15})`;
                }
                
                ctx.lineWidth = 1;
                ctx.stroke();
            }
        }
    }
}

// Animation loop
function animate() {
    ctx.clearRect(0, 0, width, height);

    nodes.forEach(node => {
        node.update();
        node.draw();
    });

    drawLines();
    animationFrameId = requestAnimationFrame(animate);
}

// Handle resize
window.addEventListener('resize', () => {
    cancelAnimationFrame(animationFrameId);
    initCanvas();
    animate();
});

// Start
initCanvas();
animate();