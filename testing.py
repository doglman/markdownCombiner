import re

if __name__ == "__main__":
    text_phrases = ["[[link#subheading|alttext]]", "[[link]]", "[[link#subheading]]", "[[link|alttext]]"]
    for text in text_phrases:
        result = re.search(r"\[\[([^#|\]]+)([^|\]]*)([^\]]*)\]\]", text)
        groups = result.groups()
        
        printText = ""

        if groups[1] != '': # i.e. there's a subheading
            printText = "[[{}{}]]".format(groups[1],groups[2])
        else:
            printText = "[[#{}{}]]".format(groups[0], groups[2])

        print(printText)