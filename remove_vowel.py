# str = "Aakash"


# def removed_vowel_text(text):
#     vowel = "aeiouAEIOU"
#     removed_text =''
#     for i in text:
#         if i not in vowel:
#             removed_text+=i
#     return removed_text
# str = input("enter the string:")
# result = removed_vowel_text(str)
# print(result)


text = "python is a powerful programming language"
text=text.split(" ")
words ={}
for i in text:
    words[i]=len(i)
print(words)


