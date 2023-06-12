import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import render


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    names = list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))
    entry = []
    for name in names:
        if name.strip():
            entry.append(name)
    return (entry)



def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None


def convert(text):

    md_text = text

    # Define a regular expression pattern to match Markdown links
    link =  r'\[([^\]]+)\]\(([^\)]+)\)'

    bold = r'\*\*(.*?)\*\*'

    # Define a regular expression pattern to match Markdown header2s
    heading2 = r'\#\#(.*)'

    # Define a regular expression pattern to match Markdown header1s
    heading1 = r'\#(.*)'

    # Define a regular expression pattern to match Markdown unordered lists
    ul = r'^(\s*[-*]\s+)(.*)$'
    # Replace Markdown bold syntax with HTML bold syntax using regular expressions
    text_bold = re.sub(bold, r'<b>\1</b>', md_text)

    # Replace Markdown headers with HTML headers using regular expressions
    text2 = re.sub(heading2, r'<h2>\1</h2>', text_bold)
    text1 = re.sub(heading1, r'<h1>\1</h1>', text2)

    # Replace Markdown unordered lists with HTML unordered lists using regular expressions
    text_ul = re.sub(ul, r'<ul>\n<li>\2</li>\n</ul>', text1, flags=re.MULTILINE)

    # Replace Markdown links with HTML links using regular expressions
    html_text = re.sub(link, r'<a href="\2">\1</a>', text_ul)

    return (html_text)


def entry_substr(word):
    """
    Returns a list of all names of encyclopedia entries that is a substring of the given word.
    """
    _, filenames = default_storage.listdir("entries")
    names = list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))
    pattern = (r'.*{}.*'.format(re.escape(word)))
    txt = []
    for name in names:
        words = re.findall(pattern, name)
    for word in words:
        if word.strip():
            txt.append(word)
    return(txt)


def check(title):
    """
    Check if the title  already exist.
    """
    _, filenames = default_storage.listdir("entries")
    names = list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))
    if title in names:
        return(1)
    return(0)
