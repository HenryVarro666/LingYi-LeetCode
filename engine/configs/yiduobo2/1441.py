TARGET = [2, 5, 6]


def _nums_color(S, i, v):
    if 'last' not in S:
        return None
    last, num, ln = S['last'], S.get('num'), S.get('_line')
    if num is not None and ln in (5, 6, 7):
        if v == num:
            return 'yellow'
        if last < v < num:
            return 'red'
    if v <= last:
        return 'green' if v in S['target'] else None
    return None


def _nums_dim(S, i, v):
    return 'last' in S and v <= S['last'] and v not in S['target']


def _formula(S):
    if 'num' not in S or S.get('_line') not in (5, 6, 7):
        if 'last' in S:
            return f"`last = {S['last']}`：上一个 target 里的数"
        return ''
    k = S['num'] - S['last'] - 1
    return (f"`{S['last']}` 和 `{S['num']}` 之间有 `{S['num']} − {S['last']} − 1 = {k}` 个空白数字"
            f" → ==每个都要 Push + Pop==")


def _for(S, B, ret):
    if 'num' not in B or S.num != B.num:
        return f'下一个想要的数 `num = {S.num}`'
    return 'target 处理完'


def _extend(S, B, ret):
    k = S.num - S.last - 1
    if k == 0:
        return f'`{S.last}` 和 `{S.num}` 相邻，没有空白数字：`["Push", "Pop"] * 0` 什么也不加'
    return f'空白数字 {k} 个：一次性加入 `["Push", "Pop"] * {k}`'


CONFIG = dict(
    num=1441, title='用栈操作构建数组', difficulty='Medium', category='栈',
    author='yiduobo', technique='一趟扫描 · 数相邻两数间的空白',
    tags=['字节30天'],
    code='''
class Solution(object):
    def buildArray(self, target, n):
        last = 0
        res = []
        for num in target:
            res.extend(["Push", "Pop"] * (num - last - 1))
            res.append("Push")
            last = num

        return res
''',
    call=f'Solution().buildArray({TARGET}, 6)',
    expect=['Push', 'Pop', 'Push', 'Push', 'Pop', 'Push', 'Pop', 'Push', 'Push'],
    views=[
        dict(type='array', var=lambda S: list(range(1, S['target'][-1] + 1)),
             label='数字 1 … target[-1]（红 = 两数之间的空白数字，黄 = num）', cell=90,
             color=_nums_color, dim=_nums_dim),
        dict(type='array', var='target', label='target', cell=90, h=210, pointers={'target.index(num)': 'yellow'},
             pointer_labels={'target.index(num)': 'num'}),
        dict(type='text', fn=_formula, h=60, size=25),
        dict(type='array', var='res', label='res（操作序列）', cell=100, h=150),
    ],
    watch=[('last', 'last', 'green'), ('num', 'num', 'yellow')],
    captions={
        'last = 0': '`last`：上一个出现在 target 里的数，一开始当作 0',
        'res = []': '`res` 记录操作序列',
        'for num in target': _for,
        'res.extend': _extend,
        'res.append("Push")': '`{num}` 本身在 target 中：再加一个 `"Push"`，留在栈里',
        'last = num': '`last = {last}`',
        'return res': '返回 `{ret}`',
    },
    cards=dict(
        one_liner='相邻两个 target 数之间有几个空白数字，就补几组 Push+Pop',
        complexity='时间 `O(target[-1])`，空间 `O(1)`（返回值不计）',
        problem=['给数组 `target` 和整数 `n`，从流 `1..n` 依次读数，用 `"Push"`/`"Pop"` 使栈（底→顶）等于 `target`',
                 '读到的数必须先 Push；栈等于 `target` 后立刻停止',
                 '示例：`target = [1,3], n = 3` → `["Push","Push","Pop","Push"]`',
                 '本视频：`target = [2,5,6], n = 6`'],
        quote='对于target中出现的数字，需要在答案中加入一个push，否则需要在答案中加入一个push和一个pop。于是可以==统计两个相邻数字之间空白数字的数目==。',
        quote_src='—— yiduobo 题解',
        idea=['不在 target 里的数（空白数字）：`"Push", "Pop"` 各一次',
              '`last` 与 `num` 之间有 `num − last − 1` 个空白数字 → 用列表乘法==一次性批量加入==',
              '再为 `num` 自己加一个 `"Push"`'],
        result='`["Push","Pop","Push","Push","Pop","Push","Pop","Push","Push"]` ✓',
        summary=['时间 `O(target[-1])`：输出长度就是这么多；空间 `O(1)`',
                 '`last` 初始为 0，这样 1 之前的空白也能统一处理',
                 '和灵神逐个读数的写法等价，这里按 target 的数==成段处理==',
                 '原文为 Python 2 风格，仅删去 docstring，代码未改'],
    ),
)
