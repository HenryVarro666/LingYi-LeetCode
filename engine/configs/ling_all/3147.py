E0 = [-2, 4, 1, -3, 5, -6, 2, -1, 3]
K = 3


def _fml(S):
    if 'i' not in S:
        return '`energy[i]` 变成「从 i 出发一直跳到末尾」的能量和（后缀和）'
    i, k = S['i'], S['k']
    if S['_line'] >= 6:
        return f"`energy[{i}] = {E0[i]} + energy[{i + k}]` = =={S['energy'][i]}=="
    return f'`i = {i}`：它能跳到 `i + k = {i + k}`，后面的已经是后缀和'


CONFIG = dict(
    num=3147, title='从魔法师身上吸取的最大能量', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='倒序原地累加后缀和',
    tags=['灵神题单·贪心与思维', '难度分 1460'],
    code='''
class Solution:
    def maximumEnergy(self, energy: List[int], k: int) -> int:
        for i in range(len(energy) - k - 1, -1, -1):
            energy[i] += energy[i + k]
        return max(energy)
''',
    call=f'Solution().maximumEnergy({E0}, {K})',
    expect=8,
    views=[
        dict(type='text', fn=_fml, size=26, h=60),
        dict(type='array', var=lambda S: E0, label='原数组 energy', h=170, cell=86),
        dict(type='array', var='energy', label='energy（原地变成后缀和：绿 = 已算好，黄 = 正在更新，蓝 = 它加上的那个）', h=200, cell=86,
             pointers={'i': 'blue'},
             color=lambda S, j, v: (None if 'i' not in S else 'yellow' if j == S['i'] else 'blue' if j == S['i'] + S['k'] else 'green' if j > S['i'] else None)),
    ],
    watch=[('i', 'i', 'blue'), ('k', 'k', 'pink'), ('i+k', 'i + k', 'cyan')],
    captions={
        'for i in range': lambda S, B, r: (f'`i = {S.i}`：==倒着==算，保证 `energy[i+k]` 已经是后缀和' if S.get('i', -1) >= 0 and S.get('i') != B.get('i')
                                           else '所有起点都算完，每个位置都是「从这里出发的能量和」'),
        'energy[i] += energy[i + k]': '`energy[{i}] += energy[{i+k}]`：从 {i} 出发 = 自己 + 跳到 {i+k} 之后的总和 = =={energy[i]}==',
        'return max(energy)': '每个位置都是一个起点的总能量，==取最大值== = =={ret}==',
    },
    cards=dict(
        one_liner='从特殊到一般：k=1 是后缀和，一般情况每隔 k 倒着累加',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`n` 个魔法师排成一排，`energy[i]` 可正可负',
                 '选一个起点，吸收后立即跳到 `i + k`，直到越界，沿途能量全部吸收',
                 '求能获得的最大能量',
                 f'示例：`energy = {E0}`，`k = {K}` → `8`'],
        quote='枚举终点 n-k,n-k+1,…,n-1，倒着遍历，步长为 -k。遍历的同时累加元素和 sufSum，计算 sufSum 的最大值，即为答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先想 `k=1`：起点 `i` 的能量和就是==后缀和==，倒着累加',
              '`k=2` 有两个终点 `n-2`、`n-1`，各自倒着按步长 `-k` 累加',
              '写法二：原地让 `energy[i] += energy[i+k]`，最后取最大值'],
        summary=['时间 `O(n)`，空间 `O(1)`（会改写输入数组）',
                 '易错：终点是 `n-k ~ n-1` 共 k 个，循环从 `n-k-1` 开始',
                 '写法一：枚举终点，用 accumulate 对 `range(i, -1, -k)` 求前缀和，取最大',
                 '同类思路：倒着遍历、把后面的结果直接用在前面'],
    ),
)
