TEMPS = [50, 60, 75, 45, 35, 55, 80, 60]


def _while_cap(S, B, ret):
    st, t, T = B.st, B.t, B.temperatures
    if not st:
        return '栈空 → 不用再弹'
    j = st[-1]
    if t >= T[j]:
        return f'栈顶 `{j}:{T[j]}` ≤ `t = {t}`：被 t ==挡住==，对左边的天永远没用 → 弹出'
    return f'栈顶 `{j}:{T[j]}` > `t = {t}` → 停止弹栈，它就是右边第一个更高的'


def _bar_color(S, i, v):
    if i == S.get('i'):
        return 'blue'
    if i in (S.get('st') or []):
        return 'purple'
    return None


def _bar_dim(S, i, v):
    cur = S.get('i')
    return cur is not None and i > cur and i not in (S.get('st') or [])


CONFIG = dict(
    num=739, title='每日温度', difficulty='Medium', category='栈',
    author='灵茶山艾府', technique='单调栈（从右到左）',
    code='''
class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        n = len(temperatures)
        ans = [0] * n
        st = []
        for i in range(n - 1, -1, -1):
            t = temperatures[i]
            while st and t >= temperatures[st[-1]]:
                st.pop()
            if st:
                ans[i] = st[-1] - i
            st.append(i)
        return ans
''',
    call=f'Solution().dailyTemperatures({TEMPS})',
    expect=[1, 1, 4, 2, 1, 1, 0, 0],
    skip=['n = len'],
    views=[
        dict(type='bars', var='temperatures', label='temperatures（紫 = 栈中候选项，灰 = 被挡住的）', h=360,
             pointers={'i': 'blue'}, color=_bar_color, dim=_bar_dim, vmax=85),
        dict(type='stack', var='st', label='st（存下标 i:温度）', fmt=lambda i: f'{i}:{TEMPS[i]}', h=120),
        dict(type='array', var='ans', label='ans（几天后升温）', cell=84, pointers={'i': 'blue'},
             color=lambda S, i, v: 'green' if S.get('i') is not None and i >= S['i'] and v > 0 else None),
    ],
    watch=[('i', 'i', 'blue'), ('t', 't'), ('st', 'st', 'purple')],
    captions={
        'ans = [0] * n': '`ans` 先全填 0：找不到更高温度时答案就是 0',
        'st = []': '栈中记录==下一个更大元素的候选项==的下标',
        'for i in range': lambda S, B, ret: (f'从右往左，处理第 `i = {S.i}` 天' if S.get('i') != B.get('i') or 'i' not in B
                                             else '所有天处理完毕'),
        't = temperatures[i]': '今天温度 `t = {t}`，去候选项里找答案',
        'while st and': _while_cap,
        'st.pop()': '弹出 `{B.st[-1]}`：比 `{t}` 矮或一样高，以后再也用不上',
        'if st:': lambda S, B, ret: (f'栈非空 → 栈顶 `{S.st[-1]}` 就是右边第一个比 `{S.t}` 高的' if S.st
                                     else '栈空 → 右边没有更高的温度，`ans` 保持 0'),
        'ans[i] = st[-1] - i': '`ans[{i}] = {st[-1]} - {i}` = =={ans[i]}== 天后升温',
        'st.append(i)': '`{i}` 入栈，成为左边的候选项（栈底→栈顶==温度递减==）',
        'return ans': '返回 `ans = {ret}`',
    },
    cards=dict(
        one_liner='从右往左，栈里只留“可能成为答案”的候选项',
        complexity='时间 `O(n)`，空间 `O(min(n, U))`',
        problem=['`temperatures[i]` 是第 `i` 天的温度',
                 '`answer[i]`：下一个更高温度出现在==几天后==，没有就填 0',
                 '示例：`[73,74,75,71,69,72,76,73]` → `[1,1,4,2,1,1,0,0]`'],
        quote='栈中记录下一个更大元素的「候选项」的下标。每次循环，我们可以在「候选项」中找到答案。',
        quote_src='—— 灵茶山艾府题解（写法一：从右到左）',
        idea=['从右往左看：如果 `t ≥ 栈顶温度`，栈顶被 `t` ==挡住==，左边的天看不到它',
              '所以弹出所有 `≤ t` 的候选项，剩下的栈顶就是答案',
              '再把 `i` 入栈 → 栈从底到顶温度==严格递减==（单调栈）'],
        result='`ans = [1,1,4,2,1,1,0,0]` ✓（换了组温差更大的数据，答案同示例 1）',
        summary=['时间 `O(n)`：每个下标最多入栈、出栈各一次',
                 '易错：从右到左时弹栈条件是 `t >= 栈顶`，==相等也要弹==',
                 '栈里存==下标==而不是温度，才能算天数差',
                 '写法二从左到右：栈是 todolist，遇到更高温度时给栈顶结账'],
    ),
)
