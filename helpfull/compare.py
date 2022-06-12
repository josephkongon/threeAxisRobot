from PIL import Image
import imagehash
hash0 = imagehash.average_hash(Image.open('image1.jpeg'))
hash1 = imagehash.average_hash(Image.open('image1Copy.jpeg'))
cutoff = 1  # maximum bits that could be different between the hashes.
print(hash1,hash0)
if hash0 - hash1 < cutoff:
  print('images are similar')
else:
  print('images are not similar')