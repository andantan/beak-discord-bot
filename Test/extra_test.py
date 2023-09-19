class Test:
    def __init__(self) -> None:
        self.wait = [1, 2, 3]
        self.stage = [4]
        self.finish = [5, 6, 7]


    @property
    def ownership(self, include_stage: bool=False):
        if include_stage:
            return [self.wait, self.stage, self.finish]
        else:
            return [self.wait, self.finish]
        

cls = Test()

print(cls.ownership)
print(cls.ownership(True))