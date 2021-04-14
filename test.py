import RecommendationAlgorithm

if __name__=='__main__':
    cf = RecommendationAlgorithm.UserCFRec("./data/ml-1m/ratings.dat")
    result = cf.recommend("1")
    print("user '1' recommend result is {} ".format(result))

    precision = cf.precision()
    print("precision is {}".format(precision))