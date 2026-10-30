def _cur(S):
    return len(S['f']) - S['p'] if 'p' in S else None


def _txt(S):
    if 'res' not in S or 'p' not in S:
        return '先造斐波那契数列：不断追加 `f[-1] + f[-2]`，直到 `f[-1] >= k`' if 'f' in S else ''
    return f"还剩 `k = {S['k']}`，已选 `{S['res']}` 个；每次选 ==不超过 k 的最大项=="


CONFIG = dict(
    num=1414, title='和为K的最少斐波那契数字数目', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='贪心 · 每次取不超过 k 的最大斐波那契数',
    tags=['灵神题单', '数学算法'],
    code='''
class Solution(object):
    def findMinFibonacciNumbers(self, k):

        f = [1, 1]
        while f[-1] < k:
            f.append(f[-1] + f[-2])
        
        res = 0
        p = 1
        while k > 0:
            while k < f[-p]:
                p += 1
            k -= f[-p]
            res += 1
        
        return res
''',
    call='Solution().findMinFibonacciNumbers(19)',
    expect=3,
    views=[
        dict(type='text', fn=_txt, size=28),
        dict(type='array', var='f', h=240, cell=96,
             color=lambda S, i, v: 'blue' if 'p' in S and i == len(S['f']) - S['p'] else None,
             dim=lambda S, i, v: 'p' in S and i > len(S['f']) - S['p']),
    ],
    watch=[('k', 'k', 'yellow'), ('p', 'p', 'blue'), ('f[-p]', 'f[-p]', 'blue'), ('res', 'res', 'green')],
    captions={
        'f = [1, 1]': '数列从 `f[1] = f[2] = 1` 开始',
        'while f[-1] < k': '`f[-1] = {f[-1]}` {"< k = " + str(k) + "，还不够大 → 继续往后生成" if f[-1] < k else ">= k = " + str(k) + "：最大项已经覆盖 k → 停止"}',
        'f.append': '`f[-1] + f[-2]` = `{f[-1]}`：追加新的一项',
        'res = 0': '`res` 记录选了几个数',
        'p = 1': '`p = 1`：从最大的一项 `f[-1]` 开始往小找',
        'while k > 0': '`k = {k}`：{"还没凑完，继续选" if k > 0 else "k 已减到 0 → 凑完了"}',
        'while k < f[-p]': '`k = {k}` {"<" if k < f[-p] else ">="} `f[-p] = {f[-p]}`：{"这一项太大，p 往小的方向走" if k < f[-p] else "这一项不超过 k，可以选"}',
        'p += 1': '换更小的一项：`p = {p}`，`f[-p] = {f[-p]}`',
        'k -= f[-p]': '选 `{f[-p]}`：`k` 从 `{B.k}` 减到 =={k}==（最大的、不超过 k 的那项，证明见思路卡）',
        'res += 1': '又选了一个数，`res = {res}`',
        'return res': '`k` 已为 0，一共选了 =={res}== 个',
    },
    cards=dict(
        one_liner='每一轮都选不超过 k 的最大斐波那契数',
        complexity='时间 `O(log k)`，空间 `O(log k)`',
        problem=['斐波那契数 `1, 1, 2, 3, 5, 8, ...`，同一个数可以重复使用',
                 '选出若干个使它们的和恰好为 `k`，求最少选几个',
                 '示例 `k = 7` → `2`（`2+5`）；本视频：`k = 19` → `3`（`13+5+1`）'],
        quote='根据上面的结论，我们每一轮都必须选择最大的，且小于等于k的数列项，然后更新k，直到k为0为止。',
        quote_src='—— yiduobo 题解原文',
        idea=['先证明答案里==不会有相邻两项==：`f[k]+f[k+1] = f[k+2]`，合并更优',
              '再证每一项最多用 2 次，且用 2 次时 `f[t+2]` 必为 0',
              '继续推出最大的 `f[n]` 必须选：不选的话剩下的和 `rest ≤ f[n]-1 < k`',
              '所以贪心：预处理数列，从大到小每次取不超过 k 的最大项'],
        summary=['时间 `O(log k)`，空间 `O(log k)`',
                 '`p` 只增不减：选完一项后剩余 `k` 比该项小，下一项只会更小',
                 '数列要生成到 `f[-1] >= k` 为止，否则最大项不够',
                 '本题证明比代码难：贪心的正确性靠「不相邻 + 系数 ≤ 2」两步'],
    ),
)
