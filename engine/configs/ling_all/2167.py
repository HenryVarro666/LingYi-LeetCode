S0 = '1100101'


def _fx(S):
    if 'pre' not in S or 'i' not in S or S.get('_line') != 8:
        return '`pre` = 前缀 `s[0..i]` 的最少耗时；剩下的后缀 `s[i+1..]` 从右端整段删，每节 1'
    i, pre, n = S['i'], S['pre'], S['n']
    return f'分割线在 `i = {i}` 右侧：`pre + (n−1−i)` = `{pre} + {n - 1 - i}` = =={pre + n - 1 - i}=='


def _col(S, k, v):
    if 'i' not in S or 'pre' not in S:
        return None
    i = S['i']
    if k == i:
        return 'blue'
    if k < i:
        return 'green'
    return 'orange'


CONFIG = dict(
    num=2167, title='移除所有载有违禁货物车厢所需要的最少时间', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='前后缀分解 · 一次遍历',
    tags=['其他线性 DP', '前后缀分解', '难度分 2219'],
    code='''
class Solution:
    def minimumTime(self, s: str) -> int:
        ans = n = len(s)
        pre = 0
        for i, ch in enumerate(s):
            if ch == '1':
                pre = min(pre + 2, i + 1)
            ans = min(ans, pre + n - 1 - i)
        return ans
''',
    call=f'Solution().minimumTime({S0!r})',
    expect=5,
    views=[
        dict(type='string', var='s', label='s（绿 = 前缀部分，蓝 = 分割线左端，橙 = 整段从右端删掉的后缀）', h=200, cell=84,
             pointers={'i': 'blue'}, color=_col),
        dict(type='text', fn=_fx, size=28, h=70),
    ],
    watch=[('i', 'i', 'blue'), ('pre', 'pre', 'green'), ('ans', 'ans', 'orange')],
    captions={
        'ans = n = len(s)': '`n = {n}`；`ans` 先设为 `n`：==整列从一端全删==，每节 1 单位',
        'pre = 0': '`pre` = 前缀 `s[0..i]` 的最少耗时，一个变量滚动就够',
        'for i, ch in enumerate(s)': '`i = {i}`，`s[{i}] = {ch}`',
        "if ch == '1'": lambda S, B, r: (f'`s[{S.i}] = 1`：这节有违禁货物，前缀里要处理它' if S.ch == '1' else f'`s[{S.i}] = 0`：没有违禁货物，`pre` ==不变=='),
        'pre = min(pre + 2, i + 1)': '`pre = min({B.pre} + 2, {i} + 1)` = =={pre}==：==单独删这节（+2）==，还是==把前 {i + 1} 节全从左端删（{i + 1}）==，取小',
        'ans = min(ans, pre + n - 1 - i)': '`ans = min({B.ans}, {pre} + {n - 1 - i})` = =={ans}==：前缀花 `{pre}`，后缀 `s[{i + 1}..]` 共 `{n - 1 - i}` 节从右端整段删',
        'return ans': '枚举完所有分割线，最少耗时 =={ret}==',
    },
    cards=dict(
        one_liner='前缀自己算，后缀整段从右端删，枚举分割线取最小',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['列车是 `0/1` 串，`1` 表示有违禁货物，要全部清掉',
                 '删最左端 1，删最右端 1，删中间任意位置 2',
                 '示例：`"1100101"` → `5`'],
        quote='计算「移除前缀 + 移除分割线左侧某些车厢 + (分割线) + 移除后缀」的最少花费。',
        quote_src='—— 灵茶山艾府题解（解法二：一次遍历）',
        idea=['枚举分割线：左半 `pre[i]`，右半 `suf[i]`，答案是两者之和的最小值',
              '`pre[i]`：`s[i] = 1` 时 `min(pre[i-1] + 2, i + 1)`，`0` 时不变',
              '把右半的中间删除合并到左半，右半只剩整段后缀删除，花费 `n−1−i`，不用 `suf` 数组'],
        summary=['时间 `O(n)`，空间 `O(1)`（解法一用 `suf` 数组是 `O(n)`）',
                 '`ans` 初值取 `n`，对应全部从一端删光',
                 '`pre` 只在 `s[i] = 1` 时变化，但 `ans` 每个 `i` 都要更新',
                 '同类前后缀分解题：238、42、2909'],
    ),
)
