"""Policy Forge game-train — additive human/oracle trajectories into MetaBrain.

Browser game exports JSON packs; ``ingest_game_pack`` runs offline meta_update
steps on the champion (never at inference). Goal axes: G-TRAIN, G-CLEAR, G-A13,
G-SIGHT…G-HEAR, G-NO_RETRAIN.
"""

from .ingest import ingest_game_pack, load_pack

__all__ = ["ingest_game_pack", "load_pack"]
