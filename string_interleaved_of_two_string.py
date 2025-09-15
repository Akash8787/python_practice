def is_interleaved(str1, str2, str3):
    # If lengths don't add up, it can't be an interleaving
    if len(str1) + len(str2) != len(str3):
        return False

    # Create a DP table where dp[i][j] represents if str3[0:i+j] is interleaving str1[0:i] and str2[0:j]
    dp = [[False] * (len(str2) + 1) for _ in range(len(str1) + 1)]

    # Iterate over the lengths of str1 and str2
    for i in range(len(str1) + 1):
        for j in range(len(str2) + 1):
            if i == 0 and j == 0:
                dp[i][j] = True  # Base case: both str1 and str2 are empty
            elif i == 0:
                dp[i][j] = dp[i][j-1] and str2[j-1] == str3[i+j-1]
            elif j == 0:
                dp[i][j] = dp[i-1][j] and str1[i-1] == str3[i+j-1]
            else:
                dp[i][j] = (dp[i-1][j] and str1[i-1] == str3[i+j-1]) or (dp[i][j-1] and str2[j-1] == str3[i+j-1])

    return dp[len(str1)][len(str2)]

# Example usage:
str1 = "abcg"
str2 = "def"
str3 = "adbcefg"

if is_interleaved(str1, str2, str3):
    print(f"'{str3}' is an interleaving of '{str1}' and '{str2}'.")
else:
    print(f"'{str3}' is NOT an interleaving of '{str1}' and '{str2}'.")
