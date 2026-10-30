NV, KV = 7, 4


def _diffs(S):
    r = S.get('res') or []
    return [abs(a - b) for a, b in zip(r, r[1:])]


def _res_color(S, i, v):
    if 'res' not in S:
        return None
    if v > KV:
        return 'blue'          # 降序铺好的 n..k+1
    if 'low' in S and S['_line'] in (7, 10) and i == len(S['res']) - 1:
        return 'yellow'        # 刚放进去的
    return 'green'


def _diff_color(S, i, v):
    d = _diffs(S)
    if v == 1 and d.index(v) != i:
        return None            # 重复的 1，没有贡献新的差值
    return 'green' if d.index(v) == i and v > 1 else ('cyan' if d.index(v) == i else None)


def _info(S):
    if 'res' not in S:
        return ''
    ds = sorted(set(_diffs(S)))
    return f'不同的相邻差：`{ds}` → ==共 {len(ds)} 种==（目标 k = {KV}）'


def _add(which):
    def f(S, B, ret):
        r = S.res
        v = r[-1]
        d = abs(r[-1] - r[-2])
        tag = '最小' if which == 'low' else '最大'
        return f'放入剩下的{tag}数 `{v}`：和前一个 `{r[-2]}` 差 =={d}==，差值依次是 k, k−1, k−2, …'
    return f


CONFIG = dict(
    num=667, title='优美的排列II', difficulty='Medium', category='数学',
    author='yiduobo', technique='构造法 · 折线交替取数',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution(object):
    def constructArray(self, n, k):
        res = [x for x in range(n, k, -1)]
        low = 1
        high = k
        while low <= high:
            res.append(low)
            low += 1
            if low <= high:
                res.append(high)
                high -= 1

        return res
''',
    call=f'Solution().constructArray({NV}, {KV})',
    expect=[7, 6, 5, 1, 4, 2, 3],
    views=[
        dict(type='array', var='res', h=210, color=_res_color, cell=96,
             label='res（蓝 = 降序铺好的 n..k+1，绿 = 折线部分，黄 = 刚放入）'),
        dict(type='array', var=_diffs, h=190, color=_diff_color, cell=96,
             label='相邻差 |res[i] − res[i−1]|（亮色 = 第一次出现的差值）'),
        dict(type='text', fn=_info, size=30),
    ],
    watch=[('low', 'low', 'blue'), ('high', 'high', 'pink'), ('len(res)', 'len(res)'), ('k', 'k', 'yellow')],
    captions={
        'res = [x for x': '先==降序==放 `n` 到 `k + 1`：`{res}`，相邻差都是 1',
        'low = 1': '剩下 `1..k` 用折线构造：`low = 1` 从小往大取',
        'high = k': '`high = k = {high}` 从大往小取；`k + 1` 后面接 `1`，差正好是 ==k==',
        'while low <= high': lambda S, B, r: ('`low = {} <= high = {}`：还有数没放'.format(S.low, S.high) if S.low <= S.high
                                              else f'`low = {S.low} > high = {S.high}`：`1..k` 全部放完'),
        'res.append(low)': _add('low'),
        'low += 1': '`low` → {low}',
        'if low <= high': lambda S, B, r: (f'`{S.low} <= {S.high}`：还能再放一个大的' if S.low <= S.high
                                           else f'`{S.low} > {S.high}`：数用完了，不再放 high'),
        'res.append(high)': _add('high'),
        'high -= 1': '`high` → {high}',
        'return res': '差值覆盖了 `1..k`，而且都在 `1..k` 之间 → 返回 `{ret}`',
    },
    cards=dict(
        one_liner='大数降序铺在前面，小数 1..k 左右横跳造出 k, k−1, …, 1',
        complexity='时间 `O(n)`，空间 `O(1)`（不计答案）',
        problem=['给你 `n` 和 `k`（`1 <= k < n`），构造 `1..n` 的一个排列',
                 '要求相邻两数之差的绝对值==恰好有 k 种不同的值==，返回任意一种',
                 '示例：`n = 3, k = 2` → `[1,3,2]`（差为 2、1）',
                 '本视频：`n = 7, k = 4` → `[7,6,5,1,4,2,3]`'],
        quote='我们可以将上面的构造调换一下顺序，变成 k + 1，1，k，2，k - 1，3，...，(k + 1) / 2 ……此时如果我们按照n到k + 2到降序插入到k + 1前面，那么这些项两两之间的差值就是1。',
        quote_src='—— yiduobo 题解原文',
        idea=['折线 `1, k+1, 2, k, 3, …`：差值依次是 `k, k−1, …, 1`，正好覆盖 1..k',
              '剩下的 `k+2..n` 怎么放？把折线==倒过来==，以 `k+1` 开头',
              '再把 `n, n−1, …, k+2` 降序接在 `k+1` 前面，新增的差全是 1'],
        summary=['时间 `O(n)`；答案数组之外只用 `low`、`high` 两个变量',
                 '`range(n, k, -1)` 生成的是 `n..k+1`，==包含 k+1==',
                 '内层 `if low <= high` 防止 k 为奇数时中间的数被放两次',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串'],
    ),
)
