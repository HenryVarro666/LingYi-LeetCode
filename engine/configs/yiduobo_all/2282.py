def _members(S):
    if 'stack' not in S or 'i' not in S or 'j' not in S:
        return set()
    if S['_line'] < 23:
        return {(S['i'], k) for k in S['stack']}
    return {(k, S['j']) for k in S['stack']}


def _hc(S, i, j, v):
    return 'pink' if (i, j) in _members(S) else None


def _stk(S):
    if 'stack' not in S or 'i' not in S or 'j' not in S:
        return ''
    H = S['heights']
    if S['_line'] < 23:
        hs = [H[S['i']][k] for k in S['stack']]
    else:
        hs = [H[k][S['j']] for k in S['stack']]
    return f"栈（位置）`{S['stack']}` 对应身高 `{hs}`，栈顶在最右"


CONFIG = dict(
    num=2282, title='在一个网格中可以看到的人数', difficulty='Medium', category='单调栈',
    author='yiduobo', technique='逐行逐列单调栈', tags=['灵神题单'],
    code='''
class Solution(object):
    def seePeople(self, heights):

        m = len(heights)
        n = len(heights[0])
        res = [[0] * n for _ in range(m)]

        for i in range(m):
            stack = [n - 1]
            for j in range(n - 2, -1, -1):
                while stack and heights[i][stack[-1]] < heights[i][j]:
                    stack.pop()
                    res[i][j] += 1
                
                if stack:
                    res[i][j] += 1

                while stack and heights[i][stack[-1]] == heights[i][j]:
                    stack.pop()

                stack.append(j)

        for j in range(n):
            stack = [m - 1]
            for i in range(m - 2, -1, -1):
                while stack and heights[stack[-1]][j] < heights[i][j]:
                    stack.pop()
                    res[i][j] += 1
                
                if stack:
                    res[i][j] += 1
                
                while stack and heights[stack[-1]][j] == heights[i][j]:
                    stack.pop()
                
                stack.append(i)
        
        return res
''',
    call='Solution().seePeople([[4,2,4,1],[1,3,2,5]])',
    expect=[[3, 2, 2, 1], [1, 2, 1, 0]],
    views=[
        dict(type='grid', var='heights', label='heights（黄 = 当前处理的人，粉 = 栈中等待被看的人）', cell=96, h=230,
             cursors=[('i', 'j', 'yellow')], color=_hc),
        dict(type='grid', var='res', label='res（每个人看到的人数，右侧 + 下方）', cell=80, h=200,
             cursors=[('i', 'j', 'green')]),
        dict(type='text', fn=_stk, h=60),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'blue'), ('stack', 'stack', 'pink')],
    captions={
        'stack = [n - 1]': '第 `{i}` 行：从最右边的人开始，他先入栈',
        'for i in range(m - 2': '这一列往上扫：当前 `i = {i}`',
        'stack = [m - 1]': '第 `{j}` 列：从最下面的人开始，他先入栈',
        'while stack and heights[i][stack[-1]] < heights[i][j]': lambda S, B, r: (
            '栈空了，右边没人可看' if not S.stack else
            f'栈顶高 `{S.heights[S.i][S.stack[-1]]}` < 我 `{S.heights[S.i][S.j]}` → ==我能看到他，而且他被我挡住了==，左边的人再也看不到他'
            if S.heights[S.i][S.stack[-1]] < S.heights[S.i][S.j] else
            f'栈顶高 `{S.heights[S.i][S.stack[-1]]}` ≥ 我 `{S.heights[S.i][S.j]}` → 不再比我矮，停止弹出'),
        'while stack and heights[stack[-1]][j] < heights[i][j]': lambda S, B, r: (
            '栈空了，下面没人可看' if not S.stack else
            f'栈顶高 `{S.heights[S.stack[-1]][S.j]}` < 我 `{S.heights[S.i][S.j]}` → ==我能看到他，而且他被我挡住了==，上面的人再也看不到他'
            if S.heights[S.stack[-1]][S.j] < S.heights[S.i][S.j] else
            f'栈顶高 `{S.heights[S.stack[-1]][S.j]}` ≥ 我 `{S.heights[S.i][S.j]}` → 不再比我矮，停止弹出'),
        'stack.pop()': lambda S, B, r: '把被挡住的人弹出栈',
        'res[i][j] += 1': '看到一个：`res[{i}][{j}] = {res[i][j]}`',
        'if stack:': lambda S, B, r: ('栈里还有人 → 栈顶比我高（或一样高），==我还能看到这个挡住后面的人==，再 +1'
                                    if S.stack else '栈空了 → 没有更高的人可看，不再加'),
        'while stack and heights[i][stack[-1]] == heights[i][j]': lambda S, B, r: (
            f'栈顶和我一样高 → 弹出：==左边的人被我们俩之一挡住，看不到更远的那个==' if S.stack and S.heights[S.i][S.stack[-1]] == S.heights[S.i][S.j]
            else '没有和我一样高的 → 不弹'),
        'while stack and heights[stack[-1]][j] == heights[i][j]': lambda S, B, r: (
            f'栈顶和我一样高 → 弹出：上面的人看不到比我同高的远处那个' if S.stack and S.heights[S.stack[-1]][S.j] == S.heights[S.i][S.j]
            else '没有和我一样高的 → 不弹'),
        'stack.append(j)': '`{j}` 入栈：它可能被左边更矮的人看到',
        'stack.append(i)': '`{i}` 入栈：它可能被上边更矮的人看到',
        'return res': '右侧 + 下方的人数都加好了：`{res}`',
    },
    max_steps=74,
    cards=dict(
        one_liner='每个方向单调栈：能看到的 = 弹出的 + 挡住的那一个',
        complexity='时间 `O(mn)`，空间 `O(max(m, n))`',
        problem=['网格 `heights[i][j]` 是每个人的身高；一个人能看到右边或下方的某人，要求两人之间的所有人都==严格矮于==这两人中较矮的那个',
                 '返回每个位置能看到的人数（只看右侧和下方）',
                 '本视频：`[[4,2,4,1],[1,3,2,5]]` → `[[3,2,2,1],[1,2,1,0]]`'],
        quote='若栈非空，说明栈顶位置的高度比当前位置高度要高，因此当前位置无法看到栈中的其他位置，但是可以看到栈顶位置，因此需要再将当前位置能看到的人数加上1。',
        quote_src='—— yiduobo 题解原文',
        idea=['先拆成一维：每行求右侧、每列求下方，写法一样',
              '从右往左扫，栈里放“还可能被左边的人看到”的人；比我矮的被我挡住，弹出并各算一个',
              '弹完后栈顶（不矮于我）也看得见，再 +1；一样高的看不到更远，要弹掉'],
        summary=['时间 `O(mn)`，空间 `O(max(m, n))`',
                 '弹出比我矮的：每弹一个就 +1；最后栈顶那个高的再 +1',
                 '等高要单独弹：看到的条件是中间严格更矮，与第一个 while 分开才能多算那一个 +1',
                 '列方向代码和行方向对称，只是把 `j` 换成 `i`',
                 '原文已是 Python 3 可运行写法，未作修改'],
    ),
)
