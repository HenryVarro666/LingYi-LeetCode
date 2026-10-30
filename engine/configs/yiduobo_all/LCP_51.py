def _head(S):
    if 'now_v' not in S:
        return ''
    return f'已做料理：美味度 `now_v = {S["now_v"]}`，饱腹感 `now_limit = {S["now_limit"]}`（要求 `≥ {S["limit"]}`）'


def _cap_if(S, B, ret):
    n = S.n
    if S.level == n:
        ok = S.now_limit >= S.limit
        return (f'`level = {n}`：{n} 道料理都决定完了；饱腹感 `{S.now_limit}` ' + ('`≥` ' if ok else '`<` ')
                + f'`{S.limit}` → ' + (f'==满足==，尝试用美味度 `{S.now_v}` 更新答案' if ok else '不满足，这种组合作废'))
    return f'`level = {S.level}`：决定第 `{S.level}` 道料理做不做'


def _fits(S):
    k = S.level
    miss = [i for i in range(len(S.materials)) if S.materials[i] < S.cookbooks[k][i]]
    return k, miss


def _cap_flag(S, B, ret):
    if S.flag:
        return f'每种食材都够 → 第 `{S.level}` 道料理==能做=='
    k, miss = _fits(S)
    return f'第 `{miss[0]}` 种食材 `{S.materials[miss[0]]} < {S.cookbooks[k][miss[0]]}` 不够 → 这道料理做不了'


CONFIG = dict(
    num='LCP 51', title='烹饪料理', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='dfs 枚举做 / 不做 · 回溯食材',
    tags=['灵神核心路线', '灵神题单·链表树与回溯'],
    code='''
class Solution(object):
    def perfectMenu(self, materials, cookbooks, attribute, limit):

        global res
        res = -1
        n = len(cookbooks)

        def dfs(level, materials, now_limit, now_v):
            global res
            if level == n:
                if now_limit >= limit:
                    res = max(res, now_v)
            
                return

            dfs(level + 1, materials, now_limit, now_v)

            flag = True
            for index in range(len(materials)):
                if materials[index] < cookbooks[level][index]:
                    flag = False
                    break
            
            if flag:
                for index in range(len(materials)):
                    materials[index] -= cookbooks[level][index]

                dfs(level + 1, materials, now_limit + attribute[level][1], now_v + attribute[level][0])

                for index in range(len(materials)):
                    materials[index] += cookbooks[level][index]

        dfs(0, materials, 0, 0)
        return res
''',
    call='Solution().perfectMenu([2, 3, 2], [[1, 1, 0], [1, 2, 1], [2, 2, 1]], [[3, 2], [2, 4], [5, 3]], 5)',
    expect=5,
    views=[
        dict(type='text', h=70, fn=_head, size=24),
        dict(type='array', var='materials', label='materials（剩余食材库存）', h=130, cell=76),
        dict(type='grid', var='cookbooks', label='cookbooks[i][j]：第 i 道料理要的第 j 种食材（黄 = 当前料理）', h=170,
             color=lambda S, i, j, v: 'yellow' if i == S.get('level') else None),
        dict(type='calls', h=250, hide=('materials',)),
    ],
    watch=[('level', 'level', 'blue'), ('now_v', 'now_v', 'green'), ('now_limit', 'now_limit', 'cyan'), ('limit', 'limit', 'orange')],
    skip=['res = -1', 'n = len(cookbooks)', 'flag = True', 'for index in range', 'flag = False', 'break', 'global res', 'if materials[index] <', 'materials[index] -=', 'materials[index] +='],
    captions={
        'dfs(0, materials, 0, 0)': '从 `dfs(0, …)` 开始：按顺序决定每道料理==做 / 不做==，`n` 很小，全部试一遍',
        'if level == n': _cap_if,
        'if now_limit >= limit': lambda S, B, r: (
            f'饱腹感 `{S.now_limit} >= {S.limit}` → 达标，`res = max(res, {S.now_v})`' if S.now_limit >= S.limit
            else f'饱腹感 `{S.now_limit} < {S.limit}` → 没吃饱，这个组合不算'),
        'res = max(res, now_v)': '`res` 取旧值和 `{now_v}` 的较大者 → ==更新答案==（初值 -1 表示做不出）',
        'dfs(level + 1, materials, now_limit, now_v)': '先试==不做== 第 `{level - 1}` 道料理：食材、美味度、饱腹感都不变',
        'if flag': _cap_flag,
        'dfs(level + 1, materials, now_limit +': '==做== 第 `{level - 1}` 道：已扣掉它的食材（库存见上），饱腹感 `{now_limit}`，美味度 `{now_v}`',
        'return res': '所有组合试完：最大美味度 `{ret}`',
    },
    max_steps=110,
    cards=dict(
        one_liner='料理很少：每道做或不做，回溯时把食材还回去',
        complexity='时间 `O(2^n·m)`，空间 `O(n+m)`',
        problem=['`materials[j]` 是第 `j` 种食材的库存，`cookbooks[i][j]` 是做第 `i` 道料理要的第 `j` 种食材',
                 '`attribute[i] = [美味度, 饱腹感]`，每道料理最多做一次',
                 '饱腹感总和 `≥ limit` 时，求最大美味度，做不到返回 `-1`',
                 '本视频：3 种食材、3 道料理，`limit = 5` → `5`'],
        quote='题目的数据规模非常小，那么就可以直接暴力搜索出所有可能的料理组合，选择其中满足饱腹感且美味度最大的组合作为答案即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`dfs(level, …)`：第 `level` 道料理做还是不做',
              '不做：直接 `level + 1`；做：先检查食材够不够（`flag`）',
              '做的话先把食材扣掉，递归完再==加回去==（回溯），美味度和饱腹感随参数传递',
              '`level == n`：饱腹感达标就更新 `res`，`res` 初值 `-1`'],
        summary=['时间 `O(2^n·m)`，空间 `O(n+m)`（`m` 是食材种类数）',
                 '`materials` 是被原地修改的列表：扣完食材后必须==加回去==，否则兄弟分支会少食材',
                 '`res` 用 `global` 保存，初值 `-1` 就是“做不出”的答案',
                 '原文已是 Python 3 可运行，无需改动']
    ),
)
