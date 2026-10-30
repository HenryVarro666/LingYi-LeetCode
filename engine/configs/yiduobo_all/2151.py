def _gcolor(S, r, c, v):
    now = S['now'] if 'now' in S else None
    if not isinstance(now, list) or len(now) < 2 or S.get('_line', 0) < 11:
        return None
    if now[r] == 1 and v < 2:
        return 'green' if v == now[c] else 'red'
    return None


CONFIG = dict(
    num=2151, title='基于陈述统计最多好人数', difficulty='Hard', category='链表、二叉树与回溯',
    author='yiduobo', technique='DFS 枚举每人好坏 + 校验好人陈述',
    tags=['灵神题单', '链表树与回溯', '难度分 1980'],
    code='''
class Solution(object):
    def maximumGood(self, statements):

        n = len(statements)

        def dfs(now):
            if len(now) == n:
                cnt = 0
                for i in range(n):
                    if now[i] == 1:
                        for j in range(n):
                            if statements[i][j] == 2:
                                continue
                            if statements[i][j] != now[j]:
                                return 0

                        cnt += 1

                return cnt

            now.append(0)
            res = dfs(now)
            now[-1] = 1
            res = max(res, dfs(now))
            now.pop()
            return res

        return dfs([])
''',
    call='Solution().maximumGood([[2, 1], [0, 2]])',
    expect=1,
    views=[
        dict(type='grid', var='statements', label='statements（好人 i 的整行陈述要和 now 相符：绿 = 相符，红 = 矛盾）', h=170, cell=100,
             color=_gcolor, cursors=[('i', 'j', 'blue', '')]),
        dict(type='array', var=lambda S: (S['now'] + [None] * 2)[:2] if isinstance(S.get('now'), list) else None,
             label='now（下标 = 玩家，1 = 好人，0 = 坏人，空 = 还没决定）', cell=100, h=140, pointers={'i': 'pink'}),
        dict(type='calls', h=190, hide=('statements', 'n')),
    ],
    watch=[('now', 'now', 'blue'), ('i', 'i', 'pink'), ('cnt', 'cnt', 'green'), ('res', 'res', 'yellow')],
    skip=['n = len(statements)', 'for i in range(n)', 'for j in range(n)', 'if statements[i][j] == 2', 'continue'],
    max_steps=110,
    captions={
        'if len(now) == n': lambda S, B, ret: ('`now` 已有 `n` 个人的好坏 → ==一种完整情况==，开始校验' if len(S['now']) == S['n']
                                               else f"`now = {S['now']}`：还没决定完，继续给下一个人分配好坏"),
        'cnt = 0': '开始校验这种情况 `now = {now}`，好人计数从 0 开始',
        'if now[i] == 1': lambda S, B, ret: (f"玩家 `{S['i']}` 在 `now` 中是好人 → 校验他的每条陈述" if S['now'][S['i']] == 1
                                              else f"玩家 `{S['i']}` 是坏人 → ==不用管==，坏人可真可假"),
        'if statements[i][j] != now[j]': lambda S, B, ret: (
            f"好人 `{S['i']}` 说玩家 `{S['j']}` 是{'好人' if S['statements'][S['i']][S['j']] else '坏人'}，`now[{S['j']}] = {S['now'][S['j']]}` → "
            + ('==矛盾==' if S['statements'][S['i']][S['j']] != S['now'][S['j']] else '相符')),
        'return 0': '好人的话和这种情况矛盾 → 这种情况不成立，返回 0',
        'cnt += 1': '好人 `{i}` 的陈述全部相符 → `cnt` = =={cnt}==',
        'return cnt': '这种情况成立，好人共 =={ret}== 个',
        'now.append(0)': '先假设下一个人是==坏人==（0），递归',
        'res = dfs(now)': '`dfs(now)`：先处理“这个人是坏人”的所有情况，得到最好人数 `{res}`',
        'now[-1] = 1': '再改成==好人==（1）',
        'res = max(res': '两边取较大：`res = max({B.res}, ...)` = =={res}==',
        'now.pop()': '回溯：把这个人从 `now` 里弹出',
        'return res': '这一层的最大好人数 =={ret}==',
        'return dfs([])': '从空列表开始 dfs，最终最大好人数 =={ret}==',
    },
    cards=dict(
        one_liner='n 很小，DFS 枚举每人好坏，只核对好人说的话',
        complexity='时间 `O(n^2 · 2^n)`，空间 `O(n)`',
        problem=['好人只说真话，坏人可真可假；`statements[i][j]` = 0 认为坏人、1 认为好人、2 没说',
                 '求可能的好人最大数目',
                 '本视频：`[[2,1],[0,2]]` → 1'],
        quote='注意到题目中n的规模很小，那么完全可以枚举出所有的情况，一共是2^15=32768种。由于好人一定说真话，坏人可能说真话可能说假话，那么实际上可以完全不理会坏人',
        quote_src='—— yiduobo 题解',
        idea=['`dfs(now)`：给第 `len(now)` 个人依次试坏人(0)、好人(1)',
              '`now` 填满就是一种完整情况：只看好人的陈述是否与 `now` 一致',
              '有矛盾返回 0，否则返回好人数；两个分支取最大'],
        result='所有 4 种情况试完，最多 1 个好人',
        summary=['时间 `O(n^2 · 2^n)`，空间 `O(n)`',
                 '不用管坏人：坏人的陈述可真可假，不构成约束',
                 '陈述值 2 表示没说，要跳过',
                 '写法特点：用递归列表 `now` 生成所有 0/1 组合，而不是位运算',
                 '回溯时 `now.append` / `now.pop` 要成对'],
    ),
)
