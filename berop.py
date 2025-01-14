import os
import json

filepath = './output/out_json/'
#filename = 'out_db538cf1-4742-453a-b270-87d28a363ad0.json'
#filename = 'out_58d0ebe4-6610-4902-9c48-b535d3ba13fc.json'
#filename = 'out_dd6bcd75-80b4-4b09-9430-0a062e6f29b1.json'
#filename = 'out_492d031d-54d3-43a5-96f1-f699617cb3c3.json'
#filename = 'out_99b25264-5ca4-4e68-b36f-b7ef791ea095.json'
#filename = 'out_1372c841-5e37-4c54-b127-cd47139a87ff.json'
#filename = 'out_4c3a5881-9666-476b-8905-4e91cc21be6d.json'
filename = 'out_latest.json'
filepathname = filepath + filename

with open(filepathname, "r") as f:
    json_dict = json.load(f)

wordlist = json_dict["wordlist"]
print(f"wordlist:\ntype: {type(wordlist)}, len: {len(wordlist)}")
print(f"keys: {wordlist[0].keys()}")

vocab_list = [word['pronunciation'][0] for word in wordlist]
#sinogram_list = [word['word'] for word in wordlist]
#sinogram_list = [word['sinogram'] for word in wordlist]
sinogram_list = [word['characters'] for word in wordlist]
#print(vocab_list)
#print(sinogram_list)

print()
[print(vocab, end=', ') for vocab in vocab_list]
print()
[print(sinogram, end=', ') for sinogram in sinogram_list]

print()
for vi, v in enumerate(vocab_list):
    #print(f"{v}, {sinogram_list[vi]}")

    print(f"{vi}: {v}, {sinogram_list[vi]}")

