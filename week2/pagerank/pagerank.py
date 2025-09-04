import os
import random
import re
import sys
import itertools
import math

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
    all_choices = {item for key, value in corpus.items() for item in itertools.chain([key], value)}
    linked_choices = {item for item in corpus[page] if len(corpus[page])}
    print(all_choices)
    print(linked_choices)
    jump = (1 - damping_factor) / len(all_choices)
    linked = (damping_factor / len(linked_choices)) + jump
    results = {}
    
    for p in all_choices:
        if linked_choices:
            if p in linked_choices:
                results[p] = linked
            else:
                results[p] = jump
        else:
            results[p] = jump + (damping_factor / len(all_choices))
    if math.isclose(sum(results.values()), 1):
        return results
        
        





def sample_pagerank(corpus, damping_factor, n):
    all_choices = {item for key, value in corpus.items() for item in itertools.chain([key], value)}
    all_choices = list(all_choices)
    choice = None
    results = dict.fromkeys(all_choices, 0)
    for sample in range(n):
        print(f"running sample...\n{sample}")
        if not choice:
            choice = random.choice(all_choices)
        probability = transition_model(corpus, choice, damping_factor)
        pages = list(probability.keys())
        weights = list(probability.values())
        choice = random.choices(pages, weights=weights, k=1)[0]
        results[choice] += 1
        print(f"~~~~choice:{choice}~~~~~")

    results = {key: value / n for key, value in results.items()}
    if math.isclose(sum(results.values()), 1):
        print(results)
    else:
        print("ERROR")
    


        







def iterate_pagerank(corpus, damping_factor):
    print('were in')
    all_choices = {item for key, value in corpus.items() for item in itertools.chain([key], value)}
    all_choices = list(all_choices)
    weights = [1/len(all_choices) for _ in enumerate(all_choices)]
    jump = (1 - damping_factor) / len(all_choices)
    print(jump)
    results = {key: value for key in all_choices for value in weights}
    print(results)
    counter = 0
    while counter < 5:
        counter += 1
        for i in all_choices:
            linked_from = {parentpage for parentpage, childpages in corpus.items() if i in childpages}
            if not linked_from:
                linked_from = all_choices
            outlinks = [value for key, value in corpus.items() if key in linked_from]
            print("~~~",outlinks,"~~~")
            page_rank_i = ((sum([value for key, value in results.items() if key in linked_from]) / len(outlinks)) * damping_factor) + jump
            print(i, linked_from)
            print(page_rank_i)
            results[i] = page_rank_i




if __name__ == "__main__":
    main()
