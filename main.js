// ACA Arcium Academy - Main JavaScript File
// Interactive components and animations

class ArciumAcademy {
    constructor() {
        this.currentPage = this.getCurrentPage();
        this.userProgress = this.loadUserProgress();
        this.animations = {};
        this.charts = {};
        this.init();
    }

    getCurrentPage() {
        const path = window.location.pathname;
        if (path.includes('ecosystem')) return 'ecosystem';
        if (path.includes('learning')) return 'learning';
        if (path.includes('community')) return 'community';
        return 'index';
    }

    loadUserProgress() {
        const saved = localStorage.getItem('arcium-progress');
        return saved ? JSON.parse(saved) : {
            eec: 0,
            badges: [],
            currentPath: null,
            completedNodes: [],
            mentorStatus: false
        };
    }

    saveUserProgress() {
        localStorage.setItem('arcium-progress', JSON.stringify(this.userProgress));
    }

    init() {
        this.initNavigation();
        this.initScrollAnimations();
        this.initPageSpecificFeatures();
        this.initCommonComponents();
    }

    initNavigation() {
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                this.handleNavigation(e, link);
            });
        });

        // Mobile menu toggle
        const mobileToggle = document.querySelector('.mobile-menu-toggle');
        if (mobileToggle) {
            mobileToggle.addEventListener('click', () => {
                this.toggleMobileMenu();
            });
        }
    }

    handleNavigation(e, link) {
        // Add active state animation
        document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
        link.classList.add('active');
        
        // Smooth transition effect
        if (this.animations.pageTransition) {
            e.preventDefault();
            this.animatePageTransition(link.href);
        }
    }

    toggleMobileMenu() {
        const mobileMenu = document.querySelector('.mobile-menu');
        if (mobileMenu) {
            mobileMenu.classList.toggle('active');
        }
    }

    initScrollAnimations() {
        // Intersection Observer for scroll animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.animateElement(entry.target);
                }
            });
        }, observerOptions);

        // Observe all animatable elements
        document.querySelectorAll('.animate-on-scroll').forEach(el => {
            observer.observe(el);
        });
    }

    animateElement(element) {
        const animationType = element.dataset.animation || 'fadeInUp';
        
        switch(animationType) {
            case 'fadeInUp':
                anime({
                    targets: element,
                    translateY: [50, 0],
                    opacity: [0, 1],
                    duration: 800,
                    easing: 'easeOutCubic'
                });
                break;
            case 'fadeInLeft':
                anime({
                    targets: element,
                    translateX: [-50, 0],
                    opacity: [0, 1],
                    duration: 800,
                    easing: 'easeOutCubic'
                });
                break;
            case 'scaleIn':
                anime({
                    targets: element,
                    scale: [0.8, 1],
                    opacity: [0, 1],
                    duration: 600,
                    easing: 'easeOutBack'
                });
                break;
        }
    }

    initPageSpecificFeatures() {
        switch(this.currentPage) {
            case 'index':
                this.initHomePage();
                break;
            case 'ecosystem':
                this.initEcosystemPage();
                break;
            case 'learning':
                this.initLearningPage();
                break;
            case 'community':
                this.initCommunityPage();
                break;
        }
    }

    initHomePage() {
        this.initHeroAnimation();
        this.initLearningPathSelector();
        this.initFeatureCounters();
        this.initBadgePreview();
    }

    initHeroAnimation() {
        // Animated network visualization using p5.js
        const heroCanvas = document.getElementById('hero-canvas');
        if (heroCanvas) {
            this.initNetworkVisualization(heroCanvas);
        }

        // Typewriter effect for hero text
        const heroTitle = document.querySelector('.hero-title');
        if (heroTitle && typeof Typed !== 'undefined') {
            new Typed('.hero-title', {
                strings: [
                    'Master Web3 with ACA Arcium Academy',
                    'Learn Privacy & Cryptographic Protocols',
                    'Build the Future of Decentralized Computing'
                ],
                typeSpeed: 50,
                backSpeed: 30,
                backDelay: 2000,
                loop: true
            });
        }
    }

    initNetworkVisualization(canvas) {
        // P5.js network animation
        const sketch = (p) => {
            let nodes = [];
            let connections = [];

            p.setup = () => {
                p.createCanvas(canvas.offsetWidth, canvas.offsetHeight);
                
                // Create network nodes
                for (let i = 0; i < 50; i++) {
                    nodes.push({
                        x: p.random(p.width),
                        y: p.random(p.height),
                        vx: p.random(-1, 1),
                        vy: p.random(-1, 1),
                        size: p.random(3, 8)
                    });
                }
            };

            p.draw = () => {
                p.clear();
                
                // Update and draw connections
                p.stroke(0, 212, 255, 50);
                p.strokeWeight(1);
                for (let i = 0; i < nodes.length; i++) {
                    for (let j = i + 1; j < nodes.length; j++) {
                        let dist = p.dist(nodes[i].x, nodes[i].y, nodes[j].x, nodes[j].y);
                        if (dist < 100) {
                            p.line(nodes[i].x, nodes[i].y, nodes[j].x, nodes[j].y);
                        }
                    }
                }

                // Update and draw nodes
                p.fill(99, 102, 241);
                p.noStroke();
                nodes.forEach(node => {
                    node.x += node.vx;
                    node.y += node.vy;
                    
                    // Bounce off edges
                    if (node.x < 0 || node.x > p.width) node.vx *= -1;
                    if (node.y < 0 || node.y > p.height) node.vy *= -1;
                    
                    p.circle(node.x, node.y, node.size);
                });
            };

            p.windowResized = () => {
                p.resizeCanvas(canvas.offsetWidth, canvas.offsetHeight);
            };
        };

        new p5(sketch, canvas);
    }

    initLearningPathSelector() {
        const pathCards = document.querySelectorAll('.learning-path-card');
        pathCards.forEach(card => {
            card.addEventListener('click', () => {
                this.selectLearningPath(card);
            });

            // Hover animations
            card.addEventListener('mouseenter', () => {
                anime({
                    targets: card,
                    scale: 1.05,
                    rotateY: 5,
                    duration: 300,
                    easing: 'easeOutCubic'
                });
            });

            card.addEventListener('mouseleave', () => {
                anime({
                    targets: card,
                    scale: 1,
                    rotateY: 0,
                    duration: 300,
                    easing: 'easeOutCubic'
                });
            });
        });
    }

    selectLearningPath(card) {
        const pathType = card.dataset.path;
        this.userProgress.currentPath = pathType;
        this.saveUserProgress();

        // Animate selection
        anime({
            targets: card,
            backgroundColor: '#6366F1',
            duration: 500,
            easing: 'easeOutCubic',
            complete: () => {
                this.showPathDetails(pathType);
            }
        });
    }

    showPathDetails(pathType) {
        const detailsContainer = document.querySelector('.path-details');
        if (detailsContainer) {
            const pathInfo = this.getPathInfo(pathType);
            detailsContainer.innerHTML = `
                <div class="path-info">
                    <h3>${pathInfo.title}</h3>
                    <p>${pathInfo.description}</p>
                    <div class="path-stats">
                        <div class="stat">
                            <span class="stat-number">${pathInfo.challenges}</span>
                            <span class="stat-label">Challenges</span>
                        </div>
                        <div class="stat">
                            <span class="stat-number">${pathInfo.ecReward}</span>
                            <span class="stat-label">EC Rewards</span>
                        </div>
                    </div>
                    <button class="btn-primary" onclick="arcium.startLearningPath('${pathType}')">
                        Start Learning Path
                    </button>
                </div>
            `;

            anime({
                targets: detailsContainer,
                opacity: [0, 1],
                translateY: [20, 0],
                duration: 600,
                easing: 'easeOutCubic'
            });
        }
    }

    getPathInfo(pathType) {
        const paths = {
            explorer: {
                title: 'Explorer Path',
                description: 'Dive deep into C-SPL (Confidential Solana Program Library) and learn how to build privacy-preserving applications on Solana.',
                challenges: 12,
                ecReward: 240
            },
            builder: {
                title: 'Builder Path',
                description: 'Master DApp development with MXES and learn to deploy scalable decentralized applications with advanced cryptographic features.',
                challenges: 15,
                ecReward: 300
            },
            guardian: {
                title: 'Guardian Path',
                description: 'Become an expert in MPC, Cerberus, and Manticore protocols. Learn advanced privacy and security implementations.',
                challenges: 18,
                ecReward: 360
            }
        };
        return paths[pathType] || paths.explorer;
    }

    initFeatureCounters() {
        const counters = document.querySelectorAll('.counter');
        counters.forEach(counter => {
            const target = parseInt(counter.dataset.target);
            const duration = 2000;
            
            anime({
                targets: counter,
                innerHTML: [0, target],
                duration: duration,
                easing: 'easeOutCubic',
                round: 1
            });
        });
    }

    initBadgePreview() {
        const badges = document.querySelectorAll('.badge-preview');
        badges.forEach(badge => {
            badge.addEventListener('click', () => {
                this.showBadgeDetails(badge);
            });
        });
    }

    showBadgeDetails(badge) {
        const badgeType = badge.dataset.badge;
        const badgeInfo = this.getBadgeInfo(badgeType);
        
        // Create modal or tooltip with badge details
        this.showModal(`
            <div class="badge-details">
                <img src="${badgeInfo.image}" alt="${badgeInfo.name}" class="badge-image">
                <h3>${badgeInfo.name}</h3>
                <p>${badgeInfo.description}</p>
                <div class="badge-requirements">
                    <h4>Requirements:</h4>
                    <ul>
                        ${badgeInfo.requirements.map(req => `<li>${req}</li>`).join('')}
                    </ul>
                </div>
            </div>
        `);
    }

    getBadgeInfo(badgeType) {
        const badges = {
            'first-mint': {
                name: 'First-Mint',
                description: 'Awarded for creating your first C-SPL token',
                image: 'resources/badge-first-mint.png',
                requirements: ['Complete C-SPL basics course', 'Deploy a simple token contract', 'Pass the minting challenge']
            },
            'key-holder': {
                name: 'Key-Holder',
                description: 'Master of cryptographic key management',
                image: 'resources/badge-key-holder.png',
                requirements: ['Complete Shamir-split challenge', 'Demonstrate key recovery', 'Pass security audit']
            }
        };
        return badges[badgeType] || badges['first-mint'];
    }

    // Ecosystem page features
    initEcosystemPage() {
        this.initEcosystemVisualization();
        this.initArchitectureDiagram();
        this.initAnalyticsDashboard();
    }

    initEcosystemVisualization() {
        const container = document.getElementById('ecosystem-network');
        if (container && typeof echarts !== 'undefined') {
            const chart = echarts.init(container);
            
            const option = {
                backgroundColor: 'transparent',
                series: [{
                    type: 'graph',
                    layout: 'force',
                    data: this.generateEcosystemNodes(),
                    links: this.generateEcosystemLinks(),
                    roam: true,
                    force: {
                        repulsion: 1000,
                        edgeLength: 200
                    },
                    itemStyle: {
                        color: '#6366F1'
                    },
                    lineStyle: {
                        color: '#00D4FF',
                        width: 2
                    }
                }]
            };
            
            chart.setOption(option);
            this.charts.ecosystem = chart;
        }
    }

    generateEcosystemNodes() {
        return [
            { name: 'ACA Bot', symbolSize: 60, category: 0 },
            { name: 'Discord Server', symbolSize: 50, category: 1 },
            { name: 'Arcium Network', symbolSize: 55, category: 2 },
            { name: 'MPC Protocols', symbolSize: 45, category: 3 },
            { name: 'C-SPL Library', symbolSize: 40, category: 4 },
            { name: 'MXES Engine', symbolSize: 42, category: 5 },
            { name: 'Learners', symbolSize: 35, category: 6 },
            { name: 'Mentors', symbolSize: 38, category: 7 }
        ];
    }

    generateEcosystemLinks() {
        return [
            { source: 'ACA Bot', target: 'Discord Server' },
            { source: 'ACA Bot', target: 'Arcium Network' },
            { source: 'Arcium Network', target: 'MPC Protocols' },
            { source: 'Arcium Network', target: 'C-SPL Library' },
            { source: 'Arcium Network', target: 'MXES Engine' },
            { source: 'ACA Bot', target: 'Learners' },
            { source: 'Learners', target: 'Mentors' }
        ];
    }

    initAnalyticsDashboard() {
        // Initialize various charts for analytics
        this.initProgressChart();
        this.initEngagementChart();
        this.initEcosystemChart();
    }

    initProgressChart() {
        const container = document.getElementById('progress-chart');
        if (container && typeof echarts !== 'undefined') {
            const chart = echarts.init(container);
            
            const option = {
                title: {
                    text: 'Learning Progress Distribution',
                    textStyle: { color: '#ffffff' }
                },
                backgroundColor: 'transparent',
                series: [{
                    type: 'pie',
                    data: [
                        { value: 35, name: 'Explorer Path' },
                        { value: 40, name: 'Builder Path' },
                        { value: 25, name: 'Guardian Path' }
                    ],
                    itemStyle: {
                        color: (params) => {
                            const colors = ['#00D4FF', '#6366F1', '#10B981'];
                            return colors[params.dataIndex];
                        }
                    }
                }]
            };
            
            chart.setOption(option);
            this.charts.progress = chart;
        }
    }

    // Learning page features
    initLearningPage() {
        this.initLearningSimulator();
        this.initBadgeSystem();
        this.initProgressTracking();
        this.initChallengeExamples();
    }

    initLearningSimulator() {
        const simulator = document.querySelector('.learning-simulator');
        if (simulator) {
            this.createLearningNodes();
            this.initNodeInteractions();
        }
    }

    createLearningNodes() {
        const nodesContainer = document.querySelector('.learning-nodes');
        if (nodesContainer) {
            const nodes = [
                { id: 'start', title: 'Start Learning', x: 50, y: 50, completed: true },
                { id: 'basics', title: 'Web3 Basics', x: 200, y: 100, completed: true },
                { id: 'privacy', title: 'Privacy 101', x: 350, y: 80, completed: false },
                { id: 'mpc', title: 'MPC Introduction', x: 500, y: 120, completed: false },
                { id: 'advanced', title: 'Advanced Topics', x: 650, y: 100, completed: false }
            ];

            nodes.forEach(node => {
                const nodeElement = document.createElement('div');
                nodeElement.className = `learning-node ${node.completed ? 'completed' : ''}`;
                nodeElement.style.left = `${node.x}px`;
                nodeElement.style.top = `${node.y}px`;
                nodeElement.innerHTML = `
                    <div class="node-content">
                        <h4>${node.title}</h4>
                        <div class="node-status">${node.completed ? '✓' : '○'}</div>
                    </div>
                `;
                
                nodeElement.addEventListener('click', () => {
                    this.selectLearningNode(node);
                });
                
                nodesContainer.appendChild(nodeElement);
            });
        }
    }

    selectLearningNode(node) {
        // Animate node selection
        const nodeElement = document.querySelector(`[data-node="${node.id}"]`);
        if (nodeElement) {
            anime({
                targets: nodeElement,
                scale: [1, 1.2, 1],
                duration: 400,
                easing: 'easeOutBack'
            });
        }

        // Show node details
        this.showNodeDetails(node);
    }

    showNodeDetails(node) {
        const detailsContainer = document.querySelector('.node-details');
        if (detailsContainer) {
            detailsContainer.innerHTML = `
                <h3>${node.title}</h3>
                <p>Learn about ${node.title.toLowerCase()} through interactive challenges and hands-on exercises.</p>
                ${!node.completed ? `
                    <button class="btn-primary" onclick="arcium.startNodeChallenge('${node.id}')">
                        Start Challenge
                    </button>
                ` : `
                    <div class="completion-badge">✓ Completed</div>
                `}
            `;
        }
    }

    // Community page features
    initCommunityPage() {
        this.initMentorNetwork();
        this.initCommunityStats();
        this.initSuccessStories();
        this.initForkingDemo();
    }

    initMentorNetwork() {
        const mentorContainer = document.querySelector('.mentor-network');
        if (mentorContainer) {
            this.loadMentors();
            this.initMentorMatching();
        }
    }

    loadMentors() {
        const mentors = [
            { name: 'Alex Chen', expertise: 'MPC & Privacy', rating: 4.9, available: true },
            { name: 'Sarah Rodriguez', expertise: 'C-SPL Development', rating: 4.8, available: true },
            { name: 'Michael Kim', expertise: 'Smart Contracts', rating: 4.7, available: false },
            { name: 'Emma Thompson', expertise: 'DeFi Protocols', rating: 4.9, available: true }
        ];

        const mentorList = document.querySelector('.mentor-list');
        if (mentorList) {
            mentorList.innerHTML = mentors.map(mentor => `
                <div class="mentor-card ${mentor.available ? 'available' : 'unavailable'}">
                    <div class="mentor-info">
                        <h4>${mentor.name}</h4>
                        <p class="mentor-expertise">${mentor.expertise}</p>
                        <div class="mentor-rating">
                            ${this.generateStarRating(mentor.rating)}
                            <span>${mentor.rating}</span>
                        </div>
                    </div>
                    <div class="mentor-status">
                        ${mentor.available ? 
                            '<button class="btn-primary btn-small" onclick="arcium.requestMentor(\'' + mentor.name + '\')">Connect</button>' :
                            '<span class="status-unavailable">Busy</span>'
                        }
                    </div>
                </div>
            `).join('');
        }
    }

    generateStarRating(rating) {
        const fullStars = Math.floor(rating);
        const hasHalfStar = rating % 1 !== 0;
        let stars = '';
        
        for (let i = 0; i < fullStars; i++) {
            stars += '★';
        }
        if (hasHalfStar) {
            stars += '☆';
        }
        
        return stars;
    }

    // Utility functions
    showModal(content) {
        const modal = document.createElement('div');
        modal.className = 'modal-overlay';
        modal.innerHTML = `
            <div class="modal-content">
                <button class="modal-close" onclick="this.parentElement.parentElement.remove()">×</button>
                ${content}
            </div>
        `;
        document.body.appendChild(modal);

        anime({
            targets: modal,
            opacity: [0, 1],
            duration: 300,
            easing: 'easeOutCubic'
        });
    }

    updateEC(amount) {
        this.userProgress.eec += amount;
        this.saveUserProgress();
        
        const ecDisplay = document.querySelector('.ec-display');
        if (ecDisplay) {
            anime({
                targets: ecDisplay,
                innerHTML: [this.userProgress.eec - amount, this.userProgress.eec],
                duration: 1000,
                easing: 'easeOutCubic',
                round: 1
            });
        }
    }

    addBadge(badgeType) {
        if (!this.userProgress.badges.includes(badgeType)) {
            this.userProgress.badges.push(badgeType);
            this.saveUserProgress();
            this.celebrateBadgeUnlock(badgeType);
        }
    }

    celebrateBadgeUnlock(badgeType) {
        // Particle celebration effect
        const celebration = document.createElement('div');
        celebration.className = 'badge-celebration';
        celebration.innerHTML = `
            <div class="celebration-content">
                <h2>🎉 Badge Unlocked! 🎉</h2>
                <img src="resources/badge-${badgeType}.png" alt="${badgeType} badge">
                <p>You've earned the ${badgeType} badge!</p>
            </div>
        `;
        document.body.appendChild(celebration);

        anime({
            targets: celebration,
            opacity: [0, 1, 1, 0],
            scale: [0.5, 1, 1, 0.8],
            duration: 3000,
            easing: 'easeOutCubic',
            complete: () => celebration.remove()
        });
    }

    // Common components initialization
    initCommonComponents() {
        this.initECCounter();
        this.initBadgeDisplay();
        this.initProgressBar();
    }

    initECCounter() {
        const ecDisplay = document.querySelector('.ec-counter');
        if (ecDisplay) {
            ecDisplay.textContent = this.userProgress.eec;
        }
    }

    initBadgeDisplay() {
        const badgeContainer = document.querySelector('.user-badges');
        if (badgeContainer) {
            badgeContainer.innerHTML = this.userProgress.badges.map(badge => `
                <img src="resources/badge-${badge}.png" alt="${badge}" class="user-badge">
            `).join('');
        }
    }

    initProgressBar() {
        const progressBar = document.querySelector('.progress-bar');
        if (progressBar) {
            const progress = this.calculateOverallProgress();
            anime({
                targets: progressBar,
                width: `${progress}%`,
                duration: 1500,
                easing: 'easeOutCubic'
            });
        }
    }

    calculateOverallProgress() {
        const totalNodes = 20; // Total learning nodes
        const completedNodes = this.userProgress.completedNodes.length;
        return (completedNodes / totalNodes) * 100;
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.arcium = new ArciumAcademy();
});

// Handle window resize for responsive charts
window.addEventListener('resize', () => {
    if (window.arcium && window.arcium.charts) {
        Object.values(window.arcium.charts).forEach(chart => {
            if (chart && chart.resize) {
                chart.resize();
            }
        });
    }
});