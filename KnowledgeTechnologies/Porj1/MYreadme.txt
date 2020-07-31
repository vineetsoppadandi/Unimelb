Read Me

- dict.txt: This is a list of approximately 370K English entries, which should
    comprise the dictionary for your approximate string search method(s). This
    dictionary is a slightly-altered version of the data from:
    https://github.com/dwyl/english-words
    The format of this file is one entry per line, in alphabetical order.
    You may use a different dictionary if you wish; if so, you should state
    the data source and justification in your report.
	
- candidates.txt: This is the list of 16925 tokens present in wordforms.txt, except
    that any token appearing in the dictionary has been excluded.
    One logical framework for the problem of finding lexical blends is that any token
    not present within the dictionary is potentially a blend. Note that there are other
    possible strategies, but we have structured this Project specifically so that
    blends do not appear in the dictionary (which may not be true for data in general).

- blends.txt: This is a tab-delimited list of tokens appearing in the tweets,
    which have been manually identified as being lexical blends.
    Each line takes the form: blend token, tab character, component word, tab character,
    component word, newline.
    Note that some of the blends do not appear in the candidates list, because they have
    been excluded in the preprocessing stage. You might be interested to try out other
    preprocessing strategies instead.
    Note that some of the tokens in the tweets may be blends that are not listed in
    blends.txt; we make no guarantees that this file represents an exhaustive list,
    only that these tokens have indeed been identified as blends.

- MYcode - runs the algorithium use the files above