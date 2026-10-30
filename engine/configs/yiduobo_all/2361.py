REG = [1, 6, 9, 5]
EXP = [5, 2, 3, 10]


def _fml(S):
    if 'new_f' not in S:
        return '`f` = 常规线当前站最少费用，`g` = 特快线当前站最少费用'
    r, e, c = S['r'], S['e'], S['expressCost']
    return (f"`f' = min({S['f']}+{r}, {S['g']}+{e})` = =={S['new_f']}==　　"
            f"`g' = min({S['f']}+{r}+{c}, {S['g']}+{e})` = =={S['new_g']}==") if S['_line'] >= 12 else '`f`、`g` 都由上一站的 `f`、`g` 推出'


CONFIG = dict(
    num=2361, title='乘坐火车路线的最少费用', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='双状态 DP · 滚动变量',
    tags=['灵神题单·动态规划'],
    code='''
class Solution(object):
    def minimumCosts(self, regular, express, expressCost):

        f = 0
        g = expressCost

        res = []

        for r, e in zip(regular, express):
            new_f = min(f + r, g + e)
            new_g = min(f + r + expressCost, g + e)
            f, g = new_f, new_g
            res.append(f)
        
        return res
''',
    call=f'Solution().minimumCosts({REG}, {EXP}, 8)',
    expect=[1, 7, 14, 19],
    views=[
        dict(type='text', fn=_fml, size=24, h=70),
        dict(type='array', var='regular', label='regular[i]：常规线第 i 站 → 第 i+1 站的费用', h=140, cell=90,
             color=lambda S, i, v: 'green' if i < len(S['res']) else 'yellow' if i == len(S['res']) else None),
        dict(type='array', var='express', label='express[i]：特快线的费用', h=140, cell=90,
             color=lambda S, i, v: 'green' if i < len(S['res']) else 'yellow' if i == len(S['res']) else None),
        dict(type='array', var='res', label='res（到每一站的最少费用 = 每轮的 f）', h=140, cell=90, color=lambda S, i, v: 'green'),
    ],
    watch=[('f', 'f', 'blue'), ('g', 'g', 'pink'), ('r', 'r', 'cyan'), ('e', 'e', 'orange'), ('res', 'res', 'green')],
    captions={
        'f = 0': '起点在常规线第 0 站：`f = 0`，不花钱',
        'g = expressCost': '想进特快线要先付 `expressCost = {expressCost}`：`g = {g}`',
        'res = []': '`res` 记录到每一站的最少费用',
        'for r, e in zip': lambda S, B, ret: (f'处理第 {len(S.res)+1} 段：常规线 `r = {S.r}`，特快线 `e = {S.e}`' if len(S.res) < len(S.regular) else '所有站都处理完了'),
        'new_f = min': '到常规线下一站：常规线走 `{B.f}+{r}={B.f+r}`，或特快线走 `{B.g}+{e}={B.g+e}` 再无代价下车 → ==取小 {new_f}==',
        'new_g = min': '到特快线下一站：常规线走完再付 `{expressCost}` 换乘 `{B.f+r+expressCost}`，或特快线直接走 `{B.g+e}` → ==取小 {new_g}==',
        'f, g = new_f': '同时更新（用旧值算新值，所以先存到 new_f、new_g）：`f = {f}`，`g = {g}`',
        'res.append': '`f <= g` 恒成立（特快线下车免费）→ 答案只记 `f = {f}`',
        'return res': '每一站的最少费用：=={ret}==',
    },
    cards=dict(
        one_liner='f、g 分别记「在常规线 / 特快线第 i 站」的最少费用',
        complexity='时间 `O(n)`，空间 `O(1)`（不算返回数组）',
        problem=['有常规线和特快线两条路线，第 `i` 站到第 `i+1` 站的费用分别是 `regular[i]`、`express[i]`',
                 '从常规线换到特快线要付 `expressCost`，换回常规线免费',
                 '求从第 0 站出发到每一站的最少费用',
                 '示例：`regular=[1,6,9,5]`，`express=[5,2,3,10]`，`expressCost=8` → `[1,7,14,19]`'],
        quote='令f[i]和g[i]分别表示来到常规线路的第i站以及特快线路的第i站所需的最少费用……很明显，每一轮的f[i]都小于等于g[i]，因此只需将每一轮的f[i]加入到答案中即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i]` 来自：常规线走一步，或特快线走一步后==免费转回==常规线',
              '`g[i]` 来自：常规线走一步后==付 expressCost 转特快==，或特快线走一步',
              '每一站只依赖上一站，所以用变量 `f`、`g` 滚动，省掉数组'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：`f, g = new_f, new_g` 要同时更新，不能先改 f 再用它算 g',
                 '特快线转回常规线免费，所以 `f <= g`，答案取 `f`',
                 '原文已是 Python 3 可运行的写法，未做修改'],
    ),
)
