CONFIG = dict(
    num=3675, title='转换字符串的最小操作次数', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='数轴模型 · 最小非 a 字母',
    tags=['贪心算法', '思维题', '难度分 1414'],
    code='''
class Solution:
    def minOperations(self, s: str) -> int:
        if 'b' in s:
            return 25
        # 'z' 的下一个字符是 '{'
        min_c = min((c for c in s if c != 'a'), default='{')
        return ord('{') - ord(min_c)
''',
    call="Solution().minOperations('yazyd')",
    expect=23,
    views=[
        dict(type='string', var='s', h=200, label='s',
             color=lambda S, i, v: 'blue' if 'min_c' in S and v == S['min_c'] else None,
             dim=lambda S, i, v: v == 'a'),
        dict(type='text', h=120, fn=lambda S: (f"最小的非 a 字母 `{S['min_c']}` 要走到 `{{`：`ord('{{') - ord('{S['min_c']}')` = =={ord('{') - ord(S['min_c'])}==" if 'min_c' in S else '字母表：b → c → … → z → a，一次操作让某个字母整体前进一格')),
    ],
    watch=[('min_c', 'min_c', 'blue')],
    captions={
        "if 'b' in s": lambda S, B, r: ("有 `b`：它要走完 b 到 z 再到 a，共 25 步，直接返回" if 'b' in S.s else "`'b' in s` → False：没有 `b`，继续找最小的字母"),
        'min_c =': "跳过 `a`，取最小字母：`min_c = '{min_c}'`（全是 a 时用默认值 `{{`）",
        'return ord': "`ord('{{') - ord('{min_c}')` = =={ret}==：从 `{min_c}` 一路走到 `z` 再变 `a`",
    },
    cards=dict(
        before=[dict(heading='数轴模型', lines=['字母 `b`…`z` 是数轴上的人，目标位置是 `z+1`（也就是 `a`）', '一次操作 = 选一个点，==这个点上的所有人==一起向右一步', '最左边的人走到终点时，右边的人早已被顺路带到，所以只看最左边的人'])],
        after=[dict(heading='为什么最左边的人决定一切', lines=['`"yazyd"`：`a` 不用动，最小的非 a 字母是 `d`', '`d → e → … → z → a`，一共 `23` 步', '更大的字母走到同一格后就合并，一起走，不额外花操作'])],
        one_liner='把字母看成数轴上的人，最小的非 a 字母走到 z+1 的距离就是答案',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每次操作：选字符 `c`，把串中==所有== `c` 换成下一个字母（`z` 的下一个是 `a`）',
                 '求把 `s` 变成全 `a` 的最少操作次数',
                 '示例：`"yz"` → `2`；本视频：`"yazyd"` → `23`'],
        quote='有一些人站在一维数轴上，b 站在最左边，z 站在最右边。目标是让所有人都移动到 z+1 的位置。',
        quote_src='—— 灵茶山艾府题解',
        idea=['同一个字母的所有位置一起动，前进的路径上的字母会被带着合并',
              '最小的非 `a` 字母走到 `z+1`，更大的字母顺路就到了',
              '全是 `a` 时 `min` 取默认值 `{`，距离恰好是 0'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`a` 不用动，必须先排除再取最小',
                 '`z` 的下一个字符是 `{`，所以用 `ord(\'{\') - ord(min_c)`',
                 '题解先给出不带提前退出的写法；视频用优化版：发现 `b` 直接返回 25'],
    ),
)
