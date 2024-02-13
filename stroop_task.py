# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 10:53:04 2024

@author: PC
"""

import pygame
import random
import time
import csv

# Define colors
colors = {
    "RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255),
    "YELLOW": (255, 255, 0),
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255)
}

def run_baseline(duration=5 * 1000):  # Default duration set to 30 seconds
    screen.fill(colors["WHITE"])
    font = pygame.font.SysFont(None, 48)
    text = font.render("+", True, colors["BLACK"])  # Using "+" as a fixation dot
    rect = text.get_rect(center=(400, 300))
    screen.blit(text, rect)
    pygame.display.flip()
    # Wait for the specified duration
    pygame.time.wait(duration)

# Initialize Pygame and set up the display
pygame.init()
screen = pygame.display.set_mode((800, 600))
run_baseline()

# Pre-generate stimuli
def generate_stimuli():
    words = ["RED", "GREEN", "BLUE", "YELLOW"]
    colors = {"RED": (255, 0, 0), "GREEN": (0, 255, 0), "BLUE": (0, 0, 255), "YELLOW": (255, 255, 0)}
    stimuli = {"neutral": [], "congruent": [], "incongruent": []}

    # Generate congruent stimuli
    for word in words:
        # For congruent condition, the word and its display color match
        stimuli["congruent"].append((word, word, word, True))  # Top word, top color, bottom word, is_correct

    # Generate incongruent stimuli
    for top_word in words:
        for bottom_word in words:
            if top_word != bottom_word:
                # For incongruent condition, the top word's display color does not match the bottom word
                stimuli["incongruent"].append((top_word, bottom_word, bottom_word, False))

    # Generate neutral stimuli
    # Neutral stimuli could be non-color words or symbols presented in color, with the bottom word indicating a color
    # This part of the code needs to be designed based on how you want to handle neutral stimuli

    # Ensure a 50% correct to incorrect ratio for incongruent and neutral if necessary and randomize
    # This might involve adjusting the number of stimuli and shuffling
    for condition in stimuli:
        random.shuffle(stimuli[condition])

    return stimuli



stimuli = generate_stimuli()

# Function to run a block of trials
def run_block(condition):
    for trial in stimuli[condition]:
        top_word, top_color, bottom_word, is_correct = trial

        # Clear screen for new trial
        screen.fill(colors["WHITE"])

        # Display the top word in its color
        font = pygame.font.SysFont(None, 48)
        top_text = font.render(top_word, True, colors[top_color])
        top_rect = top_text.get_rect(center=(400, 250))  # Centered, adjusted for top position
        screen.blit(top_text, top_rect)

        pygame.display.flip()

        # Introduce a time gap before displaying the bottom word
        pygame.time.wait(100)  # 100 milliseconds gap as an example

        # Now display the bottom word (color name) in black
        bottom_text = font.render(bottom_word, True, colors["BLACK"])
        bottom_rect = bottom_text.get_rect(center=(400, 350))  # Centered, adjusted for bottom position
        screen.blit(bottom_text, bottom_rect)

        pygame.display.flip()

        # Timing and response handling starts after displaying the bottom word
        start_time = pygame.time.get_ticks()
        response_made = False
        response = None

        while not response_made and (pygame.time.get_ticks() - start_time) < 1500:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click for "Yes"
                        response = "Yes"
                        response_made = True
                    elif event.button == 3:  # Right click for "No"
                        response = "No"
                        response_made = True

        # Calculate response time
        response_time = pygame.time.get_ticks() - start_time if response_made else 1500

        # Log trial data
        print({
            'Condition': condition,
            'Top Word': top_word,
            'Top Color': top_color,
            'Bottom Word': bottom_word,
            'Response': response,
            'Correct': is_correct,
            'Response Time': response_time
        })

        # Clear screen before the next trial
        screen.fill(colors["WHITE"])
        pygame.display.flip()
        pygame.time.wait(500)  # A brief pause between trials



# Example running one block of each condition
for condition in ["neutral", "congruent", "incongruent"]:
    for block in range(4):  # Assuming 4 blocks for each condition as mentioned
        run_block(condition)

run_baseline()
pygame.quit()
