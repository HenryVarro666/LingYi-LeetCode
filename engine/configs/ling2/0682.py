OPS = ["5", "-2", "4", "C", "D", "9", "+"]   # 示例 2 去掉最后一个 "+"，让每个操作互不相同，便于定位
IDX = 'operations.index(op)'


def _idx(S):
    return S['operations'].index(S['op']) if 'op' in S else -1


def _kind(op):
    return {'+': '+', 'D': 'D', 'C': 'C'}.get(op, 'num')


def cap_if(word, kind):
    def f(S, B, ret):
        op = S.op
        if _kind(op) == kind:
            return f'`op = "{op}"` ==是== `{word}` → 执行这个分支'
        if kind == 'C' and _kind(op) == 'num':
            return f'`"{op}"` 也不是 `"C"` → 三种符号都不是，走 `else`：==它是整数=='
        return f'`"{op}"` 不是 `{word}` → 看下一个分支'
    return f


def show(S):
    k = _idx(S)
    st = S.get('st')
    if st is None:
        return '记录从空列表开始'
    if k < 0:
        return f'记录 `{st}`，总和 `{sum(st)}`'
    op = S['op']
    ln = S.get('_line')
    if ln in (6, 8, 10, 12):
        rule = {'+': '后两项之和加到末尾', 'D': '最后一项的两倍加到末尾', 'C': '去掉最后一项'}.get(op, '把整数加到末尾')
        return f'`"{op}"`：{rule}'
    return f'记录 `{st}`'


CONFIG = dict(
    num=682, title='棒球比赛', difficulty='Easy', category='栈',
    author='灵茶山艾府', technique='用列表（栈）模拟四种操作',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution:
    def calPoints(self, operations: List[str]) -> int:
        st = []
        for op in operations:
            if op == '+':
                st.append(st[-2] + st[-1])
            elif op == 'D':
                st.append(st[-1] * 2)
            elif op == 'C':
                st.pop()
            else:
                st.append(int(op))
        return sum(st)
''',
    call=f'Solution().calPoints({OPS!r})',
    expect=13,
    views=[
        dict(type='array', var='operations', label='operations（操作序列）', cell=100,
             pointers={IDX: 'blue'}, pointer_labels={IDX: 'op'},
             dim=lambda S, i, v: 'op' in S and i < _idx(S),
             color=lambda S, i, v: 'blue' if i == _idx(S) else None),
        dict(type='stack', var='st', label='st（有效得分记录，栈顶在右）', h=150, font=30),
        dict(type='text', fn=show, size=28, h=100),
    ],
    watch=[('op', 'op', 'blue'), ('st', 'st', 'green'), ('sum(st)', 'sum(st)', 'yellow')],
    captions={
        'st = []': '用列表 `st` 当栈，记录==每一回合的有效得分==',
        'for op in operations': lambda S, B, ret: (f'处理第 `{_idx(S)}` 个操作 `"{S.op}"`'
                                                    if 'op' not in B or B.op != S.op else '所有操作处理完毕'),
        "if op == '+'": cap_if('"+"', '+'),
        "elif op == 'D'": cap_if('"D"', 'D'),
        "elif op == 'C'": cap_if('"C"', 'C'),
        'st.append(st[-2] + st[-1])': '操作二：后两项 `{B.st[-2]} + {B.st[-1]}` = =={st[-1]}==，加到末尾',
        'st.append(st[-1] * 2)': '操作三：最后一项 `{B.st[-1]}` 的两倍 = =={st[-1]}==，加到末尾',
        'st.pop()': '操作四：上一次得分 `{B.st[-1]}` 无效 → ==直接弹出栈顶==',
        'st.append(int(op))': lambda S, B, ret: (f'操作一：字符串 `"{S.op}"` 转成整数 `{S.st[-1]}` 加到末尾'
                                                 + ('（==负数也能直接 int==）' if S.st[-1] < 0 else '')),
        'return sum(st)': '遍历结束，返回记录中所有得分之和 =={ret}==',
    },
    cards=dict(
        one_liner='四种操作都只碰最后一两项 → 用列表当栈模拟',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`ops[i]` 是整数 `x`（得 x 分）、`"+"`（前两次得分之和）',
                 '`"D"`（前一次得分的两倍）或 `"C"`（前一次得分作废）',
                 '示例：`["5","2","C","D","+"]` → 记录 `[5,10,15]`，返回 `30`',
                 '本视频用 `["5","-2","4","C","D","9","+"]` → `13`'],
        quote='遍历 operations，用列表（或者栈）模拟题目的四个操作……遍历结束后，返回列表中的元素之和。',
        quote_src='—— 灵茶山艾府题解',
        idea=['操作一：把 `x` 加到列表末尾；操作二：后两项之和加到末尾',
              '操作三：最后一项的两倍加到末尾；操作四：去掉最后一项',
              '所有操作只看==列表末尾== → 列表就是一个栈'],
        result='记录 `[5, -2, -4, 9, 5]`，总和 `13` ✓',
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：`"C"` 删掉的得分，后面的 `"+"`、`"D"` ==不能再用到它==',
                 '易错：`"-2"` 是负数，不能用首字符判断是不是操作符；放到 `else` 里 `int()` 最省事',
                 '`"+"` 用的是 `st[-2] + st[-1]`，不是弹出再压回'],
    ),
)
