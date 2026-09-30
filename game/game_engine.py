import random
import pygame
from game.text_box import TextBox


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # Words used in the game
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

        # Game score
        self.score = 0

        # Feedback message
        self.feedback_msg = "Unscramble the letters above!"
        self.feedback_color = (210, 215, 225)

        # Input box
        self.input_box = TextBox(
            width // 2 - 130,
            210,
            160,
            46
        )

        # Submit button
        self.submit_btn = pygame.Rect(
            width // 2 + 45,
            210,
            95,
            46
        )

        # Fonts
        self.font_title = pygame.font.SysFont(None, 40)
        self.font_word = pygame.font.SysFont(None, 52)
        self.font_msg = pygame.font.SysFont(None, 26)
        self.font_btn = pygame.font.SysFont(None, 24)
        self.font_timer = pygame.font.SysFont(None, 28)

        # -------------------------
        # TIMER SETTINGS
        # -------------------------

        # Time allowed for each word
        self.time_limit = 20

        # Store the starting time of the round
        self.start_time = pygame.time.get_ticks()

        # Prevent multiple timeout triggers
        self.round_over = False

        # Start first round
        self.next_round()

    # --------------------------------------------------
    # SCRAMBLE WORD
    # --------------------------------------------------

    def scramble_string(self, word):
        letters = list(word)

        while True:
            random.shuffle(letters)
            shuffled = "".join(letters)

            # Make sure scrambled word is different
            # from original word
            if shuffled != word or len(word) <= 1:
                return shuffled

    # --------------------------------------------------
    # START NEXT ROUND
    # --------------------------------------------------

    def next_round(self):
        self.secret_word = random.choice(self.words)

        self.scrambled_word = self.scramble_string(
            self.secret_word
        )

        # Clear previous answer
        self.input_box.clear()

        # Reset timer
        self.start_time = pygame.time.get_ticks()

        # Reset round status
        self.round_over = False

        # Reset feedback
        self.feedback_msg = "Unscramble the letters above!"
        self.feedback_color = (210, 215, 225)

    # --------------------------------------------------
    # SUBMIT GUESS
    # --------------------------------------------------

    def submit_guess(self):

        # Don't allow guessing after round has ended
        if self.round_over:
            return

        guess = self.input_box.text.strip().upper()

        # Empty input
        if not guess:
            self.feedback_msg = "Type a word before submitting!"
            self.feedback_color = (240, 170, 50)
            return

        # --------------------------------------------------
        # FIXED VALIDATION
        # --------------------------------------------------
        #
        # The guess MUST be compared with secret_word.
        #
        # Old incorrect code:
        #
        # is_correct = (guess == self.scrambled_word)
        #
        # Correct code:
        #
        is_correct = (guess == self.secret_word)

        # --------------------------------------------------
        # CORRECT ANSWER
        # --------------------------------------------------

        if is_correct:

            self.score += 1

            self.feedback_msg = (
                f"CORRECT! '{self.secret_word}' is right."
            )

            self.feedback_color = (80, 230, 110)

            # Start next round
            self.next_round()

        # --------------------------------------------------
        # WRONG ANSWER
        # --------------------------------------------------

        else:

            self.feedback_msg = "WRONG GUESS! Try again."

            self.feedback_color = (240, 80, 80)

            self.input_box.clear()

    # --------------------------------------------------
    # TIMER EXPIRED
    # --------------------------------------------------

    def time_up(self):

        # Prevent this function from running twice
        if self.round_over:
            return

        self.round_over = True

        # Reveal the correct word
        self.feedback_msg = (
            f"TIME'S UP! The word was '{self.secret_word}'."
        )

        self.feedback_color = (255, 100, 80)

        # Clear input
        self.input_box.clear()

        # Wait a short time before next round
        # We store the time when timeout happened
        self.time_up_time = pygame.time.get_ticks()

    # --------------------------------------------------
    # EVENT HANDLING
    # --------------------------------------------------

    def handle_event(self, event):

        # Let the textbox process keyboard/mouse events
        self.input_box.handle_event(event)

        # ENTER KEY
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RETURN:
                self.submit_guess()

        # MOUSE CLICK
        elif event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                # Submit button clicked
                if self.submit_btn.collidepoint(event.pos):
                    self.submit_guess()

    # --------------------------------------------------
    # UPDATE GAME
    # --------------------------------------------------

    def update(self):

        current_time = pygame.time.get_ticks()

        # --------------------------------------------------
        # NORMAL GAME TIMER
        # --------------------------------------------------

        if not self.round_over:

            elapsed_time = (
                current_time - self.start_time
            ) / 1000

            # Timer expired
            if elapsed_time >= self.time_limit:
                self.time_up()

        # --------------------------------------------------
        # AFTER TIMEOUT
        # --------------------------------------------------

        else:

            # Give player 1.5 seconds to see the answer
            elapsed_after_timeout = (
                current_time - self.time_up_time
            ) / 1000

            if elapsed_after_timeout >= 1.5:

                self.next_round()

    # --------------------------------------------------
    # RENDER GAME
    # --------------------------------------------------

    def render(self, screen):

        # Background
        screen.fill((26, 30, 38))

        # --------------------------------------------------
        # TITLE
        # --------------------------------------------------

        title_surf = self.font_title.render(
            "Word Scramble Arena",
            True,
            (245, 245, 245)
        )

        screen.blit(
            title_surf,
            (
                self.width // 2 -
                title_surf.get_width() // 2,
                25
            )
        )

        # --------------------------------------------------
        # SCORE
        # --------------------------------------------------

        score_surf = self.font_msg.render(
            f"Score: {self.score}",
            True,
            (255, 220, 80)
        )

        screen.blit(
            score_surf,
            (
                self.width // 2 -
                score_surf.get_width() // 2,
                70
            )
        )

        # --------------------------------------------------
        # SCRAMBLED WORD
        # --------------------------------------------------

        # During normal gameplay show scrambled word.
        # When time is over reveal secret word.
        if self.round_over:

            display_word = self.secret_word

            word_color = (255, 100, 80)

        else:

            display_word = self.scrambled_word

            word_color = (100, 200, 255)

        spaced_letters = "  ".join(display_word)

        scramble_surf = self.font_word.render(
            spaced_letters,
            True,
            word_color
        )

        screen.blit(
            scramble_surf,
            (
                self.width // 2 -
                scramble_surf.get_width() // 2,
                130
            )
        )

        # --------------------------------------------------
        # TIMER BAR
        # --------------------------------------------------

        timer_x = 100
        timer_y = 105
        timer_width = self.width - 200
        timer_height = 15

        if not self.round_over:

            current_time = pygame.time.get_ticks()

            elapsed_time = (
                current_time - self.start_time
            ) / 1000

            remaining_time = max(
                0,
                self.time_limit - elapsed_time
            )

            # Calculate percentage remaining
            timer_percentage = (
                remaining_time / self.time_limit
            )

            current_timer_width = int(
                timer_width * timer_percentage
            )

        else:

            remaining_time = 0
            current_timer_width = 0

        # Timer background
        pygame.draw.rect(
            screen,
            (70, 75, 85),
            (
                timer_x,
                timer_y,
                timer_width,
                timer_height
            ),
            border_radius=7
        )

        # Timer remaining section
        if current_timer_width > 0:

            pygame.draw.rect(
                screen,
                (70, 200, 100),
                (
                    timer_x,
                    timer_y,
                    current_timer_width,
                    timer_height
                ),
                border_radius=7
            )

        # --------------------------------------------------
        # TIMER TEXT
        # --------------------------------------------------

        timer_text = self.font_timer.render(
            f"Time: {remaining_time:.1f}s",
            True,
            (235, 235, 235)
        )

        screen.blit(
            timer_text,
            (
                self.width // 2 -
                timer_text.get_width() // 2,
                330
            )
        )

        # --------------------------------------------------
        # INPUT BOX
        # --------------------------------------------------

        # Only show input while round is active
        if not self.round_over:
            self.input_box.render(screen)

        # --------------------------------------------------
        # SUBMIT BUTTON
        # --------------------------------------------------

        if not self.round_over:

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

            btn_text = self.font_btn.render(
                "SUBMIT",
                True,
                (255, 255, 255)
            )

            screen.blit(
                btn_text,
                (
                    self.submit_btn.centerx -
                    btn_text.get_width() // 2,
                    self.submit_btn.centery -
                    btn_text.get_height() // 2
                )
            )

        # --------------------------------------------------
        # FEEDBACK MESSAGE
        # --------------------------------------------------

        feedback_surf = self.font_msg.render(
            self.feedback_msg,
            True,
            self.feedback_color
        )

        screen.blit(
            feedback_surf,
            (
                self.width // 2 -
                feedback_surf.get_width() // 2,
                380
            )
        )
