S0 = 'abcb'


def _bal(S):
    idx, pre = S.get('index'), S.get('pre')
    if idx is None or pre is None or 'freq' not in S:
        return None
    return S['ma'] * len(S['freq']) == idx - pre


def _sc(S, k, v):
    idx, pre = S.get('index'), S.get('pre')
    if idx is None:
        return None
    if pre is not None and S.get('_line') in (11, 13, 14) and pre <= k < idx:
        return 'green' if (S.get('_line') in (13, 14) and _bal(S)) else 'yellow'
    return 'blue' if k == idx - 1 else None


def _fc(S, k, v):
    idx, pre = S.get('index'), S.get('pre')
    if idx is None:
        return None
    if k == idx:
        return 'yellow'
    if pre is not None and S.get('_line') in (13, 14) and k == pre and _bal(S):
        return 'green'
    return None


def _formula(S):
    idx, pre = S.get('index'), S.get('pre')
    if idx is None:
        return '`f[i]` = 前 `i` 个字符最少分成几个平衡子串，`f[0] = 0`'
    if pre is not None and S.get('_line') in (11, 13, 14) and 'freq' in S:
        L, k, m = idx - pre, len(S['freq']), S['ma']
        if S.get('_line') == 11:
            return f'子串 `s[{pre}:{idx}] = "{S["s"][pre:idx]}"`：把 `{S["s"][pre]}` 计入 `freq`'
        return f'最大次数 `{m}` × 种类 `{k}` = `{m * k}`，子串长 `{L}` → ' + ('==相等，平衡==' if m * k == L else '不等，不平衡')
    return f'求 `f[{idx}]`：先按「最后一个字符单独成段」，再往左枚举分割点 `pre`'


CONFIG = dict(
    num=3144, title='分割字符频率相等的最少子字符串', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='线性 DP：枚举分割点 + 哈希表计数',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1917'],
    code='''
class Solution(object):
    def minimumSubstringsInPartition(self, s):
        n = len(s)
        f = [0] * (n + 1)
        for index in range(1, n + 1):
            f[index] = f[index - 1] + 1
            freq = Counter()
            ma = 0
            for pre in range(index - 1, -1, -1):
                char = s[pre]
                freq[char] += 1
                ma = max(ma, freq[char])
                if ma * len(freq) == index - pre:
                    f[index] = min(f[index], f[pre] + 1)
        return f[-1]
''',
    call=f'Solution().minimumSubstringsInPartition({S0!r})',
    expect=2,
    skip=['for pre in range', 'ma = 0', 'char = s[pre]', 'ma = max'],
    max_steps=80,
    views=[
        dict(type='string', var='s', label='s（蓝 = 第 index 个字符，黄 = 当前子串 s[pre:index]，绿 = 平衡）', h=190, cell=70, pointers={'pre': 'pink'}, color=_sc),
        dict(type='map', var='freq', label='freq：子串里每个字符的出现次数', h=100, fmt=lambda k, v: f'{k}: {v}'),
        dict(type='text', fn=_formula, size=25, h=60),
        dict(type='array', var='f', label='f[i]（黄 = 正在更新的 f[index]，绿 = 平衡时用到的 f[pre]）', h=170, cell=70, color=_fc),
    ],
    watch=[('index', 'index', 'blue'), ('pre', 'pre', 'pink'), ('ma', 'ma', 'yellow'), ('f[-1]', 'f[-1]', 'green')],
    captions={
        'n = len(s)': '`n = {n}`',
        'f = [0] * (n + 1)': '`f[0] = 0`：空串不需要子串；`f[i]` 对应前 `i` 个字符',
        'for index in range': lambda S, B, r: (f'`index = {S.index}`：计算前 `{S.index}` 个字符，即 `s[0:{S.index}]`' if S.get('index') != B.get('index')
                                               else '所有前缀都算完了'),
        'f[index] = f[index - 1] + 1': '保底：最后一个字符 `{s[index-1]}` 单独成段（单个字符一定平衡）：`f[{index}] = f[{index-1}] + 1` = =={f[index]}==',
        'freq = Counter()': '新开计数器；`ma = 0` 记录次数的最大值。从 `index-1` 往左枚举分割点 `pre`',
        'freq[char] += 1': '子串向左扩一格，把 `s[{pre}] = {s[pre]}` 计入：现在子串是 `s[{pre}:{index}] = "{s[pre:index]}"`',
        'if ma * len(freq)': lambda S, B, r: (f'`ma × 种类` = `{S.ma} × {len(S.freq)}` = {S.ma * len(S.freq)}，子串长 `{S.index - S.pre}` → ==相等==，每种字符出现次数一样，平衡'
                                              if S.ma * len(S.freq) == S.index - S.pre
                                              else f'`ma × 种类` = `{S.ma} × {len(S.freq)}` = {S.ma * len(S.freq)} ≠ 子串长 `{S.index - S.pre}`，有字符次数不够，不平衡'),
        'f[index] = min(': '把 `s[{pre}:{index}]` 切出去：`f[{index}] = min({B.f[index]}, f[{pre}] + 1)` = =={f[index]}==',
        'return f[-1]': '`f[-1]` 就是整串的答案：最少 =={ret}== 个平衡子串',
    },
    cards=dict(
        one_liner='枚举上一次分割点，最大次数 × 种类 = 长度即平衡',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['把字符串分割成若干子串，每个子串里每种字符出现的次数都相同',
                 '求最少能分成几个子串',
                 '示例：`"fabccddg"` → `3`；视频用 `"abcb"` → `2`（`"abc"` + `"b"`）'],
        quote='只有当哈希表中的最大次数乘以其中字符种类的数目恰好等于子串的长度时，子串中每种字符出现的次数才相等。',
        quote_src='—— yiduobo 题解',
        idea=['`f[i]` 表示前 `i` 个字符最少分出几个子串，从 `0` 到 `i-1` 枚举分割点 `pre`',
              '`s[pre:i]` 平衡就 `f[i] = min(f[i], f[pre] + 1)`',
              '哈希表记子串里每种字符的次数，从右往左边扩边判断，不用重新数'],
        summary=['时间 `O(n^2)`，空间 `O(n)`（计数器最多 26 个键）',
                 '易错：`f[index]` 先按单字符成段设成 `f[index-1]+1`，再用更小的覆盖',
                 '`freq`、`ma` 每个 `index` 要重新初始化',
                 '原文代码无需修改即可在 Python 3 运行，仅删去了多余空行'],
    ),
)
