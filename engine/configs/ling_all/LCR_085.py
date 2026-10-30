CONFIG = dict(
    num='LCR 085', title='括号生成', difficulty='Medium', category='二叉树与回溯',
    author='灵茶山艾府', technique='回溯 · 枚举填左括号还是右括号',
    tags=[],
    code='''
class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        m = n * 2
        ans = []
        path = [''] * m
        def dfs(i: int, open: int) -> None:
            if i == m:
                ans.append(''.join(path))
                return
            if open < n:  # 可以填左括号
                path[i] = '('
                dfs(i + 1, open + 1)
            if i - open < open:  # 可以填右括号
                path[i] = ')'
                dfs(i + 1, open)
        dfs(0, 0)
        return ans
''',
    call='Solution().generateParenthesis(2)',
    expect=['(())', '()()'],
    views=[
        dict(type='array', var='path', label='path（暗 = 还没填 / 旧值；蓝箭头 = 当前要填的位置 i）', cell=84, h=210, pointers={'i': 'blue'},
             dim=lambda S, i, v: i >= S['i']),
        dict(type='text', h=60, size=26,
             fn=lambda S: f"已填 `{S['i']}` 个：左括号 =={S['open']}== 个，右括号 =={S['i'] - S['open']}== 个（右 ≤ 左 才合法）" if 'open' in S['_inner'] else ''),
        dict(type='calls', h=230),
        dict(type='stack', var='ans', label='ans', h=108),
    ],
    watch=[('i', 'i', 'blue'), ('open', 'open', 'pink'), ('右括号数', lambda S: S['i'] - S['open'] if 'open' in S['_inner'] else '', 'cyan')],
    skip=['m = n * 2', 'ans = []'],
    max_steps=80,
    captions={
        'path = [': '`path` 长度固定为 `2n`，填的时候直接覆盖，不用恢复现场',
        'dfs(0, 0)': '从 `dfs(0, 0)` 开始：填第 0 个位置，已有 0 个左括号',
        'if i == m': lambda S, B, ret: ('`i == m` → ==填满了==，得到一个合法括号串' if S.i == S.m
                                        else f'`i = {S.i} < {S.m}`：还没填满，继续选括号'),
        'ans.append': lambda S, B, ret: f"记录答案 `{S.ans[-1]}`",
        'if open < n': lambda S, B, ret: (f'`open = {S.open} < n = {S.n}`：左括号还没用完 → ==可以填左括号==' if S.open < S.n
                                          else f'`open = {S.open}` 已经等于 n → 不能再填左括号'),
        "path[i] = '('": '`path[{i}] = "("`',
        "path[i] = ')'": '`path[{i}] = ")"`',
        'dfs(i + 1, open + 1)': '填了左括号，`open` 加一，递归 `dfs({B.i+1}, {B.open+1})`',
        'if i - open < open': lambda S, B, ret: (f'右括号 `i - open = {S.i - S.open}` < 左括号 `{S.open}` → ==可以填右括号==（有左括号等着匹配）'
                                                 if S.i - S.open < S.open
                                                 else f'右括号 `{S.i - S.open}` 已不少于左括号 `{S.open}` → 不能填右括号，否则无效'),
        'dfs(i + 1, open)': '填了右括号，`open` 不变，递归 `dfs({B.i+1}, {B.open})`',
        '                return': '这条分支结束 → 回到上一层，换另一种填法',
        'return ans': '搜索结束：共 `{len(ret)}` 个有效括号串',
    },
    cards=dict(
        one_liner='每个位置只有两种选择：填左括号，或填右括号',
        complexity='时间 `O(C(2n,n))`，空间 `O(n)`（不计返回值）',
        problem=['正整数 `n` 代表括号的对数，生成所有==有效==的括号组合',
                 '示例：`n = 3` → `["((()))","(()())","(())()","()(())","()()()"]`',
                 '本视频：`n = 2` → `["(())","()()"]`'],
        quote='对于本题，它等于 O(n·C(2n,n))。但由于左右括号的约束，实际上没有这么多叶子，根据 Catalan 数，只有 C(2n,n)/(n+1) 个叶子节点。',
        quote_src='—— 灵茶山艾府题解（方法一 · 复杂度分析）',
        idea=['括号串长 `2n`，从左到右枚举每个位置填 `(` 还是 `)`',
              '填 `(` 的条件：左括号个数 `open < n`',
              '填 `)` 的条件：右括号个数 `i - open` ==小于== 左括号个数 `open`',
              '两个条件都满足就都试，搜索树自然只含合法串'],
        result='2 个有效括号串全部找到',
        summary=['时间：路径长度 × 叶子数，叶子是 Catalan 数 `C(2n,n)/(n+1)`，即 `O(C(2n,n))`',
                 '易错：右括号条件是 `i - open < open`，不是 `i - open < n`',
                 '`path` 定长直接覆盖，所以无需恢复现场',
                 '方法二：枚举「下一个左括号的位置」，每次填 0 到 balance 个右括号再放一个左括号',
                 '同类题：46. 全排列、78. 子集（回溯模板）'],
    ),
)
