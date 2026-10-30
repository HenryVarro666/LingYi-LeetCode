CONFIG = dict(
    num=1603, title='设计停车系统', difficulty='Easy', category='设计',
    author='yiduobo', technique='计数 · 剩余车位',
    tags=[],
    code='''
class ParkingSystem(object):

    def __init__(self, big, medium, small):
        self.cnt_list = [big, medium, small]

    def addCar(self, carType):
        if self.cnt_list[carType - 1] > 0:
            self.cnt_list[carType - 1] -= 1
            return True

        return False
''',
    call='''p = ParkingSystem(1, 1, 0)
res = [p.addCar(1), p.addCar(2), p.addCar(3), p.addCar(1)]
res''',
    expect=[True, True, False, False],
    views=[
        dict(type='array', var='self.cnt_list', label='cnt_list（剩余车位：大 / 中 / 小）', cell=130, h=260,
             pointers={'carType - 1': 'blue'}),
        dict(type='text', h=100, size=30,
             fn=lambda S: (f'车型 `{S["carType"]}` → 下标 `{S["carType"] - 1}`（车型从 1 开始，下标从 0 开始）'
                           if 'carType' in S else '三种车位各有固定数量')),
    ],
    watch=[('carType', 'carType', 'blue'), ('cnt_list', 'self.cnt_list', 'green')],
    captions={
        'self.cnt_list = [big': '`cnt_list` 按 大、中、小 记下三种车位的剩余数：`{self.cnt_list}`',
        'if self.cnt_list': lambda S, B, r: (f'车型 `{S.carType}` 的剩余车位 `{S.self.cnt_list[S.carType - 1]}` > 0 → ==还有空位==，可以停'
                                            if S.self.cnt_list[S.carType - 1] > 0 else
                                            f'车型 `{S.carType}` 的剩余车位 `0`，不大于 0 → ==没有空位=='),
        '-= 1': '停进去一辆，该类车位 -1：`cnt_list = {self.cnt_list}`',
        'return True': '停车成功，返回 `True`',
        'return False': '没有空位，剩余数不变，返回 `False`',
    },
    cards=dict(
        one_liner='只记各类车位还剩几个：有就减一，没有就拒绝',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['停车场有大、中、小三种车位，各有固定数量',
                 '`addCar(carType)`：1=大车，2=中车，3=小车，只能停同类车位',
                 '有空位就停并返回 `True`，否则返回 `False`',
                 '本视频：`ParkingSystem(1, 1, 0)`，依次来 1、2、3、1 型车'],
        quote='只需要统计各类车位的剩余数目，并根据当前需求的车位类型判断是否还有空余车位，并根据是否停车来修正各类车位的剩余数目即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['用长度为 3 的列表记剩余数，车型 `carType` 对应下标 `carType - 1`',
              '剩余数 `> 0` 才能停：停了就减 1',
              '剩余数为 0 直接返回 `False`，什么都不改'],
        summary=['每次操作 `O(1)`，只需要三个计数',
                 '易错：车型从 1 开始，下标要减 1',
                 '失败时不能修改剩余数',
                 '同类设计题：只维护必要的状态，不用记每辆车'],
    ),
)
