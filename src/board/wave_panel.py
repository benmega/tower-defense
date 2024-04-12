import pygame
import pygame_gui

from src.config.config import UI_BUTTON_SIZE, SCREEN_WIDTH, PLAYER_EARLY_WAVE_BONUS_MULTIPLIER
from src.screens.screen import Screen


class WavePanel(Screen):
    def __init__(self, ui_manager):
        super().__init__(ui_manager, None)  # Pass None if no background image, or specify a path
        self.buttons = []
        self.buttons = []
        self.start_x = SCREEN_WIDTH - 100  # Starting X position for the rightmost button
        self.pixels_per_second = 20
        self.panel_y = 600

    def create_wave_buttons(self, current_level):
        if current_level:
            for i, wave in enumerate(current_level.enemy_wave_list):
                # Calculate initial X position based on the wave's start time
                # This is a simplified example; adjust logic based on your game's timing and UI layout
                time_until_start = (wave.start_time - pygame.time.get_ticks()) / 1000  # Seconds until wave starts
                position_x = max(0, (time_until_start * self.pixels_per_second))
                button_width = current_level.wave_subsequent_delay / 1000 * self.pixels_per_second
                button = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect(position_x, self.panel_y, button_width, UI_BUTTON_SIZE[1]),
                    text=f'Wave {i + 1}',
                    manager=self.ui_manager,
                    object_id=pygame_gui.core.ObjectID(class_id="@button")
                )
                self.buttons.append(button)

    def handle_events(self, event, game):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                for i, button in enumerate(self.buttons):
                    if event.ui_element == button:
                        if self.start_wave_manually(i, game.level_manager.current_level):
                            game.player.add_gold(button.relative_rect[
                                                     0] * PLAYER_EARLY_WAVE_BONUS_MULTIPLIER)  # gold equal to position times player bonus
                        break

    def update(self, time_delta, enemy_wave_list):
        """

        :param time_delta:
        :param enemy_wave_list: self.level_manager.current_level.enemy_wave_list
        :return:
        """
        # Update UI Manager
        self.ui_manager.update(time_delta)
        # Here you can also include any logic to update the text on buttons or other states
        # based on the game's current status. For example:
        for i, button in enumerate(self.buttons):
            wave = enemy_wave_list[i]
            # Calculate the new position based on the time until the wave starts
            time_until_start = (wave.start_time - pygame.time.get_ticks()) / 1000  # Seconds until wave starts
            position_x = max(0, (time_until_start * self.pixels_per_second))
            if position_x == 0:
                button.visible = False
            # Update the button's position
            button.set_relative_position(pygame.Rect(position_x, button.relative_rect.y,
                                                     button.relative_rect.width, button.relative_rect.height))

    def recreate_wave_buttons(self, current_level):
        # Clear existing buttons if any
        for button in self.buttons:
            button.kill()  # Assuming pygame_gui elements have a kill method to remove them
        self.buttons.clear()

        if current_level:
            self.create_wave_buttons(current_level)

    def start_wave_manually(self, wave_index, current_level):
        # Only allow next wave to be called
        if wave_index != current_level.current_wave_index + 1:
            return False
        current_time = pygame.time.get_ticks()
        manually_started_wave = current_level.enemy_wave_list[wave_index]

        # Calculate how much earlier this wave is starting
        time_adjustment = manually_started_wave.start_time - current_time

        # Adjust the start times of all subsequent waves
        for subsequent_wave in current_level.enemy_wave_list[wave_index + 1:]:
            subsequent_wave.start_time -= time_adjustment

        # Start the wave manually
        manually_started_wave.start_time = current_time
        manually_started_wave.manually_started = True
        current_level.get_next_wave()
        current_level.enemy_wave_list[wave_index].start()
        return True  # Success
