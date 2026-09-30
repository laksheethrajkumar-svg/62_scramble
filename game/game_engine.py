import random
import pygame
from game.text_box import TextBox


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.words = [
            "PYTHON",
            "PYGAME",
            "PLANET",
            "ROCKET",
            "GALAXY",
            "STREAM",
            "PUZZLE",
            "ALGORITHM"
        ]

        self.secret_word = ""
        self.scrambled_word = ""

        self.score = 0

        # -------------------------
        # TASK 2: HINT VARIABLES
        # -------------------------
        self.revealed_letters = set()

        # -------------------------
        # TASK 3: TIMER
        # -------------------------
        self.time_limit = 20
        self.time_left = 20
        self.timer_start = pygame.time.get_ticks()

        self.feedback_msg = "Unscramble the letters above!"
        self.feedback_color = (210, 215, 225)

        # Input box
        self.input_box = TextBox(
            width // 2 - 130,
            210,
            160,
            46
        )

        # SUBMIT button
        self.submit_btn = pygame.Rect(
            width // 2 + 45,
            210,
            95,
            46
        )

        # HINT button
        self.hint_btn = pygame.Rect(
            width // 2 + 150,
            210,
            85,
            46
        )

        self.font_title = pygame.font.SysFont(None, 40)
        self.font_word = pygame.font.SysFont(None, 52)
        self.font_msg = pygame.font.SysFont(None, 26)
        self.font_btn = pygame.font.SysFont(None, 24)

        self.next_round()

    # -------------------------
    # SCRAMBLE WORD
    # -------------------------
    def scramble_string(self, word):
        letters = list(word)

        while True:
            random.shuffle(letters)
            shuffled = "".join(letters)

            if shuffled != word or len(word) <= 1:
                return shuffled

    # -------------------------
    # START NEXT ROUND
    # -------------------------
    def next_round(self):
        self.secret_word = random.choice(self.words)
        self.scrambled_word = self.scramble_string(self.secret_word)

        # Reset hints
        self.revealed_letters = set()

        # Reset timer
        self.time_left = self.time_limit
        self.timer_start = pygame.time.get_ticks()

        # Clear input
        self.input_box.clear()

        self.feedback_msg = "Unscramble the letters above!"
        self.feedback_color = (210, 215, 225)

    # -------------------------
    # TASK 1: SUBMIT GUESS
    # -------------------------
    def submit_guess(self):
        guess = self.input_box.text.strip().upper()

        if not guess:
            self.feedback_msg = "Type a word before submitting!"
            self.feedback_color = (240, 170, 50)
            return

        # IMPORTANT:
        # Compare guess with the ORIGINAL secret word
        # and NOT the scrambled word.
        is_correct = (guess == self.secret_word)

        if is_correct:
            self.score += 1

            self.feedback_msg = (
                f"CORRECT! '{self.secret_word}' is right."
            )

            self.feedback_color = (80, 230, 110)

            self.next_round()

        else:
            self.feedback_msg = "WRONG GUESS! Try again."
            self.feedback_color = (240, 80, 80)

            self.input_box.clear()

    # -------------------------
    # TASK 2: GIVE HINT
    # -------------------------
    def give_hint(self):

        # Find the first unrevealed letter
        for i in range(len(self.secret_word)):

            if i not in self.revealed_letters:

                # Reveal this letter
                self.revealed_letters.add(i)

                # Deduct 1 point
                self.score -= 1

                self.feedback_msg = "Hint revealed! -1 point."
                self.feedback_color = (255, 200, 80)

                return

        # If every letter is already revealed
        self.feedback_msg = "All letters are already revealed!"
        self.feedback_color = (210, 215, 225)

    # -------------------------
    # TASK 2: DISPLAY HINT
    # -------------------------
    def get_hint_display(self):

        display = []

        for i, letter in enumerate(self.secret_word):

            if i in self.revealed_letters:
                display.append(letter)

            else:
                display.append("_")

        return " ".join(display)

    # -------------------------
    # TASK 3: TIMER UPDATE
    # -------------------------
    def update_timer(self):

        current_time = pygame.time.get_ticks()

        elapsed_seconds = (
            current_time - self.timer_start
        ) / 1000

        self.time_left = self.time_limit - elapsed_seconds

        # Timer expired
        if self.time_left <= 0:

            self.time_left = 0

            # Reveal correct answer
            self.feedback_msg = (
                f"TIME'S UP! The word was '{self.secret_word}'."
            )

            self.feedback_color = (255, 80, 80)

            # Automatically move to next round
            self.next_round()

    # -------------------------
    # HANDLE USER INPUT
    # -------------------------
    def handle_event(self, event):

        self.input_box.handle_event(event)

        # Keyboard
        if event.type == pygame.KEYDOWN:

            # ENTER = SUBMIT
            if event.key == pygame.K_RETURN:
                self.submit_guess()

        # Mouse
        elif event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                # SUBMIT button
                if self.submit_btn.collidepoint(event.pos):
                    self.submit_guess()

                # HINT button
                elif self.hint_btn.collidepoint(event.pos):
                    self.give_hint()

    # -------------------------
    # UPDATE
    # -------------------------
    def update(self):

        # Update countdown timer
        self.update_timer()

    # -------------------------
    # RENDER SCREEN
    # -------------------------
    def render(self, screen):

        screen.fill((26, 30, 38))

        # -------------------------
        # TITLE
        # -------------------------
        title_surf = self.font_title.render(
            "Word Scramble Arena",
            True,
            (245, 245, 245)
        )

        screen.blit(
            title_surf,
            (
                self.width // 2
                - title_surf.get_width() // 2,
                25
            )
        )

        # -------------------------
        # SCORE
        # -------------------------
        score_surf = self.font_msg.render(
            f"Score: {self.score}",
            True,
            (255, 220, 80)
        )

        screen.blit(
            score_surf,
            (
                self.width // 2
                - score_surf.get_width() // 2,
                70
            )
        )

        # -------------------------
        # TIMER TEXT
        # -------------------------
        timer_text = f"Time: {max(0, int(self.time_left))}"

        timer_surf = self.font_msg.render(
            timer_text,
            True,
            (255, 255, 255)
        )

        screen.blit(
            timer_surf,
            (
                self.width // 2
                - timer_surf.get_width() // 2,
                100
            )
        )

        # -------------------------
        # TIMER BAR
        # -------------------------

        bar_width = 300
        bar_height = 18

        bar_x = (
            self.width // 2
            - bar_width // 2
        )

        bar_y = 125

        # Background
        pygame.draw.rect(
            screen,
            (70, 70, 70),
            (
                bar_x,
                bar_y,
                bar_width,
                bar_height
            ),
            border_radius=8
        )

        # Remaining time
        timer_ratio = (
            self.time_left / self.time_limit
        )

        timer_ratio = max(
            0,
            min(1, timer_ratio)
        )

        remaining_width = int(
            bar_width * timer_ratio
        )

        if remaining_width > 0:

            pygame.draw.rect(
                screen,
                (80, 200, 100),
                (
                    bar_x,
                    bar_y,
                    remaining_width,
                    bar_height
                ),
                border_radius=8
            )

        # -------------------------
        # SCRAMBLED WORD
        # -------------------------
        spaced_letters = "  ".join(
            self.scrambled_word
        )

        scramble_surf = self.font_word.render(
            spaced_letters,
            True,
            (100, 200, 255)
        )

        screen.blit(
            scramble_surf,
            (
                self.width // 2
                - scramble_surf.get_width() // 2,
                155
            )
        )

        # -------------------------
        # HINT DISPLAY
        # -------------------------
        hint_text = self.get_hint_display()

        hint_surf = self.font_msg.render(
            hint_text,
            True,
            (255, 255, 255)
        )

        screen.blit(
            hint_surf,
            (
                self.width // 2
                - hint_surf.get_width() // 2,
                190
            )
        )

        # -------------------------
        # INPUT BOX
        # -------------------------
        self.input_box.render(screen)

        # -------------------------
        # SUBMIT BUTTON
        # -------------------------
        pygame.draw.rect(
            screen,
            (50, 150, 85),
            self.submit_btn,
            border_radius=6
        )

        pygame.draw.rect(
            screen,
            (220, 220, 220),
            self.submit_btn,
            width=2,
            border_radius=6
        )

        submit_text = self.font_btn.render(
            "SUBMIT",
            True,
            (255, 255, 255)
        )

        screen.blit(
            submit_text,
            (
                self.submit_btn.centerx
                - submit_text.get_width() // 2,
                self.submit_btn.centery
                - submit_text.get_height() // 2
            )
        )

        # -------------------------
        # HINT BUTTON
        # -------------------------
        pygame.draw.rect(
            screen,
            (180, 130, 40),
            self.hint_btn,
            border_radius=6
        )

        pygame.draw.rect(
            screen,
            (220, 220, 220),
            self.hint_btn,
            width=2,
            border_radius=6
        )

        hint_button_text = self.font_btn.render(
            "HINT",
            True,
            (255, 255, 255)
        )

        screen.blit(
            hint_button_text,
            (
                self.hint_btn.centerx
                - hint_button_text.get_width() // 2,
                self.hint_btn.centery
                - hint_button_text.get_height() // 2
            )
        )

        # -------------------------
        # FEEDBACK MESSAGE
        # -------------------------
        feedback_surf = self.font_msg.render(
            self.feedback_msg,
            True,
            self.feedback_color
        )

        screen.blit(
            feedback_surf,
            (
                self.width // 2
                - feedback_surf.get_width() // 2,
                285
            )
        )
