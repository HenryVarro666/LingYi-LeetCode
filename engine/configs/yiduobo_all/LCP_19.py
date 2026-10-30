S0 = 'yrryryyr'


def _txt(S):
    if 'min_left' not in S:
        return '`r[i]` = 前 i+1 个字符里 r 的个数（前缀和）' if 'r' in S else ''
    i = S.get('index')
    if S.get('_line') in (17, 18) and i is not None:
        return f"枚举 `p2 = {i}`：`min_left = {S['min_left']}`（= 最小的 p1 − 2·r[p1−1]）"
    return f"`res = {S['res']}`，`min_left = {S['min_left']}`"


CONFIG = dict(
    num='LCP 19', title='秋叶收藏集', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='前缀和 · 枚举 p2 维护 min_left',
    tags=['灵神核心路线', '灵神题单'],
    code='''
class Solution(object):
    def minimumOperations(self, leaves):

        r = []
        for index, char in enumerate(leaves):
            if index > 0:
                r.append(r[-1])
            else:
                r.append(0)
            if char == 'r':
                r[-1] += 1

        n = len(leaves)
        res = n
        min_left = 1 - r[0] - r[0]
        for index in range(1, n - 1):
            res = min(res, min_left - index + r[index] + r[index])
            min_left = min(min_left, index - r[index - 1] - r[index - 1])

        
        return res + n - 1 - r[-1]
''',
    call=f'Solution().minimumOperations({S0!r})',
    expect=2,
    views=[
        dict(type='string', var='leaves', label='leaves', h=190, cell=80, pointers={'index': 'blue'},
             color=lambda S, i, v: ('red' if v == 'r' else 'yellow')),
        dict(type='array', var='r', label='r（r 的前缀个数）', h=190, cell=80, pointers={'index': 'blue'}),
        dict(type='text', fn=_txt, size=26, h=60),
    ],
    watch=['index', ('n', 'n', 'cyan'), ('min_left', 'min_left', 'orange'), ('res', 'res', 'green')],
    captions={
        'r = []': '`r[i]` 记录 leaves[0..i] 里 ==r 的个数==',
        'r.append(r[-1])': '不是第 0 位：先复制前一个前缀和 `r[-1]`',
        'r.append(0)': '第 0 位：前缀和从 0 开始',
        "if char == 'r'": lambda S, B, ret: f"第 {S.index} 位是 `r` → 这一位前缀和 +1" if S.char == 'r' else f"第 {S.index} 位是 `y` → 前缀和不变",
        'r[-1] += 1': '遇到 r：`r[{index}]` = =={r[-1]}==',
        'n = len': '`n = {n}`',
        'res = n': '答案初值取 `n`（最坏全改）',
        'min_left = 1': '`p1 = 1` 时 `p1 − 2·r[0]` = `1 − 2×{r[0]}` = =={min_left}==，作为 min_left 初值',
        'for index in range(1': '枚举 ==p2 = {index}==（中间 y 段的右端点）',
        'res = min': '`res = min({B.res}, min_left − p2 + 2·r[p2])` = `min({B.res}, {min_left} − {index} + {2*r[index]})` = =={res}==',
        'min_left = min': '==先算答案，再把 p2 当成下一轮的 p1 候选==：`min_left = min({B.min_left}, {index} − 2·r[{index-1}])` = =={min_left}==',
        'return res': '`res + n − 1 − r[−1]` = `{res} + {n-1} − {r[-1]}` = =={ret}==',
    },
    cards=dict(
        one_liner='操作数 = 常数 + (p1 − 2r[p1−1]) − (p2 − 2r[p2])，枚举 p2 维护最小的 p1 项',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['字符串只含 `r`（红）和 `y`（黄），可任意改字符',
                 '要变成 ==红…红 黄…黄 红…红== 的形式，三段都至少 1 个字符',
                 '求最少修改次数。本视频：`yrryryyr` → `2`'],
        quote='可以枚举p2的位置，然后找到1到p2之间，满足p1 - 2 * r[p1 - 1]最小的p1。……使用一个变量min_left记录最优的p1 - 2 * r[p1 - 1]。',
        quote_src='—— yiduobo 题解原文',
        idea=['设 `r[i]` 为前缀里 r 的个数，三段修改数相加：',
              '`tot = n−1−r[n−1] + p1−2r[p1−1] − (p2−2r[p2])`',
              'p1、p2 可拆开：枚举 p2，用 `min_left` 维护左侧最优 p1'],
        summary=['时间 `O(n)`，空间 `O(n)`；前缀和也可压成变量',
                 '先用 `min_left` 更新答案，==再用当前位置更新 min_left==，保证 p1 ≤ p2',
                 '`index` 只枚举 `1..n-2`：三段都不能为空',
                 '最后别忘了加上常数项 `n − 1 − r[-1]`'],
    ),
)
