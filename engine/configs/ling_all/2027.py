CONFIG = dict(
    num=2027, title='转换字符串的最少操作次数', difficulty='Easy', category='贪心算法',
    author='灵茶山艾府', technique='从左到右贪心（Go 原文转写）',
    tags=['贪心与思维', '从最左开始贪心', '难度分 1346'],
    code='''
class Solution:
    def minimumMoves(self, s: str) -> int:
        ans = 0
        i = 0
        while i < len(s):
            if s[i] == 'X':
                ans += 1
                i += 2  # 跳过两个字符
            i += 1
        return ans
''',
    call='Solution().minimumMoves("XXOXOXXXO")',
    expect=3,
    views=[
        dict(type='string', var='s', pointers={'i': 'blue'}, label='s', h=200,
             color=lambda S, i, v: 'orange' if v == 'X' else None,
             dim=lambda S, i, v: 'i' in S and i < S['i'] and v == 'O'),
        dict(type='text', h=70, fn=lambda S: f"已操作 ==`{S['ans']}`== 次" if 'ans' in S else ''),
    ],
    watch=[('i', 'i', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'if s[i] ==': lambda S, B, r: (f'`s[{S.i}] = X`：必须操作，以它为左端最划算' if S.s[S.i] == 'X' else f'`s[{S.i}] = O`：不用管，看下一个'),
        'ans += 1': '操作一次，把 `s[{i}..{i+2}]` 都变成 O：`ans` → =={ans}==',
        'i += 2': '后面两个字符已被改成 O，直接跳过：`i` → {i}',
        'i += 1': '`i` → {i}',
        'return ans': '一共操作 `{ret}` 次',
    },
    cards=dict(
        one_liner='遇到 X 就一次操作盖住它和后面两个',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每次操作选三个连续字符，全部变成 `O`',
                 '求把 `s` 全变成 `O` 的最少操作次数',
                 '示例：`XXOX` → `2`；本视频：`XXOXOXXXO` → `3`'],
        quote='遍历 s，遇到 X 就将其与后面两个字符改为 O，操作次数加一，然后跳过后面两个字符。',
        quote_src='—— 灵茶山艾府题解',
        idea=['最左边的 X 必须被某次操作覆盖，让它做左端能覆盖最多后续字符',
              '覆盖后的两个字符已是 O，直接跳过，不必真的修改字符串'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`for` 循环体内改 `i`，转写为 `while`）',
                 '时间 `O(n)`，空间 `O(1)`',
                 '易错点：遇到 X 要跳 3 位（`i += 2` 再加循环的 1），遇到 O 只跳 1 位'],
    ),
)
