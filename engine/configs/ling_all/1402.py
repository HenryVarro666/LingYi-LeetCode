from itertools import accumulate as _acc


def _done(S):
    """已经选入的菜数 k：f 等于前 k 个前缀和之和"""
    a, f = S['satisfaction'], S.get('f', 0)
    tot = 0
    if f == 0:
        return 0
    for k, p in enumerate(_acc(a), 1):
        tot += p
        if tot == f:
            return k
    return 0


def _color(S, i, v):
    if 'f' not in S or S['_line'] < 5:
        return None
    k = _done(S)
    if i < k:
        return 'green'
    if S['_line'] == 6 and 's' in S and i == k:
        return 'yellow'
    if S['_line'] == 7 and 's' in S and i == k:
        return 'red'
    return None


def _txt(S):
    a = S['satisfaction']
    if 'f' not in S or S['_line'] < 5:
        return '先把满意度从大到小排好'
    k = _done(S)
    pre = sum(a[:k])
    f = S['f']
    if 's' in S and S['_line'] >= 6:
        return f"现有 `f` = `{f}`（做 `{k}` 道）；考虑第 `{k + 1}` 道：前 `{k + 1}` 个数之和 `s` = ==" + str(S['s']) + "=="
    return f"已选前 `{k}` 道，`f` = ==" + str(f) + "=="


CONFIG = dict(
    num=1402, title='做菜顺序', difficulty='Hard', category='贪心与思维',
    author='灵茶山艾府', technique='排序 + 前缀和递推 f(k) = f(k-1) + s',
    tags=['灵神题单', '难度分 1679'],
    code='''
class Solution:
    def maxSatisfaction(self, satisfaction: List[int]) -> int:
        satisfaction.sort(reverse=True)
        f = 0  # f(0) = 0
        for s in accumulate(satisfaction):  # satisfaction 的前缀和
            if s <= 0:  # 后面不可能找到更大的 f(k)
                break
            f += s  # f(k) = f(k-1) + s
        return f
''',
    call='Solution().maxSatisfaction([-1,-8,0,5,-9])',
    expect=14,
    views=[
        dict(type='array', var='satisfaction', label='satisfaction（从大到小；绿 = 已选，黄 = 正在考虑，红 = 放弃）', h=300, cell=100, color=_color),
        dict(type='text', size=34, fn=_txt),
    ],
    watch=['s', ('f', 'f', 'green')],
    captions={
        'satisfaction.sort': '==从大到小排序==：做 `k` 道菜一定选最大的 `k` 个，大的后做',
        'f = 0': '`f` 是做 `k` 道菜的最大总和，`f(0) = 0`',
        'for s in accumulate': '`s` = 前缀和 `a[0] + … + a[k-1]` = {s}',
        'if s <= 0': lambda S, B, r: (f'`s = {S.s} <= 0`：再多做一道，每道菜的完成时间都 +1，总和反而不增 → ==退出循环==' if S.s <= 0
                                      else f'`s = {S.s} > 0`：多做一道，所有菜的系数各 +1，总和增加 `s`，继续'),
        'break': '跳出循环：后面的前缀和只会更小',
        'f += s': '`f(k) = f(k-1) + s`：`{B.f} + {s}` = =={f}==',
        'return f': '退出循环时的 `f` 最大 → =={ret}==',
    },
    cards=dict(
        one_liner='大的菜放后面做；多做一道菜，总和增加前缀和',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['做每道菜 1 单位时间，系数 = 完成时间 × 满意度', '可以任意排顺序，也可以不做某些菜，求系数之和最大值',
                 '示例：`[-1,-8,0,5,-9]` → `14`（做 `-1, 0, 5`）'],
        quote='假设 a 中最大的两个数分别是 4 和 3：先 4 后 3 总和为 10，先 3 后 4 总和为 11。这说明 a[i] 大的菜应该后做。所以 f(k) = f(k-1) + (a[0] + a[1] + … + a[k-1])，右边的和式是 a 的前缀和。',
        quote_src='—— 灵茶山艾府题解',
        idea=['枚举做 `k` 道菜：选最大的 `k` 个，大的放后面（排序不等式）', '从大到小排序后 `f(k) = k·a[0] + … + a[k-1]`', '相邻两项 `f(k) − f(k-1)` 恰好是前缀和 `s`',
              '`s > 0` 就接着加；`s ≤ 0` 后面只会更小，直接停'],
        summary=['时间 `O(n log n)`，空间 `O(1)`', '`s <= 0` 即退出：后面全是负数，前缀和不会再变正',
                 '`f` 在退出前严格递增，所以最后的 `f` 就是答案；全是负数时返回 `0`', '注意：`satisfaction.sort` 会原地修改输入'],
    ),
)
