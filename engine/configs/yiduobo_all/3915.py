def _get(t, p):
    r = 0
    while p > 0:
        r = max(r, t[p])
        p -= p & -p
    return r


def _fml(S):
    i = S.get('index')
    if i is None:
        return '`f[i]`：以 `nums[i]` 结尾、`nums[i]` 是==峰==的最大和；`g[i]`：`nums[i]` 是==谷=='
    k = S['k']
    return f'`index = {i}`：只能接在下标 `≤ index − k = {i - k}` 的元素后面'


def _cap_upd1(S, B, ret):
    p = B.index - B.k
    return (f'`index − k = {p}` 的元素现在才入树：`tf` 的位置 `ma − nums[{p}] = {B.ma - B.nums[p]}` ← `f[{p}] = {B.f[p]}`'
            '（==大于某值==的峰值最大和，用 `ma − 值` 翻成前缀）')


def _cap_upd2(S, B, ret):
    p = B.index - B.k
    return f'`tg` 的位置 `nums[{p}] + 1 = {B.nums[p] + 1}` ← `g[{p}] = {B.g[p]}`（==小于某值==的谷值最大和）'


def _cap_f(S, B, ret):
    r = _get(B.tg, B.v)
    return f'峰：查 `tg` 前缀 `{B.v}`（谷值 `< {B.v}`）的最大和 = `{r}` → `f[{B.index}] = {r} + {B.v}` = =={r + B.v}=='


def _cap_g(S, B, ret):
    r = _get(B.tf, B.ma - B.v - 1)
    return f'谷：查 `tf` 前缀 `ma − v − 1 = {B.ma - B.v - 1}`（峰值 `> {B.v}`）的最大和 = `{r}` → `g[{B.index}] = {r} + {B.v}` = =={r + B.v}=='


CONFIG = dict(
    num=3915, title='距离至少为 K 的交替子序列的最大和', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='峰/谷 DP + 两个值域树状数组', tags=['动态规划', '常用数据结构', '难度分 2288'],
    code='''
class Solution(object):
    def maxAlternatingSum(self, nums, k):
        
        n = len(nums)
        ma = max(nums) + 1
        f = []
        g = []
        tf = [0] * (ma + 1)
        tg = [0] * (ma + 1)

        res = 0

        for v in nums[:k]:
            f.append(v)
            g.append(v)
            res = max(res, v)
        
        def update(p, v, t):
            while p <= ma:
                t[p] = max(t[p], v)
                p += p & -p
        
        def get(p, t):
            res = 0
            while p > 0:
                res = max(res, t[p])
                p -= p & -p
            return res

        for index, v in enumerate(nums[k:], k):
            update(ma - nums[index - k], f[index - k], tf)
            update(nums[index - k] + 1, g[index - k], tg)
            f.append(get(v, tg) + v)
            g.append(get(ma - v - 1, tf) + v)
            res = max(res, f[-1], g[-1])
        
        return res
''',
    call='Solution().maxAlternatingSum([4, 1, 6, 3, 5], 2)',
    expect=15,
    skip=['n = len', 'ma = max', 'f = []', 'g = []', 'tf = [0]', 'tg = [0]', 'while p <= ma', 't[p] = max', 'p += p & p', 'p += p & -p',
          'res = 0', 'while p > 0', 'res = max(res, t[p])', 'p -= p & -p', 'return res', 'for v in nums[:k]'],
    max_steps=90,
    views=[
        dict(type='text', fn=_fml, size=24, h=50),
        dict(type='array', var='nums', label='nums', h=105, cell=70, pointers={'index': 'blue'}),
        dict(type='array', var='f', label='f（峰）', h=105, cell=70),
        dict(type='array', var='g', label='g（谷）', h=105, cell=70),
        dict(type='array', var='tf', label='tf', h=105, cell=60),
        dict(type='array', var='tg', label='tg', h=105, cell=60),
    ],
    watch=[('index', 'index', 'blue'), ('ma', 'ma', 'cyan'), ('res', 'res', 'green')],
    captions={
        'f.append(v)': '前 `k` 个元素之间距离不够，只能单独成一个序列：`f[{len(f)-1}]` = {f[-1]}',
        'res = max(res, v)': '`res` = =={res}==',
        'g.append(v)': '`g[{len(g)-1}]` 也是 `{g[-1]}`（单个元素既可当峰也可当谷）',
        'update(ma - nums': _cap_upd1,
        'update(nums[index - k] + 1': _cap_upd2,
        'f.append(get(v, tg)': _cap_f,
        'g.append(get(ma - v - 1': _cap_g,
        'res = max(res, f[-1], g[-1])': '`res = max(res, f[-1], g[-1])` = =={res}==',
    },
    cards=dict(
        one_liner='峰值 f、谷值 g，两个树状数组分别查「更小」「更大」的最大值',
        complexity='时间 `O(n log M)`，空间 `O(n + M)`',
        problem=['选下标间距 `≥ k` 的子序列，值严格交替，求元素和最大',
                 '示例：`[3,5,4,2,4]`，`k=1` → `14`',
                 '本视频：`[4,1,6,3,5]`，`k=2` → `15`（`4 < 6 > 5`）'],
        quote='令f[index]以nums[index]结尾，且nums[index]是峰值的子序列的最大和，而g[index]则表示以nums[index]结尾，且nums[index]为谷值的子序列的最大和。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[index] = max(g[p]) + v`，`p` 满足 `index − p ≥ k` 且 `nums[p] < v`',
              '值域 `≤ 10^5`，直接对值建两个树状数组：`tg` 查小于 `v`，`tf` 用 `ma − 值` 查大于 `v`',
              '到 `index` 时才把 `index − k` 放进树，距离限制自然满足'],
        summary=['时间 `O(n log M)`，`M` 是最大值；空间 `O(n + M)`',
                 '前 `k` 个元素没有转移来源，`f = g =` 自身',
                 '`update` 的参数名 `v`、`get` 的 `res` 与外层同名，画面里变量面板看外层的',
                 '原文为 Python 2 风格，无需改动，直接在 Python 3 运行'],
    ),
)
