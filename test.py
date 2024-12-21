s = "computer"


def reverse_string(s):
    res = ""
    n = len(s)
    
    for i in range(n-1, -1, -1):
        res += s[i]
        
    return res

print(reverse_string(s))