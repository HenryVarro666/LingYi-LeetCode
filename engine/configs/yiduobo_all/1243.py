def _cmp(S, B, ret):
    g, i = S.g, S.index
    a, b, c = g[i - 1], g[i], g[i + 1]
    if b > a and b > c:
        return f'`{b}` 比左 `{a}` 和右 `{c}` ==都大== → 局部最大，减 1 变成 `{b - 1}`，标记 `change`'
    return f'`{b}` 不比左右两边都大 → 看是不是局部最小'


def _cmp2(S, B, ret):
    g, i = S.g, S.index
    a, b, c = g[i - 1], g[i], g[i + 1]
    if b < a and b < c:
        return f'`{b}` 比左 `{a}` 和右 `{c}` ==都小== → 局部最小，加 1 变成 `{b + 1}`，标记 `change`'
    return f'`{b}` 既不是局部最大也不是最小 → 保持不变'


def _col(S, i, v):
    if 'index' not in S or 'g' not in S:
        return None
    return None


CONFIG = dict(
    num=1243, title='数组变换', difficulty='Easy', category='模拟',
    author='yiduobo', technique='按规则直接模拟',
    code='''
class Solution(object):
    def transformArray(self, arr):

        f = arr[:]
        n = len(f)
        change = True
        while change:
            change = False
            g = f[:]
            f = []

            for index in range(n):
                if index == 0 or index == n - 1:
                    f.append(g[index])
                elif g[index] > g[index - 1] and g[index] > g[index + 1]:
                    f.append(g[index] - 1)
                    change = True
                elif g[index] < g[index - 1] and g[index] < g[index + 1]:
                    f.append(g[index] + 1)
                    change = True
                else:
                    f.append(g[index])
        
        return f
''',
    call='Solution().transformArray([6, 2, 3, 4, 1])',
    expect=[6, 3, 3, 3, 1],
    views=[
        dict(type='array', var=lambda S: S.get('g'), label='g（上一轮的数组：只看它来判断，不能边改边看）', cell=96, h=250,
             pointers={'index': 'blue'},
             color=lambda S, i, v: 'blue' if S.get('index') == i and S.get('_line', 0) >= 13 else None),
        dict(type='array', var='f', label='f（这一轮新生成的数组；绿 = 刚被加 1 或减 1）', cell=96, h=250,
             color=lambda S, i, v: ('green' if S.get('g') is not None and i < len(S['g']) and S['g'][i] != v else None) if 'f' in S else None),
        dict(type='text', h=100, fn=lambda S: ('这一轮有数被修改，`change = True`，还要再来一轮' if S.get('change') and S.get('_line', 0) >= 13 else '这一轮还没有改动' if 'change' in S and S.get('g') is not None and S.get('_line', 0) >= 13 else '')),
    ],
    watch=['index', 'change', ('f', 'f', 'green')],
    captions={
        'f = arr[:]': '复制一份，不改原数组：`f = {f}`',
        'n = len': '数组长度 `n = {n}`',
        6: '`change` 记录这一轮有没有数被改；先设为 `True` 进入循环',
        'while change': lambda S, B, r: '上一轮有改动 → ==继续下一轮==' if S.change else '上一轮没有任何改动 → 数组稳定了，结束',
        'change = False': '新一轮开始，先假设没有改动',
        'g = f[:]': '`g` = 上一轮的结果，这一轮只读 `g`：`{g}`',
        'f = []': '`f` 清空，这一轮往里逐个放新值',
        'for index': lambda S, B, r: f'这一轮的下标都处理完了，`f = {S.f}`' if B.get('index') == S.index == S.n - 1 else f'处理下标 `{S.index}`',
        'if index == 0': lambda S, B, r: f'下标 `{S.index}` 是首/尾 → ==永远不变==，直接复制' if S.index in (0, S.n - 1) else f'下标 `{S.index}` 是中间元素，要和左右邻居比较',
        'f.append(g[index])': lambda S, B, r: f'不变：把 `g[{S.index}] = {S.g[S.index]}` 放进 `f`',
        'g[index] > g[index - 1]': _cmp,
        'g[index] < g[index - 1]': _cmp2,
        'f.append(g[index] - 1)': '`f` 放入 `{g[index]} - 1 = {g[index] - 1}`',
        'f.append(g[index] + 1)': '`f` 放入 `{g[index]} + 1 = {g[index] + 1}`',
        17: '本轮有改动 → `change = True`，下一轮还得再看',
        20: '本轮有改动 → `change = True`，下一轮还得再看',
        'return f': '一轮下来没有变化 → 稳定，返回 `{f}`',
    },
    skip=[],
    max_steps=110,
    cards=dict(
        one_liner='数据很小，照着规则一轮一轮模拟，直到不再变化',
        complexity='轮数 ≤ 值域范围，每轮 `O(n)`；空间 `O(n)`',
        problem=['每一天，对除首尾外的元素：比左右邻居==都大==则减 1，==都小==则加 1，其余不变',
                 '一直重复到某一天不再有变化，返回最终数组',
                 '本视频：`[6,2,3,4,1]` → `[6,3,3,3,1]`'],
        quote='感觉应该可以通过数学和单调性分析直接得到最终答案，但是没有什么好的思路，不过好在本题的数据规模较小，因此可以直接按照题目的规则进行模拟。',
        quote_src='—— yiduobo 题解原文',
        idea=['每一轮从 `g`（旧数组）读、往新数组 `f` 写，保证同一天里互不影响',
              '`change` 标志这一轮有没有改动，没改动就稳定了',
              '首尾元素没有两个邻居，永远不变'],
        summary=['时间 `O(n·轮数)`，空间 `O(n)`',
                 '==必须用旧数组 g 判断==：边改边比较会让同一天里后面的判断被污染',
                 '首尾元素直接复制，别越界访问 `g[-1]` 或 `g[n]`',
                 '原文没有用到整数除法等 Python 2 写法，代码照搬运行'],
    ),
)
