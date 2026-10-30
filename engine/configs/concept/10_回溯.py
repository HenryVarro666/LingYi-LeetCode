def _fmt_sets(a):
    return '[' + ', '.join('[' + ','.join(map(str, x)) + ']' for x in a) + ']'


def _formula(S):
    if 'i' not in S or 'path' not in S:
        return '回溯 = 递归 + ==恢复现场==：`path` 是一条从根到当前节点的路径'
    return f"`path = {S['path']}`　　已收集 `ans = {_fmt_sets(S['ans'])}`"


def _draw_path(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), 'path（当前路径上已选的数）', 24, T['muted'], bold=True)
    p = S.get('path')
    if p is None:
        return
    if not p:
        cv.text((x0 + 40, y0 + 78), '[ ]  空路径（根节点）', 28, T['dim'], anchor='lm')
        return
    cell = 84
    sx = x0 + 20 + ((x1 - x0 - 40) - cell * 4) / 2
    bp = B.get('path') or []
    for k, v in enumerate(p):
        X = sx + k * cell
        new = k >= len(bp) or bp[k] != v
        cv.rect((X + 5, y0 + 40, X + cell - 5, y0 + 40 + cell * 0.92), fill=T['green'], r=8,
                outline=T['yellow'] if new else T['border'], width=3 if new else 1)
        cv.text((X + cell / 2, y0 + 40 + cell * 0.46), str(v), 34, T['bg'], anchor='mm', bold=True)


_seen = {'copy': 0}


def _copy_cap(S, B, ret):
    _seen['copy'] += 1
    if _seen['copy'] == 1:
        return f"收集子集 `{S.path}`——==要复制一份==，否则之后修改 path 会改掉它"
    return f"收集子集 `{S.path}` → `ans = {_fmt_sets(S.ans)}`"


CONFIG = dict(
    num=None, title='回溯 · 通用思想与模板', author='概念讲解', category='回溯',
    technique='通用思想与模板', kind='concept', difficulty='',
    code='''
def subsets_choose(nums):          # 写法一：选或不选（输入的视角）
    ans, path = [], []
    def dfs(i):
        if i == len(nums):         # 每个数都考虑完了
            ans.append(path.copy())
            return
        dfs(i + 1)                 # 不选 nums[i]
        path.append(nums[i])       # 选 nums[i]
        dfs(i + 1)
        path.pop()                 # 恢复现场
    dfs(0)
    return ans

def subsets_pick(nums):            # 写法二：枚举选哪个（答案的视角）
    ans, path = [], []
    def dfs(i):
        ans.append(path.copy())    # 每个节点都是一个子集
        for j in range(i, len(nums)):  # 下一个数选 nums[j]
            path.append(nums[j])
            dfs(j + 1)             # 之后只能选 j 右边的数
            path.pop()             # 恢复现场
    dfs(0)
    return ans
''',
    call='''
a = subsets_choose([1, 2])
b = subsets_pick([1, 2])
(a, b)
''',
    expect=([[], [2], [1], [1, 2]], [[], [1], [1, 2], [2]]),
    skip=['            return'],
    views=[
        dict(type='text', fn=_formula, h=60),
        dict(type='array', var='nums', label='nums', pointers={'i': 'blue', 'j': 'pink'}, h=170),
        dict(type='custom', draw=_draw_path, h=140),
        dict(type='calls', label='递归调用栈（深度 = 已经做了几次选择）', h=200),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('path', 'path', 'green')],
    captions={
        2: '写法一「选或不选」：站在 ==输入== 的角度，每个数都问一次：选还是不选？',
        4: lambda S, B, ret: (f'`i = {S.i}`：两个数都考虑完了 → 得到一个子集' if S.i == len(S.nums)
                              else f'考虑 `nums[{S.i}] = {S.nums[S.i]}`：选，还是不选？'),
        5: _copy_cap,
        7: lambda S, B, ret: f'分支①：==不选== `nums[{B.i}] = {B.nums[B.i]}`，直接考虑下一个数',
        8: lambda S, B, ret: f'分支②：==选== `nums[{S.i}] = {S.nums[S.i]}`，path → `{S.path}`',
        9: lambda S, B, ret: f'带着 `path = {B.path}` 去考虑下一个数',
        10: lambda S, B, ret: (f'==恢复现场==：撤销选择，path 回到 `{S.path}`，让上一层的其他分支不受影响'
                               if _seen.setdefault('pop', [0]).append(1) or len(_seen['pop']) == 2
                               else f'恢复现场：path 回到 `{S.path}`'),
        11: '从第 0 个数开始递归',
        12: lambda S, B, ret: f'写法一结果：`{_fmt_sets(ret)}`——搜索树有 `2^n = 4` 个叶子',
        15: '写法二「枚举选哪个」：站在 ==答案== 的角度——下一个数选谁？',
        17: _copy_cap,
        18: lambda S, B, ret: ('`i = 2`：后面没有可选的数了，这一层结束' if S.i == len(S.nums) else
                               (f'`nums[{S.j}]` 之后没有数了，这一层结束' if B.get('j') == S.j else
                                f'下一个数选 `nums[{S.j}] = {S.nums[S.j]}`')),
        19: lambda S, B, ret: f'path 加入 `{S.nums[S.j]}` → `{S.path}`',
        20: lambda S, B, ret: f'递归：下一个数只能从 `nums[{B.j + 1}:]` 里选——==保证不重复==',
        21: lambda S, B, ret: f'恢复现场：path 回到 `{S.path}`',
        22: '从下标 0 开始枚举',
        23: lambda S, B, ret: f'写法二结果：`{_fmt_sets(ret)}`——同样 4 个子集，顺序不同',
    },
    cards=dict(
        one_liner='在搜索树上走一遍：做选择 → 递归 → 撤销选择',
        complexity='时间 = 路径长度 × 叶子数，如子集 `O(n·2ⁿ)`；空间 `O(n)`',
        problem_heading='什么时候用？',
        problem=['要列出 ==所有== 方案：子集、组合、排列、分割、括号',
                 '数据范围很小（n ≤ 10～20），答案个数是指数级',
                 '每一步有几种选择，选完变成规模更小的同类子问题',
                 '网格里找路径（单词搜索）→ 回溯 + 恢复现场'],
        before=[dict(heading='核心概念：路径、选择、恢复现场', lines=[
            '`path` 记录已做的选择，`dfs(i)` 负责第 `i` 步怎么选',
            '子集 / 组合：选或不选、枚举选哪个；组合再加剪枝',
            '排列：用 `on_path` 标记哪些数已经用过（46、51）',
            '递归回来后 ==撤销选择==（`path.pop()`）；收集答案要复制']),
        ],
        idea_heading='两位作者怎么说',
        quote='如果不恢复现场，当我们从 [2] 递归返回后，path 中还残留有 2，==对于后面的递归来说，这个 2 是多余的==。',
        quote_src='—— 灵茶山艾府 · 78. 子集',
        idea=['灵神的两种基本思想：==选或不选==（输入视角）/ ==枚举选哪个==（答案视角）',
              'yiduobo 78：保证 `now` 单调递增，从 `last_pos + 1` 往后枚举，每个 `now` 都是解',
              '复杂度通用公式（灵神 22）：==路径长度 × 搜索树的叶子数=='],
        summary_heading='本类 Hot100 题目 & 学习顺序',
        summary=['`78` 子集：选或不选 / 枚举选哪个',
                 '`17` 电话号码的字母组合：每一位枚举一个字母',
                 '`39` 组合总和：枚举选哪个 + 剩余和剪枝',
                 '`22` 括号生成：选左或右括号（左括号数 ≥ 右括号数）',
                 '`46` 全排列：`on_path` 标记已选的数',
                 '`131` 分割回文串：枚举下一刀切在哪',
                 '`79` 单词搜索：网格回溯，改字符再恢复',
                 '`51` N 皇后：排列型 + 列 / 两条对角线标记',
                 '易错：忘记 `path.pop()`；收集时没有复制 `path`'],
    ),
)
