import pygame
import ctypes

deck_dll = ctypes.CDLL("D:\\VS\\LastChance\\x64\\Release\\LastChance.dll")

def shuffle_deck(deck):
    deck_size = len(deck)
    deck_bytes = (ctypes.c_char_p * deck_size)(*map(lambda card: card.encode(), deck))
    deck_dll.shuffleDeck(deck_bytes, deck_size)
    shuffled_deck = [card.decode() for card in deck_bytes]
    return shuffled_deck


def deal_cards(deck):
    deck_size = len(deck)
    deck_bytes = (ctypes.c_char_p * deck_size)(*map(lambda card: card.encode(), deck))
    player_hand_size = ctypes.c_int(0)
    player_hand = (ctypes.c_char_p * 2)()
    bot_hand_size = ctypes.c_int(0)
    bot_hand = (ctypes.c_char_p * 2)()
    deck_dll.dealCards(deck_bytes, deck_size, ctypes.byref(player_hand_size), player_hand, ctypes.byref(bot_hand_size),
                       bot_hand)
    player_hand = [card.decode() for card in player_hand[:player_hand_size.value]]
    bot_hand = [card.decode() for card in bot_hand[:bot_hand_size.value]]

    for card in player_hand + bot_hand:
        deck.remove(card)

    return player_hand[::-1], bot_hand[::-1]
def calculate_score(hand):
    hand_size = len(hand)
    hand_bytes = (ctypes.c_char_p * hand_size)(*map(lambda card: card.encode(), hand))
    score = deck_dll.calculateScore(hand_bytes, hand_size)
    return score


def draw_card(screen, card, position, card_images):
    if card in card_images:
        screen.blit(card_images[card], position)
    else:
        font = pygame.font.Font(None, 36)
        text = font.render(card, True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = position
        screen.blit(text, text_rect)

def draw_table(screen, player_hand, bot_hand, player_score, card_images, message=None):
    # Завантаження зображення фону
    background_image = pygame.image.load("D:\\Карти\\Background\\Полотно.png")
    background_image = pygame.transform.scale(background_image, (1000, 750))
    screen.blit(background_image, (0, 0))

    draw_card(screen, "Player Hand", (150, 200), card_images)
    draw_card(screen, "Bot Hand", (150, 400), card_images)

    player_x = 400
    for card in player_hand:
        draw_card(screen, card, (player_x, 100), card_images)
        player_x += 50

    bot_x = 400
    if message:
        for card in bot_hand:
            draw_card(screen, card, (bot_x, 400), card_images)
            bot_x += 50
    else:
        shirt_image = pygame.image.load("D:\\Карти\\Background\\Сорочкакарти.png")
        shirt_image = pygame.transform.scale(shirt_image, (100, 150))
        screen.blit(shirt_image, (bot_x, 400))
        screen.blit(shirt_image, (bot_x + 50, 400))
        bot_x += 100

    draw_card(screen, f"Score: {player_score}", (150, 300), card_images)

    if message:
        draw_card(screen, message, (400, 300), card_images)

    pygame.display.flip()
def draw_buttons(screen, button_active):
    font = pygame.font.Font(None, 36)

    button_radius = 50

    hit_button_rect = pygame.Rect(150 - button_radius, 500 - button_radius, button_radius * 2, button_radius * 2)
    stand_button_rect = pygame.Rect(250 - button_radius, 500 - button_radius, button_radius * 2, button_radius * 2)

    hit_button_image = pygame.image.load("D:\\Карти\\Background\\Hitbutton.png").convert_alpha()
    hit_button_image = pygame.transform.scale(hit_button_image, (button_radius * 2, button_radius * 2))
    hit_button_image.set_colorkey((255, 255, 255))

    stand_button_image = pygame.image.load("D:\\Карти\\Background\\Standbutton.png").convert_alpha()
    stand_button_image = pygame.transform.scale(stand_button_image, (button_radius * 2, button_radius * 2))
    stand_button_image.set_colorkey((255, 255, 255))

    if button_active == "hit":
        pygame.draw.circle(screen, (255, 0, 0), hit_button_rect.center, button_radius)
        screen.blit(hit_button_image, hit_button_rect.topleft)
    else:
        pygame.draw.circle(screen, (255, 255, 255), hit_button_rect.center, button_radius)
        screen.blit(hit_button_image, hit_button_rect.topleft)

    if button_active == "stand":
        pygame.draw.circle(screen, (255, 0, 0), stand_button_rect.center, button_radius)
        screen.blit(stand_button_image, stand_button_rect.topleft)
    else:
        pygame.draw.circle(screen, (255, 255, 255), stand_button_rect.center, button_radius)
        screen.blit(stand_button_image, stand_button_rect.topleft)

    pygame.display.flip()

def load_card_images():
    card_images = {}
    card_names = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"]
    suits = ["H", "D", "C", "S"]  # Hearts, Diamonds, Clubs, Spades
    for card_name in card_names:
        for suit in suits:
            image_path = f"D:\\Карти\\{suit}\\{card_name}.png"
            image = pygame.image.load(image_path)
            card_images[f"{suit}{card_name}"] = image
    return card_images

def create_deck():
    suits = ["S", "H", "D", "C"]  # Spades, Hearts, Diamonds, Clubs
    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"]
    deck = [suit + rank for suit in suits for rank in ranks]
    return deck

def play_21():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("21 Game")
    clock = pygame.time.Clock()

    while True:
        deck = create_deck()
        shuffled_deck = shuffle_deck(deck)
        card_images = load_card_images()

        player_hand, bot_hand = deal_cards(shuffled_deck)
        player_score = calculate_score(player_hand)
        bot_score = calculate_score(bot_hand)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            draw_table(screen, player_hand, bot_hand, player_score, card_images)

            if player_score > 21:
                draw_table(screen, player_hand, bot_hand, player_score, card_images, "Bust! You lose!")
                pygame.time.wait(2000)
                break

            draw_buttons(screen, "hit")

            choice = None
            while choice not in ["h", "s"]:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_h:
                            choice = "h"
                        elif event.key == pygame.K_s:
                            choice = "s"

            if choice == "h":
                player_hand.append(shuffled_deck.pop())
                player_score = calculate_score(player_hand)
            else:
                break

        while calculate_score(bot_hand) < player_score and player_score <= 21:
            bot_hand.append(shuffled_deck.pop())

        player_score = calculate_score(player_hand)
        bot_score = calculate_score(bot_hand)

        draw_table(screen, player_hand, bot_hand, player_score, card_images, "Dealer's Turn...")

        if player_score > 21:
            draw_table(screen, player_hand, bot_hand, player_score, card_images, "Bust! You lose!")
        elif bot_score > 21:
            draw_table(screen, player_hand, bot_hand, player_score, card_images, "Bust! You win!")
        elif bot_score == player_score:
            draw_table(screen, player_hand, bot_hand, player_score, card_images, "Draw!")
        elif bot_score > player_score:
            draw_table(screen, player_hand, bot_hand, player_score, card_images, f"You lose! Bot has {bot_score}")
        else:
            draw_table(screen, player_hand, bot_hand, player_score, card_images, "You win!")

        pygame.time.wait(2000)
        draw_table(screen, player_hand, bot_hand, player_score, card_images, "Play again? (Y/N)")

        choice = None
        while choice not in ["y", "n"]:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        choice = "y"
                    elif event.key == pygame.K_n:
                        choice = "n"

        if choice == "n":
            pygame.quit()
            return

        screen.fill((0, 0, 0))
        pygame.display.flip()

play_21()
