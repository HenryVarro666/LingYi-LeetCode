S0 = 'babgbag'
T0 = 'bag'


def _in_loop(S):
    return S.get('_line') in (10, 11) and S.get('j') is not None and S.get('i') is not None


CONFIG = dict(
    num=115, title='不同的子序列', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='双序列 DP（LCS 型）· 滚动数组',
    tags=['灵神题单', 'LCS 进阶'],
    code='''
class Solution:
    def numDistinct(self, s: str, t: str) -> int:
        n, m = len(s), len(t)
        if n < m:
            return 0

        f = [1] + [0] * m
        for i, x in enumerate(s):
            for j in range(min(i, m - 1), max(m - n + i, 0) - 1, -1):
                if x == t[j]:
                    f[j + 1] += f[j]
        return f[m]
''',
    call=f'Solution().numDistinct({S0!r}, {T0!r})',
    expect=5,
    skip=['for j in range', 'n, m = len', 'if n < m', 'return 0'],
    max_steps=80,
    views=[
        dict(type='string', var='s', label='s（i 指向当前考虑的字母 x）', h=150, cell=70, pointers={'i': 'blue'},
             color=lambda S, k, v: 'blue' if k == S.get('i') else None),
        dict(type='string', var='t', label='t（j 是 t 里正在匹配的位置）', h=160, cell=70, pointers={'j if _line in (10, 11) else None': 'pink'}, pointer_labels={'j if _line in (10, 11) else None': 'j'},
             color=lambda S, k, v: 'pink' if k == S.get('j') and S.get('_line') in (10, 11) else None),
        dict(type='text', fn=lambda S: (f"`f[j+1]` = `s[..i]` 的子序列里 `t[..j]` 出现的次数；`f[0] = 1`（空串）" if not _in_loop(S)
                                         else f"`x = {S['x']}`，`t[{S['j']}] = {S['t'][S['j']]}` → " + ('==相等：可以配对，f[j+1] += f[j]==' if S['x'] == S['t'][S['j']] else '不相等：f[j+1] 不变')),
             size=24, h=80),
        dict(type='array', var='f', label='f[0..m]：f[k] = s 前面部分的子序列中 t[:k] 出现的次数', h=210, cell=100,
             pointers={'j if _line in (10, 11) else None': 'pink'}, pointer_labels={'j if _line in (10, 11) else None': 'j'}, index=True,
             color=lambda S, k, v: 'yellow' if S.get('j') is not None and k == S['j'] + 1 and S.get('_line') == 11 else ('pink' if S.get('j') is not None and k == S['j'] and S.get('_line') in (10, 11) else None)),
    ],
    watch=[('i', 'i', 'blue'), ('x', 'x', 'blue'), ('j', 'j', 'pink'), ('f[m]', 'f[-1]', 'green')],
    captions={
        'f = [1] + [0] * m': '`f[0] = 1`：把 `s` 的字母全删掉，得到空串，只有 1 种方法；其余先是 0',
        'for i, x in enumerate': lambda S, B, r: (f'`x = s[{S.i}] = {S.x}`：要么删掉它，要么用它去匹配 `t` 里的某个字母；`j` ==倒序==枚举，`f[j]` 才还是上一轮的值（同 0-1 背包）'
                                                  if S.get('x') is not None and (B.get('i') is None or S.i != B.i or B.get('_first')) and S.i == (B.i + 1 if B.get('i') is not None else 0)
                                                  else '`s` 的每个字母都处理完了'),
        'if x == t[j]': lambda S, B, r: (f'`x = {S.x}` 等于 `t[{S.j}] = {S.t[S.j]}` → ==不删 x==，让它和 `t[{S.j}]` 匹配' if S.x == S.t[S.j]
                                          else f'`x = {S.x}` 不等于 `t[{S.j}] = {S.t[S.j]}` → 只能删掉 x，`f[{S.j + 1}]` 保持 {S.f[S.j + 1]}'),
        'f[j + 1] += f[j]': '`f[{j+1}] += f[{j}]`：不删 x 的方案数 = 处理 x 之前 `t` 的前 {j} 个字母的个数 `{f[j]}`，累加得 =={f[j+1]}==',
        'return f[m]': '`f[{m}]` = `s` 的子序列中 `t` 出现的个数 = =={ret}==',
    },
    cards=dict(
        one_liner='删掉 s[i] 或用它匹配 t[j]，两种方案数相加',
        complexity='时间 `O(nm)`，空间 `O(m)`',
        problem=['给你字符串 `s` 和 `t`，统计 `s` 的==子序列==中 `t` 出现的个数',
                 '子序列：从 `s` 中删除某些字母后得到的字符串',
                 '示例：`s = "babgbag", t = "bag"` → `5`'],
        quote='s 的子序列，是从 s 中删除某些字母后，得到的字符串。……这个定义看似简单，但它就是解决本题的钥匙！',
        quote_src='—— 灵茶山艾府题解',
        idea=['看 `s` 的最后一个字母：删掉它，答案是 `dfs(i-1, j)`',
              '不删它：它必须和 `t[j]` 配对（要求相等），答案再加 `dfs(i-1, j-1)`',
              '记忆化搜索 1:1 翻译成递推 `f[i+1][j+1]`，再因为只用上一行，压缩成一维，`j` 倒序',
              '空串是任何串的子序列：`f[i][0] = 1`'],
        summary=['时间 `O(nm)`，空间优化后 `O(m)`',
                 '易错：初始 `f[0] = 1`，不是 0；`j` 必须倒序',
                 '`j` 的范围 `[max(m-n+i, 0), min(i, m-1)]`：剪掉不可能成立的状态',
                 '前面还有记忆化搜索和二维递推两种写法，这里选最终的滚动数组版',
                 '同类：LCS 家族（1143、583、72）'],
    ),
)
