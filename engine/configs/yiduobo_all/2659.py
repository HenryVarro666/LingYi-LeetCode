CONFIG = dict(
    num=2659, title='将数组清空', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='头指针循环移动 + 树状数组区间和',
    tags=['树状数组', '难度分 2282'],
    code='''
class Solution(object):
    def countOperationsToEmptyArray(self, nums):

        n = len(nums)
        f = [0] * (n + 1)

        def add(x, delta):
            while x <= n:
                f[x] += delta
                x += x & -x

        def get(x):
            s = 0
            while x > 0:
                s += f[x]
                x -= x & -x
            return s

        for index in range(1, n + 1):
            add(index, 1)
        
        now = 0
        res = 0
        for index, _ in sorted(enumerate(nums), key=lambda d:d[1]):
            index += 1
            if now < index:
                res += get(index) - get(now)
            else:
                res += get(n) - get(now) + get(index)

            add(index, -1)
            now = index
        
        return res
''',
    call='Solution().countOperationsToEmptyArray([2,4,1,3])',
    expect=8,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 头指针所在，黄 = 目标位置）',
             color=lambda S, i, v: ('blue' if i == S['now'] - 1 else 'yellow' if i == S['index'] - 1 else None) if 'now' in S else None, h=210),
        dict(type='array', var='f', label='f：树状数组，下标 1..n（存活的位置记 1，删了减 1）', h=190),
        dict(type='text', fn=lambda S: (f"头指针 now = {S['now']}，目标位置 index = {S['index']}（下标从 1 数）" + ('：目标在后方，直接向后走' if S['now'] < S['index'] else '：目标在前方，先走到末尾再从头走') if 'now' in S and 'index' in S else '先给每个位置记 1（都还存在）'), h=70),
    ],
    watch=['now', 'index', ('res', 'res', 'green')],
    captions={
        'f = [0]': '树状数组 `f`，下标 1..n；位置存活记 1，所以区间和 = 区间内还剩几个数',
        'add(index, 1)': '位置 `{index}` 记为 1（还在）',
        'now = 0': '头指针 `now` 从最前面（0）出发',
        'res = 0': '`res` 累计移动 + 删除的次数',
        'for index, _ in sorted': '按值从小到大依次删；`index = {index}` 是原下标',
        'index += 1': '下标改成从 1 开始：`index = {index}`',
        'if now < index': lambda S, B, r: (f'`now = {S.now} < index = {S.index}`：目标在后方，直接向后走' if S.now < S.index else f'`now = {S.now} >= index = {S.index}`：目标在前方，要先走到末尾再绕回来'),
        'res += get(index) - get(now)': '后方：经过的数 = `get({index}) - get({now})`（含目标自己）→ 走过去再删，`res` = =={res}==',
        'res += get(n) - get(now) + get(index)': '前方：`get(n)-get(now)`（走到末尾）+ `get(index)`（从头走到目标）→ `res` = =={res}==',
        'add(index, -1)': '删掉位置 `{index}`：它在树状数组里减 1',
        'now = index': '头指针移到 `{index}`，继续找下一个最小值',
        'return res': '一共 `{res}` 次操作',
        'f[x] += delta': '`f[{x}]` 加 `{delta}`',
        'x += x & -x': '`x += x & -x` → {x}',
        's += f[x]': '`s += f[{x}]` → {s}',
        'x -= x & -x': '`x -= x & -x` → {x}',
        'return s': '前缀和 `{s}`',
    },
    skip=['while x', 's = 0', 'def '],
    max_steps=80,
    cards=dict(
        one_liner='把「挪到末尾」看成头指针绕圈，走过的数 = 区间内剩余个数',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['数组互不相同；队首是最小值就删，否则挪到末尾',
                 '问：清空要多少次操作',
                 '本视频：`[2,4,1,3]` → `8`'],
        quote='不妨换一个视角，从移动数组直到合适的数来到数组头部，改成不断向后循环移动数组头部指针直到来到待删除的下一个数。',
        quote_src='—— yiduobo 题解原文',
        idea=['按值从小到大删，头指针 `now` 走到目标 `index`',
              '目标在后方：走过的数 = `get(index) - get(now)`；在前方：`get(n)-get(now)+get(index)`',
              '存活记 1、删除记 0，区间和就是剩余个数 → 树状数组；这个差值已含删除那一步，所以不用再 +1'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '前缀和之差多算了目标自己一次，恰好抵掉「删除」这一步操作',
                 '排序要带原下标：`sorted(enumerate(nums), key=...)`',
                 '对比灵神：灵神只数相邻删除位置是否「回头」，不需要树状数组',
                 '原文代码无需改动即可在 Python 3 运行'],
    ),
)
