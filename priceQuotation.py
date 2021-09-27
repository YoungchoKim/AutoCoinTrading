def get_price(cost):
    cost = int(cost)
    if cost >= 2000000:
        cost = cost // 1000
        cost = cost * 1000 + 1000
    elif cost >= 1000000:
        cost = cost // 500
        cost = cost * 500 + 500
    elif cost >= 500000:
        cost = cost // 100
        cost = cost * 100 + 100
    elif cost >= 100000:
        cost = cost // 50
        cost = cost * 50 + 50
    elif cost >= 10000:
        cost = cost // 10
        cost = cost * 10 + 10
    elif cost >= 1000:
        cost = cost // 5
        cost = cost * 5 + 5
    elif cost >= 100:
        cost = cost // 1
        cost = cost * 1 + 1
    elif cost >= 10:
        cost = round(cost+0.5,1)
    elif cost >= 10:
        cost = round(cost+0.05,2)
    return cost



        
