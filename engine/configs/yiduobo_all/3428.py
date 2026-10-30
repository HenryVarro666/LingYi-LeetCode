def _txt(S):
    if 'index' in S and 'sum_c' in S and 'res' in S and len(S['sum_c']) == len(S['nums']):
        i, n = S['index'], len(S['nums'])
        a, b = S['sum_c'][i], S['sum_c'][n - i - 1]
        return f"`nums[{i}] = {S['nums'][i]}` × (`sum_c[{i}] = {a}` + `sum_c[{n - i - 1}] = {b}`) = =={S['nums'][i] * (a + b)}=="
    if 'sum_c' in S:
        return f"`sum_c[i]` = 从前 `i` 个数里选 `0..k-1` 个的方案数，已算出 {len(S['sum_c'])} 项"
    return '先预处理阶乘、阶乘逆元，再递推 `sum_c`'


def _is_final(S):
    return 'res' in S and 'index' in S and len(S.get('sum_c', [])) == len(S['nums'])


def _hl_sum(S, i, v):
    if not _is_final(S):
        return 'green' if i == len(S['sum_c']) - 1 and len(S['sum_c']) > 1 else None
    n = len(S['nums'])
    return 'blue' if i == S['index'] else 'pink' if i == n - 1 - S['index'] else None


CONFIG = dict(
    num=3428, title='最多 K 个元素的子序列的最值之和', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='排序 + 贡献法 + sum_c 递推',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def minMaxSums(self, nums, k):
        
        mod = 10 ** 9 + 7

        n = len(nums)

        fac = [1, 1]
        inv = [None, 1]
        inv_fac = [1, 1]
        for v in range(2, n):
            fac.append(fac[-1] * v % mod)
            inv.append(-(mod // v) * inv[mod % v] % mod)
            inv_fac.append(inv_fac[-1] * inv[-1] % mod)

        def comb(n, k):
            if n < k:
                return 0
            return fac[n] * inv_fac[k] % mod * inv_fac[n - k] % mod

        sum_c = [1]
        for v in range(1, n):
            sum_c.append((sum_c[-1] * 2 - comb(v - 1, k - 1) + mod) % mod)

        res = 0
        nums.sort()
        for index, v in enumerate(nums):
            res = (res + v * (sum_c[index] + sum_c[n - index - 1]) % mod) % mod
        
        return res
''',
    call='Solution().minMaxSums([3,5,1,4,2], 2)',
    expect=90,
    views=[
        dict(type='text', fn=_txt, size=24, h=90),
        dict(type='array', var='nums', pointers={'index': 'blue', 'n - index - 1': 'pink'}, h=210, label='nums',
             color=lambda S, i, v: ('blue' if i == S['index'] else 'pink' if i == len(S['nums']) - 1 - S['index'] else None) if _is_final(S) else None),
        dict(type='array', var='sum_c', h=210, label='sum_c（以 nums[i] 为最值时，另选至多 k-1 个的方案数）', color=_hl_sum),
    ],
    watch=['v', ('res', 'res', 'green')],
    captions={
        'mod = 10': '答案对 `10^9+7` 取模',
        'n = len(nums)': '`n = {n}`',
        8: '`fac[i]` = `i!`：先放好 `0!`、`1!`',
        9: '`inv[i]` = `i` 的乘法逆元（`inv[0]` 无意义）',
        10: '`inv_fac[i]` = `i!` 的逆元',
        12: '`fac` 追加 `{v}! mod p` = `{fac[-1]}`',
        13: '线性递推逆元：`inv[{v}] = -(mod // v) × inv[mod % v]` = `{inv[-1]}`',
        14: '`inv_fac` 追加 `{v}!` 的逆元 = `{inv_fac[-1]}`',
        'if n < k': lambda S, B, r: f"`C({S['n']}, {S['k']})`：`n < k` → " + ('==选不出，返回 0==' if S['n'] < S['k'] else '可以算，继续'),
        'return fac[n]': '`C(n, k) = n! × inv(k!) × inv((n-k)!)` = =={ret}==',
        'sum_c = [1]': '`sum_c[0] = 1`：下标 0 左边没有数，只能单独成序列，1 种',
        'sum_c.append': '`sum_c[{v}] = sum_c[{v-1}] × 2 − C({v-1}, k−1)` = =={sum_c[-1]}==（新数可选可不选；多算的恰好 `k-1` 个再选它会变成 `k` 个，要减掉）',
        'res = 0': '`res` 累计所有元素的贡献',
        'nums.sort()': '子序列只看最值，==先排序==：`{nums}`',
        'for index, v in enumerate': lambda S, B, r: ('`nums` 遍历完毕' if 'index' in B and B.index == S['index'] and B.v == S['v'] and S['index'] == len(S['nums']) - 1 else
                                                      f"`nums[{S['index']}] = {S['v']}`：作最大值时左边选，作最小值时右边选"),
        'res = (res + v *': '`{v}` × (`sum_c[{index}]` + `sum_c[{n-index-1}]`) = `{v} × ({sum_c[index]} + {sum_c[n-index-1]})`，`res` → =={res}==',
        'return res': '全部贡献加完：`{res}`',
    },

    cards=dict(
        one_liner='用贡献法：每个数当最大值、当最小值各算一遍',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['整数数组 `nums`，正整数 `k`：所有长度至多 `k` 的子序列，把「最大值 + 最小值」加起来，对 `10^9+7` 取模',
                 '示例：`nums=[1,2,3], k=2` → `24`',
                 '本视频：`nums=[3,5,1,4,2], k=2` → `90`'],
        quote='题目需要计算的是所有满足条件的子序列的最大值与最小值之和，那么在这里使用贡献法是比较合适的。另一方面，由于是子序列，那么在这里就可以先将nums排序。',
        quote_src='—— yiduobo 题解原文',
        idea=['`nums[index]` 当最大值：其余元素从左边 `index` 个里选 `0..k-1` 个，方案数记 `sum_c[index]`',
              '当最小值的情形对称，方案数是 `sum_c[n-index-1]`',
              '直接求和太慢 → 用 `C(i,j)=C(i-1,j-1)+C(i-1,j)` 合并相邻项，得 `sum_c[i+1] = sum_c[i]*2 − C(i, k-1)`'],
        summary=['时间 `O(n log n)`（排序），预处理阶乘和逆元 `O(n)`',
                 '`comb` 里先判 `n < k` 返回 0，否则 `k-1` 比下标大时会越界',
                 '`sum_c` 递推里 `+ mod` 是为了避免减出负数',
                 '原文代码在 Python 3 下可直接运行，未做改动',
                 '对比灵神：灵神把最大、最小合进同一个循环并用 `s` 一个变量滚动；yiduobo 先存成 `sum_c` 数组再求和'],
    ),
)
