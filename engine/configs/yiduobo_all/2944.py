P0 = [10, 2, 9, 4, 8]


def _lo(S):
    return max(0, S['i'] - S['free'])


def _fml(S):
    if 'i' not in S or 'mi' not in S:
        return '`f[j]` = 买下反转后前 `j` 个水果的最小代价'
    if S['_line'] <= 11:
        lo = _lo(S)
        return f"买第 `{S['i'] + 1}` 个（价格 `{S['prices'][S['i']]}`），免费区间长 `free = {S['free']}` → 候选 `f[{lo}] ~ f[{S['i']}]`，取最小 `mi = {S['mi']}`"
    return f"`f[{S['i'] + 1}] = mi + prices[{S['i']}]` = `{S['mi']} + {S['prices'][S['i']]}` = =={S['mi'] + S['prices'][S['i']]}=="


def _pcolor(S, k, v):
    if 'i' not in S or 'free' not in S:
        return None
    i = S['i']
    if k == i:
        return 'yellow'
    if S.get('mi') is not None and S['_line'] <= 11 and 'j' in S and S['j'] <= k < i:
        return 'blue'
    return 'green' if k < i and 'j' not in S else None


def _fcolor(S, k, v):
    if 'i' not in S or 'j' not in S:
        return None
    lo = _lo(S)
    if S['_line'] in (9, 10, 11) and k == S['j']:
        return 'yellow'
    if lo <= k <= S['i']:
        return 'blue'
    return None


CONFIG = dict(
    num=2944, title='购买水果需要的最少金币数', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='反转数组 · 前缀 DP 枚举区间最小值',
    tags=['灵神题单·动态规划', '难度分 1709'],
    code='''
class Solution(object):
    def minimumCoins(self, prices):

        n = len(prices)
        free = n

        prices.reverse()
        f = [0]
        for i in range(n):
            mi = None
            for j in range(i, max(-1, i - free - 1), -1):
                if mi is None or mi > f[j]:
                    mi = f[j]
            f.append(mi + prices[i])
            free -= 1

        return f[-1]
''',
    call=f'Solution().minimumCoins({P0})',
    expect=16,
    skip=['mi = None'],
    views=[
        dict(type='text', fn=_fml, size=22, h=70),
        dict(type='array', var='prices', label='反转后的 prices（黄 = 这次买的，蓝 = 这次买它能免费拿到的）', h=180, cell=90, color=_pcolor),
        dict(type='array', var='f', label='f[j]（蓝 = 候选范围，黄 = 正在比较的 f[j]）', h=180, cell=90, color=_fcolor),
    ],
    watch=[('i', 'i', 'pink'), ('free', 'free', 'cyan'), ('j', 'j', 'blue'), ('mi', 'mi', 'orange')],
    captions={
        'n = len': '`n = {n}`',
        'free = n': '`free`：当前这个水果最多能免费拿到几个（反转后在它前面）。先设为 `n`，每处理一个水果减 1',
        'prices.reverse()': '==反转== prices：原来「买 i 免费拿后面」，变成「买 i 免费拿前面」',
        'f = [0]': '`f[0] = 0`：一个水果都不用买，代价 0',
        'for i in range': lambda S, B, r: (f'算 `f[{S.i + 1}]`：反转后第 `{S.i + 1}` 个水果必须买，价格 `{S.prices[S.i]}`' if S.get('i') != B.get('i') and S.get('i') is not None and 'free' in S and len(S.f) == S.i + 1 else '所有水果都算完，答案是 `f[n]`'),
        'for j in range': lambda S, B, r: (f'`j = {S.j}`：假设 `f[{S.j}]` 之后的 `{S.i - S.j}` 个水果都被免费拿到' if 'j' in S and S.j != B.get('j') else '这一轮的候选都看完了'),
        'if mi is None': lambda S, B, r: (f'`mi` 还是空 → 直接取 `f[{S.j}] = {S.f[S.j]}`' if S.mi is None else f'`mi = {S.mi}` vs `f[{S.j}] = {S.f[S.j]}`：' + ('更小，更新' if S.mi > S.f[S.j] else '不更小，保持')),
        'mi = f[j]': '`mi` 更新为 `f[{j}] = {mi}`',
        'f.append': '`f[{i+1}] = mi + prices[{i}] = {mi} + {prices[i]}` = =={f[-1]}==',
        'free -= 1': '下一个水果能免费覆盖的范围少 1：`free = {free}`',
        'return f[-1]': '`f[n]` = 买下全部水果的最小代价 = =={ret}==',
    },
    cards=dict(
        one_liner='反转后：买第 i 个能免费拿前面一段，f[i] 从一段 f 的最小值转移',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['`prices[i]` 是买第 `i+1` 个水果的价格；买第 `i` 个（从 1 起）可免费拿 `[i+1, 2i]`',
                 '求拿到所有水果的最少金币',
                 f'示例：`prices = {P0}` → `16`'],
        quote='用过代价price[i]购买i为起点的区间，看着有点别扭，不妨将price倒转过来……令f[i]表示购买前i种水果的最小代价，那么对于f[i]，必须购买price[i]，而f[i]则可以从f[i - 1]到f[(i - 1) - (n - i + 1) + 1]中的最小值转移过来。',
        quote_src='—— yiduobo 题解原文',
        idea=['反转后，买第 `i` 个水果免费拿到的是它==前面==的一段',
              '`f[i]` 必买 `prices[i]`，前面能免费的长度是 `free`，从 `f` 的一个区间里取最小值',
              '每往后一个水果，`free` 减 1；区间左端不低于 0'],
        summary=['时间 `O(n^2)`：两层循环；空间 `O(n)`',
                 '易错：`range(i, max(-1, i - free - 1), -1)` 的左端要截到 0',
                 '`prices.reverse()` 会改写输入数组',
                 '对比灵神：灵神倒着算 + 单调队列，把区间最小值降到 `O(n)`',
                 '原文已是 Python 3 可运行的写法，未做修改'],
    ),
)
