import pygame
import pygame_gui
from src.game.game_state import GameState


class EventManager:
    def __init__(self):
        self.events = []

    def process_events(self, game):
        for event in pygame.event.get():
            game.UI_manager.process_events(event)

            # UI sound feedback
            if event.type == pygame.USEREVENT and hasattr(event, 'user_type'):
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    game.audio_manager.play_ui_click()
                elif event.user_type == pygame_gui.UI_BUTTON_ON_HOVERED:
                    game.audio_manager.play_ui_hover()

            if event.type == pygame.QUIT:
                game.is_running = False
                return

            if event.type == pygame.USEREVENT:
                self._handle_ui_event(event, game)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_event(event, game)
            elif event.type == pygame.KEYDOWN:
                self._handle_key_event(event, game)

    def _handle_ui_event(self, event, game):
        if not hasattr(event, 'user_type'):
            return
        if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            self._dispatch_button(event.ui_element, game)
            # Secondary handlers that coexist with the primary per-state dispatch
            from src.game.game_state import GameState
            if game.current_state == GameState.PLAYING:
                game.UI_manager.player_info_panel.handle_events(event, game)
                game.tower_info_panel.handle_events(event, game)
            elif game.current_state == GameState.PAUSED:
                game.UI_manager.pause_screen.handle_events(event, game)
        elif event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            self._dispatch_slider(event.ui_element, event.value, game)
        elif event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
            game.UI_manager.game_data_screen.on_confirmation(game)

    def _handle_key_event(self, event, game):
        if event.key == pygame.K_ESCAPE:
            if game.current_state == GameState.PLAYING:
                if game.is_build_mode:
                    game.tower_selection_panel.deselect()
                    game.is_build_mode = False
                else:
                    game.state_manager.change_state(GameState.PAUSED)
            elif game.current_state == GameState.PAUSED:
                game.UI_manager.pause_screen.close_screen()
                game.state_manager.change_state(GameState.PLAYING)
        elif game.current_state == GameState.PLAYING:
            # Number keys 1-9 select towers by index
            num_keys = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,
                        pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]
            if event.key in num_keys:
                from src.config.config import TOWER_TYPES
                tower_list = list(TOWER_TYPES.keys())
                idx = num_keys.index(event.key)
                if idx < len(tower_list):
                    game.tower_selection_panel.update_selected_tower(tower_list[idx])
                    game.is_build_mode = True
            elif event.key == pygame.K_SPACE:
                # Space bar starts the next wave early
                level = game.level_manager.current_level
                if level:
                    next_idx = level.current_wave_index + 1
                    if next_idx < len(level.enemy_wave_list):
                        wave_panel = game.level_manager.wave_panel
                        if wave_panel.start_wave_manually(next_idx, level):
                            gold_bonus = int(50 * (next_idx + 1))
                            game.player.add_gold(gold_bonus)
                            game.UI_manager.player_info_panel.gold_label.set_text(f"Gold: {game.player.gold}")

    def _handle_mouse_event(self, event, game):
        if game.current_state == GameState.CAMPAIGN_MAP:
            game.UI_manager.campaign_map.on_click(event.pos, game)
        elif game.current_state == GameState.PLAYING:
            if event.button == 3:  # right-click cancels build mode
                game.tower_selection_panel.deselect()
                game.is_build_mode = False
                return
            if game.tower_selection_panel.is_within_panel(event.pos):
                game.tower_selection_panel.on_click(event.pos, game)
            else:
                # Check if clicking on a placed tower first
                clicked_tower = game.tower_manager.handle_click(event.pos)
                if not clicked_tower and game.is_build_mode and game.tower_manager.selected_tower_type is not None:
                    success = game.tower_manager.add_tower_if_possible(
                        event.pos[0], event.pos[1], game.player, game
                    )
                    if success:
                        game.is_build_mode = False

    def _dispatch_button(self, ui_element, game):
        state = game.current_state
        ui = game.UI_manager

        mapping = {
            GameState.MAIN_MENU: ui.main_menu.on_button_pressed,
            GameState.OPTIONS: ui.options_screen.on_button_pressed,
            GameState.LOAD_GAME: ui.game_data_screen.on_button_pressed,
            GameState.CAMPAIGN_MAP: ui.campaign_map.on_button_pressed,
            GameState.SKILLS: ui.skills_screen.on_button_pressed,
            GameState.LEVEL_COMPLETE: ui.level_end_screen.on_button_pressed,
            GameState.LEVEL_DEFEAT: ui.level_end_screen.on_button_pressed,
            GameState.PLAYING: game.level_manager.wave_panel.on_button_pressed,
        }

        if state in mapping:
            mapping[state](ui_element, game)

    def _dispatch_slider(self, ui_element, value, game):
        ui = game.UI_manager.options_screen
        ui.on_slider_moved(ui_element, value)

    def add_event(self, event):
        self.events.append(event)
