E0 = [-2, 4, 1, -3, 5, -6, 2, -1, 3]
K = 3


def _fml(S):
    if 'start' not in S:
        return '反转后：求「以 k 为步长」的最大前缀和'
    if 'index' in S and S['_line'] >= 8:
        return f"本条链：`now = {S['now']}`　　全局 `res = {S['res']}`"
    return f"第 {S['start'] + 1} 条链：从下标 `{S['start']}` 开始，每次 +{S['k']}"


def _color(S, j, v):
    if 'start' not in S:
        return None
    st, k = S['start'], S['k']
    if j % k != st:
        return None
    if 'index' in S and j == S['index']:
        return 'yellow'
    if 'index' in S and j < S['index'] and S['_line'] >= 8:
        return 'green'
    return 'blue'


CONFIG = dict(
    num=3147, title='从魔法师身上吸取的最大能量', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='反转数组 · 枚举起点按步长求前缀和',
    tags=['灵神题单·贪心与思维', '难度分 1460'],
    code='''
class Solution(object):
    def maximumEnergy(self, energy, k):

        res = -1000
        energy.reverse()
        for start in range(k):
            now = 0
            for index in range(start, len(energy), k):
                now += energy[index]
                res = max(now, res)
        
        return res
''',
    call=f'Solution().maximumEnergy({E0}, {K})',
    expect=8,
    views=[
        dict(type='text', fn=_fml, size=26, h=60),
        dict(type='array', var=lambda S: E0, label='原数组 energy', h=170, cell=86),
        dict(type='array', var='energy', label='反转后的 energy（同色 = 同一条步长为 k 的链，黄 = 当前，绿 = 已累加）', h=200, cell=86,
             pointers={'start': 'pink'}, color=_color),
    ],
    watch=[('start', 'start', 'pink'), ('index', 'index', 'blue'), ('now', 'now', 'cyan'), ('res', 'res', 'green')],
    captions={
        'res = -1000': '`res = -1000`：题目保证 `energy[i] >= -1000`，所以它比任何答案都小',
        'energy.reverse()': '后缀和不好算 → ==反转数组==，变成「从 0 往后、步长 k 的前缀和」',
        'for start in range': lambda S, B, r: (f'前缀的起点只可能是 `0 ~ k-1`，现在 `start = {S.start}`' if 'start' in S and S.start != B.get('start') else '所有起点都枚举完了'),
        'now = 0': '新的一条链，`now` 清零',
        'for index in range': lambda S, B, r: (f'沿着步长 `{S.k}` 往后：`index = {S.index}`' if 'index' in S and S.index != B.get('index') else f'`start = {S.start}` 这条链走完了'),
        'now += energy[index]': '前缀和累加：`now += {energy[index]}` → =={now}==',
        'res = max': '`res = max({B.res}, {now})` = =={res}==：每个前缀都是一个可能的答案',
        'return res': '最大的前缀和（= 原数组最大的后缀和）：=={ret}==',
    },
    cards=dict(
        one_liner='最大后缀和 → 反转成最大前缀和，按步长 k 逐条链枚举',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`energy[i]` 可正可负，选一个起点 `p`，每次跳 `k` 步直到越界，累加沿途能量',
                 '求累加和的最大值',
                 f'示例：`energy = {E0}`，`k = {K}` → `8`'],
        quote='题目要求计算的是最大的后缀和，于是可以先将数组反转过来，这样一来问题就变成了求数组中以k位步长分岔的最大前缀和。',
        quote_src='—— yiduobo 题解原文',
        idea=['反转后，原来的终点变成起点，起点只会是 `0 ~ k-1`',
              '对每个起点，沿步长 `k` 往后走，边走边累加 `now`',
              '每走一步都用当前前缀和去更新答案 `res`'],
        summary=['时间 `O(n)`（k 条链加起来恰好走完整个数组），空间 `O(1)`',
                 '易错：`now` 要在每个 `start` 重新清零',
                 '`res` 初值 `-1000` 依赖题目数据范围，更稳妥可用 `-inf`',
                 '对比灵神：灵神不反转，倒着原地累加；这里是反转后正着枚举',
                 '原文已是 Python 3 可运行的写法，未做修改'],
    ),
)
