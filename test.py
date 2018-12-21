templates = {
    "#red": ["color", "red"],
    "#24": ["gires2.wdf", "0x12345678"],
    "#35": ["gires2.wdf", "0x12345678"],
    "#2": ["gires2.wdf", "0x12345678"]
}

prefix = {
    "#": 1,
    "#r": 1, "#re": 1,
    "#2": 1,
    "#3": 1
}

text = "啊#35"

def t():

    contents = []
    i = 0
    pattern_matching = False
    last_pattern = None  # color, bold, italic
    pattern_text_cache = "#"
    while i < len(text):
        if text[i] == "#":  # 如果是#
            pattern_matching = True
        elif text[i].isalnum():  # 如果是数字或者字母
            if pattern_matching:  # 如果此时正在匹配
                pattern_text_cache += text[i]  # 则暂存该字符
                if pattern_text_cache in templates:  # 如果有该模式
                    last_pattern = templates[pattern_text_cache]  # 记录
                if pattern_text_cache not in prefix:  # 如果前缀不匹配
                    pattern_matching = False  # 退出匹配模式
                    if last_pattern:
                        contents.append(pattern_transform(last_pattern))
                    else:
                        for x in pattern_text_cache:
                            contents.append(x)
                    last_pattern = None
                    pattern_text_cache = "#"
            else:
                contents.append(text[i])
        else:
            if pattern_matching:
                pattern_matching = False  # 退出匹配模式
                if last_pattern:
                    contents.append(pattern_transform(last_pattern))
                else:
                    for x in pattern_text_cache:
                        contents.append(x)
                last_pattern = None
                pattern_text_cache = "#"
            contents.append(text[i])
        i += 1
    if last_pattern:
        contents.append(pattern_transform(last_pattern))
    elif pattern_text_cache != "#":
        for x in pattern_text_cache:
            contents.append(x)
    return contents

def pattern_transform(pattern):
    if pattern[0] == "color":
        return "Color"
    else:
        return "Emoji"

print(t())