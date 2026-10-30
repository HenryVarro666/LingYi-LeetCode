CONFIG = dict(
    num='面试题 08.09', title='括号', difficulty='Medium', category='二叉树与回溯',
    author='灵茶山艾府', technique='枚举填左括号还是右括号',
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
        dict(type='array', var='path', label='path（蓝 = 当前要填的位置 i）', cell=76, h=150, pointers={'i': 'blue'},
             color=lambda S, i, v: ('green' if v == '(' else 'pink') if v else None),
        dict(type='text', size=30, h=60,
             fn=lambda S: (f"左括号 `open` = =={S['open']}==，右括号 `i − open` = =={S['i'] - S['open']}=="
                           if 'open' in S['_inner'] else '')),
        dict(type='calls', h=250),
        dict(type='stack', var='ans', label='ans', h=110),
    ],
    watch=[('i', lambda S: S['_inner'].get('i'), 'blue'), ('open', lambda S: S['_inner'].get('open'), 'green'), 'n'],
    skip=['m = n * 2', 'ans = []', "path = [''] * m"],
    captions={
        'dfs(0, 0)': '从 `dfs(0, 0)` 开始：填第 0 个字符，已有 0 个左括号',
        'if i == m': lambda S, B, ret: (f'`i = {S.i} = m`：括号串填满 → ==得到一个合法组合==' if S.i == S.m
                                        else f'`i = {S.i} < m = {S.m}`：还没填满，继续填'),
        'ans.append': '记录答案 `{ans[-1]}`',
        'if open < n': lambda S, B, ret: (f'`open = {S.open} < n = {S.n}` → 左括号还没用完，==可以填 `(`==' if S.open < S.n
                                          else f'`open = {S.open} = n`：左括号用完了 → 不能再填 `(`'),
        "path[i] = '('": '`path[{i}] = (`',
        "path[i] = ')'": '`path[{i}] = )`',
        'if i - open < open': lambda S, B, ret: (
            f'右括号个数 `i − open = {S.i - S.open}` < 左括号 `open = {S.open}` → ==可以填 `)`==' if S.i - S.open < S.open
            else f'右括号 `{S.i - S.open}` ≥ 左括号 `{S.open}`：再填 `)` 会==不合法==，不填'),
        12: '填了 `(` 之后：`dfs({i}, {open})`，`open` 加一',
        15: '填了 `)` 之后：`dfs({i}, {open})`，`open` 不变',
        'return ans': '搜索结束：共 `{len(ret)}` 个合法括号串',
    },
    max_steps=110,
    cards=dict(
        one_liner='每一位只有两种选择：填 ( 或 )，用两条规则剪枝',
        complexity='时间 `O(C(2n,n))`，空间 `O(n)`（不计返回值）',
        problem=['设计算法，打印 `n` 对括号的所有==合法==组合',
                 '示例：`n = 3` → `((()))`、`(()())`、`(())()`、`()(())`、`()()()`',
                 '本视频：`n = 2` → `(())`、`()()`'],
        quote='分析回溯问题的时间复杂度，有一个通用公式：路径长度×搜索树的叶子数。……根据 Catalan 数，只有 C(2n,n)/(n+1) 个叶子节点。',
        quote_src='—— 灵茶山艾府题解（复杂度分析）',
        idea=['`dfs(i, open)`：填 `path[i]`，已经填了 `open` 个左括号',
              '`open < n`：左括号还有名额，就可以填 `(`',
              '`i - open < open`：右括号比左括号少，才能填 `)`',
              '这两个条件保证每个叶子都是合法括号串'],
        result='找到 2 个合法括号串：`(())`、`()()`',
        summary=['时间 `O(C(2n,n))`（Catalan 数级别），空间 `O(n)`',
                 '易错：右括号个数是 `i - open`，不是 `open` 本身',
                 '易错：填完 `(` 和 `)` 分支各自覆盖 `path[i]`，不需要恢复现场',
                 '方法二「枚举下一个左括号的位置」：`path` 存左括号下标，其余位置补右括号']),
)
