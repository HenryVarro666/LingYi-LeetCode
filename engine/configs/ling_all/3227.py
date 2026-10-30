V = 'aeiou'


def _col(S, i, v):
    return 'green' if v in V else None


def _dim(S, i, v):
    return v not in V


def _case(S):
    s = S['s']
    k = sum(ch in V for ch in s)
    if k == 0:
        return '没有元音：小红第一步就无法操作 → 小红输'
    if k % 2:
        return f'`{k}` 个元音（奇数）：小红一次移除整个字符串 → ==小红赢=='
    return f'`{k}` 个元音（正偶数）：小红留下奇数个 → 小明怎么删都剩奇数 → ==小红赢=='


def _line2(S):
    s = S['s']
    k = sum(ch in V for ch in s)
    return f'元音个数 `{k}`；只要 ≥ 1，答案就是 `true`'


CONFIG = dict(
    num=3227, title='字符串元音游戏', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='博弈 · 奇偶分类讨论',
    tags=['灵神题单·数学算法', '难度分 1452'],
    code='''
class Solution:
    def doesAliceWin(self, s: str) -> bool:
        return any(c in s for c in "aeiou")
''',
    call='Solution().doesAliceWin("leetcoder")',
    expect=True,
    views=[
        dict(type='string', var='s', color=_col, label='s（绿色 = 元音）', h=260),
        dict(type='text', fn=_case, size=28, h=110),
        dict(type='text', fn=_line2, size=28, h=100),
    ],
    watch=[],
    captions={
        'return any': lambda S, B, ret: (
            f'`any(c in s for c in "aeiou")`：依次问 a、e、i、o、u 是否出现在 `s` 里，'
            f'`leetcoder` 含 e → ==有元音== → 小红必赢，返回 `{ret}`'),
    },
    cards=dict(
        one_liner='有元音小红必赢，没有元音小红必输',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['小红先手，必须移除含==奇数==个元音的非空子串；小明必须移除含==偶数==个元音的非空子串',
                 '无法操作的人输。两人都最优，问小红能否获胜',
                 '示例：`leetcoder` → `true`；`bbcd` → `false`'],
        quote='如果 s 包含正偶数个元音，由于偶数减奇数等于奇数，小红移除任意包含奇数个元音的子串后，剩余元音个数仍然为奇数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['没有元音：小红没得删 → 输。奇数个元音：整串一次删光 → 赢',
              '正偶数个：小红删一个奇数元音的子串，剩下奇数个；小明只能删偶数个，还是剩奇数个',
              '轮到小红时总是奇数个元音，整串删光即可 → 只要有元音就赢'],
        after=[dict(heading='用 leetcoder 走一遍', lines=['`leetcoder` 有 e、e、o、e 共 `4` 个元音（正偶数）',
                                                     '小红删 `leetcoder` 整串？不行，4 是偶数；她删含 3 个元音的子串，剩 1 个元音',
                                                     '小明只能删含偶数个元音的子串，唯一的元音删不掉，只能删辅音',
                                                     '轮到小红：剩的字符串含 1 个元音，整串删光 → ==小红赢=='])],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '关键是奇偶性：奇数 − 偶数 = 奇数，小明永远无法把元音删光',
                 '写法二：`any(c in "aeiou" for c in s)`，遍历 s 一遍，同样正确',
                 '思考题：小明先手时结论怎么变？（先想想对称的奇偶分析）'],
    ),
)
