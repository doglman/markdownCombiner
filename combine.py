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
                outfile.write("\n# {}\n".format(name))
                outfile.write(infile.read())
                outfile.write("\n\n---\n---\n---\n")

def repairLinks(filePath: str) -> None:
    """
    Processes the file indicated by `filePath`, replacing internal links of the format `[[nameOfFile#subheading]]` to links of format `[[#subheading]]`
    - Used for repairing the internal file-to-file links so the links in the combined file still work.
    """

    """
    I'm thinking the Regex will looks something like:
    \[\[([^#|\]]+)([^\]]*)\]\]
    with the replacement phrase being:
    [[newPage#$1$2]]
    So 2 groups: [[group1#group2|group2]] to correspond to the document and heading/display text. 
    The heading/display text is copied into a new link, with the name of the new page placed as the document reference.
    """
    #TODO - A replacement function needs to be built for the `re.sub()` function
    with open(filePath, "r") as inFile:
        try:
            while True:
                line = next(inFile)
                new_line = re.sub("\[\[([^#|\]]+)([^\]]*)\]\]", repairLink, line)
                if new_line != "":
                    print("Next line:|| {} ||".format(line))
                    print("Now is:|| {} ||".format(new_line))
                #TODO - write line to buffer
        except StopIteration:
            print("EOF reached")

def repairLink(match_obj: re.Match)->str:
    """
    Callable for `re.sub()`'s second parameter. Reformats the regex match to be a valid link in the new document.
    
    Process:
    1. Search for any alternate text (past the '|') and extract the contents for later.
    2. Identify whether the link is to a sub-heading or not (i.e. contains a '#')
        - If it lacks a subheading, the new link is: [[#page_name]]
        - If it has a subheading, the new link is: [[#subheading]]
    3. Assemble the final subheading and return the link.
    """
    alt_text = re.search("\|[^\]]+", match_obj) 
    link_text = None
    if re.search("#", match_obj) is None:
        pass # TODO
    else:
        pass # TODO
    
    return "[[#{}{}]]".format(link_text, alt_text)

if __name__ == "__main__":
    combineFiles("./testKb", "test_out")
    repairLinks("/home/samswin/code/markdownCombiner/test_out.md")