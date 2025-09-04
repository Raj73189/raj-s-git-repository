class SolarSystem {
    constructor() {
        this.canvas = document.getElementById('particleCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.planets = [];
        this.stars = [];
        this.spaceDust = [];
        this.nebulas = [];
        this.sun = { 
            x: this.canvas.width / 2, 
            y: this.canvas.height / 2, 
            radius: 60,
            glowRadius: 120
        };
        
        this.init();
        this.animate();
        this.setupEventListeners();
    }

    init() {
        this.resizeCanvas();
        this.createStars();
        this.createPlanets();
        this.createSpaceDust();
        this.createNebulas();
    }

    resizeCanvas() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
        this.sun.x = this.canvas.width / 2;
        this.sun.y = this.canvas.height / 2;
    }

    createStars() {
        this.stars = [];
        const starCount = 500;
        for (let i = 0; i < starCount; i++) {
            this.stars.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                size: Math.random() * 2 + 0.5,
                brightness: Math.random() * 0.8 + 0.2,
                twinkleSpeed: Math.random() * 0.02 + 0.01,
                twinkleOffset: Math.random() * Math.PI * 2
            });
        }
    }

    createSpaceDust() {
        this.spaceDust = [];
        const dustCount = 100;
        for (let i = 0; i < dustCount; i++) {
            this.spaceDust.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                size: Math.random() * 1 + 0.3,
                speed: Math.random() * 0.2 + 0.1,
                angle: Math.random() * Math.PI * 2
            });
        }
    }

    createNebulas() {
        this.nebulas = [];
        const nebulaCount = 3;
        for (let i = 0; i < nebulaCount; i++) {
            this.nebulas.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                radius: Math.random() * 200 + 100,
                color: `rgba(${Math.random() * 100 + 100}, ${Math.random() * 100 + 50}, ${Math.random() * 200 + 50}, 0.1)`,
                pulseSpeed: Math.random() * 0.01 + 0.005,
                pulseOffset: Math.random() * Math.PI * 2
            });
        }
    }

    createPlanets() {
        const planetData = [
            { name: 'Mercury', distance: 80, size: 6, color: '#8C8C8C', speed: 0.12, texture: true },
            { name: 'Venus', distance: 120, size: 12, color: '#E6E6B8', speed: 0.09, texture: true },
            { name: 'Earth', distance: 160, size: 12, color: '#4B92D4', speed: 0.07, texture: true, hasClouds: true },
            { name: 'Mars', distance: 200, size: 10, color: '#C1440E', speed: 0.06, texture: true },
            { name: 'Jupiter', distance: 260, size: 25, color: '#D8CA9D', speed: 0.04, texture: true, hasBands: true },
            { name: 'Saturn', distance: 320, size: 22, color: '#E3D8B0', speed: 0.03, texture: true, hasRings: true, ringSize: 35 },
            { name: 'Uranus', distance: 380, size: 18, color: '#ACE5EE', speed: 0.02, texture: true },
            { name: 'Neptune', distance: 440, size: 18, color: '#3454D1', speed: 0.015, texture: true }
        ];

        planetData.forEach(data => {
            this.planets.push({ 
                ...data, 
                angle: Math.random() * Math.PI * 2,
                rotation: Math.random() * Math.PI * 2,
                rotationSpeed: Math.random() * 0.02 + 0.01
            });
        });
    }

    drawStars() {
        this.stars.forEach(star => {
            const brightness = star.brightness + Math.sin(Date.now() * star.twinkleSpeed + star.twinkleOffset) * 0.3;
            this.ctx.globalAlpha = Math.max(0, brightness);
            this.ctx.fillStyle = 'white';
            this.ctx.beginPath();
            this.ctx.arc(star.x, star.y, star.size, 0, Math.PI * 2);
            this.ctx.fill();
        });
        this.ctx.globalAlpha = 1;
    }

    drawSpaceDust() {
        this.spaceDust.forEach(dust => {
            dust.x += Math.cos(dust.angle) * dust.speed;
            dust.y += Math.sin(dust.angle) * dust.speed;
            
            if (dust.x < 0) dust.x = this.canvas.width;
            if (dust.x > this.canvas.width) dust.x = 0;
            if (dust.y < 0) dust.y = this.canvas.height;
            if (dust.y > this.canvas.height) dust.y = 0;

            this.ctx.globalAlpha = 0.3;
            this.ctx.fillStyle = 'rgba(255, 255, 255, 0.5)';
            this.ctx.beginPath();
            this.ctx.arc(dust.x, dust.y, dust.size, 0, Math.PI * 2);
            this.ctx.fill();
        });
        this.ctx.globalAlpha = 1;
    }

    drawNebulas() {
        this.nebulas.forEach(nebula => {
            const pulse = Math.sin(Date.now() * nebula.pulseSpeed + nebula.pulseOffset) * 0.1 + 0.9;
            const gradient = this.ctx.createRadialGradient(
                nebula.x, nebula.y, 0,
                nebula.x, nebula.y, nebula.radius * pulse
            );
            gradient.addColorStop(0, nebula.color);
            gradient.addColorStop(1, 'transparent');

            this.ctx.globalAlpha = 0.15;
            this.ctx.fillStyle = gradient;
            this.ctx.beginPath();
            this.ctx.arc(nebula.x, nebula.y, nebula.radius * pulse, 0, Math.PI * 2);
            this.ctx.fill();
        });
        this.ctx.globalAlpha = 1;
    }

    drawSun() {
        // Sun glow
        const gradient = this.ctx.createRadialGradient(
            this.sun.x, this.sun.y, 0,
            this.sun.x, this.sun.y, this.sun.glowRadius
        );
        gradient.addColorStop(0, 'rgba(255, 255, 200, 0.8)');
        gradient.addColorStop(0.5, 'rgba(255, 200, 100, 0.4)');
        gradient.addColorStop(1, 'rgba(255, 150, 50, 0)');

        this.ctx.globalAlpha = 0.6;
        this.ctx.fillStyle = gradient;
        this.ctx.beginPath();
        this.ctx.arc(this.sun.x, this.sun.y, this.sun.glowRadius, 0, Math.PI * 2);
        this.ctx.fill();

        // Sun core
        this.ctx.globalAlpha = 1;
        this.ctx.fillStyle = '#FFD700';
        this.ctx.beginPath();
        this.ctx.arc(this.sun.x, this.sun.y, this.sun.radius, 0, Math.PI * 2);
        this.ctx.fill();

        // Sun texture
        this.ctx.fillStyle = '#FFA500';
        for (let i = 0; i < 20; i++) {
            const angle = Math.random() * Math.PI * 2;
            const distance = Math.random() * this.sun.radius * 0.8;
            const size = Math.random() * 8 + 2;
            const x = this.sun.x + Math.cos(angle) * distance;
            const y = this.sun.y + Math.sin(angle) * distance;
            this.ctx.beginPath();
            this.ctx.arc(x, y, size, 0, Math.PI * 2);
            this.ctx.fill();
        }
    }

    drawPlanet(planet) {
        planet.angle += planet.speed;
        planet.rotation += planet.rotationSpeed;
        const x = this.sun.x + planet.distance * Math.cos(planet.angle);
        const y = this.sun.y + planet.distance * Math.sin(planet.angle);

        // Draw planet
        this.ctx.fillStyle = planet.color;
        this.ctx.beginPath();
        this.ctx.arc(x, y, planet.size, 0, Math.PI * 2);
        this.ctx.fill();

        // Draw planet texture
        if (planet.texture) {
            this.ctx.fillStyle = this.lightenColor(planet.color, 0.2);
            for (let i = 0; i < 5; i++) {
                const textureAngle = Math.random() * Math.PI * 2;
                const textureDist = Math.random() * planet.size * 0.7;
                const textureSize = Math.random() * planet.size * 0.3 + 1;
                const tx = x + Math.cos(textureAngle + planet.rotation) * textureDist;
                const ty = y + Math.sin(textureAngle + planet.rotation) * textureDist;
                this.ctx.beginPath();
                this.ctx.arc(tx, ty, textureSize, 0, Math.PI * 2);
                this.ctx.fill();
            }
        }

        // Draw Saturn's rings
        if (planet.hasRings) {
            this.ctx.strokeStyle = '#D8C690';
            this.ctx.lineWidth = 4;
            this.ctx.beginPath();
            this.ctx.ellipse(x, y, planet.ringSize, planet.ringSize * 0.3, planet.rotation, 0, Math.PI * 2);
            this.ctx.stroke();
        }
    }

    lightenColor(color, amount) {
        const hex = color.replace('#', '');
        const num = parseInt(hex, 16);
        const r = Math.min(255, ((num >> 16) + amount * 255));
        const g = Math.min(255, ((num >> 8 & 0x00FF) + amount * 255));
        const b = Math.min(255, ((num & 0x0000FF) + amount * 255));
        return `#${((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1)}`;
    }

    drawPlanets() {
        this.planets.forEach(planet => {
            this.drawPlanet(planet);
        });
    }

    animate() {
        requestAnimationFrame(this.animate.bind(this));
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.drawStars();
        this.drawNebulas();
        this.drawSpaceDust();
        this.drawSun();
        this.drawPlanets();
    }

    setupEventListeners() {
        window.addEventListener('resize', () => {
            this.resizeCanvas();
            this.createStars();
            this.createSpaceDust();
            this.createNebulas();
        });
    }
}

// Initialize the solar system animation when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new SolarSystem();
});
