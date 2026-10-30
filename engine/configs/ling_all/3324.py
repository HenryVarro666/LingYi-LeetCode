T = 'bca'


def _screen(S):
    if 's' not in S:
        return '屏幕上的字符串 = `s` 拼起来；每个位置只能从 `a` 加到目标字母'
    scr = ''.join(S['s'])
    return f'屏幕：`{scr}`　　目标：`{S["target"]}`'


CONFIG = dict(
    num=3324, title='出现在屏幕上的字符串序列', difficulty='Medium', category='字符串',
    author='灵茶山艾府', technique='模拟 · 枚举最后一位',
    tags=[],
    code='''
class Solution:
    def stringSequence(self, target: str) -> List[str]:
        ans = []
        s = []
        for c in target:
            s.append('')  # 占位
            for s[-1] in ascii_lowercase[:ord(c) - ord('a') + 1]:
                ans.append(''.join(s))
        return ans
''',
    call=f'Solution().stringSequence({T!r})',
    expect=['a', 'b', 'ba', 'bb', 'bc', 'bca'],
    views=[
        dict(type='string', var='target', label='target（蓝框 = 正在输入的位置）', cell=96, h=170,
             pointers={'len(s) - 1': 'blue'}),
        dict(type='text', h=100, size=32, fn=_screen),
        dict(type='array', var='ans', label='ans（出现过的字符串）', cell=110, h=200),
    ],
    watch=[('c', 'c', 'blue'), ('s', "''.join(s)", 'yellow'), ('len(ans)', 'len(ans)', 'green')],
    captions={
        'ans = []': '`ans` 记录屏幕上依次出现的每个字符串',
        's = []': '`s` 存屏幕上每个位置的字符，只能往后加，改不了左边',
        'for c in target': '要输入 `target` 的下一个字母 `c = {c}`：前面的字母已经定死了',
        "s.append('')": '先按键 1 追加一个位置，下面会从 `a` 开始改它',
        'for s[-1] in': lambda S, B, r: (f'这一位已经枚举到 `{S.c}`，循环结束 → 去输入下一个字母' if ''.join(S.s) in S.ans
                                        else f'最后一位变成 `{S.s[-1]}`（`a` 到 `{S.c}` 逐个往后按键 2）'),
        'ans.append': '屏幕现在是 `{"".join(s)}`，记入答案，一共 `{len(ans)}` 个',
        'return ans': '操作唯一，模拟完毕，共 `{len(ans)}` 个字符串',
    },
    cards=dict(
        one_liner='只能改最后一位，所以操作方式唯一，直接模拟',
        complexity='时间 `O(|Σ|n^2)`，空间 `O(n)`',
        problem=['键盘只有两个键：追加 `a`、把最后一个字符变成下一个字母',
                 '求输入 `target` 时屏幕上依次出现的所有字符串（按键最少）',
                 '示例：`target = "he"` → `a, b, ... h, ha, ... he`'],
        quote='注意我们只能添加字母，不能删除字母，也不能修改最后一个字母左边的字母，所以只有把第一个字母改成和 target[0] 一样后，才能继续向后添加/修改字母。',
        quote_src='—— 灵茶山艾府题解',
        idea=['左边的字母改不了，只能一位一位定下来',
              '每一位：先追加 `a`，再逐个按 +1 直到目标字母',
              '用 `for s[-1] in ...` 直接枚举最后一位，每次拼接一次进答案'],
        summary=['时间 `O(|Σ|n^2)`：每个字符串拼接要 `O(n)`，|Σ| = 26',
                 '`for s[-1] in ...` 把循环变量直接写进列表末尾，是这份代码的巧妙处',
                 '字母 `z` 不需要绕回 `a`：从 `a` 往上走最多到目标字母',
                 '同类：按位模拟构造序列的题'],
    ),
)
