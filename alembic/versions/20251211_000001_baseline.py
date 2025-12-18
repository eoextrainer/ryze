from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20251211_000001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('clubs',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=120), nullable=False, unique=True),
        sa.Column('tier', sa.String(length=10), nullable=False),
        sa.Column('email', sa.String(length=120), nullable=False, unique=True),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('city', sa.String(length=120)),
        sa.Column('logo_path', sa.String(length=255)),
        sa.Column('created_at', sa.DateTime())
    )

    op.create_table('players',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('first_name', sa.String(length=120), nullable=False),
        sa.Column('last_name', sa.String(length=120), nullable=False),
        sa.Column('email', sa.String(length=120), nullable=False, unique=True),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('date_of_birth', sa.Date()),
        sa.Column('height', sa.Float()),
        sa.Column('weight', sa.Float()),
        sa.Column('nationality', sa.String(length=120)),
        sa.Column('position', sa.String(length=50)),
        sa.Column('photo_path', sa.String(length=255)),
        sa.Column('subscription_tier', sa.String(length=20), nullable=False),
        sa.Column('subscription_start', sa.DateTime()),
        sa.Column('subscription_end', sa.DateTime()),
        sa.Column('created_at', sa.DateTime())
    )

    op.create_table('club_player',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('club_id', sa.Integer(), sa.ForeignKey('clubs.id'), nullable=False),
        sa.Column('player_id', sa.Integer(), sa.ForeignKey('players.id'), nullable=False),
        sa.Column('status', sa.String(length=20))
    )

    op.create_table('player_stats',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('player_id', sa.Integer(), sa.ForeignKey('players.id'), nullable=False),
        sa.Column('points_per_game', sa.Float()),
        sa.Column('assists_per_game', sa.Float()),
        sa.Column('rebounds_per_game', sa.Float()),
        sa.Column('field_goal_percentage', sa.Float()),
        sa.Column('speed_kmh', sa.Float()),
        sa.Column('attack_performance_score', sa.Float()),
        sa.Column('updated_at', sa.DateTime())
    )

    op.create_table('performances',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('player_id', sa.Integer(), sa.ForeignKey('players.id'), nullable=False),
        sa.Column('game_date', sa.Date(), nullable=False),
        sa.Column('points', sa.Integer()),
        sa.Column('assists', sa.Integer()),
        sa.Column('rebounds', sa.Integer()),
        sa.Column('field_goals_made', sa.Integer()),
        sa.Column('field_goals_attempted', sa.Integer()),
        sa.Column('opponent', sa.String(length=120))
    )

    op.create_table('player_resume',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('player_id', sa.Integer(), sa.ForeignKey('players.id'), nullable=False),
        sa.Column('club_id', sa.Integer(), sa.ForeignKey('clubs.id'), nullable=False),
        sa.Column('season_start', sa.Integer()),
        sa.Column('season_end', sa.Integer()),
        sa.Column('is_current', sa.Boolean()),
        sa.Column('is_future', sa.Boolean())
    )


def downgrade():
    op.drop_table('player_resume')
    op.drop_table('performances')
    op.drop_table('player_stats')
    op.drop_table('club_player')
    op.drop_table('players')
    op.drop_table('clubs')
