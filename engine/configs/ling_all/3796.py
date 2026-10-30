def _txt(S, B):
    ln = S.get('_line', 0)
    a, mv, df = S.get('a'), S.get('max_val'), S.get('diff')
    if ln == 9 and 'd' in S:
        i, d = S['i'], S['d']
        return f"`a[{i + 1}] = min(a[{i}] + {d}, max_val[{i + 1}])` = `min({a[i]} + {d}, {mv[i + 1]})` = =={a[i + 1]}=="
    if ln == 11:
        i = S['i']
        old = B['a'][i] if 'a' in B else a[i]
        return f"`a[{i}] = min(a[{i}], a[{i + 1}] + diff[{i}])` = `min({old}, {a[i + 1]} + {df[i]})` = =={a[i]}=="
    return '先从左往右尽量拉满，再从右往左把被突然压低的限制传回去'


def _col_a(S, i, v):
    ln = S.get('_line', 0)
    if 'i' not in S:
        return None
    if ln in (8, 9) and 'd' in S and i == S['i'] + 1:
        return 'green'
    if ln in (10, 11) and 'd' in S:
        if i == S['i']:
            return 'blue'
        if i == S['i'] + 1:
            return 'pink'
    return None


CONFIG = dict(
    num=3796, title='找到带限制序列的最大值', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='两次扫描 · 先拉满再回传',
    tags=['灵神题单', '难度分 1833'],
    code='''
class Solution:
    def findMaxVal(self, n: int, restrictions: List[List[int]], diff: List[int]) -> int:
        max_val = [inf] * n
        for i, mx in restrictions:
            max_val[i] = mx

        a = [0] * n
        for i, d in enumerate(diff):
            a[i + 1] = min(a[i] + d, max_val[i + 1])
        for i in range(n - 2, 0, -1):
            a[i] = min(a[i], a[i + 1] + diff[i])
        return max(a)
''',
    call='Solution().findMaxVal(10, [[3,1],[8,1]], [2,2,3,1,4,5,1,1,2])',
    expect=6,
    views=[
        dict(type='text', fn=_txt, size=24, h=70),
        dict(type='array', var='max_val', h=170, label='max_val[i]：位置 i 的上限（inf = 没限制）'),
        dict(type='bars', var='a', h=340, label='a[i]', color=_col_a),
    ],
    watch=['i', 'mx', 'd', ('max(a)', 'max(a)', 'green')],
    captions={
        'max_val = [inf]': '`max_val[i]` = 位置 `i` 的上限，没限制就是 `inf`',
        'for i, mx in restrictions': '读入限制：`[{i}, {mx}]`',
        'max_val[i] = mx': '`max_val[{i}] = {mx}`：`a[{i}]` 不能超过 `{mx}`',
        'a = [0] * n': '`a[0] = 0` 固定，其余先置 0',
        'for i, d in enumerate': lambda S, B, r: ('第一遍结束：`a[n-1]` 已是它能达到的最大值' if B.get('i') == S['i'] and S['i'] == len(S['diff']) - 1 else f"第一遍（左→右）：`i = {S['i']}`，`diff[{S['i']}] = {S['d']}`"),
        'a[i + 1] = min': lambda S, B, r: (f"拉满：`a[{S['i'] + 1}] = min(a[{S['i']}] + {S['d']}, max_val[{S['i'] + 1}])` = =={S['a'][S['i'] + 1]}=="
                                             + ('，被上限压低了' if S['max_val'][S['i'] + 1] < S['a'][S['i']] + S['d'] else '')),
        'for i in range(n - 2': lambda S, B, r: ('第二遍结束：`a[1..n-2]` 都已满足 `diff`' if B.get('i') == S['i'] == 1 else f"第二遍（右→左）：修正 `a[{S['i']}]`"),
        'a[i] = min': lambda S, B, r: (
            f"`a[{S['i']}]` 不能比右边的 `a[{S['i'] + 1}] + diff[{S['i']}] = {S['a'][S['i'] + 1] + S['diff'][S['i']]}` 大：" +
            (f"需要压低 `{B.a[S['i']]}` → =={S['a'][S['i']]}==" if B.a[S['i']] != S['a'][S['i']] else f"本来就是 `{S['a'][S['i']]}`，不变")),
        'return max(a)': '`max(a)` = =={ret}==',
    },
    cards=dict(
        one_liner='每个位置先拉满，被限制压低的再从右往左回传',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['构造长度 `n` 的序列 `a`：`a[0]=0`、非负、`|a[i]−a[i+1]| ≤ diff[i]`，且 `a[idx] ≤ maxVal`（restrictions）',
                 '求序列中最大值的最大可能值',
                 '示例：`n=10, restrictions=[[3,1],[8,1]], diff=[2,2,3,1,4,5,1,1,2]` → `6`'],
        quote='第一次扫描，从左到右。如果没有 maxVal[i] 的限制，那么拉满，即 a[i+1] = a[i] + diff[i] 是最优的。但这不能超过 maxVal[i+1]。',
        quote_src='—— 灵茶山艾府题解',
        idea=['第一遍从左往右：`a[i+1] = min(a[i] + diff[i], max_val[i+1])`，只考虑左边传来的约束',
              '但被突然压低的位置，会让它左边的数「离得太远」，违反 `diff`',
              '第二遍从右往左，用 `a[i+1] + diff[i]` 取 `min` 把 `a[i]` 压回来，只会变小，不破坏第一遍的约束'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '第一遍结束时 `a[n-1]` 已是最大值，因为 `0..n-2` 的限制都传过来了',
                 '第二遍从 `n-2` 到 `1`：`a[0]=0` 是固定值不能改',
                 '易错：第二遍只能取 `min`（变小），变大会违反第一遍的约束',
                 '相似题：1840 最高建筑高度（`diff = 1`，`n` 到 `10^9`）'],
    ),
)
