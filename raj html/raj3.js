// 3D Particle Animation for Background
class ParticleAnimation {
    constructor() {
        this.canvas = document.getElementById('particleCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.particles = [];
        this.mouse = { x: 0, y: 0, radius: 100 };
        
        this.init();
        this.animate();
        this.setupEventListeners();
    }

    init() {
        // Set canvas size
        this.resizeCanvas();
        
        // Create particles
        this.createParticles();
    }

    resizeCanvas() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }

    createParticles() {
        const particleCount = 150;
        const colors = [
            'rgba(102, 126, 234, 0.6)',
            'rgba(118, 75, 162, 0.6)',
            'rgba(255, 255, 255, 0.4)'
        ];

        for (let i = 0; i < particleCount; i++) {
            this.particles.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                size: Math.random() * 3 + 1,
                speedX: Math.random() * 3 - 1.5,
                speedY: Math.random() * 3 - 1.5,
                color: colors[Math.floor(Math.random() * colors.length)],
                angle: Math.random() * Math.PI * 2,
                waveAmplitude: Math.random() * 2 + 1
            });
        }
    }

    drawParticles() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Draw connections between particles
        this.drawConnections();
        
        // Draw individual particles
        this.particles.forEach(particle => {
            this.ctx.beginPath();
            this.ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
            this.ctx.fillStyle = particle.color;
            this.ctx.fill();
            
            // Add glow effect
            this.ctx.shadowBlur = 15;
            this.ctx.shadowColor = particle.color;
        });

        this.ctx.shadowBlur = 0;
    }

    drawConnections() {
        for (let i = 0; i < this.particles.length; i++) {
            for (let j = i + 1; j < this.particles.length; j++) {
                const dx = this.particles[i].x - this.particles[j].x;
                const dy = this.particles[i].y - this.particles[j].y;
                const distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < 100) {
                    const opacity = 1 - distance / 100;
                    this.ctx.beginPath();
                    this.ctx.strokeStyle = `rgba(255, 255, 255, ${opacity * 0.2})`;
                    this.ctx.lineWidth = 0.5;
                    this.ctx.moveTo(this.particles[i].x, this.particles[i].y);
                    this.ctx.lineTo(this.particles[j].x, this.particles[j].y);
                    this.ctx.stroke();
                }
            }
        }
    }

    updateParticles() {
        this.particles.forEach(particle => {
            // Add wave motion
            particle.angle += 0.02;
            particle.x += Math.sin(particle.angle) * particle.waveAmplitude * 0.3;
            particle.y += Math.cos(particle.angle) * particle.waveAmplitude * 0.3;

            // Mouse interaction
            const dx = particle.x - this.mouse.x;
            const dy = particle.y - this.mouse.y;
            const distance = Math.sqrt(dx * dx + dy * dy);
            
            if (distance < this.mouse.radius) {
                const angle = Math.atan2(dy, dx);
                const force = (this.mouse.radius - distance) / this.mouse.radius;
                particle.x += Math.cos(angle) * force * 5;
                particle.y += Math.sin(angle) * force * 5;
            }

            // Bounce off walls with 3D perspective effect
            if (particle.x < 0 || particle.x > this.canvas.width) {
                particle.speedX = -particle.speedX;
                particle.x = particle.x < 0 ? 0 : this.canvas.width;
            }
            if (particle.y < 0 || particle.y > this.canvas.height) {
                particle.speedY = -particle.speedY;
                particle.y = particle.y < 0 ? 0 : this.canvas.height;
            }

            // Move particles
            particle.x += particle.speedX;
            particle.y += particle.speedY;
        });
    }

    animate() {
        requestAnimationFrame(this.animate.bind(this));
        this.updateParticles();
        this.drawParticles();
    }

    setupEventListeners() {
        window.addEventListener('resize', () => {
            this.resizeCanvas();
        });

        window.addEventListener('mousemove', (e) => {
            this.mouse.x = e.clientX;
            this.mouse.y = e.clientY;
        });

        // Touch events for mobile
        window.addEventListener('touchmove', (e) => {
            e.preventDefault();
            this.mouse.x = e.touches[0].clientX;
            this.mouse.y = e.touches[0].clientY;
        });
    }
}

// Form animations and interactions
class FormAnimations {
    constructor() {
        this.setupFormInteractions();
    }

    setupFormInteractions() {
        const inputs = document.querySelectorAll('input');
        const button = document.querySelector('.btn');
        const form = document.querySelector('form');

        inputs.forEach(input => {
            input.addEventListener('focus', () => {
                input.parentElement.style.transform = 'translateZ(20px)';
                input.parentElement.style.borderBottomColor = 'rgba(255, 255, 255, 0.8)';
            });

            input.addEventListener('blur', () => {
                input.parentElement.style.transform = 'translateZ(10px)';
                input.parentElement.style.borderBottomColor = 'rgba(255, 255, 255, 0.2)';
            });
        });

        button.addEventListener('mouseenter', () => {
            button.style.transform = 'translateY(-5px) translateZ(20px)';
        });

        button.addEventListener('mouseleave', () => {
            button.style.transform = 'translateY(0px) translateZ(15px)';
        });

        form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.animateFormSubmission();
        });
    }

    animateFormSubmission() {
        const button = document.querySelector('.btn');
        const inputs = document.querySelectorAll('input');
        
        // Button loading animation
        button.style.background = 'linear-gradient(45deg, #4CAF50, #45a049)';
        button.querySelector('span').textContent = 'Logging in...';
        
        // Input field animations
        inputs.forEach(input => {
            input.style.transform = 'translateX(-10px)';
            input.style.opacity = '0.7';
        });

        // Simulate login process
        setTimeout(() => {
            this.resetForm();
            alert('Login successful! (This is a demo)');
        }, 2000);
    }

    resetForm() {
        const button = document.querySelector('.btn');
        const inputs = document.querySelectorAll('input');
        
        button.style.background = 'linear-gradient(45deg, #667eea, #764ba2)';
        button.querySelector('span').textContent = 'Login';
        
        inputs.forEach(input => {
            input.style.transform = 'translateX(0px)';
            input.style.opacity = '1';
            input.value = '';
        });
    }
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ParticleAnimation();
    new FormAnimations();
    
    // Add parallax effect to container
    const container = document.querySelector('.container');
    document.addEventListener('mousemove', (e) => {
        const x = (e.clientX / window.innerWidth - 0.5) * 10;
        const y = (e.clientY / window.innerHeight - 0.5) * 10;
        container.style.transform = `rotateY(${x}deg) rotateX(${-y}deg)`;
    });
});
