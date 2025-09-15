def is_anagram(str1, str2):
    # Remove spaces and convert to lowercase for case-insensitive comparison
    str1 = str1.replace(" ", "").lower()
    str2 = str2.replace(" ", "").lower()
    # Check if the sorted forms of both strings are equal
    return sorted(str1) == sorted(str2)

# Example usage
string1 = "listen"
string2 = "silent"
if is_anagram(string1, string2):
    print(f"'{string1}' and '{string2}' are anagrams.")
else:
    print(f"'{string1}' and '{string2}' are not anagrams.")
