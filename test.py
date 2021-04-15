import RecommendationAlgorithm
import json #导入json

if __name__=='__main__':
    cf = RecommendationAlgorithm.UserCFRec("./data/ml-1m/ratings.dat")
    result = cf.recommend("1")
    print(result)
    print(type(result))
    dic_json = json.loads(json.dumps(result,ensure_ascii=False,indent=4))
    print(dic_json)
    print(type(dic_json))
    print("user '1' recommend result is {} ".format(result))

    precision = cf.precision()
    print("precision is {}".format(precision))