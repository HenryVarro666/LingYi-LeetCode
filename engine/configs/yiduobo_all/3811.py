def _states(S):
    if 'x' not in S:
        return '四种前缀：异或和 = `target1` / `target1^target2` / `target2` / `0`，依次计数'
    t1, t2 = S['target1'], S['target2']
    return f"前缀异或 `x = {S['x']}`；各格对应的异或和：`{t1}` | `{t1 ^ t2}` | `{t2}` | `0`，==命中的格子变绿=="


def _hit(S, k):
    if 'x' not in S:
        return None
    t = [S['target1'], S['target1'] ^ S['target2'], S['target2'], 0]
    return 'green' if S['x'] == t[k] else None

_NAME = ['target1', 'target1^target2', 'target2', '0']
_SRC = ['zero（异或和 0 的前缀）', 't1', 'xor', 't2']
_STATE = ['t1', 'xor', 't2', 'zero']


def _cap(k):
    def f(S, B, r):
        t = [S.target1, S.target1 ^ S.target2, S.target2, 0][k]
        if S._line > 30:
            return (f'最后的 `x = {S.x}` 等于 {_NAME[k]}：整个数组的最后一段由 {_SRC[k]} 接上，答案加上它的上一轮值'
                    if S.x == t else f'`x = {S.x} ≠ {t}`，不加')
        if S.x == t:
            return f'`x = {S.x}` 等于 {_NAME[k]}：`{_STATE[k]}` 可以从 {_SRC[k]} 转移'
        return f'`x = {S.x} ≠ {t}`，`{_STATE[k]}` 不变'
    return f


CONFIG = dict(
    num=3811, title='交替按位异或分割的数目', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='前缀异或 + 四个状态变量',
    tags=['灵神题单', '动态规划', '难度分 2006'],
    code='''
class Solution:
    def alternatingXOR(self, nums, target1, target2):

        t1, xor, t2, zero = 0, 0, 0, 1
        x = 0
        mod = 10 ** 9 + 7
        for v in nums:
            x ^= v
            pre_t1, pre_xor, pre_t2, pre_zero = t1, xor, t2, zero

            if x == target1:
                t1 += pre_zero
                if t1 >= mod:
                    t1 -= mod

            if x == target1 ^ target2:
                xor += pre_t1
                if xor >= mod:
                    xor -= mod

            if x == target2:
                t2 += pre_xor
                if t2 >= mod:
                    t2 -= mod

            if x == 0:
                zero += pre_t2
                if zero >= mod:
                    zero -= mod

        res = 0
        if x == target1:
            res += pre_zero
        if x == target1 ^ target2:
            res += pre_t1
        if x == target2:
            res += pre_xor
        if x == 0:
            res += pre_t2
        return res % mod
''',
    call='Solution().alternatingXOR([1,0,0,1,1], 1, 0)',
    expect=4,
    skip=['>= mod'],
    views=[
        dict(type='array', var='nums', label='nums', cell=96, h=170,
             color=lambda S, k, v: None, dim=lambda S, k, v: False),
        dict(type='array', var=lambda S: [S['t1'], S['xor'], S['t2'], S['zero']] if 't1' in S else [0, 0, 0, 1],
             label='方案数：前缀异或和 = target1 | target1^target2 | target2 | 0', cell=120, h=200, index=False,
             color=lambda S, k, v: _hit(S, k)),
        dict(type='text', h=80, size=28, fn=_states),
    ],
    watch=[('x', 'x', 'cyan'), ('t1', 't1', 'blue'), ('xor', 'xor', 'purple'), ('t2', 't2', 'orange'), ('zero', 'zero', 'green')],
    captions={
        't1, xor, t2, zero = 0, 0, 0, 1': '四个计数：异或和为 `target1`、`target1^target2`、`target2`、`0` 的前缀的合法划分数；==零号前缀（空）异或和为 0，所以 `zero = 1`==',
        'x = 0': '`x` 是当前前缀异或和',
        'mod =': '结果对 `10^9 + 7` 取模',
        'for v in nums': '取 `nums` 的下一个数（取完就退出循环），当前 `v = {v}`',
        'x ^= v': '前缀异或和 `x ^= {v}` → ==`{x}`==',
        'pre_t1, pre_xor': '先把上一轮四个值存起来：转移只能用==上一轮==的值，避免同一个 v 被连续用两次',
        'if x == target1:': _cap(0),
        't1 += pre_zero': '`t1` += `pre_zero`（={pre_zero}）→ ==`{t1}`==：在异或和为 0 的前缀后面接一段 target1',
        'if x == target1 ^ target2:': _cap(1),
        'xor += pre_t1': '`xor` += `pre_t1`（={pre_t1}）→ ==`{xor}`==',
        'if x == target2:': _cap(2),
        't2 += pre_xor': '`t2` += `pre_xor`（={pre_xor}）→ ==`{t2}`==',
        'if x == 0:': _cap(3),
        'zero += pre_t2': '`zero` += `pre_t2`（={pre_t2}）→ ==`{zero}`==',
        'res = 0': '统计答案：只有最后一个前缀才算，用的是==最后一轮之前==（pre_*）的值',
        'return res % mod': '答案 `{res} % mod` = =={ret}==',
    },
    cards=dict(
        one_liner='区间异或转前缀异或：合法前缀只有 4 种取值循环出现',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['把 `nums` 分成连续非空块，各块异或和按 `target1, target2, target1, ...` 交替',
                 '求有多少种分割方案，对 `10^9 + 7` 取模',
                 '本视频：`nums = [1,0,0,1,1]`，`target1 = 1`，`target2 = 0`'],
        quote='对于所有合法划分的前缀异或，都需要满足：第一段异或值为target1；第二段……到第二段为止的前缀异或为target1 ^ target2；第三段……前缀异或为target2；第四段……前缀异或为0；第五段又是target1',
        quote_src='—— yiduobo 题解原文',
        idea=['合法划分的前缀异或依次是 `t1 → t1^t2 → t2 → 0 → t1 → ...`，==四个值循环==',
              '问题变成：数有多少个下标序列，前缀异或按这个顺序命中这四个值',
              '`t1[i]` 等四个状态是「结尾不超过 i」的方案数，命中目标值时从前一个状态转移'],
        summary=['时间 `O(n)`，四个变量滚动，空间 `O(1)`',
                 '转移只用上一轮的 `pre_*`，不能边改边用',
                 '答案不是四个状态之和：只有以最后一个下标结尾的前缀才算，要用 `pre_*`',
                 '原文为 Python 2 写法，本题代码无需改动即可在 Python 3 运行',
                 '对比灵神：灵神用哈希表按前缀异或和索引，不依赖周期；这里利用周期为 4'],
    ),
)
