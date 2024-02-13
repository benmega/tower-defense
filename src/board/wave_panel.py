import pygame
import pygame_gui

from src.config.config import UI_BUTTON_SIZE, SCREEN_WIDTH
from src.screens.screen import Screen


class WavePanel(Screen):
    def __init__(self, screen, ui_manager, level_manager):
        # Initialize the base Screen class
        super().__init__(screen, ui_manager, None)  # Pass None if no background image, or specify a path
        self.level_manager = level_manager
        self.buttons = []
        #self.ui_manager = ui_manager
        self.level_manager = level_manager
        #self.screen = screen
        self.buttons = []
        self.start_x = SCREEN_WIDTH - 100  # Starting X position for the rightmost button
        self.create_wave_buttons()
        self.pixels_per_second = 20


    def create_wave_buttons(self):
        if self.level_manager.current_level:
            for i, wave in enumerate(self.level_manager.current_level.enemy_wave_list):
                # Calculate initial X position based on the wave's start time
                # This is a simplified example; adjust logic based on your game's timing and UI layout
                time_until_start = (wave.start_time - pygame.time.get_ticks()) / 1000  # Seconds until wave starts
                position_x = max(0, (time_until_start * self.pixels_per_second))
                button_width = self.level_manager.current_level.wave_subsequent_delay/1000 * self.pixels_per_second
                button = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect(position_x, 600, button_width, UI_BUTTON_SIZE[1]),
                    text=f'Wave {i + 1}',
                    manager=self.ui_manager,
                    object_id = pygame_gui.core.ObjectID(class_id="@button")
                )
                self.buttons.append(button)

    def handle_events(self, event, game):
        #print(event.type)  # Print the event type to confirm we're seeing USEREVENTs
        if event.type == pygame.USEREVENT:
            #print("USEREVENT Detected", event.user_type)  # Now print the user_type of the USEREVENT
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                print("Button pressed event detected")  # Confirm we've detected a button press
                for i, button in enumerate(self.buttons):
                    if event.ui_element == button:
                        print(f"Button {i + 1} pressed - Wave {i + 1}")
                        # Start the corresponding wave manually
                        #wave.start()
                        self.start_wave_manually(i)
                        self.level_manager.current_level.get_next_wave()
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
        # Here you can also include any logic to update the text on buttons or other states
        # based on the game's current status. For example:
        for i, button in enumerate(self.buttons):
            wave = self.level_manager.current_level.enemy_wave_list[i]
            # Calculate the new position based on the time until the wave starts
            time_until_start = (wave.start_time - pygame.time.get_ticks()) / 1000  # Seconds until wave starts
            position_x = max(0, (time_until_start * self.pixels_per_second))
            if position_x == 0:
                button.visible = False
            # Update the button's position
            button.set_relative_position(pygame.Rect(position_x, button.relative_rect.y,
                                                     button.relative_rect.width, button.relative_rect.height))
            if wave.manually_started:
                button.set_text(f"Wave {i+1} - Started")
            else:
                button.set_text(f"Wave {i+1}")

    def recreate_wave_buttons(self):
        # Clear existing buttons if any
        for button in self.buttons:
            button.kill()  # Assuming pygame_gui elements have a kill method to remove them
        self.buttons.clear()

        if self.level_manager.current_level:
            self.create_wave_buttons()

    def start_wave_manually(self, wave_index):
        current_time = pygame.time.get_ticks()
        manually_started_wave = self.level_manager.current_level.enemy_wave_list[wave_index]

        # Calculate how much earlier this wave is starting
        time_adjustment = manually_started_wave.start_time - current_time

        # Adjust the start times of all subsequent waves
        for subsequent_wave in self.level_manager.current_level.enemy_wave_list[wave_index + 1:]:
            subsequent_wave.start_time -= time_adjustment

        # Start the wave manually
        manually_started_wave.start_time = current_time
        manually_started_wave.manually_started = True
        #self.update()  # Update the UI to reflect the change
