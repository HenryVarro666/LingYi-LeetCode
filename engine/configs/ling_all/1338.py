CONFIG = dict(
    num=1338, title='数组大小减半', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='出现次数从大到小 · 前缀和',
    tags=['贪心与思维', '难度分 1303'],
    code='''
class Solution:
    def minSetSize(self, arr: List[int]) -> int:
        cnt = sorted(Counter(arr).values(), reverse=True)
        m = len(arr) // 2
        for i, s in enumerate(accumulate(cnt)):
            if s >= m:
                return i + 1
''',
    call='Solution().minSetSize([3,3,3,3,5,5,5,2,2,7])',
    expect=2,
    views=[
        dict(type='array', var='arr', label='arr', cell=70, h=150),
        dict(type='array', var='cnt', label='cnt（每个数的出现次数，从大到小）', cell=100, h=210,
             pointers={'i': 'blue'},
             color=lambda S, i, v: ('green' if 'i' in S and i <= S['i'] else None),
             dim=lambda S, i, v: 'i' in S and i > S['i']),
        dict(type='text', h=90, size=30,
             fn=lambda S: (f"已删 `s = {S['s']}` 个，目标 `m = {S['m']}`，已选 =={S['i'] + 1}== 个数" if 's' in S else
                           (f"目标：至少删掉 `m = {S['m']}` 个" if 'm' in S else ''))),
    ],
    watch=[('i', 'i', 'blue'), ('s', 's', 'green'), ('m', 'm', 'orange')],
    captions={
        'cnt = sorted': '统计每个数的出现次数并从大到小排：`cnt = {cnt}`——先删出现多的，每个数能删得最多',
        'm = len(arr)': '至少要删掉一半：`m = {m}`',
        'for i, s in enumerate(accumulate(cnt))': '`s` = 前 `{i + 1}` 种数的出现次数之和 = =={s}==，也就是删了这么多个',
        'if s >= m': lambda S, B, r: (f'`s = {S.s} ≥ m = {S.m}`：已经删掉一半以上，不用再选了' if S.s >= S.m
                                      else f'`s = {S.s} < m = {S.m}`：还不够一半，再多选一个数'),
        'return i + 1': '一共选了 `i + 1` = =={ret}== 个数',
    },
    cards=dict(
        one_liner='先删出现次数最多的数，删得最快，选的数最少',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['选一个整数集合，删掉它们在数组中的==所有出现==',
                 '要求至少删掉一半元素，集合要尽量小',
                 '本视频：`[3,3,3,3,5,5,5,2,2,7]` → `2`（选 3 和 5）'],
        quote='1. 用哈希表（或者数组）统计每个元素的出现次数。2. 把出现次数从大到小排序，得到 cnt 数组。3. 遍历 cnt，计算前缀和 s，直到 s ≥ n/2 为止，返回此时的下标加一。',
        quote_src='—— 灵茶山艾府题解',
        idea=['删一个数就删掉它的全部出现，所以关心的只是每种数的==出现次数==',
              '次数越大，一个数删得越多 → 从大到小依次选',
              '前缀和第一次到达 `n/2`，此时选了几个数就是答案'],
        summary=['时间 `O(n log n)`，瓶颈在排序；空间 `O(n)`',
                 '题目保证 `n` 是偶数，所以 `m = len(arr) // 2` 没有取整问题',
                 '易错：只统计次数，不用关心具体是哪个数；返回的是下标 + 1',
                 '数组写法：`cnt = [0] * (max(arr) + 1)` 计数后排序，复杂度 `O(n + U log U)`，思路相同'],
    ),
)
