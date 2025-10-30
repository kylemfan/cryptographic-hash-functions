from Crypto.Hash import SHA256
from pypdf import PdfReader
import os
#import nltk
import bcrypt
import secrets
import string
import random

# limited digest to 8 bits
def hash_input(b: bytes) -> str:
  return SHA256.new(b).hexdigest()[:2]

def random_string(length=8) -> str:
  chars = string.ascii_letters + string.digits + string.punctuation + " "
  return ''.join(secrets.choice(chars) for i in range(length))

# weak collision resistance
def find_wcr():
  m0 = b'example'
  digest1 = hash_input(m0)
  m1 = random_string(len(m0)).encode('utf-8')
  digest2 = hash_input(m1)

  while digest2 != digest1:
    m1 = random_string(len(m0)).encode('utf-8')
    digest2 = hash_input(m1)
  print(f'\n\tCOLLISION FOUND:\n m0: {m0} | digest: {digest1} \n m1: {m1} | digest: {digest2}\n')

# strong collision resistance
def find_scr():
  digests = {} # digest : message
  m0 = random_string(random.randint(1, 10)).encode('utf-8')
  digest1 = hash_input(m0)
  digests[digest1] = m0

  while True:
    m1 = random_string(random.randint(1, 10)).encode('utf-8')
    digest2 = hash_input(m1)
    if digest2 in digests:
      print(f'\n\tCOLLISION FOUND:\n m0: {m0} | digest: {digest1} \n m1: {m1} | digest: {digest2}\n')
      break
    else:
      digests[m1] = digest2

# start breaking the hashes:
# https://www.geeksforgeeks.org/python/working-with-pdf-files-in-python/
def break_hash():
  reader = PdfReader("shadow.pdf")
  page = reader.pages[0]
  print(page.extract_text())
  page_data = page.extract_text().split('\n')
  i = 0
  while i < 16:
    i += 1
    if(os.fork() == 0):
      print(f"fork {i} {os.getpid()}")
      os._exit(0)
  # wait for child processes
  while 1:
    try:
      pid, status = os.wait()
    except ChildProcessError:
      break


if __name__ == '__main__':
  find_scr()
  print(break_hash())