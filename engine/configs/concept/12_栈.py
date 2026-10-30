TEMPS = [73, 74, 75, 71, 69, 72, 76, 73]


_cnt = {}


def _once(key):
    _cnt[key] = _cnt.get(key, 0) + 1
    return _cnt[key] == 1


def _color(S, i, v):
    if 'st' in S and i in S['st']:
        return 'purple'                       # 在栈里：还没找到答案
    if 'ans' in S and S['ans'][i] > 0:
        return 'green'                        # 已经找到答案
    return None


def _formula(S):
    if 'st' not in S:
        return '单调栈：栈里存 ==还没找到答案的下标==（todolist）'
    if 'i' in S and S['st'] and S.get('t') is not None:
        top = S['st'][-1]
        return (f"今天 `t = {S['t']}`，栈顶 `{top}` 的温度 `{S['temperatures'][top]}`"
                + ('，`t` 更大 → 栈顶找到答案' if S['t'] > S['temperatures'][top] else '，`t` 不更大 → 停'))
    return f"紫色 = 栈里的 todolist，绿色 = 已经算出答案"


CONFIG = dict(
    num=None, title='栈 · 通用思想与模板', author='概念讲解', category='栈',
    technique='通用思想与模板', kind='concept', difficulty='',
    code='''
def daily_temperatures(temperatures):  # 739. 每日温度
    n = len(temperatures)
    ans = [0] * n
    st = []                          # todolist：还没找到答案的下标
    for i, t in enumerate(temperatures):
        while st and t > temperatures[st[-1]]:  # t 比栈顶高
            j = st.pop()             # 栈顶的答案找到了
            ans[j] = i - j
        st.append(i)                 # i 等后面的人来回答
    return ans
''',
    call=f'daily_temperatures({TEMPS})',
    expect=[1, 1, 4, 2, 1, 1, 0, 0],
    views=[
        dict(type='text', fn=_formula, h=60),
        dict(type='bars', var='temperatures', label='temperatures（紫 = 在栈里，绿 = 已有答案）', pointers={'i': 'pink'},
             color=_color, vmax=80, h=300),
        dict(type='stack', var='st', label='st', fmt=lambda j: f'{j}:{TEMPS[j]}°', h=110),
        dict(type='array', var='ans', label='ans（等几天才有更高温度）', cell=70, h=150),
    ],
    watch=[('i', 'i', 'pink'), ('t', 't'), ('j', 'j', 'green')],
    captions={
        'n = len': '一共 `{n}` 天，求每天要等几天才会更暖和',
        'ans = [0] * n': '`ans` 先全填 0：找不到更高温度的那天保持 0',
        'st = []': '`st` 是 ==todolist==：存还不知道答案的下标，从底到顶温度递减',
        'for i, t': lambda S, B, ret: (f'第 `{S.i}` 天，温度 `t = {S.t}`' if B.get('i') != S.i else '所有天都处理完了'),
        'while st and t >': lambda S, B, ret: (
            '栈是空的，没有要回答的人' if not S.st else
            (f'`{S.t} > {S.temperatures[S.st[-1]]}`：今天比第 `{S.st[-1]}` 天暖和 → 它的答案找到了'
             if S.t > S.temperatures[S.st[-1]] else
             f'`{S.t} ≤ {S.temperatures[S.st[-1]]}`：栈顶不比今天冷，停止弹出')),
        'j = st.pop()': lambda S, B, ret: (f'弹出第 `{S.j}` 天：它的下一个更高温度就是今天——==之后它就是无用数据=='
                                           if _once('pop') else f'弹出第 `{S.j}` 天，它的答案是今天'),
        'ans[j] = i - j': '`ans[{j}] = {i} - {j} = {ans[j]}`',
        'st.append(i)': lambda S, B, ret: ((f'第 `{S.i}` 天入栈，等后面更暖和的一天来回答' if _once('push') else f'第 `{S.i}` 天入栈')
                                           + (f'；栈从底到顶 `{[S.temperatures[k] for k in S.st]}` 递减' if len(S.st) >= 3 else '')),
        'return ans': '返回 `{ret}`：每个下标最多入栈、出栈各一次，==O(n)==',
    },
    cards=dict(
        one_liner='后进先出；单调栈 = 及时去掉无用数据，让栈保持有序',
        complexity='时间 `O(n)`（每个元素进出栈各一次），空间 `O(n)`',
        problem_heading='什么时候用？',
        problem=['括号匹配、嵌套结构（编码字符串）→ 普通栈，后进先出',
                 '求每个元素的 ==下一个 / 上一个更大（更小）== 元素 → 单调栈',
                 '以每根柱子为高的最大矩形、接雨水 → 单调栈找左右边界',
                 '要 `O(1)` 拿到栈里的最小值 → 辅助栈同步记录'],
        before=[dict(heading='核心概念：单调栈 = 及时去掉无用数据', lines=[
            '栈里存 ==还没找到答案== 的下标，栈底到栈顶温度递减',
            '新元素 `t` 比栈顶大 → 栈顶的答案就是它，弹出',
            '被弹出的元素已经有答案，以后再也用不到——无用数据',
            '每个下标最多入栈、出栈各一次 → 两层循环也是 `O(n)`']),
        ],
        idea_heading='两位作者怎么说',
        quote='栈中记录还没算出下一个更大元素的那些数的下标。相当于==栈是一个 todolist==，在循环的过程中，现在还不知道答案是多少，在后面的循环中会算出答案。',
        quote_src='—— 灵茶山艾府 · 739. 每日温度',
        idea=['yiduobo 739：比 `T[p]` 小的位置答案就是 `p`，剩下的 ==必然 ≥ T[p]== → 单调栈',
              '灵神：「==去掉无用数据==」的想法和单调栈一样（300 题注）',
              '普通栈：yiduobo 20「左括号压栈、右括号配对」，155 用辅助栈存最小值'],
        summary_heading='本类 Hot100 题目 & 学习顺序',
        summary=['`20` 有效的括号：左括号入栈，右括号和栈顶配对',
                 '`155` 最小栈：辅助栈同步存「当前最小值」',
                 '`394` 字符串解码：遇 `[` 压栈保存现场，遇 `]` 弹栈拼接',
                 '`739` 每日温度：单调栈，栈是 todolist',
                 '`84` 柱状图中最大的矩形：单调栈找左右第一个更矮的柱子',
                 '易错：20 结束时栈必须为空；单调栈里存 ==下标== 而不是值'],
    ),
)
