#!/usr/bin/env python3
"""
ryze Basketball Platform - Complete User Credentials Report
Lists all player and club login credentials for verification
"""

from app import app, db, Club, Player

def generate_credentials_report():
    """Generate a comprehensive credentials report"""
    with app.app_context():
        print("\n" + "="*80)
        print("ryze BASKETBALL PLATFORM - USER CREDENTIALS REPORT")
        print("="*80)
        
        # All Players
        print("\n" + "="*80)
        print("ALL 30 PLAYER CREDENTIALS")
        print("="*80)
        print(f"\n{'#':<4} {'Name':<25} {'Email':<30} {'Tier':<8} {'Position':<10}")
        print("-" * 80)
        
        players = Player.query.order_by(Player.id).all()
        for i, player in enumerate(players, 1):
            tier_icon = {"tier1": "💎", "tier2": "⭐", "tier3": "🎯"}.get(player.subscription_tier, "❓")
            print(f"{i:<4} {player.first_name + ' ' + player.last_name:<25} {player.email:<30} {tier_icon} {player.subscription_tier:<8} {player.position:<10}")
        
        print(f"\n{'Default Password for ALL Players:':<40} password123")
        
        # Subscription tier breakdown
        print("\n" + "-"*80)
        print("SUBSCRIPTION TIER BREAKDOWN:")
        tier1_count = Player.query.filter_by(subscription_tier='tier1').count()
        tier2_count = Player.query.filter_by(subscription_tier='tier2').count()
        tier3_count = Player.query.filter_by(subscription_tier='tier3').count()
        
        print(f"  💎 Tier 1 (Premium - 50€, all clubs):        {tier1_count} players")
        print(f"  ⭐ Tier 2 (Pro - 29.99€, N1-N3 only):       {tier2_count} players")
        print(f"  🎯 Tier 3 (Basic - 9.99€, N3 only):         {tier3_count} players")
        
        # All Clubs
        print("\n" + "="*80)
        print("ALL 15 CLUB CREDENTIALS")
        print("="*80)
        print(f"\n{'#':<4} {'Club Name':<28} {'Email':<35} {'Tier':<8} {'City':<12}")
        print("-" * 80)
        
        clubs = Club.query.order_by(Club.id).all()
        tier_icons = {'Pro A': '🏆', 'Pro B': '⭐', 'N1': '🎯', 'N2': '🌟', 'N3': '🎪'}
        
        for i, club in enumerate(clubs, 1):
            icon = tier_icons.get(club.tier, "❓")
            print(f"{i:<4} {club.name:<28} {club.email:<35} {icon} {club.tier:<8} {club.city:<12}")
        
        print(f"\n{'Default Password for ALL Clubs:':<40} password123")
        
        # Club tier breakdown
        print("\n" + "-"*80)
        print("CLUB TIER BREAKDOWN:")
        for tier in ['Pro A', 'Pro B', 'N1', 'N2', 'N3']:
            count = Club.query.filter_by(tier=tier).count()
            icon = tier_icons.get(tier, "❓")
            print(f"  {icon} {tier:<10} {count} clubs")
        
        # Quick test credentials
        print("\n" + "="*80)
        print("QUICK TEST CREDENTIALS")
        print("="*80)
        print("\nPlayer Examples (All passwords: password123):")
        print("  - player1@ryze.fr   (Luc James, tier1 💎, Forward)")
        print("  - player2@ryze.fr   (Marc Johnson, tier2 ⭐, Guard)")
        print("  - player4@ryze.fr   (Pierre Brown, tier3 🎯, Center)")
        print("  - player15@ryze.fr  (Michel Lewis, tier1 💎)")
        print("  - player30@ryze.fr  (Stephen Fournier, tier3 🎯)")
        
        print("\nClub Examples (All passwords: password123):")
        print("  - contact@parisbball.fr   (Paris Basketball, Pro A 🏆)")
        print("  - contact@strasbourg.fr   (Strasbourg IG, Pro B ⭐)")
        print("  - contact@boulogne.fr     (Boulogne-Levallois, N1 🎯)")
        print("  - contact@toulouse.fr     (Toulouse, N2 🌟)")
        print("  - contact@lille.fr        (Lille, N3 🎪)")
        
        # Access instructions
        print("\n" + "="*80)
        print("ACCESS INSTRUCTIONS")
        print("="*80)
        print("\n1. Open browser: http://localhost:8000")
        print("2. Click 'Login' in top-right navigation")
        print("3. Toggle between 'Club Login' and 'Player Login'")
        print("4. Enter email and password: password123")
        print("5. Access dashboard with personalized data")
        
        print("\n" + "="*80)
        print("DATABASE STATISTICS")
        print("="*80)
        
        from app import PlayerStat, Performance, PlayerResume, ClubPlayer
        
        stats_count = PlayerStat.query.count()
        perf_count = Performance.query.count()
        resume_count = PlayerResume.query.count()
        link_count = ClubPlayer.query.count()
        
        print(f"\nTotal Records in Database:")
        print(f"  - Clubs:              {clubs.__len__()} records")
        print(f"  - Players:            {players.__len__()} records")
        print(f"  - Player Stats:       {stats_count} records")
        print(f"  - Performances:       {perf_count} records (10 games per player)")
        print(f"  - Player Resumes:     {resume_count} records")
        print(f"  - Club-Player Links:  {link_count} relationships")
        
        print("\n" + "="*80 + "\n")


if __name__ == '__main__':
    generate_credentials_report()
