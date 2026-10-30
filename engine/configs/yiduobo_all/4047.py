NUMS = [1, 2, 4, 4, 5]


def _f8(S):
    f = S.get('f')
    return None if f is None else list(f[:8])


def _fcol(S, i, v):
    if 'y' in S and S.get('_line') in (28, 29, 30) and i == S['y']:
        return 'yellow'
    if 'xor' in S and i == S['xor'] and v != -1:
        return 'green'
    return None


def _txt(S):
    if 'f' not in S:
        return '目标：选一些不同的数，让它们的异或 ==等于整个数组的异或==；选了几个数，就要几次操作'
    return f'整个数组异或 `xor = {S["xor"]}`；`f[x]`：用最少几个不同的数异或出 `x`；BFS 每一轮多用一个数'


CONFIG = dict(
    num=4047, title='使所有元素的异或为零所需的最小操作次数', difficulty='Medium', category='位运算',
    author='yiduobo', technique='BFS（子集异或最少用几个数）',
    code='''
class Solution(object):
    def minOperations(self, nums):
        
        

        xor = 0
        for v in nums:
            xor ^= v
        
        if xor == 0:
            return 0

        if max(nums) == min(nums):
            return -1
        
        f = [-1] * 2048
        f[0] = 0
        q = [0]
        head, tail = 0, 1
        distinct_nums = list(set(nums))
        while head < tail:
            for x in q[head : tail]:
                for v in distinct_nums:
                    y = x ^ v
                    if f[y] == -1:
                        f[y] = f[x] + 1
                        q.append(y)

            head, tail = tail, len(q)
        
        if f[xor] == len(nums):
            return -1
        return f[xor]
''',
    call=f'Solution().minOperations({NUMS})',
    expect=2,
    skip=['for v in nums', 'distinct_nums = ', 'q = [0]', 'head, tail = 0, 1', 'while head < tail', 'for x in q[head', 'for v in distinct_nums', 'y = x ^ v', 'q.append(y)',
          'f = [-1]', 'if max(nums)'],
    views=[
        dict(type='text', fn=_txt, size=22, h=64),
        dict(type='array', var='nums', label='nums', h=170, cell=84),
        dict(type='array', var=_f8, label='f[x]（下标 = 异或值；-1 = 还没出现；黄 = 正在更新，绿 = 目标 xor）', h=210, cell=84,
             pointers={'x': 'blue', 'y': 'yellow', 'xor': 'pink'}, color=_fcol),
        dict(type='array', var='q', label='BFS 队列 q（按轮次：先用 1 个数能凑出的，再 2 个数的……）', h=170, cell=60),
    ],
    watch=['xor', 'x', 'v', 'y', 'head', 'tail'],
    max_steps=80,
    captions={
        'xor ^= v': '全部异或：`xor` = {xor}',
        'if xor == 0': lambda S, B, r: ('一开始异或就是 0，不用操作 → 返回 0' if S.xor == 0 else f'`xor = {S.xor}` ≠ 0，需要操作'),
        'return 0': '直接返回 0',
        'if f[y] == -1': lambda S, B, r: (f'`{S.x} ^ {S.v}` = `{S.y}`：第一次出现 → 用的数比 `f[{S.x}]` 多一个，`f[{S.y}] = {S.f[S.x] + 1}`' if S.f[S.y] == -1
                                           else f'`{S.x} ^ {S.v}` = `{S.y}`：已经有 `f[{S.y}] = {S.f[S.y]}` 次的方法了，BFS 先到的更少 → 跳过'),
        'f[y] = f[x] + 1': '`f[{y}] = f[{x}] + 1` = =={f[y]}==，并把 `{y}` 放进队列 `q`',
        'head, tail = tail, len(q)': '这一轮结束：本轮新凑出的值是 `q[{head}:{tail}]`，下一轮从它们继续（为空就结束）',
        'if f[xor] == len(nums)': '`f[xor] = {f[xor]}`：用 {f[xor]} 个数的异或能抵消总异或，要 {f[xor]} 次操作',
        'return -1': '`f[xor]` 恰好等于 `len(nums)`：所有数都得用，没有可以保留的元素 → 做不到，返回 -1',
        'return f[xor]': '答案：=={ret}==',
    },
    cards=dict(
        one_liner='操作的本质：挑一个不同元素子集，其异或等于总异或',
        complexity='时间 `O(V·d)`（`V=2048` 个异或值，`d` 个不同元素），空间 `O(V)`',
        problem=['每次选两个值不同的元素，把其中一个换成它们的异或',
                 '求最少操作次数使整个数组异或为 0；做不到返回 -1',
                 '本视频：`nums=[1,2,4,4,5]` → `2`（异或 = 6 = 2 ^ 4）'],
        quote='本题实际上就是要找出一个最小的子集，满足这个子集中元素的异或值恰好等于整个数组的元素的异或值，然后通过操作将这些元素对异或值的影响抹掉。',
        quote_src='—— yiduobo 题解原文',
        idea=['先判边界：总异或为 0 返回 0；所有元素相同又没法操作 → -1',
              '重复元素没意义，只看不同元素：选若干个让异或恰好等于总异或',
              'BFS 从 0 出发，每轮异或上一个不同元素，`f[x]` 记最少用几个'],
        summary=['时间 `O(2048·d)`，`d` 是不同元素个数，空间 `O(2048)`',
                 '`f[xor] == len(nums)` 时每个元素都要被用掉，做不到 → -1',
                 '先判 `xor == 0` 与「元素全相同」两个边界',
                 '原文为 Python 2 风格，本题无需改动即可在 Python 3 运行',
                 '题面库里没有，题意按 yiduobo 原文复述；答案已用暴力搜索核对过'],
    ),
)
