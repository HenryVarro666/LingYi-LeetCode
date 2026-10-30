def _grp(i):
    g, tot = 1, 1
    while i >= tot:
        g += 1
        tot += g
    return g


def _col(S, i, v):
    if 'res' not in S:
        return None
    need = S['res'] * (S['res'] + 1) // 2
    if i >= need:
        return None
    return ['green', 'cyan', 'purple', 'orange', 'pink'][(_grp(i) - 1) % 5]


def _txt(S):
    if 'res' not in S:
        return '第 `i` 组放 `i` 个人：共需 `1 + 2 + … + k = k(k+1)/2` 个人'
    r, n = S['res'], len(S['grades'])
    need = r * (r + 1) // 2
    ok = '<=' if need <= n else '>'
    return f"试 ==`{r}`== 组：至少要 `{r}×{r + 1}/2 = {need}` 人 {ok} 总人数 `{n}`"


CONFIG = dict(
    num=2358, title='分组的最大数量', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='贪心 · 组大小 1,2,3… 枚举答案',
    tags=['贪心算法', '划分型贪心', '难度分 1503'],
    code='''
class Solution(object):
    def maximumGroups(self, grades):
        
        res = 1
        while res * (res + 1) // 2 <= len(grades):
            res += 1
        
        return res - 1
''',
    call='Solution().maximumGroups([10,6,12,7,3,5,9,2,1,8])',
    expect=4,
    views=[
        dict(type='text', fn=_txt, size=26),
        dict(type='array', var='grades', label='grades 的 10 个人，按 1、2、3… 人一组依次占位（同色 = 同一组）', cell=84, color=_col, h=300),
        dict(type='text', fn=lambda S: '组的人数取 1,2,3,… 最省人；按分数从低到高依次填进去，总分自然递增', size=24),
    ],
    watch=[('res', 'res', 'green'), ('len(grades)', 'len(grades)', 'cyan'), ('res*(res+1)//2', '需要人数', 'yellow')],
    captions={
        'res = 1': '先假设能分 `1` 组，然后往上试',
        'while res': lambda S, B, r: (f"`{S.res} × {S.res + 1} // 2 = {S.res * (S.res + 1) // 2} <= {len(S.grades)}` → ==能分 {S.res} 组==，试试更多"
                                      if S.res * (S.res + 1) // 2 <= len(S.grades)
                                      else f"`{S.res} × {S.res + 1} // 2 = {S.res * (S.res + 1) // 2} > {len(S.grades)}` → 人数不够，==不能分 {S.res} 组=="),
        'res += 1': '`res` → {res}：继续检查分 `{res}` 组需要的人数',
        'return res - 1': '`res = {res}` 是第一个人数不够的组数，答案是 `res - 1` = =={res - 1}==',
    },
    cards=dict(
        one_liner='人数按 1、2、3… 一组一组排，只看人够不够',
        complexity='时间 `O(√n)`，空间 `O(1)`',
        problem=['把学生分成有序的若干组：后一组总分更高，且人数更多',
                 '求最多能分几组',
                 '示例：`[10,6,12,7,3,5]` → `3`；本视频 10 人 → `4`'],
        quote='为了尽可能多地分组，在分组人数上的最优做法就是按1、2、3、...，这种形式类推上去。',
        quote_src='—— yiduobo 题解原文',
        idea=['人数按 `1,2,3,…` 递增最省人；分数从低到高依次放进各组，后一组每个人都不低于前一组且多一个人，总分必然更高',
              '所以根本不用管怎么分，只看 `k(k+1)/2 <= n`',
              '从 1 往上枚举 `res`，找到最大的 `k`'],
        summary=['时间 `O(√n)`，空间 `O(1)`',
                 '循环退出时 `res` 是第一个不满足的值，所以返回 `res - 1`',
                 '分数的具体数值完全不影响答案，只与人数 `n` 有关',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`'],
    ),
)
