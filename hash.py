from Crypto.Hash import SHA256
import bcrypt
import secrets
import string

# limited digest to 8 bits
def hash_input(b: bytes) -> str:
  return SHA256.new(b).hexdigest()[:2]

def random_string(length=8) -> str:
  chars = string.ascii_letters + string.digits + string.punctuation + " "
  return ''.join(secrets.choice(chars) for i in range(length))

# weak collision resistance
def find_weak_collision() -> str:
  m0 = b'example'
  digest1 = hash_input(m0)
  m1 = random_string(len(m0)).encode('utf-8')
  digest2 = hash_input(m1)

  while digest2 != digest1:
    m1 = random_string(len(m0)).encode('utf-8')
    digest2 = hash_input(m1)
  print(f'COLLISION FOUND:\n m0: {m0} | digest: {digest1} \n m1: {m1} | digest: {digest2}')

if __name__ == '__main__':
  find_weak_collision()