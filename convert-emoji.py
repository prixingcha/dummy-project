unicode_code_point = "\U0001F44D"
emoji = unicode_code_point 
unicode_text = "\\U{:0>8X}".format(ord(emoji))

print(unicode_code_point)

print(unicode_text)
