import pygame
import pygame_gui

from src.config.config import UI_BUTTON_SIZE
from src.screens.screen import Screen


class WavePanel(Screen):
    def __init__(self, ui_manager, level_manager, screen):
        # Initialize the base Screen class
        super().__init__(screen, ui_manager, None)  # Pass None if no background image, or specify a path
        self.level_manager = level_manager
        self.buttons = []
        self.ui_manager = ui_manager
        self.level_manager = level_manager
        self.screen = screen
        self.buttons = []
        self.create_wave_buttons()


    def create_wave_buttons(self):
        if self.level_manager.current_level:
            for i, wave in enumerate(self.level_manager.current_level.enemy_wave_list):
                button = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect(50 + i * UI_BUTTON_SIZE[0], 600, UI_BUTTON_SIZE[0], UI_BUTTON_SIZE[1]),
                    text=f'Wave {i + 1}',
                    manager=self.ui_manager
                )
                self.buttons.append(button)

    def handle_events(self, events):
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                for i, button in enumerate(self.buttons):
                    if event.ui_element == button:
                        # Start the corresponding wave manually
                        # TODO make buttons start waves
                        self.level_manager.current_level.enemy_wave_list[i].start()
                        break

    # def draw(self):
    #     # Custom drawing code for the panel, if you have additional information to render
    #     for i, wave in enumerate(self.level_manager.current_level.enemy_wave_list):
    #         # Example: Draw a simple text indicating the wave's status
    #         font = pygame.font.Font(None, 24)
    #         status_text = "Ready" if wave.manually_started else "Waiting"
    #         text_surf = font.render(status_text, True, (255, 255, 255))
    #         self.screen.blit(text_surf, (10, 300 + i *  UI_BUTTON_SIZE[1] - 20))

    def update(self, time_delta):
        # Update UI Manager
        self.ui_manager.update(time_delta)
        self.update_wave_buttons()
        # Here you can also include any logic to update the text on buttons or other states
        # based on the game's current status. For example:
        for i, button in enumerate(self.buttons):
            wave = self.level_manager.current_level.enemy_wave_list[i]
            if wave.manually_started:
                button.set_text(f"Wave {i+1} - Started")
            else:
                button.set_text(f"Wave {i+1}")

    def update_wave_buttons(self):
        # Clear existing buttons if any
        for button in self.buttons:
            button.kill()  # Assuming pygame_gui elements have a kill method to remove them
        self.buttons.clear()

        # Recreate buttons based on the current level's waves
        if self.level_manager.current_level:
            self.create_wave_buttons()