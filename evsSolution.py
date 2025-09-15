# Write a Python function that takes a string input and returns the character that appears most frequently (excluding spaces).
# If multiple characters have the same highest frequency, return the one that appears first in the string. 
# Example 1: 
# Input:  "fastapi is fantastic" 
# Output: "a"

# str = "fastapi is fantastic"

# str=str.replace(" ",'')

s = "fastapi is fantastic"
# Step 1: Remove spaces and build a frequency dictionary manually
freq = {}
for i in range(len(s)):
    ch = s[i]
    # print(ch)
    if ch != ' ':
        # print(ch)
        # Manually count if not already counted
        if ch not in freq:
            # print(ch)
            count = 0
            for j in range(len(s)):
                if s[j] == ch:
                    count += 1
            freq[ch] = count
            print(freq[ch])

# Step 2: Find the max frequency character that appears first
max_count = -1
result_char = ''
for i in range(len(s)):
    ch = s[i]
    if ch != ' ' and freq[ch] > max_count:
        max_count = freq[ch]
        result_char = ch

print(result_char)





#============================================================================================================================

# You are given two strings word1 and word2. Merge the strings by adding letters in alternating order, starting with word1. 
# If a string is longer than the other, append the additional letters onto the end of the merged string. 
# Return the merged string. 
# Example 1: 
# Input: word1 = "abc", word2 = "pqr" 
# Output: "apbqcr" 
# Explanation: The merged string will be merged as so: 
# word1:  a   b   c 
# word2:    p   q   r 
# merged: a p b q c r


word1 = "abc"
word2 = "pqr"

merged = ""
i = 0
j = 0
len1 = len(word1)
len2 = len(word2)

# Alternate characters from both strings
while i < len1 and j < len2:
    merged += word1[i]
    # print("Merge:",merged)
    merged += word2[j]
    # print("Merge:",merged)
    i += 1
    j += 1

# # Append remaining characters from word1, if any
# while i < len1:
#     merged += word1[i]
#     i += 1

# # Append remaining characters from word2, if any
# while j < len2:
#     merged += word2[j]
#     j += 1

print(merged)






