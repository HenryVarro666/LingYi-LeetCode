SETUP = '''
class _Ch(str):
    pass

class _S(str):
    def __iter__(self):
        for k, c in enumerate(str.__str__(self)):
            x = _Ch(c)
            x.idx = k
            yield x
'''


def _idx(S):
    c = S.get('b')
    return getattr(c, 'idx', None) if c is not None else None


def _color(S, i, v):
    k = _idx(S)
    if k is None:
        return None
    if i == k:
        return 'blue'
    return None


def _txt(S):
    if 'c' not in S:
        return ''
    k = _idx(S)
    if k is None:
        return f"`c = {S['c']}`"
    return f"`c = {S['c']}`（c 为 0 时遇到 `]` 就当作左括号）；最终答案 = c // 2"


CONFIG = dict(
    num=1963, title='使字符串平衡的最小交换次数', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='前缀计数 · 最后 c // 2',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1689'],
    setup=SETUP,
    code='''
class Solution:
    def minSwaps(self, s: str) -> int:
        c = 0
        for b in s:
            if b == '[' or c == 0:
                c += 1
            else:
                c -= 1
        return c // 2
''',
    call='Solution().minSwaps(_S("]]][[["))',
    expect=2,
    views=[
        dict(type='text', fn=_txt, size=26),
        dict(type='string', var='s', label='s（蓝 = 当前括号）', cell=84, color=_color, h=200),
        dict(type='text', fn=lambda S: ('这一步：`c == 0` 却遇到 `]` → ==把它换成 `[`==，c + 1，相当于做了一次交换' if S.get('b') == ']' and S.get('c') == 1 and S.get('_line') == 6 else '平衡串的每个前缀里，`[` 的个数都不少于 `]`'), size=26),
    ],
    watch=[('b', 'b', 'blue'), ('c', 'c', 'pink')],
    captions={
        'c = 0': '`c` = 未匹配的左括号个数（左括号 +1，右括号 -1）',
        'for b in s': "取下一个括号：`b = '{b}'`",
        "if b == '['": lambda S, B, r: (f"`'{S.b}'` 是左括号，`c` 加一" if S.b == '[' else (f"`'{S.b}'` 是右括号，但 `c = {S.c}` 已经是 0 → 前面没有左括号可配，它==必须被换走==" if S.c == 0 else f"`'{S.b}'` 是右括号，`c = {S.c} > 0` → 有左括号可配")),
        'c += 1': lambda S, B, r: (f"`c` → {S.c}" if S.b == '[' else f"不真的交换，直接把这个 `]` 当成 `[`（相当于和最右边的 `[` 交换）：`c` → =={S.c}=="),
        'c -= 1': '右括号和一个未匹配的左括号配对：`c` → {c}',
        'return c // 2': '每次交换把一个 -1 变成 +1，使最终 `c` 多 2，所以交换次数 = `c // 2` = `{c} // 2` = =={ret}==',
    },
    max_steps=60,
    cards=dict(
        one_liner='右括号多了就换走，每次交换让 c 多 2，答案 c // 2',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`s` 由相同数量的 `[` 和 `]` 组成，可以任意交换两个位置的括号',
                 '返回使 `s` 成为平衡字符串的最少交换次数',
                 '示例：`]]][[[` → `2`'],
        quote='平衡字符串的任意一个前缀中，左括号的数量都大于等于右括号的数量。……这个右括号要换到最后面去，也就是找最右边的左括号交换。',
        quote_src='—— 灵茶山艾府题解',
        idea=['从左到右数未匹配的左括号 `c`；`c = 0` 时遇到右括号就出问题了',
              '必须把它和==最右边==的左括号交换（执行 -1 的时刻越晚越好）',
              '不用真交换：把这个 `]` 当成 `[`，`c` 反而 +1；每次交换让最终的 `c` 多 2，答案 `c // 2`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '题解先给了「模拟交换」，再去掉交换，最后去掉 `ans` 变量，本视频演示最简写法',
                 '易错：`b == "[" or c == 0` 的含义是 `c == 0` 时右括号也算作 +1',
                 '同类：1614、1249 等合法括号字符串（RBS）题'],
    ),
)
