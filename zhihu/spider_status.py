#爬取状态

class Status():

    #用户信息表状态
    class Catch():

        def __init__(self):
            self.not_catch = 0
            self.catched = 1
            self.is_catching = 2
            self.user_not_useful = 3
            self.failed = 4
            self.user_not_exist = 5
            pass

    #用户关注表状态
    class Following():

        def __init__(self):
            self.not_catch = 0
            self.catched = 1
            self.is_catching = 2
            self.useless = 3
            self.failed = 4
            pass