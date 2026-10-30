def _txt(S):
    if 'i' not in S:
        return '先看有没有比 `complexity[0]` 小或相等的数，再算 `(n-1)!`'
    i = S['i']
    if i >= len(S['complexity']):
        return f"右边全都比 `{S['complexity'][0]}` 大 → 答案就是 ==(n-1)! = {S['ans']}=="
    return f"`complexity[{i}] = {S['complexity'][i]}` vs `complexity[0] = {S['complexity'][0]}`；已乘到 =={i-1}!== 即 `ans = {S['ans']}`"


CONFIG = dict(
    num=3577, title='统计计算机解锁顺序排列数', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='脑筋急转弯 · 全排列',
    tags=['灵神题单', '难度分 1750'],
    code='''
class Solution:
    def countPermutations(self, complexity: List[int]) -> int:
        MOD = 1_000_000_007
        ans = 1
        for i in range(1, len(complexity)):
            if complexity[i] <= complexity[0]:
                return 0
            ans = ans * i % MOD
        return ans
''',
    call='Solution().countPermutations([2,3,5,4,6])',
    expect=24,
    views=[
        dict(type='text', fn=_txt, h=90),
        dict(type='array', var='complexity', pointers={'i': 'blue'}, h=260, label='complexity',
             color=lambda S, i, v: 'orange' if i == 0 else ('blue' if 'i' in S and i == S['i'] else ('green' if 'i' in S and 0 < i < S['i'] else None))),
    ],
    watch=['i', ('complexity[0]', 'complexity[0]', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'MOD =': '答案要对 `10^9+7` 取模',
        'ans = 1': '`ans` 从 1 开始，准备累乘 `1×2×…×(n-1)`',
        'if complexity[i] <= complexity[0]': '`complexity[{i}] = {complexity[i]}` {"<=" if complexity[i] <= complexity[0] else ">"} `complexity[0] = {complexity[0]}`：{"==不比 0 号大==，解锁不了 → 返回 0" if complexity[i] <= complexity[0] else "比 0 号大，0 号能直接解锁它 → 继续"}',
        'return 0': '右边出现 `<= complexity[0]` 的机器，永远解锁不了，方案数 ==0==',
        'ans = ans * i': '再多一台机器可任意插入：`ans = ans × {i} % MOD = {ans}`，即 {i}!',
        'return ans': '所有数都比 0 号大，0 号一台就能解锁全部 → 方案数 ==(n-1)! = {ans}==',
    },
    cards=dict(
        one_liner='0 号右边都比它大，就能任意排列：答案是 (n-1)!',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['编号 0 的电脑已解锁，用 `j<i` 且 `complexity[j]<complexity[i]` 的电脑解锁 `i`',
                 '问有多少种 `0..n-1` 的排列能表示合法解锁顺序，结果对 `10^9+7` 取模',
                 '示例：`[1,2,3]` → `2`；`[3,3,3,4,4,4]` → `0`',
                 '本视频：`[2,3,5,4,6]` → `24`'],
        quote='当且仅当计算机 0 右边的所有计算机的密码复杂度都比 complexity[0] 大，才能解锁所有计算机。',
        quote_src='—— 灵茶山艾府题解（定理）',
        idea=['每一轮解锁的机器复杂度只会越来越大，所以都比 `complexity[0]` 大',
              '必要性反证：若右边有 `<= complexity[0]` 的机器，往左找更小的会撞上矛盾',
              '满足条件时 0 号一台就能解锁所有 → 其余 `n-1` 台任意排，共 `(n-1)!` 种'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '先判断再累乘；遇到 `<=` 立刻返回 0（注意是 `<=` 不是 `<`）',
                 '每次乘完要取模，防止数字爆炸',
                 '排列的是 1..n-1，0 号不参与排列'],
    ),
)
