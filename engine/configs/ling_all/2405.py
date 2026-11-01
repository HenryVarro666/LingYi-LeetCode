CONFIG = dict(
    num=2405, title='子字符串的最优划分', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='贪心 + 位掩码记录出现字符（Go 原文转写）',
    tags=['贪心与思维', '划分型贪心', '难度分 1355'],
    code='''
class Solution:
    def partitionString(self, s: str) -> int:
        ans, vis = 1, 0
        for c in s:
            if vis >> (ord(c) & 31) & 1 > 0:
                vis = 0
                ans += 1
            vis |= 1 << (ord(c) & 31)
        return ans
''',
    call='Solution().partitionString("abacaba")',
    expect=4,
    views=[
        dict(type='text', h=90, fn=lambda S: ("当前这组已有字符：" + (''.join(chr(96 + k) for k in range(1, 27) if S['vis'] >> k & 1) or '（空）') + f"　｜　已分 ==`{S['ans']}`== 组") if 'vis' in S else ''),
        dict(type='string', var='s', label='s', h=170),
    ],
    watch=['c', ('vis', 'bin(vis)', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'ans, vis = 1, 0': '`ans = 1`：至少有一组；`vis = 0`：用二进制位记录当前组里出现过的字母',
        'for c in s': '看字符 `{c}`',
        'if vis >>': lambda S, B, r: (f'`{S.c}` 已在当前组里出现过 → 必须在它前面切一刀' if S.vis >> (ord(S.c) & 31) & 1 else f'`{S.c}` 没出现过 → 继续放进当前组'),
        'vis = 0': '清空当前组，字符 `{c}` 将作为新一组的开头',
        'ans += 1': '开新的一组：`ans` → =={ans}==',
        'vis |=': '把 `{c}` 记入当前组：`vis` = `{bin(vis)}`',
        'return ans': '最少分成 `{ret}` 组',
    },
    cards=dict(
        one_liner='尽量让每一组长，遇到重复字符才切',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['把 `s` 划分成若干子串，每个子串内字符互不相同',
                 '求最少划分成几个子串',
                 '示例：`abacaba` → `4`'],
        quote='贪心：从左往右遍历，没出现过就分到同一组。',
        quote_src='—— 灵茶山艾府题解',
        idea=['当前组能多长就多长，直到遇到组里已有的字符才开新组',
              '用一个整数 `vis` 的二进制位当集合，`c & 31` 把字母映射到 1~26 位',
              '检查 `vis >> k & 1`，加入 `vis |= 1 << k`，开新组时 `vis = 0`'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`c & 31` 对应 `ord(c) & 31`）',
                 '时间 `O(n)`，空间 `O(1)`',
                 '易错点：`ans` 初值是 1（最后一组没有被计入）；开新组后别忘了把当前字符加入 `vis`'],
    ),
)
