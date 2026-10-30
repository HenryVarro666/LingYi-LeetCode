

def _txt(S):
    if 'res' in S and 'left_part' in S:
        res, lp = S['res'], S['left_part']
        rp = res ^ lp
        l, r = S['left'][lp], S['right'][rp]
        return (f'`res = {res}`：`left_part = {lp}`，`right_part = {rp}`；`left[{lp}] = {l}`，`right[{rp}] = {r}`'
                + (f'，`{l} + {r}` ' + ('≤' if l + r <= len(S['nums']) else '>') + f' `n = {len(S["nums"])}`' if l is not None and r is not None else ''))
    if 'state' in S and 'cnt' in S:
        return f'`state = {S["state"]}`（二进制 {S["state"]:03b}）：`cnt` = 数组里能并入 state 的数的个数（要 ≥ k）'
    return '前后各算一遍：「按位或恰好 = state」最少要用到前几个数'


def _gcolor(S, i, v):
    return 'green' if v is not None else None


CODE = '''
class Solution(object):
    def maxValue(self, nums, k):

        one = min(3, k)

        def get(nums):
            f = [[False] * 8 for _ in range(one + 1)]
            f[0][0] = True
            g = [None] * 8

            for index, v in enumerate(nums):
                for state in range(8):
                    for cnt in range(one - 1, -1, -1):
                        if f[cnt][state]:
                            nxt_state = state | v
                            f[cnt + 1][nxt_state] = True
                            if g[nxt_state] is None:
                                g[nxt_state] = index + 1
        
            for state in range(8):
                if g[state] is None:
                    continue
                cnt = 0
                for index, v in enumerate(nums):
                    if (state | v) == state:
                        cnt += 1
                        if cnt == k:
                            g[state] = max(g[state], index + 1)
                            break
            
                if cnt < k:
                    g[state] = None
        
            return g

        
        left = get(nums)
        right = get(nums[::-1])

        for res in range(7, -1, -1):
            for left_part in range(8):
                right_part = res ^ left_part
                if left[left_part] is not None and right[right_part] is not None and left[left_part] + right[right_part] <= len(nums):
                    return res
'''
L_FINAL = CODE.strip('\n').split('\n').index('        for res in range(7, -1, -1):') + 1


CONFIG = dict(
    num=3287, title='求出数组中最大序列值', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='前后缀 OR 状态 DP + 最小前缀长度 g',
    tags=['灵神题单·位运算', '灵神题单·动态规划', '难度分 2545'],
    code=CODE,
    call='Solution().maxValue([1, 1, 2, 3, 4], 2)',
    expect=7,
    views=[
        dict(type='text', h=55, size=24, fn=_txt),
        dict(type='array', var='nums', label='当前遍历的数组（第二遍是倒序）', h=190, cell=64,
             pointers={'index': 'blue'}),
        dict(type='table', var='f', label='f[cnt][state]（绿 = 能选 cnt 个数，按位或恰好 = state）', h=215, cell=56,
             rows=lambda S: [f'选{c}个' for c in range(len(S['f']))], cols=lambda S: [f'{s:03b}' for s in range(8)],
             values=False, color=lambda S, i, j, v: ('green' if v else None)),
        dict(type='array', var='g', label='g[state]：用前 g 个数就能凑出 state（· = 不行）', h=140, cell=64,
             color=_gcolor),
    ],
    watch=[('index', 'index', 'blue'), ('state', 'state', 'cyan'), ('res', 'res', 'green')],
    skip=['one = min', 'f = [[False]', 'f[0][0] = True', 'g = [None]', 'for state in range(8)', 'for cnt in range(one - 1',
          'if f[cnt][state]', 'nxt_state = state | v', 'f[cnt + 1][nxt_state]', 'if g[nxt_state] is None', 'if g[state] is None',
          'continue', 'cnt = 0', 'if (state | v) == state', 'cnt += 1', 'if cnt == k', 'g[state] = max', 'g[state] = None', 'g[nxt_state] = index + 1',
          'break', 'right_part = res ^ left_part', 'for left_part in range(8)', 24],
    captions={
        'for index, v in enumerate(nums):': lambda S, B, r: (
            '从第 0 个数开始：`f[0][0] = True`（什么都不选，按位或 = 0）' if 'index' not in B
            else (f'`nums[{S.index}] = {S.nums[S.index]}` 处理完：`f[cnt][state]` → `f[cnt+1][state | {S.nums[S.index]}]` 都标好了，新凑出的 state 记 `g`'
                  if B.get('index') == S.get('index') else
                  f'`nums[{S.index - 1}] = {S.nums[S.index - 1]}` 处理完：`f[cnt][state]` → `f[cnt+1][state | {S.nums[S.index - 1]}]`，新凑出的 state 记 `g = {S.index}`')),
        'if cnt < k': lambda S, B, r: (f'`state = {S.state}`：能并入它的数有 `cnt = {S.cnt}` 个，' + (f'≥ k → `g[{S.state}]` = =={S.g[S.state]}==' if S.cnt >= S.k else f'< k → 凑不齐，`g[{S.state}] = None`')),
        'return g': '`g[state]` = 前多少个数里能恰好选出 k 个，或起来等于 state（`None` = 不行）：{g}',
        'left = get(nums)': '正着算一遍：`left[state]` = 左半部分最少要用前几个数',
        'right = get(nums[::-1])': '倒着再算一遍：`right[state]` = 右半部分最少要用后几个数',
        'for res in range(7, -1, -1)': '从大到小试答案 `res = {res}`：能做出就是最大',
        'if left[left_part] is not None': lambda S, B, r: (lambda l, rr, n: (f'`left[{S.left_part}] = {l}`，`right[{S.res ^ S.left_part}] = {rr}`：'
                                                            + ('两边前缀+后缀 `' + f'{l} + {rr} ≤ {n}' + '` → ==不重叠，成立==' if l is not None and rr is not None and l + rr <= n
                                                               else '有一边凑不出或会重叠 → 换下一个 left_part')))(S.left[S.left_part], S.right[S.res ^ S.left_part], len(S.nums)),
        'return res': '找到了：最大序列值 `{res}`',
    },
    max_steps=130,
    cards=dict(
        one_liner='把「前半 OR」和「后半 OR」拆开，各算出能凑出哪些值',
        complexity='时间 `O(n·log(ma)·ma + ma²)`，空间 `O(ma)`',
        problem=['从 `nums` 选长为 `2k` 的子序列，前 k 个的 OR 异或后 k 个的 OR',
                 '求最大值，`nums[i] < 128`',
                 '演示：`nums = [1,1,2,3,4], k = 2` → `7`（`(1 OR 1) XOR (2 OR 4)`）'],
        quote='对于这类两个部分的结果组合形成最终结果的问题，一般的处理方法就是找一个分割点划开，然后分别计算前半部分和后半部分可以达成的所有可行结果，从中选出最优的结果对构成最终的结果。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[cnt][state]`：能否选 cnt 个数，按位或恰好是 state；`g[state]` 记最少用前几个数',
              '选的个数 `cnt` 最多只要 `min(7, k)`：每个二进制位至多让一个数出力；不够 k 个就用「群演」（不引入新位的数）补齐',
              '从大到小试 `res`，枚举 `left_part`，`right_part = res ^ left_part`，前缀 + 后缀长度不超过 `n` 就成立'],
        summary=['时间 `O(n·log(ma)·ma + ma²)`，空间 `O(ma)`（`ma` = 128）',
                 '关键：`g[state] + right[…] ≤ n` 保证前后两部分不重叠',
                 '「群演」：能并入 state 的数（`state | v == state`）数够 k 个，`state` 才真正可行',
                 '为了画得下，演示把 `128` 缩成 `8`、`127` 缩成 `7`、`min(7, k)` 缩成 `min(3, k)`（示例数都 < 8）；原文为 Python 2 风格，但代码在 Python 3 下无需其他改动'],
    ),
)
