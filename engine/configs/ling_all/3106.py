def _txt(S):
    if 'k' not in S:
        return ''
    base = f"剩余操作次数 `k = {S['k']}`"
    if 'dis' in S and 'i' in S:
        base += f"　　变成 a 的最小代价 `dis = min({S['c']-97}, {122-S['c']+1})` = =={S['dis']}=="
    return base


CONFIG = dict(
    num=3106, title='满足距离约束且字典序最小的字符串', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='字符串贪心 · 从左往右变 a',
    tags=['灵神题单', '字符串贪心', '难度分 1515'],
    code='''
class Solution:
    def getSmallestString(self, s: str, k: int) -> str:
        s = list(s)
        for i, c in enumerate(map(ord, s)):
            dis = min(c - ord('a'), ord('z') - c + 1)
            if dis > k:
                s[i] = chr(c - k)
                break
            s[i] = 'a'
            k -= dis
        return ''.join(s)
''',
    call='Solution().getSmallestString("xaxcd", 4)',
    expect='aawcd',
    views=[
        dict(type='text', fn=_txt, size=26),
        dict(type='string', var='s', label='s（粉 = 当前字符 i，绿 = 已变成 a）', cell=90, h=200,
             pointers={'i': 'pink'},
             color=lambda S, i, v: 'green' if i < S.get('i', 0) else None),
    ],
    watch=['i', 'c', 'dis', ('k', 'k', 'green')],
    captions={
        's = list': '字符串转成列表，才能逐位修改',
        'for i, c in enumerate': '从左往右看 `i = {i}`，字符 `{s[i]}`（ASCII {c}）',
        'dis = min': '变成 `a` 有两条路：往回减 `{c - 97}` 次，或绕 `z` 加 `{122 - c + 1}` 次 → 取小 `dis = {dis}`',
        'if dis > k': lambda S, B, r: (f'`dis = {S.dis}` > `k = {S.k}`：钱不够变成 a，只能尽量往小减' if S.dis > S.k
                                      else f'`dis = {S.dis}` ≤ `k = {S.k}`：够用，把它变成 a（越靠左越优先）'),
        'chr(c - k)': '变不成 a，就把字符往前减 `k` → `{s[i]}`，`k` 用光',
        'break': '`k` 已经花完，后面的字符保持原样，退出',
        "s[i] = 'a'": '`s[{i}]` 变成 `a`',
        'k -= dis': '花掉 `dis`：`k = {B.k} − {dis} = {k}`',
        "return": '拼成字符串 =={ret}==',
    },
    cards=dict(
        one_liner='优先把左边的字母变成 a，钱不够就尽量往小减',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['每次操作把一个字母改成别的字母，字母表 a–z ==首尾相接==',
                 '总距离不超过 `k`，求字典序最小的字符串',
                 '示例：`s = "xaxcd"`，`k = 4` → `"aawcd"`'],
        quote='贪心，优先把左边的字母变成 a。把 s[i] 变成 a，可以不断减一到 a，也可以不断加一到 a，二者取最小值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['字典序看左边的字母最重要：能变 `a` 就变 `a`',
              '代价 `dis = min(c − a, z − c + 1)`，因为 `z` 加一就回到 `a`',
              '某一位 `dis > k`：变不成 `a`，就把它减 `k`，`k` 用完退出'],
        summary=['时间 `O(n)`，空间 `O(n)`（C++ 可原地改）',
                 '循环绕圈：`dis` 里的 `z − c + 1` 不能漏掉 `+1`',
                 '不够变 a 时用 `chr(c - k)`，之后 `k = 0` 必须 break',
                 '`k` 够用时每位都变 a，字符串变成全 a'],
    ),
)
