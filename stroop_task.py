# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 10:53:04 2024

@author: PC
"""

def msmain(arg1):
    import subprocess
    import pkg_resources
    
    
    def install_package(package_name):
        # 패키지가 이미 설치되어 있는지 확인
        installed_packages = {pkg.key for pkg in pkg_resources.working_set}
        if package_name not in installed_packages:
            # 패키지가 설치되어 있지 않을 경우 설치
            subprocess.check_call(["python", "-m", "pip", "install", package_name])
            print(f"{package_name} has been installed.")
        else:
            # 패키지가 이미 설치되어 있음
            print(f"{package_name} is already installed.")
    
    # 패키지 이름 설정
    package_names = ['pygame', 'PyAutoGUI', 'pywin32']
    for package_name in package_names:
        install_package(package_name)
        
    import pyautogui
    import pygame
    import random
    import time
    import csv
    from datetime import datetime
    import os
    import pickle
    ##
    
    base_path = f"C:/Users/msbak/Desktop/eeg_saves/{arg1}"
    
    # Create base directory if it doesn't exist
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    
    # Create block directories
    block_paths = []
    for i in range(1, 9):  # 1 to 8
        block_path = os.path.join(base_path, f"block{i}")
        block_paths.append(block_path)
        if not os.path.exists(block_path):
            os.makedirs(block_path)
                   
    ##

    W, H = 1920, 1080
    FONT_SZ = int(round(46*(W/800)))
    
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
        font = pygame.font.SysFont(None, FONT_SZ)
        text = font.render("+", True, colors["BLACK"])  # Using "+" as a fixation dot
        rect = text.get_rect(center=(int(W/2), int(H/2)))
        screen.blit(text, rect)
        pygame.display.flip()
        # Wait for the specified duration
        pygame.time.wait(duration)
    
    # Pre-generate stimuli
    def generate_stimuli():
        # words = ["RED", "GREEN", "BLUE", "YELLOW"]
        colors = {"RED": (255, 0, 0), "GREEN": (0, 255, 0), "BLUE": (0, 0, 255), "YELLOW": (255, 255, 0)}
        stimuli = {"neutral": [], "congruent": [], "incongruent": []}
        
        # neutral, match
        for color in colors:
            stimuli["neutral"].append(('XXXX', colors[color], color, True))
            
        # neutral, non-match
        for color in colors:
            for color2 in colors:
                if color != color2:
                    stimuli["neutral"].append(('XXXX', colors[color], color2, False))
            
        # congruent, match
        for color in colors:
            stimuli["congruent"].append((color, colors[color], color, True))
            
        # congruent, non-match
        for color in colors:
            for color2 in colors:
                if color != color2:
                    stimuli["congruent"].append((color, colors[color], color2, False))
    
        # incongruent, match
        for color in colors:
            for color2 in colors:
                if color != color2:
                    stimuli["incongruent"].append((color, colors[color2], color2, True))
            
        # incongruent, non-match
        for color in colors:
            for color2 in colors:
                if color != color2:
                    stimuli["incongruent"].append((color, colors[color2], color, False))
    
        return stimuli
    
    
    def stimuli_중복확인(stimuli):
        # mskey = 'neutral'
        msset = []
        for mskey in stimuli:
            for i in range(len(stimuli[mskey])):
                msset.append(stimuli[mskey][i][:3])
        print(len(msset), len(set(msset)))
        print('중복 없음', len(msset) == len(set(msset)))
        
    stimuli = generate_stimuli()
    stimuli_중복확인(stimuli)
    
    def 카드랜덤배정(true_ratio = 0.5): # true_ratio = 0.5 인자는 표시만 해놓음. 아직 숫자 바꿔도 적용안됨
        stimuli_selected = {"neutral": [], "congruent": [], "incongruent": []}
        
        for mskey in stimuli:
            msset_a_condition_true = []
            msset_a_condition_false = []
            for i in range(len(stimuli[mskey])):
                if stimuli[mskey][i][-1]:
                    msset_a_condition_true.append(stimuli[mskey][i])
                elif not(stimuli[mskey][i][-1]):
                    msset_a_condition_false.append(stimuli[mskey][i])
            """  
            경우의 수에서, True, False 각각 10개를 뽑을껀데 총 경우의수가 네개 일 경우 예외처리가 필요함.
            예외처리 대신 네개의 경우의 수를 3번 자가 중첩시켜서 12개의 경우의 수로 만들고, 
            모든 conditions 를 12개의 경우의 수로 만들어서 동일하게 처리
            """
            if len(msset_a_condition_true) == 4:
                msset_a_condition_true_duplicate = []
                for _ in range(3):
                    msset_a_condition_true_duplicate += msset_a_condition_true
                msset_a_condition_true = msset_a_condition_true_duplicate
                
            print(mskey, len(msset_a_condition_true), len(msset_a_condition_false))
            
            slist = random.sample(msset_a_condition_true, 10) + random.sample(msset_a_condition_false, 10)
            random.shuffle(slist)
            stimuli_selected[mskey] = slist
            
        return stimuli_selected
        
    stimuli_selected = 카드랜덤배정()
    
    # 여기 2셋 저장해놓고, 모든 subject에 대해 똑같은거 쓰는게 좋을까?
    
    # Function to run a block of trials
    def run_block(stimuli_selected, savepath=None):
        # mssave = []
        # condition = list(stimuli_selected.keys())[0]
        for condition in stimuli_selected:
            
            # trial = stimuli_selected[condition][0]
            for trial in stimuli_selected[condition]:
                pygame.event.clear()

                top_word, top_color, bottom_word, is_correct = trial
        
                # Clear screen for new trial
                screen.fill(colors["WHITE"])
        
                # Display the top word in its color
                font = pygame.font.SysFont(None, FONT_SZ)
                top_text = font.render(top_word, True, top_color)
                top_rect = top_text.get_rect(center=(W/2, int(H/2 - (H*(1/12)))))  # Centered, adjusted for top position
                screen.blit(top_text, top_rect)
        
                pygame.display.flip()
        
                # Introduce a time gap before displaying the bottom word
                pygame.time.wait(100)  # 100 milliseconds gap as an example
                
                # Now display the bottom word (color name) in black
                bottom_text = font.render(bottom_word, True, colors["BLACK"])
                bottom_rect = bottom_text.get_rect(center=(W/2, int(H/2 + (H*(1/12)))))  # Centered, adjusted for bottom position
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
                            
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:  # ESC 키를 누르면
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
    
                # Clear screen before the next trial
                screen.fill(colors["WHITE"])
                pygame.display.flip()
                nonvalid_click_time = None
                nonvalid_click_time_saves = []
                # pygame.time.wait(500)  # A brief pause between trials
                wait_time_start = pygame.time.get_ticks()
                while pygame.time.get_ticks() - wait_time_start < 500:  # 500 ms wait
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            quit()
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            # Log the mouse click but do not end the wait early
                            nonvalid_click_time = pygame.time.get_ticks() - wait_time_start
                            nonvalid_click_time_saves.append(nonvalid_click_time)
                            print(f"Mouse click logged at {nonvalid_click_time} ms during wait - No action taken")
                            
                msdict = {
                    'Condition': condition,
                    'Top Word': top_word,
                    'Top Color': top_color,
                    'Bottom Word': bottom_word,
                    'Response': response,
                    'Correct': is_correct,
                    'Response Time': response_time,
                    'response_made': response_made,
                    'nonvalid_click_time': nonvalid_click_time_saves
                }
                print('Response', msdict['Response'], 'Correct', msdict['Correct'], \
                      'Response Time', msdict['Response Time'])
                # mssave.append(msdict)
                
                base_path = savepath
                filename = datetime.now().strftime("%Y_%m_%d_%H_%M_%S_eegdata.pkl")
                full_path = os.path.join(base_path, filename)
                
                # Save msdict to a file with the generated filename
                with open(full_path, 'wb') as file:
                    pickle.dump(msdict, file)
    
    
    #%%
    
    # Example running one block of each condition
    # Initialize Pygame and set up the display
    pygame.init()
    # Initialize Pygame and set up the display in fullscreen mode
    # pygame.init()
    screen = pygame.display.set_mode((W, H), pygame.FULLSCREEN)
    
    # screen = pygame.display.set_mode((W,H))
    
    initial_x, initial_y = pyautogui.position()
    x, y = 67, 1016
    pyautogui.click(x, y)
    pyautogui.click(initial_x, initial_y) 
    
    for block_n in range(8):
        run_baseline()
        run_block(stimuli_selected, savepath=block_paths[block_n])
    pygame.quit()

#%%
import sys

if __name__ == "__main__":
    msmain(sys.argv[1])

# 종료 버튼 누르기
# 인자 입력받아서 폴더 만들고 저장하기
# block 단위로 저장하기





