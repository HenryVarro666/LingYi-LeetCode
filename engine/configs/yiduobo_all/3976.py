def _idx(S):
    v = S.get('v')
    if v is None or 'nums' not in S:
        return 0 if 'nums' in S else None
    return S['nums'].index(v)


def _txt(S):
    if 'f' not in S:
        return '四种状态：`f` 没操作 · `m` 乘中 · `d` 除中 · `g` 操作已结束'
    g = S.get('g')
    g = '无' if g is None else g
    return f"`f = {S['f']}`（没操作）  `m = {S['m']}`（乘中）  `d = {S['d']}`（除中）  `g = {g}`（已结束）"


CONFIG = dict(
    num=3976, title='乘以系数后最大子数组和', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='四状态 DP · 变量迭代',
    tags=['灵神核心路线', '难度分 1981'],
    code='''
class Solution(object):
    def maxSubarraySum(self, nums, k):
        
        def div(x):
            if x >= 0:
                return x // k
            return -(-x // k)
        
        f = nums[0]
        m = nums[0] * k
        d = div(nums[0])
        g = None

        res = max(f, m, d)

        for v in nums[1:]:
            nxt_f = max(f, 0) + v
            nxt_m = max(f, m, 0) + v * k
            nxt_d = max(f, d, 0) + div(v)
            nxt_g = max(m, d) + v
            if g is not None:
                nxt_g = max(nxt_g, g + v)
            f, m, d, g = nxt_f, nxt_m, nxt_d, nxt_g
            res = max(res, f, m, d, g)
        
        return res
''',
    call='Solution().maxSubarraySum([-2, 3, 4, -5], 2)',
    expect=14,
    skip=['def div'],
    views=[
        dict(type='text', fn=_txt, size=25, h=70),
        dict(type='array', var='nums', label='nums', h=190, cell=90, pointers={'v': 'blue'},
             color=lambda S, i, v: 'blue' if i == _idx(S) else None),
        dict(type='text', h=60, size=26,
             fn=lambda S: f"当前最优 `res = {S['res']}`" if 'res' in S else ''),
    ],
    watch=['v', ('f', 'f', 'cyan'), ('m', 'm', 'orange'), ('d', 'd', 'purple'), ('g', 'g', 'pink'), ('res', 'res', 'green')],
    captions={
        'f = nums[0]': '第 0 个数：没操作的最大子段和就是它自己 `f = {f}`',
        'm = nums[0] * k': '它也可以被乘：`m = {nums[0]} × {k}` = =={m}==',
        'd = div(nums[0])': '或被除（正数向下、负数向上取整）：`d = {d}`',
        'g = None': '刚开始还没有“操作已结束”的状态，`g = None`',
        'res = max(f, m, d)': '只有一个数时答案取三者最大：`res = {res}`',
        'if x >= 0': lambda S, B, r: f'`x = {S.x}`：非负，向下取整，直接 `//`' if S.x >= 0 else f'`x = {S.x}`：负数要向上取整，不能直接 `//`',
        'return x // k': '`{x} // {k}` = =={ret}==',
        'return -(-x // k)': '负数：先取反再 `//` 再取反，相当于向上取整 = =={ret}==',
        'for v in nums[1:]': '从下标 1 往后，处理 `v = {v}`',
        'nxt_f =': '没操作：前面为负就丢掉重来 `max({f}, 0) + {v}` = =={nxt_f}==',
        'nxt_m =': '乘中：可接没操作 `f`、乘中 `m`，或自己开头 `0`：`max({f}, {m}, 0) + {v}×{k}` = =={nxt_m}==',
        'nxt_d =': '除中：可接 `f`、`d` 或自己开头：`max({f}, {d}, 0) + div({v})` = =={nxt_d}==',
        'nxt_g = max(m': '操作段刚结束：`v` 不操作，接在 `m` 或 `d` 后面：`max({m}, {d}) + {v}` = {nxt_g}',
        'if g is not None': lambda S, B, r: '`g` 已有值：还可以接着上一轮的 `g` 继续不操作' if S.g is not None else '`g` 还是 None：没有上一轮的“已结束”状态可接，跳过',
        'nxt_g = max(nxt_g': '`nxt_g = max(nxt_g, g + v)` = =={nxt_g}==',
        'f, m, d, g =': '四个状态同时更新：`f={f}`，`m={m}`，`d={d}`，`g={g}`',
        'res = max(res': '==每一轮都要用四个状态更新答案==：`res = {res}`',
        'return res': '答案 `{res}`',
    },
    cards=dict(
        one_liner='贪心很难界定除法生效段，改用四状态 DP',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['选一段子数组，每个数 ==乘 k== 或 ==除 k==（正数向下、负数向上取整）',
                 '再求操作后任意非空子数组的最大和',
                 '本视频：`[-2,3,4,-5], k=2` → `14`'],
        quote='贪心不好使，那么就自然考虑使用动态规划。……可以分为四种，因此可以令f[index]、m[index]、d[index]、g[index]分别表示对于nums[0]到nums[index]。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f`：还没操作；`m`：正在乘，nums[index] 是乘段最后一个；`d`：正在除，同理',
              '`g`：操作段已结束，之后只能不操作',
              '`m` 只能接 `f` 或 `m`，`d` 只能接 `f` 或 `d`，乘除不混用',
              '每一轮用四个状态的最大值更新答案'],
        summary=['时间 `O(n)`，空间 `O(1)`（用变量迭代代替数组）',
                 '`g` 初始为 `None`，用到前要判断',
                 '负数除要向上取整：`-(-x // k)`，不能直接 `x // k`',
                 '对比灵神：灵神只用三阶段、乘除各跑一遍；yiduobo 用四状态一遍跑完'],
    ),
)
