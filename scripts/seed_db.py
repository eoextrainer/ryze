#!/usr/bin/env python3
import os
import sys
from datetime import datetime
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app_server import app, db, Club, Player, ClubPlayer, PlayerStat, Performance, PlayerResume, Agent
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
                logo_path='res/logo/ryze.png'
            )
            db.session.add(c)
    db.session.commit()

    # Create 15 French agents
    agents_data = [
        ("Jean", "Dupont", "agent1@france.fr", "Paris", "Elite Agency", "0600000001"),
        ("Marie", "Durand", "agent2@france.fr", "Lyon", "Pro Agents", "0600000002"),
        ("Pierre", "Lefevre", "agent3@france.fr", "Marseille", "Hexagone Sports", "0600000003"),
        ("Luc", "Moreau", "agent4@france.fr", "Toulouse", "Elite Agency", "0600000004"),
        ("Sophie", "Lambert", "agent5@france.fr", "Nice", "Pro Agents", "0600000005"),
        ("Antoine", "Roux", "agent6@france.fr", "Nantes", "Hexagone Sports", "0600000006"),
        ("Claire", "Fontaine", "agent7@france.fr", "Strasbourg", "Elite Agency", "0600000007"),
        ("Julien", "Garnier", "agent8@france.fr", "Montpellier", "Pro Agents", "0600000008"),
        ("Camille", "Faure", "agent9@france.fr", "Bordeaux", "Hexagone Sports", "0600000009"),
        ("Hugo", "Blanc", "agent10@france.fr", "Lille", "Elite Agency", "0600000010"),
        ("Emma", "Perrin", "agent11@france.fr", "Rennes", "Pro Agents", "0600000011"),
        ("Louis", "Marchand", "agent12@france.fr", "Reims", "Hexagone Sports", "0600000012"),
        ("Chloe", "Robin", "agent13@france.fr", "Le Havre", "Elite Agency", "0600000013"),
        ("Lucas", "Guerin", "agent14@france.fr", "Saint-Etienne", "Pro Agents", "0600000014"),
        ("Manon", "Benoit", "agent15@france.fr", "Grenoble", "Hexagone Sports", "0600000015"),
    ]
    for first_name, last_name, email, city, agency, phone in agents_data:
        if not Agent.query.filter_by(email=email).first():
            a = Agent(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password_hash=generate_password_hash('password123'),
                city=city,
                agency=agency,
                phone=phone
            )
            db.session.add(a)
    db.session.commit()

    # Create 30 players with provided dataset
    players_data = [
        ("Luc", "James", "player1@ryze.fr", "tier1"),
        ("Marc", "Johnson", "player2@ryze.fr", "tier2"),
        ("Jean", "Williams", "player3@ryze.fr", "tier2"),
        ("Pierre", "Brown", "player4@ryze.fr", "tier3"),
        ("Nicolas", "Jones", "player5@ryze.fr", "tier1"),
        ("Philippe", "Garcia", "player6@ryze.fr", "tier2"),
        ("Laurent", "Miller", "player7@ryze.fr", "tier1"),
        ("Olivier", "Davis", "player8@ryze.fr", "tier3"),
        ("David", "Rodriguez", "player9@ryze.fr", "tier2"),
        ("Thierry", "Martinez", "player10@ryze.fr", "tier3"),
        ("Eric", "Hernandez", "player11@ryze.fr", "tier2"),
        ("Christian", "Lopez", "player12@ryze.fr", "tier2"),
        ("Vincent", "Sanchez", "player13@ryze.fr", "tier2"),
        ("Francois", "Clark", "player14@ryze.fr", "tier1"),
        ("Michel", "Lewis", "player15@ryze.fr", "tier1"),
        ("Anthony", "Lee", "player16@ryze.fr", "tier3"),
        ("Jamal", "Walker", "player17@ryze.fr", "tier1"),
        ("DeShawn", "Hall", "player18@ryze.fr", "tier2"),
        ("Marcus", "Allen", "player19@ryze.fr", "tier1"),
        ("Andre", "Young", "player20@ryze.fr", "tier1"),
        ("Tyrone", "Durand", "player21@ryze.fr", "tier1"),
        ("Isiah", "Moreau", "player22@ryze.fr", "tier1"),
        ("Magic", "Simon", "player23@ryze.fr", "tier1"),
        ("Larry", "Laurent", "player24@ryze.fr", "tier2"),
        ("Charles", "Lefevre", "player25@ryze.fr", "tier3"),
        ("Scottie", "Dupont", "player26@ryze.fr", "tier3"),
        ("Michael", "Bernard", "player27@ryze.fr", "tier1"),
        ("Kobe", "Petit", "player28@ryze.fr", "tier1"),
        ("LeBron", "Gérard", "player29@ryze.fr", "tier1"),
        ("Stephen", "Fournier", "player30@ryze.fr", "tier3"),
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
