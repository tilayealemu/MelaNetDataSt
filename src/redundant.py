import json
import sys
import operator

supported = """
ሀ ሁ ሂ ሄ ህ ሆ
ለ ሉ ሊ ላ ሌ ል ሎ ሏ
መ ሙ ሚ ማ ሜ ም ሞ ሟ
ረ ሩ ሪ ራ ሬ ር ሮ ሯ
ሰ ሱ ሲ ሳ ሴ ስ ሶ ሷ
ሸ ሹ ሺ ሻ ሼ ሽ ሾ ሿ
ቀ ቁ ቂ ቃ ቄ ቅ ቆ ቋ
በ ቡ ቢ ባ ቤ ብ ቦ ቧ
ቨ ቩ ቪ ቫ ቬ ቭ ቮ ቯ
ተ ቱ ቲ ታ ቴ ት ቶ ቷ
ቸ ቹ ቺ ቻ ቼ ች ቾ ቿ
ኋ
ነ ኑ ኒ ና ኔ ን ኖ ኗ
ኘ ኙ ኚ ኛ ኜ ኝ ኞ ኟ
አ ኡ ኢ ኤ እ ኦ
ኧ
ከ ኩ ኪ ካ ኬ ክ ኮ
ኳ
ወ ዉ ዊ ዋ ዌ ው ዎ
ዘ ዙ ዚ ዛ ዜ ዝ ዞ ዟ
ዠ ዡ ዢ ዣ ዤ ዥ ዦ ዧ
የ ዩ ዪ ያ ዬ ይ ዮ
ደ ዱ ዲ ዳ ዴ ድ ዶ ዷ
ጀ ጁ ጂ ጃ ጄ ጅ ጆ ጇ
ገ ጉ ጊ ጋ ጌ ግ ጐ ጓ ጔ
ጠ ጡ ጢ ጣ ጤ ጥ ጦ ጧ
ጨ ጩ ጪ ጫ ጬ ጭ ጮ ጯ
ጰ ጱ ጲ ጳ ጴ ጵ ጶ ጷ
ፀ ፁ ፂ ፃ ፄ ፅ ፆ ፇ
ፈ ፉ ፊ ፋ ፌ ፍ ፎ ፏ
ፐ ፑ ፒ ፓ ፔ ፕ ፖ
""".split()

same = {
    'ሃ':'ሀ',
    'ሐ':'ሀ', 'ሑ':'ሁ', 'ሒ':'ሂ', 'ሓ':'ሀ', 'ሔ':'ሄ', 'ሕ':'ህ', 'ሖ':'ሆ', 'ሗ':'ኋ',
    'ሠ':'ሰ', 'ሡ':'ሱ', 'ሢ':'ሲ', 'ሣ':'ሳ', 'ሤ':'ሴ', 'ሥ':'ስ', 'ሦ':'ሶ', 'ሧ':'ሷ',
    'ቈ':'ቆ', 'ቍ':'ቁ',
    'ኲ':'ኩ', 'ኰ':'ኮ',
    'ኸ':'ሀ', 'ኹ':'ሁ', 'ኺ':'ሂ', 'ኻ':'ሀ', 'ኼ':'ሄ', 'ኽ':'ህ', 'ኾ':'ሆ',
    'ኅ':'ሀ', 'ኃ':'ሀ',
    'ኆ':'ኖ',
    'ኣ':'አ',
    'ኵ':'ኩ',
    'ዐ':'አ', 'ዑ':'ኡ', 'ዒ':'ኢ', 'ዓ':'አ', 'ዔ':'ኤ', 'ዕ':'እ', 'ዖ':'ኦ',
    'ጸ':'ፀ', 'ጹ':'ፁ', 'ጺ':'ፂ', 'ጻ':'ፃ', 'ጼ':'ፄ', 'ጽ':'ፅ', 'ጾ':'ፆ', 'ጿ':'ፇ',
    'ጎ':'ጐ', 'ጏ':'ጐ', 'ጕ':'ጉ'
}

def replace(str):
    for c in str:
        if c in same:
            str = str.replace(c, same[c])
    return str

def remove_redundant(filename):
    data = []
    stat = {}
    unsupported = set()
    with open(filename) as f:
        for line_num, json_line in enumerate(f):
            spec = json.loads(json_line)
            spec["text"] = replace(spec["text"])
            data.append(spec)
            for c in spec["text"]:
                if c not in stat:
                    stat[c] = 1
                else:
                    stat[c] += 1
                if c != ' ' and c not in supported:
                    unsupported.add(c)

    with open(filename, 'w') as f:
        for line in data:
           print(json.dumps(line, ensure_ascii=False), file=f)
    print("== Unsupported characters ==")
    print(unsupported)
    print("== Character stat ==")
    stat = sorted(stat.items(), key=operator.itemgetter(1), reverse=True)
    print(stat)