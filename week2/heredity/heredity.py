import csv
import itertools
import sys
from collections import deque
import math

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])
    print(people)

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                        False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    print(one_gene)
    print(two_genes)
    mutation = PROBS["mutation"]
    data = dict()
    for person in people:
        print(person)
        gene_count = 2 if person in two_genes else 1 if person in one_gene else 0
        print(gene_count)
        trait_value = True if person in have_trait else False
        print(trait_value)
        has_parents = True if people[person]["mother"] or people[person]["father"] else False
        print("hasparents", has_parents)
        if not has_parents:
            person_prob = PROBS["gene"][gene_count]
            trait_prob = PROBS["trait"][gene_count][trait_value]
            results = person_prob * trait_prob
            data[person] = results
            continue
        mother = people[person]["mother"]
        father = people[person]["father"]
        mother_prob = 0.5 if mother in one_gene else (1 - mutation) if mother in two_genes else mutation
        father_prob = 0.5 if father in one_gene else (1 - mutation) if father in two_genes else mutation
        if gene_count == 0:
            child_prob = (1 - mother_prob) * (1 - father_prob)
        elif gene_count == 1:
            child_prob = mother_prob * (1 - father_prob) + father_prob * (1 - mother_prob)
        elif gene_count == 2:
            child_prob = mother_prob * father_prob
        child_prob *= PROBS["trait"][gene_count][trait_value]
        data[person] = child_prob

    apple = math.prod(data.values())
    print(apple)
    return(apple)


def update(probabilities, one_gene, two_genes, have_trait, p):
    for person in probabilities:
        gene_count = 1 if person in one_gene else 2 if person in two_genes else 0
        has_trait = True if person in have_trait else False
        probabilities[person]["gene"][gene_count] += p
        probabilities[person]["trait"][has_trait] += p


def normalize(probabilities):
    for person in probabilities:
        gene_check = True if sum(probabilities[person]["gene"].values()) == 1 else False
        trait_check = True if sum(probabilities[person]["trait"].values()) == 1 else False
        if gene_check and trait_check:
            continue
        if not gene_check:
            total_gene = sum(probabilities[person]["gene"].values())
            for gene, value in probabilities[person]["gene"].items():
                probabilities[person]["gene"][gene] = (value / total_gene)
        if not trait_check:
            total_trait = sum(probabilities[person]["trait"].values())
            for trait, value in probabilities[person]["trait"].items():
                probabilities[person]["trait"][trait] = (value / total_trait)
        




if __name__ == "__main__":
    main()
