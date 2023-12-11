import os
import random
import re
import sys
import copy


DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # raise NotImplementedError

    trans_model = {}
    if len(corpus[page]) > 0:
        n = len(corpus[page])
        for p in corpus[page]:
            trans_model[p] = damping_factor / n
    else:
        n = len(corpus)
        for p in corpus:
            trans_model[p] = damping_factor / n
    n = len(corpus)
    d = (1 - damping_factor) / n
    for tm in trans_model:
        trans_model[tm] += d
    return trans_model


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # raise NotImplementedError

    page = random.choice(list(corpus.keys()))
    count = {}
    for k in corpus:
        count[k] = 0
    for i in range(1, n):
        tm = transition_model(corpus, page, damping_factor)
        next_page = random.choices(list(tm.keys()), weights=list(tm.values()), k=1)[0]
        count[next_page] += 1
        page = next_page
    res = {}
    for k in corpus:
        res[k] = count[k] / n
    return res


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # raise NotImplementedError

    for k in corpus:
        if len(corpus[k]) == 0:
            corpus[k] = set(corpus.keys())
    n = len(corpus)
    page_rank = {}
    for key in corpus:
        page_rank[key] = 1 / n

    pre_val = list(page_rank.values())
    pre_page_rank = copy.deepcopy(page_rank)

    stop = True
    while stop:
        for p in page_rank:
            s = 0
            for k in corpus:
                if p in corpus[k]:
                    s += pre_page_rank[k] / len(corpus[k])
            page_rank[p] = ((1 - damping_factor) / n) + (damping_factor * s)
        val = list(page_rank.values())
        ss = []
        stop = False
        for i in range(0, len(val)):
            ss.append(pre_val[i] - val[i])
        for e in ss:
            if e > 0.001:
                stop = True
        pre_val = val
        pre_page_rank = page_rank.copy()
    return page_rank


if __name__ == "__main__":
    main()
