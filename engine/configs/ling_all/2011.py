def _sign(S):
    ops = S['operations']
    parts = [('+1' if s[1] == '+' else '-1') for s in ops]
    return '  '.join(f'`{s}`→=={p}==' for s, p in zip(ops, parts)) + f'  合计 = =={sum(1 if s[1] == "+" else -1 for s in ops)}=='


CONFIG = dict(
    num=2011, title='执行操作后的变量值', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='看中间字符 · 一行求和',
    tags=[],
    code='''
class Solution:
    def finalValueAfterOperations(self, operations: List[str]) -> int:
        return sum(1 if s[1] == '+' else -1 for s in operations)
''',
    call="Solution().finalValueAfterOperations(['--X', 'X++', 'X++', '++X', 'X--'])",
    expect=1,
    views=[
        dict(type='array', var='operations', h=200, label='operations'),
        dict(type='text', fn=_sign, size=28, h=200),
    ],
    watch=[],
    captions={
        'return sum': '遍历每个操作 `s`：中间字符 `s[1]` 是 `+` 就加 1，是 `-` 就减 1；全部求和得 ==`{ret}`==',
    },
    cards=dict(
        one_liner='四种写法的中间字符，决定了加还是减',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['变量 `X` 初始为 0，操作有 `++X`、`X++`、`--X`、`X--`',
                 '`++` 加 1，`--` 减 1，求执行完所有操作后的 `X`',
                 '示例：`["--X","X++","X++"]` → `1`'],
        quote='根据题意，对每个操作 s=operations[i]，如果中间字符 s[1] 是 + 号，把答案加一，否则把答案减一。',
        quote_src='—— 灵茶山艾府题解',
        idea=['前缀 `++X` 与后缀 `X++`，中间字符都是 `+`',
              '前缀 `--X` 与后缀 `X--`，中间字符都是 `-`',
              '所以只看 `s[1]`，一行 `sum` 搞定'],
        after=[dict(heading='附：趣味写法', lines=[
            '`int(s[1] + "1")`：把中间字符拼上 `"1"`',
            '`"+1"` 转成 `+1`，`"-1"` 转成 `-1`',
            '效果和 `1 if ... else -1` 完全一样'])],
        before=[dict(heading='四种操作的中间字符', lines=[
            '`++X` 的中间是 `+`，`X++` 的中间也是 `+`',
            '`--X` 的中间是 `-`，`X--` 的中间也是 `-`',
            '长度恒为 3，所以 `s[1]` 一眼就能判断'])],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '不用区分前缀和后缀：`X` 的最终值与顺序无关',
                 '题解还给了趣味写法：`sum(int(s[1] + "1") for s in operations)`'],
    ),
)
