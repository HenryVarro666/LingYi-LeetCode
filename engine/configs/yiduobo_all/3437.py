_V = lambda S: S['_inner'].get('v')


CONFIG = dict(
    num=3437, title='全排列 III', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='搜索回溯（相邻元素奇偶不同）',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def permute(self, n):
        
        def dfs(now, vis, res):
            if len(now) == n:
                res.append(now[:])
                return
            
            for v in range(1, n + 1):
                if vis[v] or (now and (v + now[-1]) % 2 == 0):
                    continue
                vis[v] = True
                now.append(v)
                dfs(now, vis, res)
                now.pop()
                vis[v] = False
        
        res = []
        dfs([], [False] * (n + 1), res)
        return res
''',
    call='Solution().permute(3)',
    expect=[[1, 2, 3], [3, 2, 1]],
    views=[
        dict(type='array', var=lambda S: S['_inner'].get('now', []), label='now（当前排列）', h=130, cell=70),
        dict(type='array', var=lambda S: S['_inner'].get('vis', []), label='vis[v]（True = 已用，下标从 1 起）', h=140, cell=70,
             pointers={_V: 'pink'}, pointer_labels={_V: 'v'},
             color=lambda S, i, v: 'green' if v else None),
        dict(type='calls', h=190),
        dict(type='stack', var='res', label='res', h=100),
    ],
    watch=[('v', lambda S: S['_inner'].get('v'), 'pink'), ('now', lambda S: S['_inner'].get('now'), 'blue')],
    skip=['res = []', 'vis[v] = True', 'continue'],
    captions={
        'if len(now) == n': lambda S, B, ret: (f'`len(now) = {len(S.now)} == n` → ==填满了==，一个交替排列' if len(S.now) == S.n
                                               else f'`len(now) = {len(S.now)} < n`：还要继续填第 `{len(S.now) + 1}` 个数'),
        'res.append': lambda S, B, ret: f'记入答案 `{S.res[-1]}`（`now[:]` ==复制==，否则之后会被改）',
        '                return': '记录完毕 → 返回上一层',
        'for v in range': '枚举这一位填 `v = {v}`',
        'if vis[v] or': lambda S, B, ret: (
            f'`{S.v}` 已经用过 → 跳过' if S.vis[S.v] else
            f'`{S.v} + {S.now[-1]} = {S.v + S.now[-1]}` 是偶数 → 和上一个数==同奇偶==，不能相邻，跳过' if (S.now and (S.v + S.now[-1]) % 2 == 0)
            else (f'`{S.v}` 没用过，且和上一个数 `{S.now[-1]}` 奇偶不同 → 可以填' if S.now else f'`{S.v}` 没用过，第一位没有上一个数 → 可以填')),
        'continue': '这个 `v` 不合法 → 试下一个',
        'vis[v] = True': '标记 `{v}` 已用',
        'now.append(v)': '`{v}` 标记已用，并放到末尾：`now = {now}`',
        'dfs(now, vis, res)': '递归填下一位',
        'now.pop()': '==回溯==：撤销末尾的数 → `now = {now}`',
        'vis[v] = False': '`{v}` 重新变成可用，换下一个 `v`',
        'dfs([], [False]': '从空排列开始 dfs；`vis` 长度 `n + 1`，下标 1..n 直接对应数字',
        'return res': '全部搜完：共 `{len(ret)}` 个交替排列，已是==字典序==',
    },
    max_steps=100,
    cards=dict(
        one_liner='普通全排列回溯，再加一条：相邻两数不能同奇偶',
        complexity='时间 `O(n·n!)`（有剪枝，实际更少），空间 `O(n)`',
        problem=['给定 `n`，交替排列是前 `n` 个正整数的排列，且==相邻元素不同时为奇或偶==',
                 '按==字典序==返回所有交替排列',
                 '示例：`n = 3` → `[[1,2,3],[3,2,1]]`'],
        quote='经典搜索回溯问题的变形，依然可以使用回溯法解决。本题中要求相邻元素不能同奇偶，因此在搜索的每一步都需要保证当前填充的元素与上一个填充的元素不同奇偶。',
        quote_src='—— yiduobo 题解',
        idea=['`vis` 标记已用的数，`now` 是当前路径',
              '`v` 从小到大枚举 → 找到的排列天然按字典序',
              '`(v + now[-1]) % 2 == 0` 就是“同奇偶”，直接跳过'],
        result='找到 2 个交替排列 ✓',
        summary=['时间 `O(n·n!)` 的上界，剪枝后远小于它；空间 `O(n)`',
                 '易错点：`res.append(now[:])` 要复制',
                 '易错点：回溯时 `now.pop()` 和 `vis[v] = False` 缺一不可',
                 '第一位 `now` 为空，没有奇偶限制，所以先判 `now and ...`'],
    ),
)
