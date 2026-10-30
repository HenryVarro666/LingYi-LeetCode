def _s_color(S, k, v):
    line, p = S.get('_line', 0), S.get('p')
    if line < 16 and p is not None:
        return 'green' if k < p else None
    if line < 22 and p is not None:
        return 'pink' if k > p else None
    idx = S.get('index')
    if idx is None:
        return None
    if k == idx:
        return 'yellow'
    return 'green' if k < idx else 'pink'


CONFIG = dict(
    num=3983, title='一次替换后的子序列', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='前后缀贪心匹配 · 枚举修改位置',
    tags=['双序列双指针', '状态机 DP', '难度分 1755'],
    code='''
class Solution(object):
    def canMakeSubsequence(self, s, t):
        
        prefix = []
        suffix = []

        p = 0
        for index in range(len(t)):
            if p < len(s) and s[p] == t[index]:
                prefix.append(index)
                p += 1
        
        if p == len(s):
            return True

        p = len(s) - 1
        for index in range(len(t) - 1, -1, -1):
            if p >= 0 and s[p] == t[index]:
                suffix.append(index)
                p -= 1
        
        for index in range(len(s)):
            if index > 0:
                if len(prefix) < index:
                    left = len(t)
                else:
                    left = prefix[index - 1]
            else:
                left = -1

            if index < len(s) - 1:
                if len(suffix) < len(s) - index - 1:
                    right = -1
                else:
                    right = suffix[len(s) - index - 2]
            else:
                right = len(t)

            if left + 1 < right:
                return True
            

        
        return False
''',
    call='Solution().canMakeSubsequence("abcd", "aebfd")',
    expect=True,
    views=[
        dict(type='string', var='s', label='s（绿 = 前缀已匹配，粉 = 后缀已匹配，黄 = 枚举的修改位置）', cell=84, h=200,
             pointers={'p if _line < 22 else None': 'blue', 'index if _line >= 22 else None': 'yellow'},
             pointer_labels={'p if _line < 22 else None': 'p', 'index if _line >= 22 else None': 'index'},
             color=_s_color),
        dict(type='string', var='t', label='t（绿 = 前缀匹配到的位置，粉 = 后缀匹配到的位置）', cell=84, h=200,
             pointers={'index if _line < 22 else None': 'blue'}, pointer_labels={'index if _line < 22 else None': 'index'},
             color=lambda S, k, v: ('green' if k in S.get('prefix', ()) else 'pink' if k in S.get('suffix', ()) else None)),
        dict(type='text', fn=lambda S: (f"`prefix = {S['prefix']}`，`suffix = {S['suffix']}`（从右往左存）" if 'prefix' in S else ''), size=24, h=60),
        dict(type='text', fn=lambda S: (f"`left = {S['left']}`，`right = {S['right']}`：中间空位 `{max(0, S['right'] - S['left'] - 1)}` 个" if 'left' in S and 'right' in S and S.get('_line', 0) >= 22 else ''), size=26, h=60),
    ],
    watch=[('p', 'p', 'blue'), ('index', 'index', 'yellow'), ('left', 'left', 'cyan'), ('right', 'right', 'orange')],
    captions={
        'prefix = []': '`prefix[k]`：s 的前缀 `s[0..k]` 在 t 里贪心匹配到的==最靠左==位置',
        'suffix = []': '`suffix[k]`：s 的后缀从右往左，在 t 里贪心匹配到的==最靠右==位置',
        'p = 0': '`p` 指向 s 中下一个要匹配的字母',
        'for index in range(len(t)):': '正向扫描 t：能匹配 `s[p]` 就匹配',
        'if p < len(s) and s[p] == t[index]': lambda S, B, r: (f"`s[{S.p}] = '{S.s[S.p]}'` 对 `t[{S.index}] = '{S.t[S.index]}'` → "
                                                              + ('==匹配==' if S.s[S.p] == S.t[S.index] else '不同，跳过')
                                                              if S.p < len(S.s) else 's 已匹配完'),
        'prefix.append': '记下匹配位置 `index = {index}`：`prefix = {prefix}`',
        'p += 1': '`p` → {p}，匹配 s 的下一个字母',
        'if p == len(s)': lambda S, B, r: ('s 本身已是 t 的子序列，不用改 → ==直接 True==' if S.p == len(S.s)
                                           else f'`p = {S.p} < {len(S.s)}`：s 没能全部匹配，必须修改一个字母'),
        'p = len(s) - 1': '反向再来一遍：`p` 从 s 末尾开始',
        'for index in range(len(t) - 1': '反向扫描 t，能匹配 `s[p]` 就匹配',
        'if p >= 0 and s[p] == t[index]': lambda S, B, r: (f"`s[{S.p}] = '{S.s[S.p]}'` 对 `t[{S.index}] = '{S.t[S.index]}'` → "
                                                           + ('==匹配==' if S.s[S.p] == S.t[S.index] else '不同，跳过')
                                                           if S.p >= 0 else 's 的后缀已匹配完'),
        'suffix.append': '记下匹配位置 `index = {index}`：`suffix = {suffix}`',
        'p -= 1': '`p` → {p}，匹配 s 的前一个字母',
        'for index in range(len(s))': '枚举修改 `s[index]`：前面 `index` 个走前缀，后面走后缀',
        'if index > 0': lambda S, B, r: (f'`index = {S.index}`：前缀有 `{S.index}` 个字母要匹配' if S.index > 0 else '`index = 0`：前缀为空，`left = -1`'),
        'if len(prefix) < index': lambda S, B, r: (f'`len(prefix) = {len(S.prefix)} < {S.index}`：前缀凑不齐 → 这个位置不可行'
                                                   if len(S.prefix) < S.index else f'`len(prefix) = {len(S.prefix)} ≥ {S.index}`：前缀够用'),
        'left = len(t)': '`left = len(t)`：t 里放不下前缀，不可能再有空位',
        'left = prefix[index - 1]': '`left = prefix[{index - 1}] = {left}`：前缀在 t 里最早能结束的位置',
        'left = -1': '前缀为空：`left = -1`',
        'if index < len(s) - 1': lambda S, B, r: (f'后面还有 `{len(S.s) - S.index - 1}` 个字母要匹配' if S.index < len(S.s) - 1 else '`index` 是最后一个：后缀为空，`right = len(t)`'),
        'if len(suffix) < len(s) - index - 1': lambda S, B, r: (f'`len(suffix) = {len(S.suffix)} < {len(S.s) - S.index - 1}`：后缀凑不齐 → 不可行'
                                                                if len(S.suffix) < len(S.s) - S.index - 1 else f'`len(suffix) = {len(S.suffix)} ≥ {len(S.s) - S.index - 1}`：后缀够用'),
        'right = -1': '`right = -1`：后缀凑不齐，`left + 1 < right` 必然不成立',
        'right = suffix[': '`right = suffix[{len(s) - index - 2}] = {right}`：后缀在 t 里最晚能开始的位置',
        'right = len(t)': '后缀为空：`right = len(t)`',
        'if left + 1 < right': lambda S, B, r: (f'`left + 1 = {S.left + 1} < right = {S.right}` → ==中间有空位==，改 `s[{S.index}]` 去匹配它'
                                                if S.left + 1 < S.right else f'`left + 1 = {S.left + 1} ≥ right = {S.right}` → 没有空位，换下一个修改位置'),
        'return True': '找到可行的修改位置 → `True`',
        'return False': '所有位置都试过了 → `False`',
    },
    cards=dict(
        one_liner='前缀和后缀都尽量“压缩”，中间留出一个空位给被改的字母',
        complexity='时间 `O(n + m)`，空间 `O(n)`',
        problem=['最多把 `s` 的一个字母改成任意小写字母',
                 '问能否使 `s` 成为 `t` 的子序列',
                 '示例：`s = "abcd"`，`t = "aebfd"` → `true`（把 `c` 改成 `f`）'],
        quote='以index为界，s[0]到s[index - 1]这个前缀，必须是t某个前缀的子序列，而s[index + 1]到s[-1]这个后缀必须是t某个后缀的子序列，同时，t中的前缀和后缀间，必须至少有一个空位的间隔。',
        quote_src='—— yiduobo 题解原文',
        idea=['先正向贪心：`prefix` 记录 s 每个前缀在 t 中最早结束的位置',
              '再反向贪心：`suffix` 记录 s 每个后缀在 t 中最晚开始的位置',
              '枚举修改位置 `index`：`left + 1 < right` 即中间至少一个空位'],
        result='改 `s[2]`：前缀 `ab` 到 t[2]，后缀 `d` 从 t[4]，中间 t[3] 可放修改后的字母 ✓',
        summary=['时间 `O(n + m)`，空间 `O(n)`',
                 '`suffix` 是从右往左存的，后缀的下标要用 `len(s) - index - 2`',
                 '前缀或后缀凑不齐时，分别令 `left = len(t)` 或 `right = -1`',
                 's 本身已是子序列时，先返回 True',
                 '原文为 Python 2 风格，Python 3 下无需修改即可运行',
                 '对比灵神：灵神用 j0 / j1 一次遍历的状态机，这里是前后缀分解'],
    ),
)
