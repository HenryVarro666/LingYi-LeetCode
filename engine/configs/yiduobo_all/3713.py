S0 = 'aabc'


def _txt(S):
    if 'freq_freq' not in S or 'right' not in S:
        return '`freq`：字符 → 次数；`freq_freq`：次数 → 有几种字符是这个次数'
    ff = S['freq_freq']
    sub = S['s'][S['left']:S['right'] + 1]
    if S.get('_line') not in (18, 19):
        return f'子串 `{sub!r}`：正在更新 freq / freq_freq'
    if len(ff) == 1:
        return f'子串 `{sub!r}`：freq_freq 只有 ==1== 种次数 → 平衡'
    return f'子串 `{sub!r}`：freq_freq 有 `{len(ff)}` 种次数 → 不平衡'


CONFIG = dict(
    num=3713, title='最长的平衡子串 I', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='枚举子串 · 次数的次数 freq_freq',
    tags=['灵神核心路线', '灵神题单·常用数据结构'],
    code='''
class Solution(object):
    def longestBalanced(self, s):
        
        n = len(s)
        res = 0
        for left in range(n):
            freq = {}
            freq_freq = {}
            for right in range(left, n):
                freq[s[right]] = freq.get(s[right], 0) + 1
                f = freq[s[right]]
                freq_freq[f] = freq_freq.get(f, 0) + 1
                if f > 1:
                    freq_freq[f - 1] -= 1
                    if freq_freq[f - 1] == 0:
                        freq_freq.pop(f - 1)
                
                if len(freq_freq) == 1:
                    res = max(res, right - left + 1)
        
        return res
''',
    call=f'Solution().longestBalanced({S0!r})',
    expect=3,
    max_steps=58,
    skip=['f = freq[s[right]]'],
    views=[
        dict(type='string', var='s', label='s（框 = 子串 s[left: right + 1]）', pointers={'left': 'blue', 'right': 'pink'},
             window=('left', 'right'), cell=110, h=230),
        dict(type='map', var='freq', label='freq（字符 → 次数）', fmt=lambda k, v: f"'{k}': {v}", h=130, font=32),
        dict(type='map', var='freq_freq', label='freq_freq（次数 → 几种字符）', fmt=lambda k, v: f'{k}次: {v}种', h=130, font=32),
        dict(type='text', fn=_txt, size=28, h=70),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), 'f', ('res', 'res', 'green')],
    captions={
        'n = len': '`n = {n}`',
        'res = 0': '`res` 记录最长平衡子串长度',
        'for left in range': lambda S, B, ret: (f'枚举起点 `left = {S.left}`' if 'left' not in B or S.left != B.left else '所有起点枚举完'),
        'freq_freq = {}': '`freq_freq` 也清空',
        'freq = {}': '换了起点，`freq` 重新统计',
        'for right in range': lambda S, B, ret: (f'终点后移到 `right = {S.right}`，新加入 `{S.s[S.right]!r}`'
                                                 if 'right' not in B or S.right != B.right or not B.freq else f'以 `left = {S.left}` 为起点的子串枚举完'),
        'freq[s[right]] =': '在 `s[left: right]` 的基础上==只多了== `s[right]`：`freq[{s[right]!r}]` → {freq[s[right]]}',
        'freq_freq[f] = freq_freq.get': '`f = {f}`：次数 `{f}` 多了一种字符 → `freq_freq[{f}] = {freq_freq[f]}`',
        'if f > 1:': lambda S, B, ret: (f'`f = {S.f} > 1`：它是从 `{S.f - 1}` 变来的，次数 `{S.f - 1}` 要少一种' if S.f > 1
                                        else '`f = 1`：新字符，没有旧次数要撤销'),
        'freq_freq[f - 1] -= 1': '`freq_freq[{f - 1}]` 减一 → {freq_freq[f - 1]}',
        'if freq_freq[f - 1] == 0': lambda S, B, ret: (f'`freq_freq[{S.f - 1}]` 变成 0 → 要弹出这个次数' if S.freq_freq[S.f - 1] == 0
                                                       else f'`freq_freq[{S.f - 1}] = {S.freq_freq[S.f - 1]}`，仍有字符是这个次数'),
        'freq_freq.pop': '弹出次数 `{f - 1}`，现在 `freq_freq = {freq_freq}`',
        'if len(freq_freq) == 1': lambda S, B, ret: (f'freq_freq 只有一个键：所有字符都出现 `{next(iter(S.freq_freq))}` 次 → ==平衡=='
                                                     if len(S.freq_freq) == 1 else f'freq_freq 有 `{len(S.freq_freq)}` 个键：次数不全相同 → 不平衡'),
        'res = max': lambda S, B, ret: (f'长度 `{S.right - S.left + 1}` 更新 `res = {S.res}`' if S.res != B.res
                                        else f'长度 `{S.right - S.left + 1}` 不超过 `{S.res}`'),
        'return res': '最长平衡子串长度 =={ret}==',
    },
    cards=dict(
        one_liner='再统计一次「次数的次数」：只剩一种次数就是平衡',
        complexity='时间 `O(n^2)`，空间 `O(|Σ|)`',
        problem=['子串中所有==不同字符出现的次数都相同==，称为平衡子串',
                 '求 `s` 的最长平衡子串长度，`n ≤ 1000`',
                 '示例：`"abbac"` → `4`；本视频 `"aabc"` → `3`（`"abc"`）'],
        quote='使用一个哈希表freq记录当前子串中每种字符出现的次数，同时使用另一个哈希表==freq_freq记录freq中每种次数出现的次数==……若freq_freq中仅有一个元素，就说明当前子串中仅有一种次数',
        quote_src='—— yiduobo 题解原文',
        idea=['`s[left: right+1]` 的计数 = `s[left: right]` 的计数 + `s[right]`，增量更新',
              '字符次数 `f−1 → f`：`freq_freq[f]` 加一，`freq_freq[f−1]` 减一，减到 0 就弹出',
              '`len(freq_freq) == 1` 即所有字符次数相同'],
        summary=['时间 `O(n^2)`，空间 `O(|Σ|)`',
                 '易错：`freq_freq[f−1]` 减到 0 必须 `pop`，否则 `len` 判断出错',
                 '每换一个起点，两个哈希表都要清空',
                 '原文为 Python 2 风格写法，代码可直接在 Python 3 运行，未作改动',
                 '对比灵神：灵神用 `mx × kinds == 长度` 判平衡，只需一个哈希表'],
    ),
)
