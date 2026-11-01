S0 = 'at 7 51 pm 50 60'


def _tok(S):
    return S['s'].split(' ') if 's' in S else None


def _col(S, i, v):
    if 'token' not in S:
        return None
    toks = _tok(S)
    cur = toks.index(S['token'])
    if i == cur:
        return 'blue'
    if i < cur and v[0].isdigit():
        return 'green'
    return None

CONFIG = dict(
    num=2042, title='检查句子中的数字是否递增', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='分割后维护上一个数字（Go 原文转写）',
    tags=[],
    code='''
class Solution:
    def areNumbersAscending(self, s: str) -> bool:
        prev = 0
        for token in s.split(" "):
            if token[0].isdigit():
                v = int(token)
                if v <= prev:
                    return False
                prev = v
        return True
''',
    call=f'Solution().areNumbersAscending({S0!r})',
    expect=False,
    views=[
        dict(type='text', h=70, size=30,
             fn=lambda S: (f"`token = '{S['token']}'`，上一个数字 `prev = {S['prev']}`" + (f"，`v = {S['v']}`" if 'v' in S else '')) if 'token' in S else '`prev = 0`：比任何正数都小'),
        dict(type='array', var=_tok, label='s.split(" ")（蓝 = 当前 token，绿 = 已通过的数字）', cell=100, h=260,
             pointers={"s.split(' ').index(token)": 'blue'}, pointer_labels={"s.split(' ').index(token)": 'token'},
             color=_col),
    ],
    watch=[('token', 'token', 'blue'), ('v', 'v', 'cyan'), ('prev', 'prev', 'orange')],
    captions={
        'prev = 0': '`prev` 记上一个数字；数字都是正整数，初始 0 就够小',
        'for token in': '按空格切开，逐个看：`token = "{token}"`',
        'token[0].isdigit()': lambda S, B, ret: (f"首字符 `'{S.token[0]}'` 是数字 → 整个 token 是数字" if S.token[0].isdigit()
                                                 else f"首字符 `'{S.token[0]}'` 是字母 → 是单词，跳过"),
        'v = int(token)': '转成整数：`v = {v}`',
        'if v <= prev': lambda S, B, ret: (f'`v = {S.v} <= prev = {S.prev}` → ==不是严格递增==' if S.v <= S.prev
                                           else f'`v = {S.v} > prev = {S.prev}` → 仍然严格递增'),
        'return False': '出现 `v <= prev`（相等也不行）→ 返回 `False`',
        'prev = v': '更新 `prev = {prev}`，下一个数字要比它大',
        'return True': '全部数字都严格递增 → 返回 `True`',
    },
    cards=dict(
        one_liner='从左到右扫，只要有数字不大于上一个就失败',
        complexity='时间 `O(n)`，空间 `O(n)`（切分结果）',
        problem=['句子由单词和不含前导零的正整数 token 组成，用单个空格分隔',
                 '检查句中所有数字是否从左到右==严格递增==',
                 '示例：`"hello world 5 x 5"` → `false`；本视频用 `"at 7 51 pm 50 60"`'],
        idea=['`prev` 初始为 0，数字都是正数',
              '只看每个 token 的首字符：数字 token 一定全是数字',
              '`v <= prev` 立刻返回 `False`，否则更新 `prev`'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`unicode.IsDigit` → `str.isdigit`，`strconv.Atoi` → `int`）',
                 '时间 `O(n)`，空间 `O(n)`',
                 '易错：相等也不是严格递增，所以是 `v <= prev`',
                 '题目保证数字不含前导零且至少两个数字，所以首字符判断足够'],
    ),
)
