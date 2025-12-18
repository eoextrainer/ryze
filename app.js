// Players Database
const playersDatabase = [
    {
        id: 1,
        name: "LeBron James",
        position: "forward",
        team: "Los Angeles Lakers",
        height: "6'9\"",
        experience: "20 Years",
        ppg: 25.7,
        rpg: 10.5,
        apg: 8.2,
        rating: 9.8,
        image: "res/player-1.png"
    },
    {
        id: 2,
        name: "Kevin Durant",
        position: "forward",
        team: "Phoenix Suns",
        height: "6'10\"",
        experience: "16 Years",
        ppg: 29.1,
        rpg: 6.7,
        apg: 5.0,
        rating: 9.7,
        image: "res/player-2.png"
    },
    {
        id: 3,
        name: "Giannis Antetokounmpo",
        position: "forward",
        team: "Milwaukee Bucks",
        height: "6'11\"",
        experience: "11 Years",
        ppg: 31.1,
        rpg: 11.8,
        apg: 5.7,
        rating: 9.6,
        image: "res/player-3.png"
    },
    {
        id: 4,
        name: "Stephen Curry",
        position: "guard",
        team: "Golden State Warriors",
        height: "6'2\"",
        experience: "14 Years",
        ppg: 29.4,
        rpg: 5.2,
        apg: 6.5,
        rating: 9.5,
        image: "res/player-4.png"
    },
    {
        id: 5,
        name: "Luka Doncic",
        position: "guard",
        team: "Dallas Mavericks",
        height: "6'7\"",
        experience: "5 Years",
        ppg: 28.8,
        rpg: 9.6,
        apg: 8.0,
        rating: 9.4,
        image: "res/player-5.png"
    },
    {
        id: 6,
        name: "Jayson Tatum",
        position: "forward",
        team: "Boston Celtics",
        height: "6'8\"",
        experience: "6 Years",
        ppg: 30.1,
        rpg: 8.8,
        apg: 4.6,
        rating: 9.3,
        image: "res/player-6.png"
    },
    {
        id: 7,
        name: "Nikola Jokic",
        position: "center",
        team: "Denver Nuggets",
        height: "6'11\"",
        experience: "10 Years",
        ppg: 24.5,
        rpg: 11.8,
        apg: 9.8,
        rating: 9.9,
        image: "res/player-7.png"
    },
    {
        id: 8,
        name: "Joel Embiid",
        position: "center",
        team: "Philadelphia 76ers",
        height: "7'0\"",
        experience: "8 Years",
        ppg: 33.1,
        rpg: 10.2,
        apg: 4.2,
        rating: 9.2,
        image: "res/player-8.png"
    },
    {
        id: 9,
        name: "Donovan Mitchell",
        position: "guard",
        team: "Cleveland Cavaliers",
        height: "6'3\"",
        experience: "7 Years",
        ppg: 26.3,
        rpg: 4.3,
        apg: 5.2,
        rating: 8.9,
        image: "https://via.placeholder.com/250x350?text=Donovan+Mitchell"
    },
    {
        id: 10,
        name: "Damian Lillard",
        position: "guard",
        team: "Portland Trail Blazers",
        height: "6'2\"",
        experience: "12 Years",
        ppg: 32.2,
        rpg: 4.8,
        apg: 7.3,
        rating: 9.1,
        image: "https://via.placeholder.com/250x350?text=Damian+Lillard"
    },
    {
        id: 11,
        name: "Anthony Davis",
        position: "forward",
        team: "Los Angeles Lakers",
        height: "6'10\"",
        experience: "14 Years",
        ppg: 23.2,
        rpg: 9.9,
        apg: 2.6,
        rating: 9.0,
        image: "https://via.placeholder.com/250x350?text=Anthony+Davis"
    },
    {
        id: 12,
        name: "Devin Booker",
        position: "guard",
        team: "Phoenix Suns",
        height: "6'6\"",
        experience: "9 Years",
        ppg: 27.1,
        rpg: 4.5,
        apg: 7.2,
        rating: 8.8,
        image: "https://via.placeholder.com/250x350?text=Devin+Booker"
    },
    {
        id: 13,
        name: "Kawhi Leonard",
        position: "forward",
        team: "Los Angeles Clippers",
        height: "6'7\"",
        experience: "13 Years",
        ppg: 23.8,
        rpg: 3.9,
        apg: 3.9,
        rating: 9.0,
        image: "https://via.placeholder.com/250x350?text=Kawhi+Leonard"
    },
    {
        id: 14,
        name: "Jimmy Butler",
        position: "forward",
        team: "Miami Heat",
        height: "6'7\"",
        experience: "13 Years",
        ppg: 22.9,
        rpg: 5.9,
        apg: 5.3,
        rating: 8.7,
        image: "https://via.placeholder.com/250x350?text=Jimmy+Butler"
    },
    {
        id: 15,
        name: "Tyrese Haliburton",
        position: "guard",
        team: "Indiana Pacers",
        height: "6'5\"",
        experience: "3 Years",
        ppg: 20.7,
        rpg: 3.7,
        apg: 10.9,
        rating: 8.6,
        image: "https://via.placeholder.com/250x350?text=Tyrese+Haliburton"
    }
];

// State
let currentFilter = 'all';
let currentSearchTerm = '';

// DOM Elements
const playersGrid = document.getElementById('playersGrid');
const filterButtons = document.querySelectorAll('.filter-btn');
const searchInput = document.getElementById('searchInput');
const searchBtn = document.getElementById('searchBtn');
const modal = document.getElementById('playerModal');
const closeBtn = document.querySelector('.close');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    renderPlayers();
    setupEventListeners();
});

// Setup Event Listeners
function setupEventListeners() {
    // Filter buttons
    filterButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            filterButtons.forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            currentFilter = e.target.dataset.filter;
            renderPlayers();
        });
    });

    // Search
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            currentSearchTerm = searchInput.value.toLowerCase();
            renderPlayers();
        }
    });

    searchBtn.addEventListener('click', () => {
        currentSearchTerm = searchInput.value.toLowerCase();
        renderPlayers();
    });

    // Modal
    closeBtn.addEventListener('click', closeModal);
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeModal();
        }
    });

    // Close modal with Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.classList.contains('show')) {
            closeModal();
        }
    });
}

// Filter and Search Players
function filterPlayers() {
    return playersDatabase.filter(player => {
        const matchesFilter = currentFilter === 'all' || player.position === currentFilter;
        const matchesSearch = 
            player.name.toLowerCase().includes(currentSearchTerm) ||
            player.team.toLowerCase().includes(currentSearchTerm) ||
            player.position.toLowerCase().includes(currentSearchTerm);
        
        return matchesFilter && matchesSearch;
    });
}

// Render Players
function renderPlayers() {
    const filteredPlayers = filterPlayers();
    playersGrid.innerHTML = '';

    if (filteredPlayers.length === 0) {
        playersGrid.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 3rem; color: #b3b3b3;">No players found matching your criteria.</div>';
        return;
    }

    filteredPlayers.forEach(player => {
        const playerCard = createPlayerCard(player);
        playersGrid.appendChild(playerCard);
    });

    // Intersection Observer for animations
    observeElements();
}

// Create Player Card
function createPlayerCard(player) {
    const card = document.createElement('div');
    card.className = 'player-card';
    card.innerHTML = `
        <div class="player-image">
            <img src="${player.image}" alt="${player.name}" onerror="this.style.display='none'">
        </div>
        <div class="player-info">
            <h3>${player.name}</h3>
            <div class="player-position">${player.position.toUpperCase()}</div>
            <div class="player-team">${player.team}</div>
            <div class="player-rating">⭐ ${player.rating}/10</div>
        </div>
    `;

    card.addEventListener('click', () => openModal(player));
    return card;
}

// Open Modal
function openModal(player) {
    document.getElementById('modalImage').src = player.image;
    document.getElementById('modalName').textContent = player.name;
    document.getElementById('modalPosition').textContent = player.position.toUpperCase();
    document.getElementById('modalTeam').textContent = player.team;
    document.getElementById('modalHeight').textContent = player.height;
    document.getElementById('modalExperience').textContent = player.experience;
    document.getElementById('modalPPG').textContent = player.ppg.toFixed(1);
    document.getElementById('modalRPG').textContent = player.rpg.toFixed(1);
    document.getElementById('modalAPG').textContent = player.apg.toFixed(1);
    document.getElementById('modalRating').textContent = player.rating.toFixed(1);

    modal.classList.add('show');
    document.body.style.overflow = 'hidden';
}

// Close Modal
function closeModal() {
    modal.classList.remove('show');
    document.body.style.overflow = 'auto';
}

// Intersection Observer for lazy animations
function observeElements() {
    const options = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'slideUp 0.6s ease-out forwards';
                observer.unobserve(entry.target);
            }
        });
    }, options);

    document.querySelectorAll('.player-card').forEach(card => {
        observer.observe(card);
    });
}

// Smooth scroll for navigation
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href !== '#' && document.querySelector(href)) {
            e.preventDefault();
            document.querySelector(href).scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});
