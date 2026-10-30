def _txt(S):
    if 'index' not in S or 'cnt_list' not in S or 'num' not in S:
        return '从右往左，累计「当前字符之后更小的字符」造成的排名贡献'
    c = S['cnt_list']
    less = sum(c[:S['num']])
    return f'`s[{S["index"]}] = {S["s"][S["index"]]}`，右边比它小的字符共 `{less}` 个；`res = {S.get("res", 0)}`'


CONFIG = dict(
    num=1830, title='使字符串有序的最少操作次数', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='类康托展开 · 乘法逆元去重',
    tags=['组合数学', '字符串'],
    code='''
class Solution(object):
    def makeStringSorted(self, s):
        n = len(s)
        fac = [1]
        inv_fac = [1]
        mod = 10 ** 9 + 7
        for index in range(1, n + 1):
            fac.append(fac[-1] * index % mod)
            inv_fac.append(self.quickPow(fac[-1], mod - 2, mod))

        cnt_list = [0] * 26
        res = 0
        for index in range(n - 1, -1, -1):
            num = ord(s[index]) - 97
            cnt = sum(cnt_list[:num])
            tmp = cnt * fac[n - index - 1] % mod

            cnt_list[num] += 1
            for char_num in range(26):
                tmp = tmp * inv_fac[cnt_list[char_num]] % mod
            
            res += tmp
            if res >= mod:
                res -= mod

        return res

    def quickPow(self, base, k, mod):
        if k == 1:
            return base

        res = self.quickPow(base, k // 2, mod)
        res = res ** 2 % mod
        if k % 2 == 1:
            res = res * base % mod
        return res
''',
    call="Solution().makeStringSorted('cbab')",
    expect=10,
    skip=[19, 20, 28, 29, 30, 32, 33, 34, 35, 36, 'n = len(s)', 'mod = 10', 'cnt_list = [0]', 'if res >= mod', 'res -= mod'],
    max_steps=70,
    views=[
        dict(type='string', var='s', label='s', h=175, cell=80, pointers={'index if num >= 0 else -1': 'blue'}, pointer_labels={'index if num >= 0 else -1': 'index'}),
        dict(type='text', fn=_txt, size=26, h=70),
        dict(type='array', var='cnt_list', label='cnt_list：已扫描过的字符个数（下标 0=a, 1=b, …）', h=170, cell=34,
             pointers={'num': 'pink'}, color=lambda S, i, v: 'blue' if v else None, dim=lambda S, i, v: v == 0),
        dict(type='array', var='fac', label='fac[i] = i! % mod', h=140, cell=150),
    ],
    watch=[('index', 'index', 'blue'), ('cnt', 'cnt', 'pink'), ('tmp', 'tmp', 'yellow'), ('res', 'res', 'green')],
    captions={
        'fac = [1]': '`fac[i]` = `i!`（取模），`inv_fac[i]` = `i!` 的乘法逆元',
        'fac.append(fac': '`fac[{index}] = {index}! % mod` = {fac[-1]}',
        'inv_fac.append': '用费马小定理 `x^(mod-2)` 算出 `{index}!` 的逆元（快速幂），之后「除以 {index}!」就变成「乘 inv_fac[{index}]」',
        'num = ord': '`s[{index}] = {s[index]}`，编号 `num = {num}`',
        'cnt = sum': '右边比 `{s[index]}` 小的字符有 `cnt = {cnt}` 个：它们放首位的排列都比 s 小',
        'tmp = cnt * fac': '每个这样的首位，剩下 `{n - index - 1}` 位有 `{n - index - 1}!` 种排法 → `tmp = {cnt} × {fac[n - index - 1]}` = =={tmp}==（还没去重）',
        'cnt_list[num] += 1': '把 `{s[index]}` 计入 `cnt_list`（现在统计的是 `s[{index}:]`）',
        'res += tmp': lambda S, B, r: ('已对 26 个字母各乘 `inv_fac[个数]`（= 除以 ∏cnt!，去掉相同字符造成的重复）：`tmp` = ' + str(S.tmp) + f'；`res` = {B.res} + {S.tmp} = =={S.res}=='),
        'return res': '最少操作 `{ret}` 次 = 当前排列在所有排列里的名次（从 0 数）',
    },
    cards=dict(
        one_liner='操作次数 = 当前排列比它小的排列个数（康托展开）',
        complexity='时间 `O(n·26 + n log mod)`，空间 `O(n)`',
        problem=['题目的操作恰好是「求上一个排列」，要回到最小的有序排列',
                 '所以答案 = 当前字符串是第几小的排列（从 0 数），结果对 `10^9+7` 取模',
                 '示例：`"cba"` → `5`；本视频 `"cbab"` → `10`'],
        quote='题目问多少次操作可以使得字符串有序，也就是多少次操作可以回到最初的排列。对于这个问题，也可以看做问当前排列在所有排列中是第几小的排列，对于这个问题，可以使用经典的类康托展开算法来进行求解。',
        quote_src='—— yiduobo 题解原文',
        idea=['比 `s` 小的排列：首位更小的 + 首位相同、后面更小的（递归同样问题）',
              '首位更小：右边有 `cnt` 个更小字符，每个后面 `(n-1)!` 种；有重复字符要除以 `∏cnt!`',
              '取模下不能直接除 → 用乘法逆元 `x^(mod-2)`，提前预处理 `1!` 到 `n!` 的逆元'],
        summary=['时间 `O(n·26)`，预处理逆元 `O(n log mod)`，空间 `O(n)`',
                 '原文为 Python 2 写法，`quickPow` 里的 `k / 2` 已改为 `k // 2`',
                 '易错：`cnt_list` 要先加上当前字符，再对 26 个字母统一乘逆元',
                 '易错：`res` 每次加完要手动减 mod，保持在范围内',
                 '同类题：康托展开、第 k 个排列、3518 最小回文排列 II'],
    ),
)
