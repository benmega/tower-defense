<<<<<<< HEAD
<<<<<<< HEAD
"""
Design tokens — the single source of truth for all UI values.

RULE: All new UI code reads colors, spacing, and timing from here.
      Never write bare RGB tuples or hex strings in screen/board/manager code.
      When touching existing code, migrate its hardcoded values to this module.
"""

# ── Colors: Medieval Gold & Dark Stone ──────────────────────────────

# Primary palette
GOLD         = "#DAA520"   # selected / active state
GOLD_LIGHT   = "#DCCC94"   # button normal bg
GOLD_BRIGHT  = "#FFD700"   # borders on hover / active
GOLD_DARK    = "#B8860B"   # active bg
PARCHMENT    = "#F0E68C"   # hovered bg
AMBER        = "#E38F2E"   # normal border

# Backgrounds
BG_DARKEST   = "#1A1D22"   # window / modal backdrop
BG_DARK      = "#25292e"   # panel surfaces
BG_MID       = "#2E3440"   # slightly elevated surfaces

# Text
TEXT_WHITE   = "#FFFFFF"
TEXT_LIGHT   = "#c5cbd8"   # labels on dark bg
TEXT_MUTED   = "#6d736f"   # disabled / secondary
TEXT_SHADOW  = "#505050"

# Semantic
HEALTH_GREEN = "#27AE60"
HEALTH_RED   = "#C0392B"
DANGER       = "#E74C3C"
GOLD_INCOME  = "#F1C40F"   # economy / gold indicators

# ── RGB tuples (for pygame draw calls) ──────────────────────────────
# Names mirror the hex constants above so callers never guess.

RGB_BG_DARK      = (37, 41, 46)       # == BG_DARK
RGB_BG_DARKEST   = (26, 29, 34)       # == BG_DARKEST
RGB_BG_MID       = (46, 52, 64)       # == BG_MID
RGB_GOLD_LIGHT   = (220, 204, 148)    # == GOLD_LIGHT
RGB_GOLD_BRIGHT  = (255, 215, 0)      # == GOLD_BRIGHT
RGB_AMBER        = (227, 143, 46)     # == AMBER
RGB_WHITE        = (255, 255, 255)
RGB_BLACK        = (0, 0, 0)
RGB_HEALTH_RED   = (192, 57, 43)
RGB_HEALTH_GREEN = (39, 174, 96)
RGB_PANEL_BG     = (37, 41, 46)       # tower_selection_panel background
RGB_OVERLAY      = (26, 29, 34, 180)  # modal semi-transparent overlay

# ── Spacing scale (pixels, base-4) ──────────────────────────────────
SPACE_XS  = 4
SPACE_SM  = 8
SPACE_MD  = 16
SPACE_LG  = 24
SPACE_XL  = 32
SPACE_2XL = 48
SPACE_3XL = 64

# ── Border radii (pixels) ───────────────────────────────────────────
RADIUS_SM = 6
RADIUS_MD = 14    # matches theme.json button corner radius
RADIUS_LG = 20

# ── Typography sizes (base pixels, before SCALE is applied) ─────────
FONT_XS  = 10
FONT_SM  = 12
FONT_MD  = 16
FONT_LG  = 20
FONT_XL  = 24
FONT_2XL = 32

# ── Animation timing (seconds) ──────────────────────────────────────
ANIM_FAST   = 0.15
ANIM_NORMAL = 0.30
ANIM_SLOW   = 0.50

# ── Sound paths (relative to game working directory) ─────────────────
# Use AudioManager helpers for playback; never call pygame.mixer directly.
SFX_BUTTON_CLICK = 'assets/sounds/mixkit-light-hammering-on-metal-798.wav'
SFX_BUTTON_HOVER = 'assets/sounds/mixkit-tape-measure-extend-810.wav'
SFX_MENU_OPEN    = 'assets/sounds/mixkit-metal-medieval-construction-818.wav'
SFX_SUCCESS      = 'assets/sounds/mixkit-fantasy-game-success-notification-270.wav'
SFX_UNLOCK       = 'assets/sounds/mixkit-unlock-game-notification-253.wav'
SFX_WIN_FANFARE  = 'assets/sounds/mixkit-medieval-show-fanfare-announcement-226.wav'
SFX_TOWER_BUILD  = 'assets/sounds/hammer-hit-on-wood.wav'
=======
# RGB color constants
RGB_OVERLAY = (0, 0, 0, 180)
RGB_BG_DARK = (15, 15, 25)
RGB_BG_MID = (35, 35, 55)
RGB_AMBER = (255, 160, 0)
RGB_GOLD_BRIGHT = (255, 215, 0)
RGB_HEALTH_GREEN = (50, 200, 50)
RGB_HEALTH_RED = (220, 50, 50)
GOLD_INCOME = (255, 215, 0)

# UI spacing
SPACE_LG = 20

# Border radius
RADIUS_MD = 8

# Sound effect paths
SFX_SUCCESS = 'assets/sounds/mixkit-fantasy-game-success-notification-270.wav'
SFX_UNLOCK = 'assets/sounds/mixkit-unlock-game-notification-253.wav'
SFX_TOWER_BUILD = 'assets/sounds/tower_build_effect_2.mp3'
>>>>>>> claude/great-franklin-30172d
=======
ANIM_NORMAL = 0.3   # fade/transition duration in seconds

SPACE_SM = 8        # small gap between UI elements
SPACE_MD = 16       # medium margin / padding

TEXT_LIGHT = (230, 230, 230)   # label colour on dark backgrounds
>>>>>>> claude/festive-edison-84275f
