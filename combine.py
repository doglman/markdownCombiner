"""
This file was created to combine an Obsidian Vault's markdown files into a single file.
That combined file can then be exported to a PDF, hopefully with the internal links working correctly.

Here's what that process should look like:
1. Recursively search through the provided directory, concatenating all '.md' files into a single text file.
2. Perform a regex find-and-replace to correct page links.
"""

import glob
import re

def combineFiles(path: str, outputName: str) -> None:
    """Searches through the provided directory, concatenating all .md files into a single text file.
    Inserts the filename as a level one header and inserts 3 horizontal bars to divide pages.
    
    Citation: https://stackoverflow.com/a/17749339
    """
    read_files = glob.glob("{}/*.md".format(path))

    with open("{}.md".format(outputName), "w") as outfile:
        for f in read_files:
            with open(f, "r") as infile:
                name = f.removeprefix("{}/".format(path))
                name = name.removesuffix(".md")
                # print("File title is: {}".format(name))
                outfile.write("\n# {}\n".format(name)) # Write the files' name as a Level 1 Heading
                outfile.write(infile.read())
                outfile.write("\n\n---\n---\n---\n") # Write some extra newlines and dividing lines between pages

def repairLinks(filePath: str) -> None:
    """
    Processes the file indicated by `filePath`, replacing internal links of the format `[[nameOfFile#subheading]]` to links of format `[[#subheading]]`
    - Used for repairing the internal file-to-file links so the links in the combined file still work.
    """
    # Read the provided file into a list of strings
    # https://stackoverflow.com/a/4719562
    with open(filePath, "r") as inFile:
        lineList = inFile.readlines()

    # Go through each line, repairing links as necessary, and appending to a new list
    newLineList = []

    for line in lineList:
        # https://pynative.com/python-regex-replace-re-sub/
        new_line = re.sub(r"[^!`]\[\[([^#|\]]+)([^|\]]*)([^\]]*)\]\]", extractLinkSubgroups, line)
        if new_line != line:
            print("Next line:|| {} ||".format(line))
            print("Now is:|| {} ||".format(new_line))

        # Overwrite the old line with the new one
        newLineList.append(new_line)

    # Save results, overwriting the provided file.    
    with open(filePath, 'w') as outFile:
        outFile.writelines(newLineList)
    

def extractLinkSubgroups(match_obj: re.Match)-> str:
    """
    Callable for `re.sub()`'s second parameter. Extracts the correct subgroups for a link depending on if it links to a subheading or not.
    
    Assumes `match_obj` are matches for the following regular expression: `\[\[([^#|\]]+)([^|\]]*)([^\]]*)\]\]`
    
    ...which has 3 sub-groups for the possible link, header, and alt text fields, i.e. [[link#heading|altText]]
    """
    groups = match_obj.groups()
    
    if groups[1] != '': #i.e. there's a subheading
        return " [[{}{}]]".format(groups[1],groups[2])
    else:
        return " [[#{}{}]]".format(groups[0], groups[2])

if __name__ == "__main__":
    combineFiles("./testKb", "test_out")
    repairLinks("/home/samswin/code/markdownCombiner/test_out.md")