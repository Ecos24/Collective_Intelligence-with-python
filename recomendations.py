from math import sqrt

# A dictionary of movie critics & their rating of a small set of movies
critics = {'Lisa': {'Lady in the water': 2.5, 'Snakes on a plane': 3.5, 'Just my luck': 3.0, 'Superman returns': 3.5, 'You,Me & dupree': 2.5, 'The night listener': 3.0},
           'Gene': {'Lady in the water': 3.0, 'Snakes on a plane': 3.5, 'Just my luck': 1.5, 'Superman returns': 5.0, 'You,Me & dupree': 3.5, 'The night listener': 3.0},
           'Michael': {'Lady in the water': 2.5, 'Snakes on a plane': 3.0, 'Superman returns': 3.5, 'The night listener': 4.0},
           'Claudia': {'Snakes on a plane': 3.5, 'Just my luck': 3.0, 'Superman returns': 4.0, 'You,Me & dupree': 2.5, 'The night listener': 4.5},
           'Mick': {'Lady in the water': 3.0, 'Snakes on a plane': 4.0, 'Just my luck': 2.0, 'Superman returns': 3.0, 'You,Me & dupree': 2.0, 'The night listener': 3.0},
           'Jack': {'Lady in the water': 3.0, 'Snakes on a plane': 4.0, 'Superman returns': 5.0, 'You,Me & dupree': 3.5, 'The night listener': 3.0},
           'Toby': {'Snakes on a plane': 4.5, 'Superman returns': 4.0, 'You,Me & dupree': 1.0}}

# Based on Euclidean Distance
# Returns a distance-based similarity score for person1 & person2
def sim_distance(prefs, person1, person2):
    #Get the list of shared_items
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1
    # if they have no rating in common, return 0
    if len(si) == 0:
        return 0

    #Add up the squares of all the differences
    sum_of_squares = sum([pow(prefs[person1][item]-prefs[person2][item], 2) for item in prefs[person1] if item in prefs[person2]])

    return 1/(1+sum_of_squares)

# Returns the Pearson correlation coefficient for p1 & p2
def sim_pearson(prefs, p1, p2):
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item] = 1
    
    # Find the number of elements
    n = len(si)

    # if they have no rating in common
    if n == 0:
        return 0

    # Add up all the preferences
    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])

    # Sum up the squares
    sum1Sq = sum([pow(prefs[p1][it], 2) for it in si])
    sum2Sq = sum([pow(prefs[p2][it], 2) for it in si])

    # Sum up the product
    pSum = sum([prefs[p1][it]*prefs[p2][it] for it in si])

    # Calculate pearson score
    num = pSum - (sum1*sum2/n)
    den = sqrt((sum1Sq-pow(sum1, 2)/n)*(sum2Sq-pow(sum2, 2)/n))
    if den == 0:
        return 0

    r = num/den

    return r

# Returns the best matches for person from the prefs dictionary.
# Number of results and similarity function are optional params.
def topMatches(prefs, person, n=6, similarity = sim_pearson):
    score = [(similarity(prefs, person, others), others) for others in prefs if others != person]
    # Sort the list so the highest scores appear at the top
    score.sort()
    score.reverse()
    return score[0:n]

# Get recomendations for a person by using a weighted average of every other user's ranking
def getRecommendations(prefs, person, similarity = sim_pearson):
    totals = {}
    simSum = {}
    for others in prefs:
        # don't compare me to myself
        if others == person:
            continue
        sim = similarity(prefs, person, others)

        # ignore scores of zero or lower
        if sim < 0:
            continue

        print ('Critic: ',others,'\tSimilarity: ',sim)
        print ('------------------------------------------------')

        for item in prefs[others]:
            # only score movies i heven't seen yet
            if item not in prefs[person] or prefs[person][item] == 0:
                # Similarity*score
                totals.setdefault(item, 0)
                totals[item] += prefs[others][item]*sim
                # Sum of similarities
                simSum.setdefault(item, 0)
                simSum[item] += sim
                print (item, ': ', totals[item])
        
    # Create the normalised list
    ranking = [(total/simSum[item], item) for item, total in totals.items()]

    # Return the sorted list
    ranking.sort()
    ranking.reverse()
    return ranking