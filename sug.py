with open("Text.txt","r") as f:
  text = f.read()
text = text.lower()
all_word = list(set(text.split()))

def search(all_word,input):
  x = [(i,l.startswith(input)) for i,l in enumerate(all_word)]
  output = []
  for i,l in x:
    if l:
      output.append(all_word[i])
  return output


