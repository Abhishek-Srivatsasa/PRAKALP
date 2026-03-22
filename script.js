// Radar Animation
const canvas = document.getElementById('radarCanvas');
const ctx = canvas.getContext('2d');

function initRadar() {
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;
}

const targets = [
    { x: 0.2, y: 0.3, size: 4, alpha: 1 },
    { x: 0.6, y: 0.7, size: 6, alpha: 0.8 },
    { x: 0.8, y: 0.2, size: 3, alpha: 0.5 }
];

function drawRadar() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw concentric circles
    ctx.strokeStyle = 'rgba(0, 212, 255, 0.1)';
    ctx.lineWidth = 1;
    for (let i = 1; i <= 5; i++) {
        ctx.beginPath();
        ctx.arc(canvas.width / 2, canvas.height / 2, (canvas.height / 5) * i, 0, Math.PI * 2);
        ctx.stroke();
    }

    // Draw Crosshair
    ctx.beginPath();
    ctx.moveTo(canvas.width / 2, 0);
    ctx.lineTo(canvas.width / 2, canvas.height);
    ctx.moveTo(0, canvas.height / 2);
    ctx.lineTo(canvas.width, canvas.height / 2);
    ctx.stroke();

    // Draw Targets
    targets.forEach(target => {
        ctx.fillStyle = `rgba(16, 185, 129, ${target.alpha})`;
        ctx.beginPath();
        ctx.arc(target.x * canvas.width, target.y * canvas.height, target.size, 0, Math.PI * 2);
        ctx.fill();
        
        // Target Labels
        ctx.font = '10px Space Mono';
        ctx.fillText(`TRGT_0${targets.indexOf(target) + 1}`, target.x * canvas.width + 10, target.y * canvas.height - 10);

        // Slow movement for targets
        target.x += (Math.random() - 0.5) * 0.001;
        target.y += (Math.random() - 0.5) * 0.001;
    });

    requestAnimationFrame(drawRadar);
}

// Telemetry Updates
function updateTelemetry() {
    const coordsEl = document.getElementById('coords');
    const altitudeEl = document.getElementById('altitude');
    
    setInterval(() => {
        const lat = (28.6139 + (Math.random() - 0.5) * 0.01).toFixed(4);
        const lon = (77.2090 + (Math.random() - 0.5) * 0.01).toFixed(4);
        const alt = (40 + Math.random() * 5).toFixed(1);
        
        coordsEl.innerText = `LAT: ${lat} | LON: ${lon}`;
        altitudeEl.innerText = `${alt}m`;
    }, 2000);
}

// Kill-Switch Logic
const killSwitch = document.getElementById('killSwitch');
let isAlertActive = false;

killSwitch.addEventListener('click', () => {
    isAlertActive = !isAlertActive;
    if (isAlertActive) {
        document.body.classList.add('red-alert');
        killSwitch.innerText = 'RESET SYSTEM';
        playSoundEffect(true);
    } else {
        document.body.classList.remove('red-alert');
        killSwitch.innerText = 'INITIATE KILL-SWITCH';
        playSoundEffect(false);
    }
});

function playSoundEffect(active) {
    // Virtual sound simulation - visual feedback is key
    console.log(active ? 'ALERT: SYSTEM OVERRIDE' : 'SYSTEM READY');
}

// Scroll Handling
function scrollToSection(id) {
    const el = document.getElementById(id);
    el.scrollIntoView({ behavior: 'smooth' });
}

// Live Feed Logic
const webcam = document.getElementById('webcam');
const startFeedBtn = document.getElementById('startFeed');
const feedTimestamp = document.getElementById('feedTimestamp');
let stream = null;

async function initCamera() {
    try {
        if (!stream) {
            stream = await navigator.mediaDevices.getUserMedia({ 
                video: { 
                    width: { ideal: 1280 },
                    height: { ideal: 720 },
                    facingMode: "user"
                }, 
                audio: false 
            });
            webcam.srcObject = stream;
            startFeedBtn.innerText = 'TERMINATE LINK';
            startFeedBtn.classList.remove('btn-primary');
            startFeedBtn.classList.add('btn-danger');
            console.log('NEURAL LINK ESTABLISHED');
        } else {
            stopCamera();
        }
    } catch (err) {
        console.error("Camera access denied:", err);
        alert("CRITICAL ERROR: Unable to establish neural link. Please check hardware permissions.");
    }
}

function stopCamera() {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        webcam.srcObject = null;
        stream = null;
        startFeedBtn.innerText = 'INITIALIZE NEURAL LINK';
        startFeedBtn.classList.remove('btn-danger');
        startFeedBtn.classList.add('btn-primary');
        console.log('NEURAL LINK TERMINATED');
    }
}

startFeedBtn.addEventListener('click', initCamera);

// Update Feed Timestamp
function updateTimestamp() {
    const now = new Date();
    const ts = now.toISOString().replace('T', ' ').slice(0, 19);
    if (feedTimestamp) feedTimestamp.innerText = ts;
}

setInterval(updateTimestamp, 1000);

// Initialize
window.addEventListener('resize', initRadar);
initRadar();
drawRadar();
updateTelemetry();
updateTimestamp();

// Add interactive effect to Arch cards
document.querySelectorAll('.arch-card').forEach(card => {
    card.addEventListener('mouseenter', () => {
        card.style.borderColor = 'var(--acc-cyan)';
    });
    card.addEventListener('mouseleave', () => {
        card.style.borderColor = 'var(--glass-border)';
    });
});
