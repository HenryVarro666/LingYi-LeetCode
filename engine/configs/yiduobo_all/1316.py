def _pair(S, k, v):
    if 'i' not in S or 'l' not in S:
        return None
    i, l = S['i'], S['l']
    if i + l <= k < i + 2 * l:
        return 'green'
    return None


def _top(S):
    if 'l' not in S or 'i' not in S:
        return '先预处理 29 进制前缀哈希 `s`，再枚举前半部分长度 `l`'
    i, l, t = S['i'], S['l'], S['text']
    a, b = t[i:i + l], t[i + l:i + 2 * l]
    return f"`l = {l}`：前半 ==`{a}`==（蓝） vs 后半 ==`{b}`==（绿）" if 'i' in S else f'枚举 `l = {l}`'


CONFIG = dict(
    num=1316, title='不同的循环子字符串', difficulty='Hard', category='字符串',
    author='yiduobo', technique='枚举长度 + 29 进制前缀哈希',
    tags=['灵神题单', '字符串'],
    code='''
class Solution(object):
    def distinctEchoSubstrings(self, text):

        n = len(text)
        s = [ord(text[0]) - 97]
        mod = 10 ** 9 + 7
        for char in text[1:]:
            s.append((s[-1] * 29 + ord(char) - 97) % mod)

        res = 0
        power = 1
        for l in range(1, n // 2 + 1):
            power = power * 29 % mod
            used = set()
            for i in range(n - l - l + 1):
                j = i + l - 1
                if i == 0:
                    v = s[j]
                else:
                    v = (s[j] - s[i - 1] * power % mod + mod) % mod
                
                if v not in used:
                    next_i = j + 1
                    next_j = next_i + l - 1
                    next_v = (s[next_j] - s[next_i - 1] * power % mod + mod) % mod
                    if v == next_v:
                        res += 1
                        used.add(v)

        return res
''',
    call='Solution().distinctEchoSubstrings("aabaab")',
    expect=2,
    views=[
        dict(type='text', fn=_top, size=28, h=90),
        dict(type='string', var='text', label='text（蓝框 = 前半部分，绿 = 后半部分）', cell=84, h=250,
             pointers={'i': 'blue'}, window=('i', 'i+l-1'), color=_pair),
        dict(type='array', var='s', label='s：前缀 29 进制哈希', cell=96, h=190,
             pointers={'i+l-1': 'pink'}, pointer_labels={'i+l-1': 'j'}),
        dict(type='set', var='used', label='used（本轮已计数的前半部分哈希）', fmt=lambda x: str(x), h=130),
    ],
    watch=[('l', 'l', 'blue'), ('i', 'i', 'blue'), ('v', 'v', 'cyan'), ('next_v', 'next_v', 'pink'), ('res', 'res', 'green')],
    skip=['for char in', 'mod = 10', 'power = 1', 'if i == 0', 'power = power * 29', 'j = i + l - 1', 'next_i = j + 1', 'next_j = next_i'],
    captions={
        's = [ord': '`s[0]` = 首字母编码 `{s[0]}`（a→0, b→1 …）',
        's.append': '`s[-1] * 29 + 字母` 取模：像前缀和一样累出 `s` = {s}',
        'for l in range': '枚举前半部分长度 `l = {l}`，后半部分紧跟其后',
        'used = set()': '每个 `l` 单独去重：`used` 记下已算过的前半部分哈希',
        'for i in range': '枚举前半部分起点 `i = {i}`，前半 `text[{i}:{i+l}]`，后半 `text[{i+l}:{i+2*l}]`',
        'if i == 0': lambda S, B, r: ('`i == 0`：前缀就是整段，直接 `v = s[j]`' if S.i == 0
                                      else '`i > 0`：要把 `i` 之前的前缀减掉'),
        'v = s[j]': '`v = s[{j}] = {v}`：`text[0:{l}]` 的哈希',
        'v = (s[j]': '`v = s[{j}] − s[{i-1}] × 29^{l}`（取模）= =={v}==：前半部分哈希',
        'if v not in used': lambda S, B, r: (f'前半部分哈希 `{S.v}` 没记录过 → 要检查后半部分' if S.v not in S.used
                                             else f'`{S.v}` 已在 `used` 里 → 同样的字符串不重复计数'),
        'next_v = ': '后半部分 `text[{next_i}:{next_i+l}]` 同样公式：`next_v` = =={next_v}==',
        'if v == next_v': lambda S, B, r: (f'`{S.v} == {S.next_v}` → 前后两半相同，是一个合法答案' if S.v == S.next_v
                                           else f'`{S.v} ≠ {S.next_v}` → 前后两半不同，跳过'),
        'res += 1': '找到一个新的合法子串：`res` → =={res}==',
        'used.add': '把 `{v}` 记入 `used`，同一轮里再遇到就不再计数',
        'return res': '所有长度枚举完，共有 `{res}` 个不同的 “A+A” 子串',
    },
    cards=dict(
        one_liner='枚举前半长度和起点，用 29 进制前缀哈希 O(1) 比较前后两半',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['求 `text` 中有多少个==不同==的非空子串，能写成 `a + a`（某个字符串重复两次）',
                 '示例：`"abcabcabc"` → `3`（`abcabc`、`bcabca`、`cabcab`）；本视频用 `"aabaab"` → `2`（`aa`、`aabaab`）',
                 '`text` 长度 ≤ 2000'],
        quote='先枚举答案字符串前半部分的长度l，再枚举前半部分的起点i。这样一来，前半部分就是text[i : i + l]，而后半部分则是text[i + l : i + l + l]。',
        quote_src='—— yiduobo 题解原文',
        idea=['`s[i]` 是 `text[:i+1]` 的 29 进制哈希，像前缀和一样可以做“区间哈希” `s[j] − s[i−1] × 29^l`',
              '前后两半的哈希相等 → 字符串相同；每个 `l` 用 `used` 对前半哈希去重',
              '取模 `10^9+7`，29 是大于 26 的质数，减少冲突'],
        summary=['时间 `O(n^2)`：`l` 有 n/2 个，`i` 有 O(n) 个，每次比较 `O(1)`',
                 '原文为 Python 2 写法，`n / 2` 已改为 `n // 2`',
                 '易错：减法后要 `+ mod` 再取模，避免负数；`power` 随 `l` 逐步乘 29',
                 '去重只在同一个 `l` 内：不同 `l` 的字符串长度不同，天然不同'],
    ),
)
