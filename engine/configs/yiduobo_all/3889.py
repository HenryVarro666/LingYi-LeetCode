def _txt(S):
    if 'freq' not in S:
        return ''
    if 'c' not in S:
        return '`freq` 只记「前半段字符」的净值：前半段 `+1`，后半段映射到镜像后 `−1`'
    c = S['c']
    if 'delta' in S and 'v' in S and S['_line'] >= 15:
        return f"`'{c}'` 归到 `freq[{S['v']!r}]`，加 `{S['delta']:+d}`"
    return f"当前字符 `'{c}'`：前半段（`0-4`、`a-m`）记 `+1`，后半段记 `−1` 并换成镜像字符"


CONFIG = dict(
    num=3889, title='镜像频次距离', difficulty='Medium', category='字符串',
    author='yiduobo', technique='哈希表 · 镜像对净差值',
    tags=[],
    code='''
class Solution(object):
    def mirrorFrequency(self, s):
        
        freq = {}
        for c in s:
            if '0' <= c <= '4':
                v = int(c)
                delta = 1
            elif '5' <= c <= '9':
                v = 9 - int(c)
                delta = -1
            elif 'a' <= c <= 'm':
                v = c
                delta = 1
            else:
                v = chr(ord('a') + ord('z') - ord(c))
                delta = -1
        
            freq[v] = freq.get(v, 0) + delta
        
        return sum([abs(f) for f in freq.values()])
''',
    call="Solution().mirrorFrequency('4m7nb2z')",
    expect=3,
    views=[
        dict(type='text', h=90, size=28, fn=_txt),
        dict(type='string', var='s', label='s（蓝 = 当前字符）', cell=100, h=190,
             color=lambda S, k, v: 'blue' if 'c' in S and 'freq' in S and k == S['s'].index(S['c']) else None),
        dict(type='map', var='freq', label='freq（镜像对的净差：前半段 − 后半段）', fmt=lambda k, v: f"{k!r}: {v}", h=230, font=30),
    ],
    watch=[('c', 'c', 'blue'), 'v', 'delta'],
    captions={
        'freq = {}': '`freq` 的键是镜像对里==前半段那个字符==，值是它的次数减去镜像字符的次数',
        'for c in s': '依次取字符 `c`',
        "if '0' <= c <= '4'": lambda S, B, r: f"`'0' <= '{S.c}' <= '4'` → " + ('==成立：数字前半段==' if '0' <= S.c <= '4' else '不成立'),
        "elif '5' <= c <= '9'": lambda S, B, r: f"`'5' <= '{S.c}' <= '9'` → " + ('==成立：数字后半段==' if '5' <= S.c <= '9' else '不成立'),
        "elif 'a' <= c <= 'm'": lambda S, B, r: f"`'a' <= '{S.c}' <= 'm'` → " + ('==成立：字母前半段==' if 'a' <= S.c <= 'm' else '不成立，剩下的就是字母后半段 n-z'),
        'v = int(c)': '前半段数字自己当键：`v = {v}`',
        'v = 9 - int(c)': '镜像数字之和为 9：`9 - {int(c)} = {v}`，换成前半段的键',
        'v = chr(': "镜像字母 ascii 之和恒为 `ord('a') + ord('z')`：`'{c}'` 的镜像是 `{v!r}`",
        'v = c': '前半段字母自己当键：`v = {v!r}`',
        'delta = 1': '前半段：次数 `+1`',
        'delta = -1': '后半段：次数 `−1`',
        'freq[v] =': '`freq[{v!r}]` = `{B.freq.get(v, 0)} {delta:+d}` = =={freq[v]}==',
        'return sum': lambda S, B, r: f"每个键取绝对差再求和：`{'+'.join(str(abs(x)) for x in S.freq.values())}` = =={r}=="
    },
    cards=dict(
        one_liner='用哈希表记录每个镜像对的次数之差，最后取绝对值求和',
        complexity='时间 `O(n)`，空间 `O(|Σ|)`',
        problem=['字符串由小写字母和数字组成；`a↔z`、`b↔y`…，`0↔9`、`1↔8`… 互为镜像',
                 '每个镜像对只算一次：`|freq(c) − freq(m)|`，求所有镜像对之和',
                 '本视频：`s = "4m7nb2z"` → `3`'],
        quote='若某个字符c处于前半段，例如0到4，或者a到m，那么就将freq[c]加上1，反之则计算c的镜像字符m，然后将freq[m]减去1。',
        quote_src='—— yiduobo 题解原文',
        idea=['只在前半段字符上建键：前半段 `+1`，后半段换成镜像字符后 `−1`',
              '数字镜像之和为 9：`v = 9 - int(c)`；字母镜像 ascii 之和为 `ord(a) + ord(z)`',
              '遍历结束后，每个键的值就是 `freq(c) − freq(m)`，取绝对值求和'],
        summary=['时间 `O(n)`，空间 `O(|Σ|)`',
                 '一次遍历搞定，不用先统计再配对（灵神是先 Counter 再枚举 18 对）',
                 '键里数字用 `int`、字母用字符，两者不会冲突',
                 '易错点：后半段字符要先换成镜像再减 1，而不是直接减自己'],
    ),
)
