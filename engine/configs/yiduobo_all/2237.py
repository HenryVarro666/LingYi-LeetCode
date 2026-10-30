CONFIG = dict(
    num=2237, title='计算街道上满足所需亮度的位置数量', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='差分数组 + 前缀和',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def meetRequirement(self, n, lights, requirement):

        f = [0] * (n + 1)
        for pos, rng in lights:
            f[max(0, pos - rng)] += 1
            f[min(n - 1, pos + rng) + 1] -= 1

        now = 0
        res = 0
        for index in range(n):
            now += f[index]
            if now >= requirement[index]:
                res += 1
        
        return res
''',
    call='Solution().meetRequirement(5, [[0,1],[2,1],[3,2]], [0,2,1,4,1])',
    expect=4,
    views=[
        dict(type='text', fn=lambda S: ('灯 `[pos, range]` 照亮 `[pos−range, pos+range]`，夹在 `[0, n−1]` 内' if 'pos' not in S else f"当前灯：`pos={S['pos']}`，`range={S['rng']}` → 照亮 `[{max(0, S['pos'] - S['rng'])}, {min(S['n'] - 1, S['pos'] + S['rng'])}]`")),
        dict(type='array', var='f', label='差分数组 f', pointers={'index': 'blue'}, h=170),
        dict(type='array', var='requirement', label='requirement（所需亮度）', pointers={'index': 'pink'}, h=170,
             color=lambda S, i, v: ('green' if S['now'] >= v else 'red') if 'index' in S and 'now' in S and i <= S['index'] else None),
        dict(type='text', fn=lambda S: (f"位置 `{S['index']}`：亮度 `now = {S['now']}`，要求 `{S['requirement'][S['index']]}`" if 'index' in S and 'now' in S else '')),
    ],
    watch=['now', ('res', 'res', 'green'), 'index'],
    captions={
        'f = [0]': '差分数组 `f` 长度 `n + 1 = {n + 1}`：多留一格，放“区间结束后的 −1”',
        'f[max(0, pos - rng)] += 1': '区间左端 `max(0, {pos} − {rng}) = {max(0, pos - rng)}`：街道有边界，不能小于 0 → `f[{max(0, pos - rng)}] += 1`',
        'f[min(n - 1, pos + rng) + 1] -= 1': '区间右端 `min({n - 1}, {pos} + {rng}) = {min(n - 1, pos + rng)}`，==右端 + 1== 处减 1 → `f[{min(n - 1, pos + rng) + 1}] -= 1`',
        'now += f[index]': '差分求前缀和：位置 `{index}` 的亮度 `now = {B.now} + {f[index]} = {now}`',
        'if now >= requirement': lambda S, B, r: (f'位置 `{S.index}`：亮度 `{S.now}` ≥ 要求 `{S.requirement[S.index]}` → ==满足==' if S.now >= S.requirement[S.index] else f'位置 `{S.index}`：亮度 `{S.now}` < 要求 `{S.requirement[S.index]}` → 不满足'),
        'res += 1': '满足数量 `res` → {res}',
        'return res': '满足要求的位置共 `{res}` 个',
    },
    cards=dict(
        one_liner='开灯问题：区间加一用差分，扫一遍前缀和',
        complexity='时间 `O(n + m)`，空间 `O(n)`（m 为灯的数量）',
        problem=['街道长 `n`（位置 `0 ~ n-1`），每盏灯 `[position, range]` 照亮 `[position−range, position+range]`',
                 '`requirement[i]` 是位置 `i` 需要的亮度（被几盏灯照到）',
                 '求亮度满足要求的位置数。示例：`n=5` → `4`'],
        quote='又是经典的开灯问题，处理方法依然是差分数组。……另外还需要特别注意本题的街道有边界，因此在计算照亮区间时需要注意不要越界。',
        quote_src='—— yiduobo 题解原文',
        idea=['一盏灯 = 区间 `[l, r]` 全部加 1 → 差分：`f[l] += 1`，`f[r+1] -= 1`',
              '`l` 取 `max(0, …)`、`r` 取 `min(n-1, …)`，防止越界',
              '最后从左到右累加 `f`，累加值就是该位置的亮度，和 `requirement` 比大小'],
        summary=['时间 `O(n + m)`，空间 `O(n)`',
                 '`f` 要开 `n + 1`：`r + 1` 最大可以到 `n`',
                 '比较用 `>=`：亮度刚好等于要求也算满足',
                 '原文为 Python 2 风格，代码无需改动',
                 '同类题：1109 航班预订统计、370 区间加法'],
    ),
)
