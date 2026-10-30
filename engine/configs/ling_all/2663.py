def _chars(S):
    s = S.get('s')
    if isinstance(s, list):
        return [chr(x) for x in s]
    return list(s) if s else []


def _bad(S, i):
    s = S.get('s')
    if not isinstance(s, list) or i >= len(s):
        return False
    return (i > 0 and s[i] == s[i - 1]) or (i > 1 and s[i] == s[i - 2])


def _txt(S):
    s, k = S.get('s'), S.get('k')
    if not isinstance(s, list) or 'i' not in S or S['i'] >= len(s):
        return '把 s 看成 k 进制数：从最后一位加一，遇到回文就继续加，满 k 就进位'
    i = S['i']
    if s[i] == k:
        return f"`s[{i}]` 加到了 `{chr(k)}`（超出前 k 个字母）→ ==进位=="
    parts = []
    if i > 0:
        parts.append(f"`s[{i}]={chr(s[i])}` {'==' if s[i] == s[i-1] else '≠'} `s[{i-1}]={chr(s[i-1])}`")
    if i > 1:
        parts.append(f"`s[{i}]={chr(s[i])}` {'==' if s[i] == s[i-2] else '≠'} `s[{i-2}]={chr(s[i-2])}`")
    return '；'.join(parts) if parts else f'`s[{i}]` 左边没有字母，不会形成回文'


CONFIG = dict(
    num=2663, title='字典序最小的美丽字符串', difficulty='Hard', category='贪心与思维',
    author='灵茶山艾府', technique='k 进制加一 · 只查左侧两个字母',
    tags=['灵神题单', '难度分 2416'],
    code='''
class Solution:
    def smallestBeautifulString(self, s: str, k: int) -> str:
        a = ord('a')
        k += a
        s = list(map(ord, s))
        n = len(s)
        i = n - 1  # 从最后一个字母开始
        s[i] += 1  # 先加一
        while i < n:
            if s[i] == k:  # 需要进位
                if i == 0:  # 无法进位
                    return ""
                # 进位
                s[i] = a
                i -= 1
                s[i] += 1
            elif i and s[i] == s[i - 1] or i > 1 and s[i] == s[i - 2]:
                s[i] += 1  # 如果 s[i] 和左侧的字符形成回文串，就继续增加 s[i]
            else:
                i += 1  # 反过来检查后面是否有回文串
        return ''.join(map(chr, s))
''',
    call='Solution().smallestBeautifulString("dacd", 4)',
    expect='dbac',
    views=[
        dict(type='text', fn=_txt, size=27, h=100),
        dict(type='array', var=_chars, label='s（当前被加一的位置 i；红 = 与左侧形成回文）', cell=110, h=300,
             pointers={'i': 'blue'},
             color=lambda S, k, v: ('red' if _bad(S, k) and k == S.get('i') else 'blue' if k == S.get('i') else None) if isinstance(S.get('s'), list) else None),
        dict(type='text', fn=lambda S: ('字母 a、b、c、d 对应 0、1、2、3；加一就是 d → 下一个字母' if isinstance(S.get('s'), list) else ''), size=24, h=70),
    ],
    watch=[('i', 'i', 'blue'), ('n', 'n'), ('k', 'k')],
    captions={
        'a = ord': '`a = {a}`，把字母当成数字处理',
        'k += a': '`k` 变成上界 `{k}`：字母编码 == `k` 就是越界了',
        's = list': '`s` 转成编码数组：{s}',
        'n = len': '`n = {n}`',
        'i = n - 1': '先从最后一个字母开始：`i = {i}`',
        's[i] += 1': '末位加一：`s[{i}]` → `{chr(s[i])}`（要比原来的大）',
        'while i < n': lambda S, B, r: (f'`i = {S.i}`，继续检查和修正' if S.i < S.n else '`i == n`：整个字符串都没有回文了，结束'),
        'if s[i] == k': lambda S, B, r: (f"`s[{S.i}]` 已经到 `{chr(S.k)}`，超出前 k 个字母 → ==要进位==" if S.s[S.i] == S.k
                                         else f"`s[{S.i}] = '{chr(S.s[S.i])}'` 还在前 k 个字母内，不用进位"),
        'if i == 0': lambda S, B, r: ('最高位也进不了位 → 不存在更大的美丽字符串' if S.i == 0 else '不是最高位，可以向前进位'),
        'return ""': '返回空串',
        's[i] = a': '这一位归零（回到 `a`）',
        'i -= 1': '进位给左边：`i` → {i}',
        's[i] += 1': lambda S, B, r: (f"`s[{S.i}]` 加一 → `{chr(S.s[S.i])}`" if S.get('i') != S.n - 1 or S.s[S.i] != B.s[S.i] + 0 else ''),
        'elif i and': lambda S, B, r: (f"`s[{S.i}]` 与左侧形成回文（长 2 或长 3）→ ==继续加一=="
                                       if ((S.i and S.s[S.i] == S.s[S.i - 1]) or (S.i > 1 and S.s[S.i] == S.s[S.i - 2]))
                                       else f"`s[{S.i}] = '{chr(S.s[S.i])}'` 与左边两个字母都不同 → 这一位没问题"),
        'else': '没有回文，继续',
        'i += 1': '这一位没问题，去检查它后面一位（后面的字母要重新“凑”）：`i` → {i}',
        'return \'\'.join': '全部合法，答案 `{ret!r}`',
    },
    max_steps=70,
    cards=dict(
        one_liner='把字符串当 k 进制数加一，遇到回文就继续加',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['==美丽字符串==：只含前 `k` 个字母，且没有长度 `>= 2` 的回文子串',
                 '给定美丽字符串 `s`，求字典序比它大的最小美丽字符串，没有返回 `""`',
                 '示例：`s = "dacd"`，`k = 4` → `"dbac"`'],
        quote='「不包含任何长度为 2 或更长的回文串」等价于「不包含长度为 2 和长度为 3 的回文串」。换句话说，不能出现 s[i]=s[i-1] 以及 s[i]=s[i-2]。',
        quote_src='—— 灵茶山艾府题解',
        idea=['回文去掉首尾仍是回文，所以只需检查 `s[i]` 与它左边两个字母',
              '要字典序最小，修改位置越靠右越好：把 `s` 看成 k 进制数，末位加一',
              '加一后若与左侧形成回文就继续加；满 k 就进位；没问题就往右检查后面'],
        result='`dacd` → 末位 `d` 进位 → … → `dbac`：每一位都和左边两个字母不同 ✓',
        summary=['时间 `O(n)`：每位最多加两三次就能避开左侧两个字母，不是 `O(nk)`',
                 '`s[i] == k` 要先判断进位，再判断回文',
                 '题目保证输入是美丽字符串，所以左侧没问题，只需检查 `i` 及其右边',
                 '进位到最高位仍超过 `k` → 无解，返回空串'],
    ),
)
