CONFIG = dict(
    num=891, title='子序列宽度之和', difficulty='Hard', category='贪心算法',
    author='yiduobo', technique='打乱顺序不影响 · 逐个数算 +2^(k-1) −2^(n-k)',
    tags=['灵神题单·贪心与思维', '难度分 2000'],
    code='''
class Solution(object):
    def sumSubseqWidths(self, A):
        
        n = len(A)
        pow2 = [1]
        mod = 10 ** 9 + 7
        for index in range(n):
            pow2.append((pow2[-1] + pow2[-1]) % mod)
        
        res = 0
        for index, num in enumerate(sorted(A)):
            res += num * (pow2[index] - pow2[n - index - 1])
            res %= mod
        
        return res
''',
    call='Solution().sumSubseqWidths([2, 1, 3, 5])',
    expect=30,
    views=[
        dict(type='text', size=28, fn=lambda S, B: '每个数 x：作最大值被加 `2^(下标)` 次，作最小值被减 `2^(n-下标-1)` 次' if 'num' not in S else
             f"num = {S['num']}：`{S['num']} × (2^{S['index']} − 2^{S['n']-S['index']-1})` = {S['num']} × ({S['pow2'][S['index']]} − {S['pow2'][S['n']-S['index']-1]})，res = =={S['res']}=="),
        dict(type='array', var='sorted(A)', pointers={'index': 'blue'}, h=220, label='sorted(A)：index 处的数是第 index+1 大'),
        dict(type='array', var='pow2', h=220, label='pow2：2 的幂次（预处理）'),
    ],
    watch=[('n', 'n', 'blue'), ('index', 'index', 'pink'), ('num', 'num', 'green'), ('res', 'res', 'orange')],
    captions={
        'n = len(A)': '`n = {n}`',
        'pow2 = [1]': '`pow2` 从 `2^0 = 1` 开始',
        'mod = ': '结果要对 `10^9+7` 取模',
        'for index in range(n)': lambda S, B, r: ('预处理完毕：`pow2 = ' + f'{S.pow2}' + '`' if 'index' in B and B.index == S.index else f'预处理第 `{S.index}` 项'),
        'pow2.append': '下一项 = 上一项 × 2：`pow2 = {pow2}`',
        'res = 0': '`res` 累计宽度之和',
        'for index, num in enumerate': lambda S, B, r: ('所有数都算完，循环结束' if 'num' in B and 'index' in B and B.index == S.index and B.num == S.num and S.index == S.n - 1 and B.res == S.res else f'`A` 排序后第 `{S.index+1}` 大的数 `num = {S.num}`（下标 {S.index}）'),
        'res += ': '`num` 比 `{index}` 个数大 → 作最大值被加 `2^{index}` = {pow2[index]} 次；比 `{n-index-1}` 个数小 → 作最小值被减 `2^{n-index-1}` = {pow2[n-index-1]} 次：`{B.res} + {num}×({pow2[index]}−{pow2[n-index-1]})` = =={res}==',
        'res %= mod': '取模：`res = {res}`',
        'return res': '所有数的贡献加完，返回 `{res}`',
    },
    cards=dict(
        one_liner='不看序列，只看每个数：当最大值被加，当最小值被减',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['宽度 = 序列最大值 − 最小值，求 `A` 所有非空子序列宽度之和（对 `10^9+7` 取模）',
                 '示例：`[2,1,3]` → `6`',
                 '本视频演示：`[2,1,3,5]` → `30`'],
        quote='即使随意打乱A，最后得到的答案依然不变。……A中第k大的数x将为答案提供x * (2^(k - 1) - 2^(n - k))。',
        quote_src='—— yiduobo 题解原文',
        idea=['子序列只关心数值：打乱 `A` 答案不变，所以排序',
              '第 `k` 大的数 `x`：和比它小的 `k-1` 个数任意组合 → 作最大值 `2^(k-1)` 次，累加',
              '和比它大的 `n-k` 个数任意组合 → 作最小值 `2^(n-k)` 次，减去'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '下标从 0 开始：`index` 对应第 `index+1` 大，所以是 `2^index − 2^(n-index-1)`',
                 'Python 中 `%` 会让 `res` 保持非负，负数也能正确取模',
                 '原文已是 Python 3 可运行写法，未作修改（`range`、`enumerate`）',
                 '对比灵神：灵神 `pow2[i]` 与 `pow2[-1-i]` 配对，思路相同'],
    ),
)
