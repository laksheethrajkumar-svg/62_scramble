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

        # Stores the positions of letters revealed by hints
        self.revealed_letters = set()

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

        # HINT button beside SUBMIT
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

    def scramble_string(self, word):
        letters = list(word)

        while True:
            random.shuffle(letters)
            shuffled = "".join(letters)

            if shuffled != word or len(word) <= 1:
                return shuffled

    def next_round(self):
        self.secret_word = random.choice(self.words)
        self.scrambled_word = self.scramble_string(self.secret_word)

        # Reset revealed letters for the new word
        self.revealed_letters = set()

        self.input_box.clear()

    def submit_guess(self):
        guess = self.input_box.text.strip().upper()

        if not guess:
            self.feedback_msg = "Type a word before submitting!"
            self.feedback_color = (240, 170, 50)
            return

        # Task 1 fix:
        # Compare the guess with the original secret word,
        # NOT the scrambled word.
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

    def give_hint(self):
        # Find the first letter that has not been revealed yet
        for i in range(len(self.secret_word)):

            if i not in self.revealed_letters:
                self.revealed_letters.add(i)

                # Deduct 1 point for using a hint
                self.score -= 1

                self.feedback_msg = "Hint revealed! -1 point."
                self.feedback_color = (255, 200, 80)

                return

        # All letters have already been revealed
        self.feedback_msg = "All letters are already revealed!"
        self.feedback_color = (210, 215, 225)

    def get_hint_display(self):
        # Example:
        # PYTHON
        # P _ _ _ _ _
        #
        # After another hint:
        # P Y _ _ _ _
        #
        # And so on.

        display = []

        for i, letter in enumerate(self.secret_word):

            if i in self.revealed_letters:
                display.append(letter)
            else:
                display.append("_")

        return " ".join(display)

    def handle_event(self, event):
        self.input_box.handle_event(event)

        # Press ENTER to submit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.submit_guess()

        # Mouse clicks
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            # SUBMIT button
            if self.submit_btn.collidepoint(event.pos):
                self.submit_guess()

            # HINT button
            elif self.hint_btn.collidepoint(event.pos):
                self.give_hint()

    def update(self):
        pass

    def render(self, screen):
        screen.fill((26, 30, 38))

        # Title
        title_surf = self.font_title.render(
            "Word Scramble Arena",
            True,
            (245, 245, 245)
        )

        screen.blit(
            title_surf,
            (
                self.width // 2 - title_surf.get_width() // 2,
                25
            )
        )

        # Score
        score_surf = self.font_msg.render(
            f"Score: {self.score}",
            True,
            (255, 220, 80)
        )

        screen.blit(
            score_surf,
            (
                self.width // 2 - score_surf.get_width() // 2,
                70
            )
        )

        # Scrambled word
        spaced_letters = "  ".join(self.scrambled_word)

        scramble_surf = self.font_word.render(
            spaced_letters,
            True,
            (100, 200, 255)
        )

        screen.blit(
            scramble_surf,
            (
                self.width // 2 - scramble_surf.get_width() // 2,
                125
            )
        )

        # Hint display
        hint_text = self.get_hint_display()

        hint_surf = self.font_msg.render(
            hint_text,
            True,
            (255, 255, 255)
        )

        screen.blit(
            hint_surf,
            (
                self.width // 2 - hint_surf.get_width() // 2,
                175
            )
        )

        # Input box
        self.input_box.render(screen)

        # SUBMIT button
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

        # HINT button
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

        # Feedback message
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
