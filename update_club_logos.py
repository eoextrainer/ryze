#!/usr/bin/env python3
"""
Update club logos in database
"""

from app import app, db, Club

def update_club_logos():
    """Assign logos to all clubs"""
    with app.app_context():
        clubs = Club.query.order_by(Club.id).all()
        
        # Logo mapping - using appropriate file extensions
        logo_files = [
            'logo-1.png', 'logo-2.png', 'logo-3.jpeg', 'logo-4.png', 'logo-5.png',
            'logo-6.jpeg', 'logo-7.png', 'logo-8.jpeg', 'logo-9.png', 'logo-10.jpeg',
            'logo-11.png', 'logo-12.jpeg', 'logo-13.jpeg', 'logo-14.jpeg', 'logo-15.png'
        ]
        
        for i, club in enumerate(clubs):
            club.logo_path = f'res/logo/{logo_files[i]}'
            print(f"✅ {club.name}: {club.logo_path}")
        
        db.session.commit()
        print(f"\n✅ Updated logos for {len(clubs)} clubs")

if __name__ == '__main__':
    update_club_logos()
