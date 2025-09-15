str="rar"

rev =''
for i in str:
    rev=i+rev
# print(rev)

if str==rev:
    print("palindrom")
else:
    print("Not a plaindrom")