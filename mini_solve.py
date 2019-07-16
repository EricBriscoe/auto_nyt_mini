import pyautogui
from selenium import webdriver


def clues_lookup(clues):
    browser = webdriver.Chrome(executable_path="./chromedriver")
    browser.get("https://www.wordplays.com/crossword-solver/")

    answers = []

    for clue in clues:
        search_box = browser.find_element(by="name", value="clue")
        search_button = browser.find_element_by_name("go")
        search_box.send_keys(clue)
        search_button.click()

        answer_table = browser.find_element_by_class_name("wp-widget-content")
        answer_row = answer_table.find_element_by_class_name("odd")
        answers.append(answer_row.text.split(" ")[0])

    browser.quit()
    return answers


class MiniPuzzle:
    def __init__(self):
        self.across_clues = []
        self.down_clues = []
        self.browser = webdriver.Chrome(executable_path="./chromedriver")

    def read_today(self):
        browser = self.browser
        browser.get("https://www.nytimes.com/crosswords/game/mini")
        clue_frames = browser.find_elements_by_class_name(name="ClueList-list--2dD5-")
        across_list = clue_frames[0].find_elements_by_class_name(name="Clue-li--1JoPu")
        down_list = clue_frames[1].find_elements_by_class_name(name="Clue-li--1JoPu")
        clues = []
        for index, clue in enumerate(across_list):
            clue_text = clue.text[2:]
            clues.append(clue_text)
            self.across_clues.append([index, clue_text])

        answers = clues_lookup(clues)
        for i, ans in enumerate(answers):
            self.across_clues[i].append(ans)

        print(self.across_clues)

    def solve(self):
        resume_button = self.browser.find_elements_by_class_name(
            name="buttons-modalButton--1REsR"
        )
        if len(resume_button) > 0:
            resume_button[0].click()

        for word in self.across_clues:
            pyautogui.typewrite(f"{word[2]}\n")

    def quit(self):
        self.browser.quit()


if __name__ == "__main__":
    mini_puzzle = MiniPuzzle()
    mini_puzzle.read_today()
    mini_puzzle.solve()
    input("Done?")
    mini_puzzle.quit()
