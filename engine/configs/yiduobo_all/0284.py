CONFIG = dict(
    num=284, title='顶端迭代器', difficulty='Medium', category='设计',
    author='yiduobo', technique='peek 缓存',
    setup='''
class Iterator:
    def __init__(self, nums):
        self.nums = nums
        self.i = 0
    def hasNext(self):
        return self.i < len(self.nums)
    def next(self):
        v = self.nums[self.i]
        self.i += 1
        return v
''',
    code='''
class PeekingIterator(object):
    def __init__(self, iterator):
        self.peek_res = None
        self.iterator = iterator


    def peek(self):
        if self.peek_res is None:
            self.peek_res = self.iterator.next()
            return self.peek_res
        return self.peek_res

    def next(self):
        if self.peek_res is not None:
            tmp = self.peek_res
            self.peek_res = None
            return tmp
        else:
            return self.iterator.next()

    def hasNext(self):
        return self.peek_res is not None or self.iterator.hasNext()
''',
    call='''it = PeekingIterator(Iterator([1, 2, 3]))
[it.next(), it.peek(), it.peek(), it.next(), it.hasNext(), it.next(), it.hasNext()]''',
    expect=[1, 2, 2, 2, True, 3, False],
    views=[
        dict(type='array', var='self.iterator.nums', label='原迭代器的数据（蓝色箭头 = 下一个要取的位置）', h=190,
             pointers={'self.iterator.i': 'blue'},
             color=lambda S, i, v: 'green' if i < S.get('self.iterator.i', 0) else None),
        dict(type='text', fn=lambda S: (f"peek 缓存 `peek_res` = =={S['self.peek_res']}==" if S.get('self.peek_res') is not None
                                        else 'peek 缓存为空') if 'self.peek_res' in S else '', h=70, size=34),
    ],
    watch=[('peek_res', 'self.peek_res', 'yellow'), ('下标', 'self.iterator.i', 'blue'), ('tmp', 'tmp', 'green')],
    captions={
        3: '`peek_res` 是 peek 缓存，==None 表示缓存为空==',
        'self.iterator = iterator': '保存原迭代器，缓存为空时向它要数据',
        8: lambda S, B, r: (
            '缓存为空 → 要从原迭代器取一个并存进缓存' if S['self.peek_res'] is None else '缓存里已经有值 → 直接返回它，不再推进原迭代器'),
        9: '从原迭代器取出 `{peek_res}` 存进缓存：原迭代器已前进，但这个值还没被 next 消费',
        10: 'peek 返回 `{peek_res}`，缓存保留',
        11: 'peek 返回 `{peek_res}`，缓存保留',
        14: lambda S, B, r: (
            '缓存有值 → next 应该先给出它' if S['self.peek_res'] is not None else '缓存为空 → 直接交给原迭代器'),
        15: '先把缓存的值 `{tmp}` 拿出来',
        16: '消费掉了，清空缓存',
        17: 'next 返回缓存里的 `{tmp}`',
        19: 'next 直接返回原迭代器的下一个：`{ret}`',
        22: lambda S, B, r: f'缓存非空 或 原迭代器还有元素 → {r}',
    },
    cards=dict(
        one_liner='多存一个 peek 缓存：偷看的那个数先放缓存里',
        complexity='每个操作 `O(1)`，空间 `O(1)`',
        problem=['已有一个迭代器，只支持 `next()` 和 `hasNext()`',
                 '设计 `PeekingIterator`，额外支持 `peek()`：==查看下一个元素但不移动==',
                 '示例：`[1,2,3]`：`next→1`，`peek→2`，`next→2`，`next→3`，`hasNext→False`',
                 '本视频照此示例，多一次重复 `peek`'],
        quote='我的思路也比较简单，就是维护一个peek缓存。',
        quote_src='—— yiduobo 题解原文',
        idea=['`peek`：缓存空就从原迭代器取一个存起来，缓存有值就直接返回',
              '`next`：缓存有值就返回并清空；缓存空就直接用原迭代器',
              '`hasNext`：缓存有值，或原迭代器还有，就为 True'],
        summary=['所有操作 `O(1)`，只多一个缓存变量',
                 '易错点：用 None 表示缓存为空，所以元素本身不能是 None（题目是整数，没问题）',
                 '易错点：`peek` 取出后必须保存，否则原迭代器已前进、数据就丢了',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串和开头的空注释行'],
    ),
)
