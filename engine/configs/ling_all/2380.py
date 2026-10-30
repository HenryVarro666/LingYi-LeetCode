CONFIG = dict(
    num=2380, title='二进制字符串重新安排顺序需要的时间', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='把 1 看成车 · 线性 DP',
    tags=[],
    code='''
class Solution:
    def secondsToRemoveOccurrences(self, s: str) -> int:
        f = pre0 = 0
        for c in s:
            if c == '0': pre0 += 1
            elif pre0: f = max(f + 1, pre0)  # 前面有 0 的时候才会移动
        return f
''',
    call='Solution().secondsToRemoveOccurrences("0110101")',
    expect=4,
    views=[
        dict(type='string', var='s', label='s（1 = 车，0 = 空位；车往左开）', h=200),
        dict(type='text', h=110, size=34, fn=lambda S: f"前面的 0 有 `{S['pre0']}` 个，最后一辆车要 =={S['f']}== 秒" if 'pre0' in S else ''),
    ],
    watch=[('c', 'c', 'blue'), ('pre0', 'pre0', 'pink'), ('f', 'f', 'green')],
    captions={
        'f = pre0 = 0': '`f`：前面的车都到位需要的秒数；`pre0`：前面 0 的个数',
        'for c in s': '看下一个字符 `c = {c}`',
        "if c == '0'": lambda S, B, r: ("遇到 `0`：路上多一个空位，`pre0` 加 1" if S.c == '0' else "遇到 `1`：这是一辆车"),
        'elif pre0': lambda S, B, r: (f'这辆车前面有 `{B.pre0}` 个 0 → ==要移动==：至少 `pre0` 秒，被前车堵住则是 `f + 1`，取大：`f = max({B.f} + 1, {B.pre0}) = {S.f}`'
                                       if B.pre0 else '这辆车前面没有 0，原地不动，`f` 不变'),
        'return f': '最后一辆车到位用了 `{f}` 秒',
    },
    cards=dict(
        one_liner='1 是车往左开，每辆车到位时间取 max(前车+1, 前面0的个数)',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每一秒所有 `"01"` 同时变成 `"10"`，直到没有 `"01"`',
                 '求需要的秒数',
                 '示例：`"0110101"` → `4`'],
        quote='把 s 看成是一条道路，1 看成车，替换操作看成是车往左移动（如果左侧为 0 的话）。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`f` 表示前面所有车到位的秒数，`pre0` 是前面 0 的个数',
              '车自己要走过 `pre0` 个 0，至少 `pre0` 秒',
              '若被前车堵住，则前车到位后下一秒才能到位：`f + 1`'],
        summary=['时间 `O(n)`，空间 `O(1)`（`f` 和 `pre0` 都压缩成变量）',
                 '易错：只有前面有 0 时车才会动，`elif pre0` 不能漏',
                 '转移：`f = max(f + 1, pre0)`'],
    ),
)
