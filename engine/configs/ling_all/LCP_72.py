def _wl(S):
    return S['idx'] - 1 if 'idx' in S else None


def _txt(S):
    if 'idx' not in S or 'm' not in S:
        return ''
    a = S['a']
    if len(a) < 2 or S['idx'] >= len(a):
        return f'车队长度 `{len(a)}`，目标 `{S["m"]}`'
    s = a[S['idx'] - 1] + a[S['idx']]
    return f'当前最小相邻和：`a[{S["idx"]-1}] + a[{S["idx"]}] = {s}`　车队 {len(a)} 辆 → 目标 {S["m"]} 辆'


CONFIG = dict(
    num='LCP 72', title='补给马车', difficulty='Easy', category='模拟',
    author='灵茶山艾府', technique='暴力模拟 · 每轮找相邻和最小',
    code='''
class Solution:
    def supplyWagon(self, a: List[int]) -> List[int]:
        m = len(a) // 2
        while len(a) > m:
            idx = 1
            for i in range(1, len(a)):
                if a[i - 1] + a[i] < a[idx - 1] + a[idx]:
                    idx = i
            a[idx - 1] += a[idx]
            a.pop(idx)
        return a
''',
    call='Solution().supplyWagon([7,3,6,1,8])',
    expect=[10, 15],
    views=[
        dict(type='text', size=28, h=70, fn=_txt),
        dict(type='array', var='a', label='a（蓝 = 正在比较的 i，粉 = 当前最小对的右端 idx，框 = 最小对）', cell=110, h=260,
             pointers={'i': 'blue', 'idx': 'pink'}, window=(_wl, 'idx')),
    ],
    watch=[('m', 'm', 'orange'), ('idx', 'idx', 'pink'), ('i', 'i', 'blue')],
    captions={
        'm = len(a) // 2': '目标长度：原来的一半向下取整，`m = {m}`',
        'while len(a) > m': lambda S, B, r: (f'当前 `{len(S.a)}` 辆 > 目标 `{S.m}` → 还要合并一次' if len(S.a) > S.m else f'当前 `{len(S.a)}` 辆，达到目标 → 结束'),
        'idx = 1': '每轮先假设最小相邻对是 `(a[0], a[1])`，用 `idx` 记它的右端',
        'for i in range': lambda S, B, r: ('这一轮枚举完了，`idx = ' + str(S.idx) + '` 就是最小对的右端' if 'i' in B and B.i == S.i else f'枚举相邻对 `(a[{S.i - 1}], a[{S.i}])`'),
        'if a[i - 1]': lambda S, B, r: (f'`a[{S.i-1}] + a[{S.i}] = {S.a[S.i-1] + S.a[S.i]}`，当前最小 `{S.a[S.idx-1] + S.a[S.idx]}` → ' + ('==更小==，换' if S.a[S.i-1] + S.a[S.i] < S.a[S.idx-1] + S.a[S.idx] else '不更小（并列也不换，保住编号小的）')),
        'idx = i': '更小，`idx` 更新为 `{idx}`',
        'a[idx - 1] += a[idx]': '把右边那辆并入左边：`a[{idx-1}]` = `{B.a[idx-1]} + {B.a[idx]}` = =={a[idx-1]}==',
        'a.pop(idx)': '删掉右边那辆，车队剩 `{len(a)}` 辆',
        'return a': '车队长度达标，返回 `{a}`',
    },
    cards=dict(
        one_liner='每轮扫一遍找相邻和最小的一对，合并到左边再删右边',
        complexity='时间 `O(n^2)`，空间 `O(1)`',
        problem=['`supplies[i]` 是第 i 辆马车的物资，目标是把车队长度减半（向下取整）',
                 '每次合并物资之和最小的相邻两辆；并列取编号最小的',
                 '示例：`[7,3,6,1,8]` → `[10,15]`'],
        quote='不断循环，每次找到相邻和最小的 `a[i-1]` 和 `a[i]`，然后把 `a[i-1]` 增加 `a[i]`，并去掉 `a[i]`。',
        quote_src='—— 灵茶山艾府题解',
        idea=['数据范围只有 1000，每轮 `O(n)` 扫一遍，共 `n/2` 轮，暴力够用',
              '`idx` 记最小对的右端点，比较用 `<` 而不是 `<=`，==并列时保留靠前的==',
              '合并 = 左边加右边，再 `pop` 掉右边'],
        summary=['时间 `O(n^2)`，空间 `O(1)`（原地修改 `a`）',
                 '`idx` 从 1 开始，`i` 也从 1 开始：相邻对至少要有两个元素',
                 '并列取编号最小：必须用严格 `<`',
                 '`a.pop(idx)` 本身是 `O(n)`，不影响总复杂度'],
    ),
)
