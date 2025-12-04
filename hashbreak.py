from Crypto.Hash import SHA256
from pypdf import PdfReader
import os
import nltk
import bcrypt
import secrets
import string
import random
import time

done_people: dict = {}

from nltk.corpus import words as nltk_words
nltk.download('words')

def parse_shadow_lines(page_data):
    users = []
    for line in page_data:
        line = line.strip()
        if not line or ':' not in line:
            continue
        user, hash_str = line.split(':', 1)
        users.append((user, hash_str))
        done_people[user] = False
    return users

def build_word_list() -> list[str]:
    # single words, alphabetic only, 6–10 letters
    wl: list[str] = [
        w.lower()
        for w in nltk_words.words()
        if w.isalpha() and 6 <= len(w) <= 10
    ]
    return wl

def crack_user(wordlist, users, num: int):
    start = time.perf_counter()
    solutions: list[tuple] = [(None, None) for _ in range(len(users))]
    with open("output.txt", "wb") as f:
        for j, (username, hash_str) in enumerate(users):
            if done_people.get(username, False):
                continue
            hash_bytes = hash_str.encode('utf-8')
            i = num
            while i < len(wordlist):
                pw = wordlist[i].encode('utf-8')
                if bcrypt.checkpw(pw, hash_bytes):
                    end = time.perf_counter()
                    done_people[username] = True
                    solutions[j] = (wordlist[i], (end - start))
                    print(solutions[j], ' ',users[j][0])
                    f.write(f"{username}:{wordlist[i]}:{end-start}\n".encode())
                    break
                i += 16
    end = time.perf_counter()
    return solutions, (end - start)

def break_hash(wl, users):
    i = 0
    # create 16 child processes to break hashes faster (16 processes faster than 1)
    while i < 16:
        if(os.fork() == 0):
            print(f"fork {i} {os.getpid()}")
            return crack_user(wl, users, i)
            os._exit(0)
        i += 1
    # wait for child processes
    while 1:
        try:
            pid, status = os.wait()
        except ChildProcessError:
            break

# https://www.geeksforgeeks.org/python/working-with-pdf-files-in-python/
if __name__ == "__main__":
    #print(break_hash())
    reader = PdfReader("shadow1.pdf")
    page = reader.pages[0]
    #print(page.extract_text())
    page_data = page.extract_text().split('\n')
    users = parse_shadow_lines(page_data)
    wl = build_word_list()
    users = parse_shadow_lines(page_data)
    #print(users)
    break_hash(wl, users)
    #crack_user(wl, users, 16)