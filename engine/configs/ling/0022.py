CONFIG = dict(
    num=22, title='括号生成', difficulty='Medium', category='回溯',
    author='灵茶山艾府', technique='选或不选：当前位置填左括号还是右括号',
    code='''
class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        ans = []
        path = [''] * (n * 2)  # 所有括号长度都是 2n

        # 目前填了 left 个左括号，right 个右括号
        def dfs(left: int, right: int) -> None:
            if right == n:  # 填完 2n 个括号
                ans.append(''.join(path))
                return
            if left < n:  # 可以填左括号
                path[left + right] = '('  # 直接覆盖
                dfs(left + 1, right)
            if right < left:  # 可以填右括号
                path[left + right] = ')'  # 直接覆盖
                dfs(left, right + 1)

        dfs(0, 0)  # 一开始没有填括号
        return ans
''',
    call='Solution().generateParenthesis(3)',
    expect=['((()))', '(()())', '(())()', '()(())', '()()()'],
    views=[
        dict(type='array', var='path', label='path（蓝 = 下一个要填的位置 left+right，暗 = 旧值）', cell=70, h=130,
             color=lambda S, i, v: 'blue' if i == S['left'] + S['right'] else None,
             dim=lambda S, i, v: 'left' in S and i > S['left'] + S['right']),
        dict(type='text', fn=lambda S: (f"已填 `left = {S['left']}` 个 `(`、`right = {S['right']}` 个 `)`；约束：==right ≤ left ≤ n==" if 'left' in S else ''), h=50, size=26),
        dict(type='calls', h=318),
        dict(type='stack', var='ans', label='ans', h=104),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('n', 'n')],
    captions={
        "path = [''] * (n * 2)": '所有括号长度都是 `2n = {2 * n}`：开好定长 path，之后==直接覆盖==，不用恢复现场',
        'dfs(0, 0)': '一开始没有填括号：`dfs(0, 0)`',
        'if right == n': lambda S, B, ret: (
            f'`right == n`：填了 `{S.n}` 个右括号，左括号一定也是 `{S.n}` 个 → ==填完 2n 个括号==' if S.right == S.n else
            f'`right = {S.right} < n`：还没填完，看位置 `{S.left + S.right}` 能填什么'),
        "ans.append(''.join(path))": "拼成 `'{ans[-1]}'` 加入答案",
        '                return': '返回上一层',
        'if left < n': lambda S, B, ret: (
            f'`left = {S.left} < n`：左括号还没用完 → ==可以填左括号==' if S.left < S.n else
            f'`left = n`：左括号已经用完，不能再填 `(`'),
        "path[left + right] = '('": "直接覆盖：`path[{left + right}] = '('`",
        'dfs(left + 1, right)': '递归 `dfs({left}, {right})`：多了一个左括号',
        'if right < left': lambda S, B, ret: (
            f'`right = {S.right} < left = {S.left}`：前缀里 `(` 更多 → ==可以填右括号==' if S.right < S.left else
            f'`right == left = {S.left}`：再填 `)` 前缀就不合法了 → ==不能填右括号==，返回'),
        "path[left + right] = ')'": "直接覆盖：`path[{left + right}] = ')'`",
        'dfs(left, right + 1)': '递归 `dfs({left}, {right})`：多了一个右括号',
        'return ans': '全部合法括号生成完毕，共 `{len(ret)}` 个（Catalan 数）',
    },
    max_steps=60,
    cards=dict(
        one_liner='填左括号看 left < n，填右括号看 right < left',
        complexity='时间 `O(C(2n,n))`，空间 `O(n)`（不计返回值）',
        problem=['给定括号对数 `n`，生成所有==有效的==括号组合',
                 '示例：`n = 3` → `["((()))","(()())","(())()","()(())","()()()"]`'],
        quote='本质上来说，我们需要在 `0,1,2,…,2n-1` 中选 `n` 个位置填入左括号……但有额外约束，对于括号字符串的任意前缀，==右括号的个数不能超过左括号的个数==。',
        quote_src='—— 灵茶山艾府题解「分析」',
        idea=['把「填左括号」看成选、「填右括号」看成不选',
              '`left < n` 才能填 `(`；`right < left` 才能填 `)`',
              '因为始终 `right ≤ left ≤ n`，`right == n` 时一定填满了 `2n` 个'],
        result='5 个有效括号全部生成 ✓（中间分支已快进）',
        summary=['叶子数是 Catalan 数 `C(2n,n)/(n+1)`，总时间 `O(C(2n,n))`',
                 'path 定长 `2n` 直接覆盖：不需要恢复现场；用空列表 append 就要 pop',
                 '为什么 `path[0]` 一定是 `(`？一开始 `right == left`，不能填 `)`',
                 '方法二「枚举下一个左括号的位置」：`for right in range(balance + 1)`'],
    ),
)
