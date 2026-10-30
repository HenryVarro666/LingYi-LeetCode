def _pair_color(S, i, v):
    a, b = S['s1'][i], S['s2'][i]
    if a == b:
        return None
    return 'blue' if a == 'x' else 'pink'


CONFIG = dict(
    num=1247, title='交换字符使得字符串相同', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='只数不同位 · xy / yx 配对',
    tags=['贪心算法', '思维题', '难度分 1597'],
    code='''
class Solution:
    def minimumSwap(self, s1: str, s2: str) -> int:
        cnt = Counter(x for x, y in zip(s1, s2) if x != y)
        d = cnt['x'] + cnt['y']
        return -1 if d % 2 else d // 2 + cnt['x'] % 2
''',
    call='Solution().minimumSwap("xxxyx", "yyyxx")',
    expect=3,
    views=[
        dict(type='string', var='s1', h=170, label='s1（蓝 = s1 为 x、s2 为 y；粉 = s1 为 y、s2 为 x）', color=_pair_color),
        dict(type='string', var='s2', h=170, label='s2', color=_pair_color),
        dict(type='map', var='cnt', h=200, label='cnt：不同位置里 s1 的字符（x → “xy”对，y → “yx”对）', fmt=lambda k, v: f'{k} : {v}'),
        dict(type='text', size=34, h=80, fn=lambda S: f"不同的位置共 `d = {S['d']}` 个" if 'd' in S else ''),
    ],
    watch=['cnt', 'd'],
    captions={
        'cnt = Counter': '只看 s1、s2 不同的位置，按 s1 的字符计数：`x` 型（s1=x, s2=y）有 =={cnt["x"]}== 个，`y` 型（s1=y, s2=x）有 =={cnt["y"]}== 个',
        'd = cnt': '不同位置总数 `d = {cnt["x"]} + {cnt["y"]}` = =={d}==',
        'return': lambda S, B, ret: (f"`d = {S.d}` 是奇数：无解 → ==-1==" if S.d % 2 else
            f"`d // 2 = {S.d // 2}` 次配对交换，再加 `cnt['x'] % 2 = {S.cnt['x'] % 2}` 次转换 = =={ret}=="),
    },
    cards=dict(
        before=[dict(heading='先把不同的位置分成两型', lines=[
            '相同的位置（如 `x` 对 `x`）完全不用动，只看==不同的位置==',
            '`xy` 型：`s1` 是 x、`s2` 是 y；`yx` 型：反过来',
            '两个 `xy` 型：交换第一个的 `s1` 和第二个的 `s2`，==一次修好两个==；两个 `yx` 型同理',
            '一个 `xy` 加一个 `yx`：要先转换一次，再修好，共 ==2 次=='])],
        after=[dict(heading='为什么这样配对最优', lines=[
            '偶数 + 偶数：每次交换让 `d` 减 2，这是单次操作的极限',
            '奇数 + 奇数：多交换一次，就变成偶数 + 偶数，这一次是必要的',
            '所以不需要相同位置的字母参与交换',
            '`d` 为奇数：`x` 的总数是奇数，无解'])],
        one_liner='只看不同的位置，xy 配 xy、yx 配 yx，每次消两个',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`s1`、`s2` 只含 `x`、`y`，每次交换 `s1` 的一个字符和 `s2` 的一个字符',
                 '求使两串相同的最少交换次数，不可能则返回 `-1`',
                 '示例：`"xy","yx"` → `2`'],
        quote='对于不同的字母，这种做法是尽量「内部消化」。对于偶数+偶数的情况，每次交换操作都使 d 减二，这是单次操作的极限。',
        quote_src='—— 灵茶山艾府题解',
        idea=['相同位置不用管，只统计不同位置：`xy` 型（s1 是 x）和 `yx` 型（s1 是 y）的个数',
              '同型两个一组，交换一次就能同时修好（如 `xy`、`xy` 交换 s1[i] 与 s2[j]）',
              '两型各剩一个时，需要 ==2 次==；`d` 为奇数时无解'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`d` 是奇数就是 `-1`：x 的总数必须是偶数才能平分',
                 '答案 `d // 2 + cnt["x"] % 2`：奇数+奇数时多一次转换，之后变成偶数+偶数',
                 '思考题：多于两种字符的情形要怎么做？'],
    ),
)
