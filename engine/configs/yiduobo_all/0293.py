CONFIG = dict(
    num=293, title='翻转游戏', difficulty='Easy', category='字符串',
    author='yiduobo', technique='一趟遍历找 ++',
    code='''
class Solution(object):
    def generatePossibleNextMoves(self, currentState):

        res = []
        n = len(currentState)
        for index in range(n - 1):
            if currentState[index] == currentState[index + 1] == '+':
                res.append(currentState[:index] + '--' + currentState[index + 2:])

        return res
''',
    call="Solution().generatePossibleNextMoves('+++-++')",
    expect=['--+-++', '+---++', '+++---'],
    views=[
        dict(type='string', var='currentState', label='currentState', h=190,
             pointers={'index': 'blue', 'index + 1': 'pink'}, window=('index', 'index + 1'),
             color=lambda S, i, v: 'green' if 'index' in S and S['index'] <= i <= S['index'] + 1 and S['currentState'][S['index']] == S['currentState'][S['index'] + 1] == '+' else None),
        dict(type='array', var='res', label='res（翻转一次后的所有可能）', h=170, cell=150),
    ],
    watch=[('n', 'n'), ('index', 'index', 'blue'), ('res', 'len(res)', 'green')],
    captions={
        'res = []': '`res` 用来装每一种翻转一次后的字符串',
        'n = len': '`n` = {n}，相邻两格要一起看，所以只枚举到 `n - 2`',
        'for index': '枚举相邻的一对：下标 `{index}` 和 `{index + 1}`',
        'if currentState[index]': lambda S, B, r: (
            f"`currentState[{S.index}]` = '{S.currentState[S.index]}'，`currentState[{S.index + 1}]` = '{S.currentState[S.index + 1]}'"
            + ('：连续两个 `+` → 这里可以翻转' if S.currentState[S.index] == S.currentState[S.index + 1] == '+' else '：不是连续的 `++` → 跳过')),
        'res.append': '把这一对换成 `--`：==前面 {currentState[:index]!r}== + `--` + ==后面 {currentState[index + 2:]!r}==，加入答案',
        'return res': '没有更多的 `++` 了，共 `{len(res)}` 种走法',
    },
    cards=dict(
        one_liner='找出每一对连续的 `++`，翻成 `--`，各得一种结果',
        complexity='时间 `O(n^2)`（每次拼接 `O(n)`），空间 `O(1)`（不含答案）',
        problem=['两人轮流把字符串里==连续两个 `++`== 翻成 `--`，无法操作的人输',
                 '本题只要求：给定 `currentState`，返回==一次操作后==所有可能的结果',
                 '示例：`++++` → `--++`、`+--+`、`++--`',
                 '本视频：`+++-++` → 三种结果'],
        quote='题目只要求找出一次操作后的字符串，那么只需一趟遍历，找出连续出现两次的加号，将其替换成减号后加入到答案数组中即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['不用博弈、不用递归，只看==一步==',
              '下标 `index` 与 `index + 1` 都是 `+` 就是一个可翻转位置',
              '用切片拼出新字符串：前段 + `--` + 后段，原串不变'],
        summary=['时间 `O(n^2)`：最多 `n-1` 个位置，每次切片拼接 `O(n)`',
                 '易错点：循环只到 `n - 2`，否则 `index + 1` 越界',
                 '`a == b == \'+\'` 是链式比较，等价于 `a == b and b == \'+\'`',
                 '原文为 Python 2 风格，本题代码无需改动'],
    ),
)
