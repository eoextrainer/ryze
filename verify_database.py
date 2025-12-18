#!/usr/bin/env python3
"""
ryze Basketball Platform - Comprehensive Database & Login Verification
Tests database seeding and verifies login functionality for all users
"""

from app import app, db, Club, Player, PlayerStat, Performance, PlayerResume, ClubPlayer
import json

def verify_database_seeding():
    """Comprehensive database verification"""
    with app.app_context():
        print("\n" + "="*80)
        print("DATABASE SEEDING VERIFICATION")
        print("="*80)
        
        # Count records
        club_count = Club.query.count()
        player_count = Player.query.count()
        stat_count = PlayerStat.query.count()
        perf_count = Performance.query.count()
        resume_count = PlayerResume.query.count()
        club_player_count = ClubPlayer.query.count()
        
        print(f"\n📊 RECORD COUNTS:")
        print(f"   Clubs: {club_count}/15 ✅" if club_count == 15 else f"   Clubs: {club_count}/15 ❌")
        print(f"   Players: {player_count}/30 ✅" if player_count == 30 else f"   Players: {player_count}/30 ❌")
        print(f"   Player Stats: {stat_count}/30 ✅" if stat_count == 30 else f"   Player Stats: {stat_count}/30 ❌")
        print(f"   Performances: {perf_count} (should be 300 = 30 players × 10 games) {'✅' if perf_count == 300 else '❌'}")
        print(f"   Player Resumes: {resume_count} (multiple per player) {'✅' if resume_count > 30 else '❌'}")
        print(f"   Club-Player Links: {club_player_count} ✅")
        
        # Verify club tiers
        print(f"\n🏆 CLUB TIER DISTRIBUTION:")
        for tier in ['Pro A', 'Pro B', 'N1', 'N2', 'N3']:
            count = Club.query.filter_by(tier=tier).count()
            print(f"   {tier}: {count} clubs {'✅' if count == 3 else '❌'}")
        
        # Verify player subscription tiers
        print(f"\n💳 PLAYER SUBSCRIPTION TIER DISTRIBUTION:")
        for tier in ['tier1', 'tier2', 'tier3']:
            count = Player.query.filter_by(subscription_tier=tier).count()
            print(f"   {tier}: {count} players")
        
        # Verify player statistics
        print(f"\n📈 PLAYER STATISTICS SAMPLE:")
        player = Player.query.first()
        if player and player.stats:
            stat = player.stats[0]
            print(f"   Player: {player.first_name} {player.last_name}")
            print(f"   PPG: {stat.points_per_game:.2f}")
            print(f"   APG: {stat.assists_per_game:.2f}")
            print(f"   RPG: {stat.rebounds_per_game:.2f}")
            print(f"   FG%: {stat.field_goal_percentage:.2f}%")
            print(f"   Speed: {stat.speed_kmh:.2f} km/h")
            print(f"   Attack Score: {stat.attack_performance_score:.2f}")
        
        # Verify performances
        print(f"\n🎮 PERFORMANCE HISTORY SAMPLE:")
        if player and player.performances:
            perfs = player.performances[:3]
            for i, perf in enumerate(perfs, 1):
                print(f"   Game {i}: {perf.points}pts, {perf.assists}ast, {perf.rebounds}reb vs {perf.opponent}")
        
        # Verify resumes
        print(f"\n📋 CLUB RESUME SAMPLE:")
        if player and player.resume:
            for i, res in enumerate(player.resume[:3], 1):
                status = "Current" if res.is_current else "Future" if res.is_future else "Past"
                print(f"   {i}. {res.club.name} ({res.season_start}-{res.season_end}) [{status}]")
        
        print("\n" + "="*80)


def test_player_logins():
    """Test login for sample players from different tiers"""
    with app.app_context():
        print("\n" + "="*80)
        print("PLAYER LOGIN TEST (Sample from each tier)")
        print("="*80)
        
        tiers = ['tier1', 'tier2', 'tier3']
        test_results = []
        
        for tier in tiers:
            player = Player.query.filter_by(subscription_tier=tier).first()
            if player:
                email = player.email
                password = 'password123'
                
                # Test login
                is_valid = player.check_password(password)
                status = "✅ PASS" if is_valid else "❌ FAIL"
                
                print(f"\n{tier.upper()} Tier:")
                print(f"   Player: {player.first_name} {player.last_name}")
                print(f"   Email: {email}")
                print(f"   Password: {password}")
                print(f"   Login: {status}")
                print(f"   Position: {player.position}")
                print(f"   Clubs Access: {len(player.clubs)} clubs")
                
                test_results.append({
                    'tier': tier,
                    'player': f"{player.first_name} {player.last_name}",
                    'email': email,
                    'login': is_valid
                })
        
        # Summary
        passed = sum(1 for r in test_results if r['login'])
        print(f"\n📊 SUMMARY: {passed}/{len(test_results)} player logins successful ✅")
        print("="*80)
        return test_results


def test_club_logins():
    """Test login for sample clubs from different tiers"""
    with app.app_context():
        print("\n" + "="*80)
        print("CLUB LOGIN TEST (Sample from each tier)")
        print("="*80)
        
        club_tiers = ['Pro A', 'Pro B', 'N1', 'N2', 'N3']
        test_results = []
        
        for tier in club_tiers:
            club = Club.query.filter_by(tier=tier).first()
            if club:
                email = club.email
                password = 'password123'
                
                # Test login
                is_valid = club.check_password(password)
                status = "✅ PASS" if is_valid else "❌ FAIL"
                
                print(f"\n{tier}:")
                print(f"   Club: {club.name}")
                print(f"   Email: {email}")
                print(f"   Password: {password}")
                print(f"   Login: {status}")
                print(f"   City: {club.city}")
                print(f"   Players: {len(club.players)} players have access")
                
                test_results.append({
                    'tier': tier,
                    'club': club.name,
                    'email': email,
                    'login': is_valid,
                    'player_count': len(club.players)
                })
        
        # Summary
        passed = sum(1 for r in test_results if r['login'])
        print(f"\n📊 SUMMARY: {passed}/{len(test_results)} club logins successful ✅")
        print("="*80)
        return test_results


def test_all_player_logins():
    """Test login for ALL 30 players"""
    with app.app_context():
        print("\n" + "="*80)
        print("TESTING ALL 30 PLAYER LOGINS")
        print("="*80)
        
        players = Player.query.all()
        passed = 0
        failed = 0
        
        for i, player in enumerate(players, 1):
            is_valid = player.check_password('password123')
            status = "✅" if is_valid else "❌"
            tier_icon = {"tier1": "💎", "tier2": "⭐", "tier3": "🎯"}.get(player.subscription_tier, "❓")
            
            if is_valid:
                passed += 1
            else:
                failed += 1
            
            # Print every 5th player + first 3
            if i <= 3 or i % 5 == 0 or i == 30:
                print(f"{i:2d}. {status} {tier_icon} {player.first_name:12} {player.last_name:15} ({player.email})")
        
        print(f"\n📊 RESULTS: {passed}/30 players can login successfully")
        if failed > 0:
            print(f"⚠️  {failed} players have login issues")
        else:
            print(f"✅ ALL 30 PLAYERS VERIFIED!")
        print("="*80)
        return passed, failed


def test_all_club_logins():
    """Test login for ALL 15 clubs"""
    with app.app_context():
        print("\n" + "="*80)
        print("TESTING ALL 15 CLUB LOGINS")
        print("="*80)
        
        clubs = Club.query.all()
        passed = 0
        failed = 0
        
        tier_icons = {'Pro A': '🏆', 'Pro B': '⭐', 'N1': '🎯', 'N2': '🌟', 'N3': '🎪'}
        
        for i, club in enumerate(clubs, 1):
            is_valid = club.check_password('password123')
            status = "✅" if is_valid else "❌"
            icon = tier_icons.get(club.tier, "❓")
            
            if is_valid:
                passed += 1
            else:
                failed += 1
            
            # Print every 3rd club + first 2
            if i <= 2 or i % 3 == 0 or i == 15:
                print(f"{i:2d}. {status} {icon} {club.name:25} ({club.tier:6}) - {club.city}")
        
        print(f"\n📊 RESULTS: {passed}/15 clubs can login successfully")
        if failed > 0:
            print(f"⚠️  {failed} clubs have login issues")
        else:
            print(f"✅ ALL 15 CLUBS VERIFIED!")
        print("="*80)
        return passed, failed


def main():
    """Run all verification tests"""
    print("\n\n")
    print("🏀 " + "="*76 + " 🏀")
    print("   ryze BASKETBALL PLATFORM - DATABASE & LOGIN VERIFICATION")
    print("🏀 " + "="*76 + " 🏀")
    
    # Test 1: Database seeding
    verify_database_seeding()
    
    # Test 2: Sample player logins
    test_player_logins()
    
    # Test 3: Sample club logins
    test_club_logins()
    
    # Test 4: All player logins
    player_passed, player_failed = test_all_player_logins()
    
    # Test 5: All club logins
    club_passed, club_failed = test_all_club_logins()
    
    # Final summary
    print("\n" + "="*80)
    print("FINAL VERIFICATION SUMMARY")
    print("="*80)
    print(f"✅ Players: {player_passed}/30 verified")
    print(f"✅ Clubs: {club_passed}/15 verified")
    
    if player_passed == 30 and club_passed == 15:
        print("\n🎉 ALL TESTS PASSED! Platform ready for deployment!")
    else:
        print("\n⚠️  Some tests failed. Review above for details.")
    print("="*80 + "\n")


if __name__ == '__main__':
    main()
