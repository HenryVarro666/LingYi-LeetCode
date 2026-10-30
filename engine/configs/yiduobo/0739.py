TEMPS = [40, 35, 50, 45, 30, 60, 55, 70]


def _while_cap(S, B, ret):
    st, T, idx = B.stack, B.T, B.index
    if not st:
        return '栈空 → 停止'
    j = st[-1]
    if T[idx] > T[j]:
        return f'`T[{idx}] = {T[idx]}` > 栈顶 `T[{j}] = {T[j]}` → 栈顶的“下一个更大”就是 `{idx}`'
    return f'`T[{idx}] = {T[idx]}` ≤ 栈顶 `T[{j}] = {T[j]}` → 停止，栈里剩下的都 ≥ 它'


def _bar_color(S, i, v):
    if i == S.get('index'):
        return 'cyan'
    if i in (S.get('stack') or []):
        return 'purple'
    return None


def _bar_dim(S, i, v):
    res, st = S.get('res'), S.get('stack') or []
    return res is not None and res[i] > 0 and i not in st


CONFIG = dict(
    num=739, title='每日温度', difficulty='Medium', category='栈',
    author='yiduobo', technique='单调栈（从左到右）',
    code='''
class Solution(object):
    def dailyTemperatures(self, T):
        stack = [0]
        res = [0] * len(T)
        for index in range(1, len(T)):
            while stack and T[index] > T[stack[-1]]:
                res[stack[-1]] = index - stack[-1]
                stack.pop()
            stack.append(index)

        return res
''',
    call=f'Solution().dailyTemperatures({TEMPS})',
    expect=[2, 1, 3, 2, 1, 2, 1, 0],
    views=[
        dict(type='bars', var='T', label='T（紫 = 栈里等答案的，灰 = 已有答案）', h=360,
             pointers={'index': 'cyan'}, color=_bar_color, dim=_bar_dim, vmax=75),
        dict(type='stack', var='stack', label='stack（下标:温度，温度单调不增）', fmt=lambda i: f'{i}:{TEMPS[i]}', h=120),
        dict(type='array', var='res', label='res', cell=84,
             color=lambda S, i, v: 'green' if v > 0 else None),
    ],
    watch=[('index', 'index', 'cyan'), ('T[index]', 'T[index]'), ('stack', 'stack', 'purple')],
    captions={
        'stack = [0]': '第 0 天先入栈：它的答案要等后面的数字来更新',
        'res = [0] * len(T)': '`res` 全填 0：一直没被更新的位置答案就是 0',
        'for index in range': lambda S, B, ret: (f'扫描第 `index = {S.index}` 天，`T[{S.index}] = {S.T[S.index]}`'
                                                 if S.get('index') != B.get('index') or 'index' not in B else '扫描结束'),
        'while stack and': _while_cap,
        'res[stack[-1]] = index - stack[-1]': '更新答案：`res[{stack[-1]}] = {index} - {stack[-1]}` = =={res[stack[-1]]}==',
        'stack.pop()': '`{B.stack[-1]}` 已找到答案，从栈中弹出',
        'stack.append(index)': '`{index}` 自身也要入栈，等后续的数字来更新它',
        'return res': '返回 `res = {ret}`',
    },
    cards=dict(
        one_liner='栈里存还没找到答案的位置，遇到更大的数就弹出结算',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`temperatures[i]` 是第 `i` 天的温度',
                 '`answer[i]`：下一个更高温度出现在==几天后==，没有就填 0',
                 '示例：`[73,74,75,71,69,72,76,73]` → `[1,1,4,2,1,1,0,0]`'],
        quote='对于T[0]到T[p-1]中还未找到答案的这些位置，其中数值小于T[p]的所有位置的下一个更大数字的位置就是p，而剩下的这些位置上的数字则必然大于等于T[p]',
        quote_src='—— yiduobo 题解',
        idea=['`T[p]` 可以更新前面==还没找到答案==的位置，同时自己也要存起来等待',
              '没被更新的位置一定 ≥ `T[p]` → 很自然想到用==单调栈==维护它们',
              '`T[index]` 大于栈顶 → 弹出并更新答案，重复直到 ≤ 栈顶'],
        result='`res = [2,1,3,2,1,2,1,0]` ✓（第 5 天一次弹出 3 个等待者）',
        summary=['时间 `O(n)`：每个下标最多进栈、出栈各一次',
                 '弹栈条件是==严格大于==：相等的温度不算“更高”',
                 '先用 `stack[-1]` 更新 `res`，再 `pop`，顺序别反',
                 '原文为 Python 2 写法：仅删去文档字符串，逻辑未改'],
    ),
)
