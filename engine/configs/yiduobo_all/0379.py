CONFIG = dict(
    num=379, title='电话目录管理系统', difficulty='Medium', category='设计',
    author='yiduobo', technique='集合维护空闲号码',
    tags=['常用数据结构'],
    code='''
class PhoneDirectory(object):

    def __init__(self, maxNumbers):
        self.idle = set(range(maxNumbers))

    def get(self):
        if len(self.idle) == 0:
            return -1
        return self.idle.pop()

    def check(self, number):
        return number in self.idle

    def release(self, number):
        self.idle.add(number)
''',
    call='''d = PhoneDirectory(3)
r = [d.get(), d.get(), d.check(0), d.check(2)]
d.release(0)
r += [d.check(0), d.get(), d.get(), d.get()]
r''',
    expect=[0, 1, False, True, True, 2, 0, -1],
    views=[
        dict(type='set', var='self.idle', label='idle（还没被占用的号码）', fmt=lambda x: str(x), h=200),
        dict(type='calls', label='正在执行', h=150),
    ],
    watch=[('idle', 'self.idle', 'green'), ('number', 'number', 'blue')],
    captions={
        'self.idle = set': '开始时 `0 ~ {maxNumbers-1}` 都空闲：`idle = {self.idle}`',
        'len(self.idle) == 0': lambda S, B, r: ('`idle` 空了：没有号码可分配' if not S.self.idle else '`idle` 里还有号码，可以分配'),
        'return -1': '没有空闲号码 → 返回 `-1`',
        'self.idle.pop()': '`get`：从集合里 ==pop 一个== 号码交出去，它就不再空闲 → 返回 `{ret}`',
        'number in self.idle': '`check({number})`：在集合里就是空闲 → ==`{ret}`==',
        'self.idle.add': '`release({number})`：把号码==放回集合==，又可以被分配',
    },
    cards=dict(
        one_liner='用一个集合装着所有还没用的号码',
        complexity='每个操作 `O(1)`，空间 `O(maxNumbers)`',
        problem=['设计电话目录：`get()` 分配一个空闲号码（没有则返回 `-1`）',
                 '`check(n)` 查询号码 `n` 是否空闲，`release(n)` 回收号码 `n`',
                 '号码范围 `0 ~ maxNumbers-1`；本视频 `maxNumbers = 3`'],
        quote='只需使用一个集合维护当前还未使用的电话号码就行了。题目中的三种操作分别对应了集合的pop、in以及add操作。',
        quote_src='—— yiduobo 题解原文',
        idea=['集合里放的就是==空闲==号码，分配 = 取走，回收 = 放回',
              '`get` 对应 `pop`，`check` 对应 `in`，`release` 对应 `add`',
              '集合为空时 `get` 返回 `-1`'],
        summary=['每个操作 `O(1)`，空间 `O(maxNumbers)`',
                 '集合装的是==空闲==号码，别装反了',
                 '`release` 对集合重复 add 无副作用',
                 '视频里把每次操作的返回值收集成列表 `r`（`release` 无返回）'],
    ),
)
