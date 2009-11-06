#!/usr/bin/python
import random
text = 'sometext'
text_shuffled = [(j,text[j]) for j in range(len(text))]
random.shuffle(text_shuffled)
index = 3
print text_shuffled
text_shuffled_string = ''.join([i[1] for i in text_shuffled])
print text_shuffled_string
indices = [i[0] for i in text_shuffled[:index]]
text_shuffled.sort()
text_sorted = text_shuffled
blank = [' ']*len(text)
print indices
for i in indices:
    blank[i] = text[i]
print ''.join(blank)

