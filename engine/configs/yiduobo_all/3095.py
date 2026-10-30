def _bits(S):
    if 'freq' not in S:
        return ''
    f = S['freq']
    on = [f'第{t}位×{f[t]}' for t in range(6) if f[t]]
    return f"窗口各位上 1 的个数：{'，'.join(on) if on else '全为 0'}　｜　或值 `now` = `{S.get('now', 0):06b}` = =={S.get('now', 0)}==，k = `{S['k']}`"


CONFIG = dict(
    num=3095, title='或值至少为 K 的最短子数组 I', difficulty='Easy', category='位运算',
    author='yiduobo', technique='滑动窗口 + 数位计数',
    tags=[],
    code='''
class Solution(object):
    def minimumSubarrayLength(self, nums, k):

        freq = [0] * 30
        p = 0
        now = 0
        res = -1
        for index, v in enumerate(nums):
            if p == index:
                now = v
                p += 1
                for t in range(30):
                    if v & (1 << t) == (1 << t):
                        freq[t] += 1

            while p < len(nums) and now < k:
                now |= nums[p]
                for t in range(30):
                    if nums[p] & (1 << t) == (1 << t):
                        freq[t] += 1
                p += 1
            
            if now < k:
                break

            if res == -1 or res > p - index:
                res = p - index
            
            for t in range(30):
                if nums[index] & (1 << t) == (1 << t):
                    freq[t] -= 1
                    if freq[t] == 0:
                        now ^= (1 << t)
        
        return res
''',
    call='Solution().minimumSubarrayLength([2,1,8,4,3], 10)',
    expect=2,
    views=[
        dict(type='text', fn=_bits, size=24, h=70),
        dict(type='array', var='nums', pointers={'index': 'blue', 'p': 'pink'},
             window=('index', 'p - 1'), h=250,
             dim=lambda S, i, v: 'index' in S and not (S['index'] <= i < S['p'])),
    ],
    watch=[('index', 'index', 'blue'), ('p', 'p', 'pink'), 'now', 'k', ('res', 'res', 'green')],
    skip=['for t in range(30)', 'if v & (1 << t)', 'if nums[p] & (1 << t)', 'if nums[index] & (1 << t)'],
    max_steps=90,
    captions={
        'freq = [0]': '`freq[t]` 记录窗口里第 t 位上有几个 1',
        'if p == index': '`p == index`？窗口为空，要先放一个数进来',
        'now = v': '窗口只有 `{v}`，或值 `now = {now}`',
        'freq[t] += 1': '第 `{t}` 位是 1 → `freq[{t}]` 变成 =={freq[t]}==',
        'while p < len(nums) and now < k': lambda S, B, r: (
            f'`now = {S.now} < k = {S.k}` 且右边还有数 → ==继续扩右边界==' if S.p < len(S.nums) and S.now < S.k
            else (f'`now = {S.now} ≥ k = {S.k}` → 够了，不再扩' if S.now >= S.k else '右边没数可扩了')),
        'now |= nums[p]': '把 `nums[{p}]` 并进来：`now |= {nums[p]}` → =={now}==',
        'p += 1': '右边界 `p` → {p}（窗口是 `[index, p)`）',
        'if now < k': lambda S, B, r: (f'`now = {S.now} < k`：扩到头也不够，后面更不可能 → ==结束==' if S.now < S.k
                                       else f'`now = {S.now} ≥ k = {S.k}`：当前窗口合格'),
        'if res == -1 or res > p - index': '窗口长度 `p - index = {p - index}`，和 `res = {B.res}` 比，更短才更新',
        'res = p - index': '`res` 更新为 =={res}==',
        'freq[t] -= 1': '左端 `nums[{index}]` 出窗口，第 `{t}` 位计数 -1 → `freq[{t}] = {freq[t]}`',
        'if freq[t] == 0': lambda S, B, r: (f'`freq[{S.t}] == 0`：窗口里这一位再没有 1' if S.freq[S.t] == 0 else f'`freq[{S.t}] = {S.freq[S.t]}`：窗口里还有别的数带这一位 → 或值不变'),
        'now ^= (1 << t)': '这一位 ==计数清零==，窗口里再没有 1 → 或值 `now` 去掉这一位 → {now}',
        'return res': '最短特别子数组长度 `{res}`',
    },
    cards=dict(
        one_liner='滑动窗口 + 每一位上 1 的个数，或值才能“删”',
        complexity='时间 `O(30n)`，空间 `O(30)`',
        problem=['`nums` 非负，`k` 为整数；子数组的按位或 ≥ `k` 就“特别”',
                 '求最短特别子数组的长度，没有就 `-1`',
                 '示例：`[2,1,8], k=10` → `3`；本视频：`[2,1,8,4,3], k=10` → `2`'],
        quote='若当前窗口内元素的或值小于k，就不断向右扩展窗口右边界……我在这里使用了一个哈希表来记录窗口内每种位上有多少个1',
        quote_src='—— yiduobo 题解原文',
        idea=['或运算只增不减：窗口不够就==右扩==，够了就记长度、左缩',
              '或没法“撤销”一个数 → 记每一位有多少个 1',
              '左端出窗时某一位计数归零，才把这一位从 `now` 里去掉'],
        summary=['时间 `O(30n)`，空间 `O(30)`；数据规模很小，暴力也能过',
                 '`if p == index`：窗口被缩空时要先放一个数进来',
                 '`now < k` 说明扩到数组末尾也不够，直接 `break`',
                 '原文就是 Python 3 可运行写法，未做修改'],
    ),
)
