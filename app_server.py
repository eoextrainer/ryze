"""
<<<<<<< HEAD
ryze Basketball Platform - Flask Backend
=======
dunes Basketball Platform - Flask Backend
>>>>>>> 513add7 (Update: project documentation, structure, workflows, and archives)
Supports clubs and players with subscription tiers and private dashboards
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, g
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime, timedelta
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ryze-basketball-secret-key-2025'

# Prefer DATABASE_URL if provided (Render MySQL), fallback to local SQLite
db_url = os.environ.get('DATABASE_URL')
if db_url:
    # Normalize DB URLs for SQLAlchemy dialects
    if db_url.startswith('mysql://'):
        db_url = db_url.replace('mysql://', 'mysql+pymysql://', 1)
    if db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql+psycopg2://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ryze_basketball.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Simple verification route to check DB connectivity and basic table counts
@app.route('/verify_db')
def verify_db():
    try:
        clubs = Club.query.count()
        players = Player.query.count()
        perf = Performance.query.count()
        return jsonify({
            'database': app.config['SQLALCHEMY_DATABASE_URI'],
            'clubs': clubs,
            'players': players,
            'performances': perf
        })
    except Exception as e:
        return jsonify({'error': str(e), 'database': app.config['SQLALCHEMY_DATABASE_URI']}), 500

# ==================== Auth Smoke Test ====================
@app.route('/auth/smoke')
def auth_smoke():
    """Iterate seeded users and verify password hashes match expected defaults.
    Players: PlayerPass123! | Clubs: ClubPass123!
    """
    results = {
        'players_total': 0,
        'players_ok': 0,
        'players_fail': 0,
        'clubs_total': 0,
        'clubs_ok': 0,
        'clubs_fail': 0
    }
    try:
        player_pw = 'PlayerPass123!'
        club_pw = 'ClubPass123!'

        players = Player.query.all()
        results['players_total'] = len(players)
        for p in players:
            if p.password_hash and check_password_hash(p.password_hash, player_pw):
                results['players_ok'] += 1
            else:
                results['players_fail'] += 1

        clubs = Club.query.all()
        results['clubs_total'] = len(clubs)
        for c in clubs:
            if c.password_hash and check_password_hash(c.password_hash, club_pw):
                results['clubs_ok'] += 1
            else:
                results['clubs_fail'] += 1

        results['status'] = 'ok'
        return jsonify(results)
    except Exception as e:
        results['status'] = 'error'
        results['error'] = str(e)
        return jsonify(results), 500

# Expose MOBILE_ONLY flag to all templates
@app.context_processor
def inject_mobile_flag():
    return {"MOBILE_ONLY": app.config.get("MOBILE_ONLY", False)}

# ==================== Database Models ====================

class Club(db.Model):
    __tablename__ = 'clubs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    tier = db.Column(db.String(10), nullable=False)  # Pro A, Pro B, N1, N2, N3
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(120))
    logo_path = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    players = db.relationship('Player', secondary='club_player', backref='clubs')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Player(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    date_of_birth = db.Column(db.Date)
    height = db.Column(db.Float)  # cm
    weight = db.Column(db.Float)  # kg
    nationality = db.Column(db.String(120))
    position = db.Column(db.String(50))  # Guard, Forward, Center
    photo_path = db.Column(db.String(255))
    subscription_tier = db.Column(db.String(20), nullable=False)  # tier1 (50€), tier2 (29.99€), tier3 (9.99€)
    subscription_start = db.Column(db.DateTime, default=datetime.utcnow)
    subscription_end = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    stats = db.relationship('PlayerStat', backref='player', cascade='all, delete-orphan')
    performances = db.relationship('Performance', backref='player', cascade='all, delete-orphan')
    resume = db.relationship('PlayerResume', backref='player', cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class ClubPlayer(db.Model):
    __tablename__ = 'club_player'
    id = db.Column(db.Integer, primary_key=True)
    club_id = db.Column(db.Integer, db.ForeignKey('clubs.id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    status = db.Column(db.String(20), default='interested')  # interested, viewing, signed


class PlayerStat(db.Model):
    __tablename__ = 'player_stats'
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    points_per_game = db.Column(db.Float, default=0)
    assists_per_game = db.Column(db.Float, default=0)
    rebounds_per_game = db.Column(db.Float, default=0)
    field_goal_percentage = db.Column(db.Float, default=0)
    speed_kmh = db.Column(db.Float, default=0)
    attack_performance_score = db.Column(db.Float, default=0)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)


class Performance(db.Model):
    __tablename__ = 'performances'
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    game_date = db.Column(db.Date, nullable=False)
    points = db.Column(db.Integer, default=0)
    assists = db.Column(db.Integer, default=0)
    rebounds = db.Column(db.Integer, default=0)
    field_goals_made = db.Column(db.Integer, default=0)
    field_goals_attempted = db.Column(db.Integer, default=0)
    opponent = db.Column(db.String(120))


class PlayerResume(db.Model):
    __tablename__ = 'player_resume'
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    club_id = db.Column(db.Integer, db.ForeignKey('clubs.id'), nullable=False)
    season_start = db.Column(db.Integer)  # year
    season_end = db.Column(db.Integer)  # year
    is_current = db.Column(db.Boolean, default=False)
    is_future = db.Column(db.Boolean, default=False)  # Next club to play for
    
    club = db.relationship('Club', backref='player_resumes')


class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text)
    category = db.Column(db.String(50), nullable=False)  # club, player, global
    club_id = db.Column(db.Integer, db.ForeignKey('clubs.id'))
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ==================== Agent Model ====================
class Agent(db.Model):
    __tablename__ = 'agents'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    agency = db.Column(db.String(120))
    city = db.Column(db.String(120))
    phone = db.Column(db.String(40))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# ==================== Club Highlight Videos ====================

# Central list of 15 highlight videos mapped by club order (1..15)
# Uses YouTube embed URLs with consistent params; start offsets added where provided.
HIGHLIGHT_EMBED_URLS = [
    "https://www.youtube.com/embed/A3F_6V2n8t0?rel=0&modestbranding=1&playsinline=1&autoplay=1&mute=1",
    "https://www.youtube.com/embed/tbqw1BmiiHI?rel=0&modestbranding=1&playsinline=1&autoplay=1&mute=1",
    "https://www.youtube.com/embed/C7ZYEckFw7I?rel=0&modestbranding=1&playsinline=1&autoplay=1&mute=1",
    "https://www.youtube.com/embed/d_JI-QGcpgI?rel=0&modestbranding=1&playsinline=1&autoplay=1&mute=1",
    "https://www.youtube.com/embed/ugnpqWKxeXM?rel=0&modestbranding=1&playsinline=1&autoplay=1&mute=1",
    "https://www.youtube.com/embed/VBPGrvNo5yY?rel=0&modestbranding=1&playsinline=1&autoplay=1&mute=1",
    "https://www.youtube.com/embed/k0Pa-1Z9fo8?rel=0&modestbranding=1&playsinline=1&autoplay=1&mute=1",
    "https://www.youtube.com/embed/VxgIIl3fvnc?rel=0&modestbranding=1&playsinline=1&autoplay=1&mute=1",
    "https://www.youtube.com/embed/8miVw4vhNUs?rel=0&modestbranding=1&playsinline=1&autoplay=1&mute=1",
    # video 10 has t=3301s -> embed uses start=3301
    "https://www.youtube.com/embed/wGW_brMHK-o?rel=0&modestbranding=1&playsinline=1&start=3301&autoplay=1&mute=1",
    # video 11 has t=1s
    "https://www.youtube.com/embed/umBzUhvS5gE?rel=0&modestbranding=1&playsinline=1&start=1&autoplay=1&mute=1",
    "https://www.youtube.com/embed/PDX4-KigsB8?rel=0&modestbranding=1&playsinline=1&autoplay=1&mute=1",
    "https://www.youtube.com/embed/fhGp1dsSLrw?rel=0&modestbranding=1&playsinline=1&autoplay=1&mute=1",
    "https://www.youtube.com/embed/cvqimCayboE?rel=0&modestbranding=1&playsinline=1&autoplay=1&mute=1",
    "https://www.youtube.com/embed/dJUOwOBAhKo?rel=0&modestbranding=1&playsinline=1&autoplay=1&mute=1",
]


def get_club_video_map():
    """Return a stable mapping of club.id -> highlight URL based on club id order.
    The first 15 clubs get the provided URLs one-to-one. If more clubs exist, URLs cycle.
    """
    clubs_all = Club.query.order_by(Club.id.asc()).all()
    mapping = {}
    for idx, club in enumerate(clubs_all):
        mapping[club.id] = HIGHLIGHT_EMBED_URLS[idx % len(HIGHLIGHT_EMBED_URLS)]
    return mapping


def embed_to_watch(embed_url: str) -> str:
    """Convert a YouTube embed URL to a watch URL for CTA."""
    try:
        # Extract ID between '/embed/' and next '?'
        if '/embed/' in embed_url:
            vid = embed_url.split('/embed/')[1].split('?')[0]
            return f"https://www.youtube.com/watch?v={vid}"
    except Exception:
        pass
    return embed_url

# ==================== Routes ====================

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page for clubs and players"""
    if request.method == 'POST':
        data = request.get_json()
        user_type = data.get('user_type')  # 'club' or 'player'
        email = data.get('email')
        password = data.get('password')
        
        if user_type == 'club':
            club = Club.query.filter_by(email=email).first()
            if club and club.check_password(password):
                session['user_id'] = club.id
                session['user_type'] = 'club'
                session['user_name'] = club.name
                return jsonify({'success': True, 'redirect': '/club/dashboard'})
            return jsonify({'success': False, 'message': 'Invalid credentials'})
        
        elif user_type == 'player':
            player = Player.query.filter_by(email=email).first()
            if player and player.check_password(password):
                session['user_id'] = player.id
                session['user_type'] = 'player'
                session['user_name'] = f"{player.first_name} {player.last_name}"
                return jsonify({'success': True, 'redirect': '/player/dashboard'})
            return jsonify({'success': False, 'message': 'Invalid credentials'})
    
    return render_template('login.html')


@app.route('/club/dashboard')
def club_dashboard():
    """Club private dashboard with Netflix-like UI"""
    if 'user_type' not in session or session['user_type'] != 'club':
        return redirect(url_for('login'))
    
    club_id = session['user_id']
    club = Club.query.get(club_id)
    
    # Get players associated with this club
    players = db.session.query(Player).join(ClubPlayer).filter(ClubPlayer.club_id == club_id).all()
    
    # Get stats for filtering
    top_players = sorted(players, key=lambda p: p.stats[0].points_per_game if p.stats else 0, reverse=True)[:5]
    top_scorers = sorted(players, key=lambda p: p.stats[0].points_per_game if p.stats else 0, reverse=True)
    top_passers = sorted(players, key=lambda p: p.stats[0].assists_per_game if p.stats else 0, reverse=True)
    top_rebounders = sorted(players, key=lambda p: p.stats[0].rebounds_per_game if p.stats else 0, reverse=True)
    
    # Get highlight video for this club
    video_map = get_club_video_map()
    video_url = video_map.get(club.id)

    return render_template('club_dashboard.html', club=club, players=players, top_players=top_players,
                         top_scorers=top_scorers, top_passers=top_passers,
                         top_rebounders=top_rebounders, video_url=video_url)


@app.route('/player/dashboard')
def player_dashboard():
    """Player private dashboard"""
    if 'user_type' not in session or session['user_type'] != 'player':
        return redirect(url_for('login'))
    
    player_id = session['user_id']
    player = Player.query.get(player_id)
    
    # Get last 10 performances
    performances = Performance.query.filter_by(player_id=player_id).order_by(Performance.game_date.desc()).limit(10).all()
    
    # Get resume
    resume = PlayerResume.query.filter_by(player_id=player_id).order_by(PlayerResume.season_start.desc()).all()
    
    # Get news
    news = News.query.filter((News.player_id == player_id) | (News.category == 'global')).order_by(News.created_at.desc()).limit(5).all()

    # Accessible clubs based on subscription tier
    tier_map = {
        'tier1': ['Pro A', 'Pro B', 'N1', 'N2', 'N3'],
        'tier2': ['N1', 'N2', 'N3'],
        'tier3': ['N3']
    }
    allowed_tiers = tier_map.get(player.subscription_tier, ['N3'])
    accessible_clubs = Club.query.filter(Club.tier.in_(allowed_tiers)).order_by(Club.id.asc()).all()
    # Use stable global mapping, then select for accessible clubs
    all_videos = get_club_video_map()
    club_videos = {club.id: all_videos.get(club.id) for club in accessible_clubs}
    club_watch_urls = {club.id: embed_to_watch(all_videos.get(club.id) or "") for club in accessible_clubs}
    
    return render_template('player_dashboard.html', player=player, performances=performances,
                         resume=resume, news=news, accessible_clubs=accessible_clubs,
                         club_videos=club_videos, club_watch_urls=club_watch_urls)


@app.route('/player/club/<int:club_id>')
def player_club_info(club_id):
    """Player-facing club info page"""
    if 'user_type' not in session or session['user_type'] != 'player':
        return redirect(url_for('login'))

    player_id = session.get('user_id')
    player = Player.query.get(player_id)
    club = Club.query.get_or_404(club_id)
    
    # Verify access based on subscription tier
    tier_map = {
        'tier1': ['Pro A', 'Pro B', 'N1', 'N2', 'N3'],
        'tier2': ['N1', 'N2', 'N3'],
        'tier3': ['N3']
    }
    allowed_tiers = tier_map.get(player.subscription_tier if player else 'tier3', ['N3'])
    if club.tier not in allowed_tiers:
        return "Access denied - club not in your subscription tier", 403
    
    # Map club ID to video URL (stable by global club order)
    video_url = get_club_video_map().get(club_id)
    watch_url = embed_to_watch(video_url or "")
    return render_template('player_club_info.html', club=club, video_url=video_url, watch_url=watch_url)


@app.route('/club/player/<int:player_id>')
def club_player_profile(player_id):
    """View individual player profile from club perspective"""
    if 'user_type' not in session or session['user_type'] != 'club':
        return redirect(url_for('login'))
    
    club_id = session['user_id']
    club = Club.query.get(club_id)
    player = Player.query.get_or_404(player_id)
    
    # Verify club has access to this player
    club_player_link = ClubPlayer.query.filter_by(club_id=club_id, player_id=player_id).first()
    if not club_player_link:
        return "Access denied - player not in your subscription tier", 403
    
    # Get player data
    performances = Performance.query.filter_by(player_id=player_id).order_by(Performance.game_date.desc()).limit(10).all()
    resume = PlayerResume.query.filter_by(player_id=player_id).order_by(PlayerResume.season_start.desc()).all()
    news = News.query.filter((News.player_id == player_id) | (News.category == 'global')).order_by(News.created_at.desc()).limit(5).all()
    
    return render_template('club_player_profile.html', club=club, player=player, 
                         performances=performances, resume=resume, news=news)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    """Logout user"""
    session.clear()
    return redirect(url_for('index'))


@app.route('/api/players/filter')
def filter_players():
    """API endpoint to filter players"""
    filter_type = request.args.get('type')  # best, height, speed, attack
    
    players = Player.query.all()
    
    if filter_type == 'best':
        players = sorted(players, key=lambda p: sum([s.points_per_game for s in p.stats]) / len(p.stats) if p.stats else 0, reverse=True)
    elif filter_type == 'height':
        players = sorted(players, key=lambda p: p.height or 0, reverse=True)
    elif filter_type == 'speed':
        players = sorted(players, key=lambda p: p.stats[0].speed_kmh if p.stats else 0, reverse=True)
    elif filter_type == 'attack':
        players = sorted(players, key=lambda p: p.stats[0].attack_performance_score if p.stats else 0, reverse=True)
    
    return jsonify([{
        'id': p.id,
        'name': f"{p.first_name} {p.last_name}",
        'position': p.position,
        'height': p.height,
        'photo': p.photo_path
    } for p in players[:20]])


# ==================== Initialize Database ====================

def init_db():
    """Initialize the database with sample data"""
    with app.app_context():
        db.create_all()
        
        # Check if data already exists
        if Club.query.first():
            print("Database already populated")
            return
        
        print("Populating database with sample data...")
        
        # Create 15 clubs (5 per tier)
        clubs_data = [
            # Pro A (3 clubs)
            ('Paris Basketball', 'Pro A', 'contact@parisbball.fr', 'Paris'),
            ('Monaco Basketball', 'Pro A', 'contact@monaco.fr', 'Monaco'),
            ('Asvel Lyon', 'Pro A', 'contact@asvel.fr', 'Lyon'),
            
            # Pro B (3 clubs)
            ('Strasbourg IG', 'Pro B', 'contact@strasbourg.fr', 'Strasbourg'),
            ('Dijon Basketball', 'Pro B', 'contact@dijon.fr', 'Dijon'),
            ('Nanterre 92', 'Pro B', 'contact@nanterre.fr', 'Nanterre'),
            
            # N1 (3 clubs)
            ('Boulogne-Levallois', 'N1', 'contact@boulogne.fr', 'Boulogne'),
            ('Saint-Quentin', 'N1', 'contact@stquentin.fr', 'Saint-Quentin'),
            ('Roanne', 'N1', 'contact@roanne.fr', 'Roanne'),
            
            # N2 (3 clubs)
            ('Toulouse', 'N2', 'contact@toulouse.fr', 'Toulouse'),
            ('Marseille', 'N2', 'contact@marseille.fr', 'Marseille'),
            ('Bordeaux', 'N2', 'contact@bordeaux.fr', 'Bordeaux'),
            
            # N3 (3 clubs)
            ('Lille', 'N3', 'contact@lille.fr', 'Lille'),
            ('Nice', 'N3', 'contact@nice.fr', 'Nice'),
            ('Nantes', 'N3', 'contact@nantes.fr', 'Nantes'),
        ]
        
        clubs = []
        for name, tier, email, city in clubs_data:
            club = Club(name=name, tier=tier, email=email, city=city)
            club.set_password('password123')
            clubs.append(club)
            db.session.add(club)
        
        db.session.commit()
        
        # Create 30 players with random subscription tiers
        first_names = ['Luc', 'Marc', 'Jean', 'Pierre', 'Nicolas', 'Philippe', 'Laurent', 'Olivier', 'David', 'Thierry',
                      'Eric', 'Christian', 'Vincent', 'Francois', 'Michel', 'Anthony', 'Jamal', 'DeShawn', 'Marcus', 'Andre',
                      'Tyrone', 'Isiah', 'Magic', 'Larry', 'Charles', 'Scottie', 'Michael', 'Kobe', 'LeBron', 'Stephen']
        
        last_names = ['James', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
                     'Hernandez', 'Lopez', 'Sanchez', 'Clark', 'Lewis', 'Lee', 'Walker', 'Hall', 'Allen', 'Young',
                     'Durand', 'Moreau', 'Simon', 'Laurent', 'Lefevre', 'Dupont', 'Bernard', 'Petit', 'Gérard', 'Fournier']
        
        positions = ['Guard', 'Forward', 'Center']
        nationalities = ['France', 'USA', 'Spain', 'Germany', 'Italy', 'Portugal', 'Greece', 'Serbia']
        
        players = []
        tier_distribution = random.choices(['tier1', 'tier2', 'tier3'], weights=[10, 10, 10], k=30)
        
        for i in range(30):
            player = Player(
                first_name=first_names[i],
                last_name=last_names[i],
                email=f"player{i+1}@ryze.fr",
                date_of_birth=datetime(1990 + i % 20, random.randint(1, 12), random.randint(1, 28)).date(),
                height=180 + random.randint(-20, 20),
                weight=80 + random.randint(-20, 30),
                nationality=random.choice(nationalities),
                position=random.choice(positions),
                photo_path=f"res/player-{(i % 8) + 1}.png",
                subscription_tier=tier_distribution[i],
                subscription_start=datetime.utcnow(),
                subscription_end=datetime.utcnow() + timedelta(days=365)
            )
            player.set_password('password123')
            players.append(player)
            db.session.add(player)
        
        db.session.commit()
        
        # Create player stats for all players
        for player in players:
            stat = PlayerStat(
                player_id=player.id,
                points_per_game=random.uniform(5, 25),
                assists_per_game=random.uniform(1, 8),
                rebounds_per_game=random.uniform(2, 15),
                field_goal_percentage=random.uniform(40, 55),
                speed_kmh=random.uniform(20, 35),
                attack_performance_score=random.uniform(60, 95)
            )
            db.session.add(stat)
        
        db.session.commit()
        
        # Create sample performances (last 10 games for each player)
        for player in players:
            for j in range(10):
                perf = Performance(
                    player_id=player.id,
                    game_date=datetime.utcnow() - timedelta(days=j),
                    points=random.randint(5, 35),
                    assists=random.randint(0, 10),
                    rebounds=random.randint(0, 15),
                    field_goals_made=random.randint(2, 15),
                    field_goals_attempted=random.randint(5, 30),
                    opponent=random.choice([c.name for c in clubs])
                )
                db.session.add(perf)
        
        db.session.commit()
        
        # Create player resumes (club history + future assignment)
        for i, player in enumerate(players):
            # Add 2-3 past clubs
            for j in range(random.randint(2, 3)):
                club = random.choice(clubs)
                resume = PlayerResume(
                    player_id=player.id,
                    club_id=club.id,
                    season_start=2020 + j,
                    season_end=2021 + j,
                    is_current=False,
                    is_future=False
                )
                db.session.add(resume)
            
            # Assign a future club (next team to play for)
            future_club = clubs[i % len(clubs)]
            future_resume = PlayerResume(
                player_id=player.id,
                club_id=future_club.id,
                season_start=2026,
                season_end=2027,
                is_current=False,
                is_future=True
            )
            db.session.add(future_resume)
        
        db.session.commit()
        
        # Create relationships between players and clubs based on subscription tier
        tier_to_clubs = {
            'tier1': clubs,  # All clubs
            'tier2': clubs[3:],  # N1, N2, N3
            'tier3': clubs[9:]   # N3 only
        }
        
        for player in players:
            eligible_clubs = tier_to_clubs.get(player.subscription_tier, [])
            selected_clubs = random.sample(eligible_clubs, min(3, len(eligible_clubs)))
            for club in selected_clubs:
                club_player = ClubPlayer(club_id=club.id, player_id=player.id)
                db.session.add(club_player)
        
        db.session.commit()
        
        print("✅ Database initialized successfully!")
        print(f"📊 Created 15 clubs and 30 players")
        print("🔐 Default credentials: email + 'password123'")


if __name__ == '__main__':
    # Initialize schema and seed if empty, then start server
    with app.app_context():
        db.create_all()
        try:
            # Seed sample data only if empty to avoid duplicates
            if Club.query.first() is None:
                init_db()
        except Exception as e:
            # Non-fatal: log and continue with empty DB
            print(f"⚠️  Database initialization skipped or failed: {e}")

    port = int(os.environ.get('PORT', 8000))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = os.environ.get('FLASK_DEBUG', '0') in ('1', 'true', 'True')

    print("\n✅ ryze Basketball Platform Ready!")
    print(f"📍 Server: http://{host}:{port}")
    print("🔐 Demo Credentials:")
    print("   Club: contact@parisbball.fr / password123")
    print("   Player: player1@ryze.fr / password123\n")
    app.run(debug=debug, port=port, host=host)
