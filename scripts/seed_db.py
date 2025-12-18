#!/usr/bin/env python3
import os
from datetime import datetime
from app_server import app, db, Club, Player, ClubPlayer, PlayerStat, Performance, PlayerResume
from werkzeug.security import generate_password_hash

def ensure_defaults():
    # Create 15 clubs with provided dataset
    clubs_data = [
        ("Paris Basketball", "contact@parisbball.fr", "Pro A"),
        ("Monaco Basketball", "contact@monaco.fr", "Pro A"),
        ("Asvel Lyon", "contact@asvel.fr", "Pro A"),
        ("Strasbourg IG", "contact@strasbourg.fr", "Pro B"),
        ("Dijon Basketball", "contact@dijon.fr", "Pro B"),
        ("Nanterre 92", "contact@nanterre.fr", "Pro B"),
        ("Boulogne-Levallois", "contact@boulogne.fr", "N1"),
        ("Saint-Quentin", "contact@stquentin.fr", "N1"),
        ("Roanne", "contact@roanne.fr", "N1"),
        ("Toulouse", "contact@toulouse.fr", "N2"),
        ("Marseille", "contact@marseille.fr", "N2"),
        ("Bordeaux", "contact@bordeaux.fr", "N2"),
        ("Lille", "contact@lille.fr", "N3"),
        ("Nice", "contact@nice.fr", "N3"),
        ("Nantes", "contact@nantes.fr", "N3"),
    ]
    for name, email, tier in clubs_data:
        if not Club.query.filter_by(email=email).first():
            c = Club(
                name=name,
                tier=tier,
                email=email,
                password_hash=generate_password_hash('password123'),
                city='Paris',
                logo_path='res/logo/dunes.png'
            )
            db.session.add(c)
    db.session.commit()

    # Create 30 players with provided dataset
    players_data = [
        ("Luc", "James", "player1@dunes.fr", "tier1"),
        ("Marc", "Johnson", "player2@dunes.fr", "tier2"),
        ("Jean", "Williams", "player3@dunes.fr", "tier2"),
        ("Pierre", "Brown", "player4@dunes.fr", "tier3"),
        ("Nicolas", "Jones", "player5@dunes.fr", "tier1"),
        ("Philippe", "Garcia", "player6@dunes.fr", "tier2"),
        ("Laurent", "Miller", "player7@dunes.fr", "tier1"),
        ("Olivier", "Davis", "player8@dunes.fr", "tier3"),
        ("David", "Rodriguez", "player9@dunes.fr", "tier2"),
        ("Thierry", "Martinez", "player10@dunes.fr", "tier3"),
        ("Eric", "Hernandez", "player11@dunes.fr", "tier2"),
        ("Christian", "Lopez", "player12@dunes.fr", "tier2"),
        ("Vincent", "Sanchez", "player13@dunes.fr", "tier2"),
        ("Francois", "Clark", "player14@dunes.fr", "tier1"),
        ("Michel", "Lewis", "player15@dunes.fr", "tier1"),
        ("Anthony", "Lee", "player16@dunes.fr", "tier3"),
        ("Jamal", "Walker", "player17@dunes.fr", "tier1"),
        ("DeShawn", "Hall", "player18@dunes.fr", "tier2"),
        ("Marcus", "Allen", "player19@dunes.fr", "tier1"),
        ("Andre", "Young", "player20@dunes.fr", "tier1"),
        ("Tyrone", "Durand", "player21@dunes.fr", "tier1"),
        ("Isiah", "Moreau", "player22@dunes.fr", "tier1"),
        ("Magic", "Simon", "player23@dunes.fr", "tier1"),
        ("Larry", "Laurent", "player24@dunes.fr", "tier2"),
        ("Charles", "Lefevre", "player25@dunes.fr", "tier3"),
        ("Scottie", "Dupont", "player26@dunes.fr", "tier3"),
        ("Michael", "Bernard", "player27@dunes.fr", "tier1"),
        ("Kobe", "Petit", "player28@dunes.fr", "tier1"),
        ("LeBron", "Gérard", "player29@dunes.fr", "tier1"),
        ("Stephen", "Fournier", "player30@dunes.fr", "tier3"),
    ]
    for first_name, last_name, email, tier in players_data:
        if not Player.query.filter_by(email=email).first():
            p = Player(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password_hash=generate_password_hash('password123'),
                subscription_tier=tier
            )
            db.session.add(p)
    db.session.commit()

    # Link first 15 players to corresponding clubs
    clubs = Club.query.order_by(Club.id).all()
    players = Player.query.order_by(Player.id).all()
    for idx in range(min(15, len(clubs), len(players))):
        c = clubs[idx]
        p = players[idx]
        if ClubPlayer.query.filter_by(club_id=c.id, player_id=p.id).count() == 0:
            db.session.add(ClubPlayer(club_id=c.id, player_id=p.id, status='interested'))
    db.session.commit()

    # Seed one stat/performance per first 10 players
    for p in players[:10]:
        if PlayerStat.query.filter_by(player_id=p.id).count() == 0:
            db.session.add(PlayerStat(player_id=p.id, points_per_game=12.3, assists_per_game=5.1, rebounds_per_game=6.8))
        if Performance.query.filter_by(player_id=p.id).count() == 0:
            db.session.add(Performance(player_id=p.id, game_date=datetime.utcnow().date(), points=22, assists=7, rebounds=9, field_goals_made=8, field_goals_attempted=15, opponent='Lyon Elite'))
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        ensure_defaults()
        print('Seed completed:', {'clubs': Club.query.count(), 'players': Player.query.count()})
