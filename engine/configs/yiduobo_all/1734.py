def _top(S):
    if 'res' not in S:
        return '`encoded[i] = perm[i] ^ perm[i+1]`，`n` 是奇数；先求出 `perm[0]`，再顺着往后推'
    line = S['_line']
    if line in (7, 8):
        return f"`1^2^...^{S['n']}` = perm 全体异或；`res[0] = {S['res'][0]}`"
    if line in (9, 10):
        return f"奇数项 encoded 异或 = `perm[1]^...^perm[n-1]`；`res[0] = {S['res'][0]}`"
    return f"`perm[0] = {S['res'][0]}`，已知 `perm[i]` 和 `encoded[i]` → `perm[i+1] = perm[i] ^ encoded[i]`"


def _ecolor(S, i, v):
    line = S['_line']
    if line in (9, 10) and i % 2 == 1:
        if 'index' in S and i == S['index'] and line == 10:
            return 'yellow'
        return 'blue'
    if line in (11, 12) and 'num' in S and 'res' in S and i == len(S['res']) - 2 + (0 if line == 12 else 1):
        return 'yellow'
    return None


CONFIG = dict(
    num=1734, title='解码异或后的排列', difficulty='Medium', category='位运算',
    author='yiduobo', technique='奇数项异或消元 · 先求 perm[0]',
    tags=['灵神题单', '位运算'],
    code='''
class Solution(object):
    def decode(self, encoded):

        n = len(encoded) + 1

        res = [0]
        for index in range(1, n + 1):
            res[0] ^= index
        for index in range(1, n - 1, 2):
            res[0] ^= encoded[index]
        for num in encoded:
            res.append(res[-1] ^ num)
        
        return res
''',
    call='Solution().decode([6, 5, 4, 6])',
    expect=[2, 4, 1, 5, 3],
    views=[
        dict(type='text', fn=_top, size=24, h=90),
        dict(type='array', var='encoded', h=140, label='encoded', cell=76, color=_ecolor),
        dict(type='array', var='res', h=140, label='res（最终就是 perm）', cell=76,
             color=lambda S, i, v: 'green' if i == 0 else ('yellow' if i == len(S['res']) - 1 and S['_line'] in (11, 12) else None)),
    ],
    watch=['n', ('res[0]', 'res[0]', 'green'), 'index', 'num'],
    captions={
        'n = len(encoded) + 1': '`encoded` 长度是 `n - 1`，所以 `n = {n}`（`n` 是奇数）',
        'res = [0]': '`res[0]` 先放 0，接下来用异或把 `perm[0]` 累出来',
        'for index in range(1, n + 1)': lambda S, B, r: ('`1..n` 枚举完了' if B.get('index') == S.index and S.index == S.n else f'枚举 `index = {S.index}`，要把它异或进 `res[0]`'),
        'res[0] ^= index': '`res[0] ^= {index}` → {res[0]}：把 `1 ^ 2 ^ ... ^ n`（即 `y`，全体 perm 的异或）累进来',
        'for index in range(1, n - 1, 2)': lambda S, B, r: ('奇数下标的 `encoded` 取完了' if B.get('index') == S.index and S.index == S.n - 2 else f'`index = {S.index}`：只取奇数下标的 `encoded`'),
        'res[0] ^= encoded[index]': '`res[0] ^= encoded[{index}] = {encoded[index]}` → {res[0]}：奇数项异或 `x` 与 `y` 只差 `perm[0]`',
        'for num in encoded': lambda S, B, r: ('`encoded` 全部用完，`res` 有 `n` 项' if len(S.res) == S.n else f'`perm[0] = {S.res[0]}` 已知；取 `encoded` 的下一个 `num = {S.num}`'),
        'res.append(res[-1] ^ num)': '`perm[i+1] = perm[i] ^ encoded[i]`：`{B.res[-1]} ^ {num}` = =={res[-1]}==',
        'return res': '还原出的排列 =={res}==，恰好是 `1..n` 的一个排列 ✓',
    },
    max_steps=60,
    cards=dict(
        one_liner='n 是奇数：奇数项 encoded 异或 + 1..n 异或 = perm[0]',
        complexity='时间 `O(n)`，空间 `O(1)`（不计返回数组）',
        problem=['`perm` 是 `1..n` 的排列，`n` 是奇数；`encoded[i] = perm[i] ^ perm[i + 1]`',
                 '给定 `encoded`，还原 `perm`',
                 '示例：`encoded=[3,1]` → `[1,2,3]`；本视频 `[6,5,4,6]` → `[2,4,1,5,3]`'],
        quote='由于n是个奇数，那么就可以将encoded[1]、encoded[3]、...、encoded[n - 2]这些奇数项拎出来异或在一起',
        quote_src='—— yiduobo 题解原文',
        idea=['`encoded[1] ^ encoded[3] ^ ...` 展开后恰好是 ==`perm[1] ^ perm[2] ^ ... ^ perm[n-1]`==，记作 `x`',
              '`perm` 是 `1..n` 的排列：`y = perm[0] ^ ... ^ perm[n-1] = 1 ^ 2 ^ ... ^ n`',
              '`x` 和 `y` 只差一项 `perm[0]` → ==`perm[0] = x ^ y`==',
              '有了 `perm[0]`，往后 `perm[i+1] = perm[i] ^ encoded[i]` 一路推出'],
        summary=['时间 `O(n)`，空间 `O(1)`（不计结果）',
                 '易错：奇数下标是 `1, 3, ..., n-2`，所以循环是 `range(1, n - 1, 2)`',
                 '`n` 必须是奇数，这样奇数下标的 `encoded` 才能刚好两两拼出 `perm[1..n-1]`',
                 '`res[0]` 先用 `1..n` 异或、再异或奇数项，一次累成 `x ^ y`',
                 '原文为 Python 2 风格（`class Solution(object)`），代码无需改动'],
    ),
)
