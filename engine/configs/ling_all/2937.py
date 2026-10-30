def _col(S, i, v):
    return 'green' if i < S.get('lcp', 0) else None


CONFIG = dict(
    num=2937, title='使三个字符串相等', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='最长公共前缀 · zip 三串',
    code='''
class Solution:
    def findMinimumOperations(self, s1: str, s2: str, s3: str) -> int:
        lcp = 0
        for x, y, z in zip(s1, s2, s3):
            if x != y or x != z:
                break
            lcp += 1
        return -1 if lcp == 0 else len(s1) + len(s2) + len(s3) - lcp * 3
''',
    call='Solution().findMinimumOperations("abcd", "abce", "abd")',
    expect=5,
    views=[
        dict(type='string', var='s1', label='s1', pointers={'lcp': 'blue'}, color=_col, h=150),
        dict(type='string', var='s2', label='s2', color=_col, h=130),
        dict(type='string', var='s3', label='s3', color=_col, h=130),
        dict(type='text', fn=lambda S: f"公共前缀长度 `lcp` = =={S['lcp']}==" if 'lcp' in S else '', h=70),
    ],
    watch=[('lcp', 'lcp', 'green'), 'x', 'y', 'z'],
    captions={
        'lcp = 0': '`lcp` 记录三个字符串的最长公共前缀长度，先设为 0',
        'for x, y, z in zip': '`zip` 同时取三个字符串同一位置的字母：`{x}`、`{y}`、`{z}`，最短的串走完就停',
        'if x != y or x != z': lambda S, B, r: (f"`{S.x}`、`{S.y}`、`{S.z}` 不全相等 → 前缀到此为止，==break==" if (S.x != S.y or S.x != S.z)
                                                 else f"`{S.x}`、`{S.y}`、`{S.z}` 三个字母相同 → 这一位可以保留"),
        'break': '前缀断开，之后的字母不可能再相等，退出循环',
        'lcp += 1': '公共前缀又长了一位：`lcp` = =={lcp}==',
        'return': lambda S, B, r: ('`lcp = 0`：第一个字母就不同，删到只剩 1 个字符也不会相等 → ==-1==' if S.lcp == 0
                                   else f'总长 `{len(S.s1) + len(S.s2) + len(S.s3)}` 减去保留的 `3 × {S.lcp}` = ==`{r}`== 次删除'),
    },
    cards=dict(
        one_liner='只能删末尾 → 三个串最后都剩公共前缀',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每次可删某个字符串（长度 ≥ 2）的最右字符，问让 `s1 s2 s3` 相等的最少操作数，不可能返回 `-1`',
                 '示例：`"abc" "abb" "ab"` → `2`',
                 '本视频：`"abcd" "abce" "abd"` → `5`'],
        quote='设 lcp 为三个字符串的最长公共前缀的长度。如果 lcp=0，无法操作成一样的，返回 -1。否则返回三个字符串的长度之和，减去剩下的长度 3·lcp。',
        quote_src='—— 灵茶山艾府题解',
        idea=['删除只发生在末尾，最终留下的一定是公共前缀', '最优是留满最长公共前缀，删掉其余所有字母',
              '`lcp = 0` 时首字母就不同，永远不会相等'],
        summary=['时间 `O(n)`，n 为最短字符串长度；空间 `O(1)`',
                 '易错：`lcp = 0` 必须返回 `-1`，不是总长度',
                 '`zip` 自动在最短串处停止，不会越界'],
    ),
)
