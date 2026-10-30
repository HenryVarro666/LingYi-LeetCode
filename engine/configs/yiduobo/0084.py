H = [2, 1, 5, 6, 2, 3]


def _tail(S):
    """主循环结束后的收尾阶段：此时 index 是栈内序号，必小于 stack[-1]（本例成立）"""
    st, idx = S.get('stack'), S.get('index')
    return bool(st) and isinstance(idx, int) and idx < st[-1]


def _rect(S):
    """当前正在计算的矩形 (l, r, 高)；没有则 None（只用于画图）"""
    st, idx, h = S.get('stack'), S.get('index'), S.get('height')
    if not st or not isinstance(idx, int):
        return None
    if _tail(S):
        if idx >= len(st):
            return None
        l = 0 if idx == 0 else st[idx - 1] + 1
        return l, st[-1], H[st[idx]]
    if h is not None and H[st[-1]] > h:
        l = st[-2] + 1 if len(st) > 1 else 0
        return l, idx - 1, H[st[-1]]
    return None


def _p_main(S):
    return None if _tail(S) else S.get('index')


def _p_tail(S):
    return S['stack'][S['index']] if _tail(S) else None


def _color(S, i, v):
    r = _rect(S)
    st = S.get('stack') or []
    if r and ((_tail(S) and i == st[S['index']]) or (not _tail(S) and i == st[-1])):
        return 'yellow'
    if not _tail(S) and i == S.get('index'):
        return 'cyan'
    if i in st:
        return 'purple'
    return None


def _formula(S):
    r = _rect(S)
    if not r:
        return '图例：紫 = list（栈）中　青 = index　黄框 = 正在计算的矩形'
    l, rr, h = r
    return f'矩形：左边界 `{l}`，右边界 `{rr}`，高 `{h}` → 面积 `{h} × {rr - l + 1}` = =={h * (rr - l + 1)}=='


def _while_cap(S, B, ret):
    st, h = B.stack, B.height
    if not st:
        return '栈空 → 停止'
    j = st[-1]
    if H[j] > h:
        return f'栈顶 `{j}:{H[j]}` > `{h}` → 它的右边界找到了：就是 `index - 1 = {B.index - 1}`'
    return f'栈顶 `{j}:{H[j]}` ≤ `{h}` → 停止，剩下的柱子继续找右边界'


def _if_cap(S, B, ret):
    st, h = B.stack, B.height
    if not st:
        return 'list（栈）为空 → 直接加入'
    j = st[-1]
    if H[j] <= h:
        return f'`{h}` ≥ 栈顶 `{j}:{H[j]}` → list 仍单调递增，大家的右边界都还没找到'
    return f'`{h}` < 栈顶 `{j}:{H[j]}` → list 里比它高的柱子，==右边界都找到了=='


CONFIG = dict(
    num=84, title='柱状图中最大的矩形', difficulty='Hard', category='栈',
    author='yiduobo', technique='单调栈 · 找左右边界',
    code='''
class Solution(object):
    def largestRectangleArea(self, heights):
        stack = []
        res = 0
        for index, height in enumerate(heights):
            if not stack or heights[stack[-1]] <= height:
                stack.append(index)
            else:
                while len(stack) > 0 and heights[stack[-1]] > height:
                    if len(stack) > 1:
                        width = index - stack[-2] - 1
                    else:
                        width = index
                    res = max(res, heights[stack[-1]] * width)
                    stack.pop()
                stack.append(index)

        if stack:
            for index in range(len(stack)):
                if index == 0:
                    res = max(res, heights[stack[index]] * (stack[-1] + 1))
                else:
                    res = max(res, heights[stack[index]] * (stack[-1] - stack[index - 1]))

        return res
''',
    call=f'Solution().largestRectangleArea({H})',
    expect=10,
    views=[
        dict(type='bars', var='heights', label='heights', h=380, vmax=7,
             pointers={_p_main: 'cyan', _p_tail: 'yellow'},
             pointer_labels={_p_main: 'index', _p_tail: 'stack[index]'},
             window=(lambda S: _rect(S)[0] if _rect(S) else None, lambda S: _rect(S)[1] if _rect(S) else None),
             window_color='yellow', color=_color),
        dict(type='stack', var='stack', label='stack（下标:高度，单调递增的 list）', fmt=lambda i: f'{i}:{H[i]}', h=120),
        dict(type='text', fn=_formula, size=27),
    ],
    watch=[('index', 'index', 'cyan'), ('height', 'height'), ('width', 'width'), ('res', 'res', 'green')],
    captions={
        'stack = []': 'list（其实就是栈）：存==还没找到右边界==的柱子，高度单调递增',
        'res = 0': '`res = 0`',
        'for index, height': lambda S, B, ret: (f'探索到 `index = {S.index}`，`height = {S.height}`'
                                                if S.index != B.get('index') else '主循环结束'),
        'if not stack or': _if_cap,
        'stack.append(index)': '把 `{index}` 加入 list，和大家一起寻找右边界',
        'while len(stack) > 0': _while_cap,
        'if len(stack) > 1': lambda S, B, ret: (f'存在 `list[-2] = {S.stack[-2]}` → 左边界是 `{S.stack[-2]} + 1`'
                                                if len(S.stack) > 1 else '不存在 `list[-2]` → 左边界就是 0'),
        'width = index - stack[-2] - 1': '宽 = `{index} - {stack[-2]} - 1` = `{width}`（右边界 `index - 1`，左边界 `list[-2] + 1`）',
        'width = index': '宽 = `index` = `{width}`（从第 0 根柱子一直到 `index - 1`）',
        'res = max(res, heights[stack[-1]] * width)': '面积 `{heights[stack[-1]]} × {width}` = =={heights[stack[-1]] * width}==，`res = {res}`',
        'stack.pop()': '`{B.stack[-1]}` 算完了，从 list 中 pop 出去',
        'if stack:': '探索到末尾，list 不为空：剩下柱子的右边界都是 `list[-1] = {stack[-1]}`',
        'for index in range(len(stack))': lambda S, B, ret: (
            f'处理 list 中第 `{S.index}` 个：柱子 `{S.stack[S.index]}`，高 `{H[S.stack[S.index]]}`'
            if S.index != B.get('index') else '剩余柱子处理完毕'),
        'if index == 0': lambda S, B, ret: ('第 0 个 → 左边界是 0' if S.index == 0
                                            else f'左边界 = `list[{S.index - 1}] + 1 = {S.stack[S.index - 1] + 1}`'),
        'res = max(res, heights[stack[index]] * (stack[-1] + 1))':
            '面积 `{heights[stack[index]]} × ({stack[-1]} + 1)` = =={heights[stack[index]] * (stack[-1] + 1)}==，`res = {res}`',
        'res = max(res, heights[stack[index]] * (stack[-1] - stack[index - 1]))':
            '面积 `{heights[stack[index]]} × ({stack[-1]} - {stack[index - 1]})` = =={heights[stack[index]] * (stack[-1] - stack[index - 1])}==，`res = {res}`',
        'return res': '返回 `res = {ret}`',
    },
    cards=dict(
        one_liner='对每根柱子找左右边界，用单调递增的 list 一趟算完',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`heights[i]` 是第 `i` 根柱子的高度，宽度都为 1',
                 '求柱状图中能勾勒出的==最大矩形面积==',
                 '示例：`[2,1,5,6,2,3]` → `10`（高 5、宽 2）'],
        quote='答案矩形的高一定就是其中某个柱子的高，且==这个柱子是构成答案的柱子中最矮的那一个==。',
        quote_src='—— yiduobo 题解',
        idea=['问题变成：对每根柱子找到 `left` 与 `right` 边界',
              '维护一个高度==单调递增==的 list，里面的柱子都还没找到右边界',
              '`height[k]` 更矮 → 比它高的柱子：右边界 `k-1`，左边界 `list[-2]+1`',
              '扫到末尾 list 不空：剩下柱子的右边界都是 `list[-1]`'],
        result='最大面积 `10`：以高 5 的柱子为高，宽 2 ✓',
        summary=['时间 `O(n)`：每根柱子最多进出 list 一次——这个 list 实际上就是栈',
                 '易错：list 只剩一根柱子时，左边界是 0，宽 = `index`',
                 '收尾循环里 `index` 是==栈内序号==，柱子是 `stack[index]`',
                 '原文为 Python 2 写法：仅删去文档字符串，逻辑未改'],
    ),
)
