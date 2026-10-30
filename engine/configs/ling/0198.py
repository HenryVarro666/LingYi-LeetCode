def _f_color(S, k, v):
    if 'i' not in S:
        return None
    i = S['i']
    if k == i + 2:
        return 'green'
    if k == i + 1:
        return 'blue'
    if k == i:
        return 'pink'
    return None


def _formula(S):
    if 'i' not in S:
        return '`f` 前面插两个 0：`f[0]`、`f[1]` 对应 `dfs(-2)`、`dfs(-1)`（没有房子，偷 0）' if 'f' in S else ''
    i, x, f = S['i'], S['x'], S['f']
    a, b = f[i + 1], f[i] + x
    return (f"`f[{i + 2}] = max(f[{i + 1}], f[{i}] + x)` = max({a}, {f[i]} + {x}) = =={max(a, b)}==")


def _legend(cv, S, B, box, T):
    x, y = box[0] + 24, (box[1] + box[3]) / 2
    for c, t in [('green', 'f[i+2] = dfs(i)'), ('blue', 'f[i+1]：不偷第 i 间'), ('pink', 'f[i] + x：偷第 i 间')]:
        cv.rect((x, y - 11, x + 22, y + 11), fill=T[c], r=5)
        cv.text((x + 32, y), t, 22, T['muted'], anchor='lm')
        x += 32 + cv.tlen(t, 22) + 36


def _cap_f(S, B, ret):
    i, x, f = S.i, S.x, S.f
    no, yes = f[i + 1], f[i] + x
    pick = '偷' if yes > no else '不偷'
    return (f'不偷 `nums[{i}]`：`f[{i + 1}] = {no}`；偷：`f[{i}] + {x} = {yes}` → '
            f'=={pick}==，`f[{i + 2}] = {f[i + 2]}`')


CONFIG = dict(
    num=198, title='打家劫舍', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='选或不选：记忆化搜索 → 递推',
    code='''
class Solution:
    def rob(self, nums: List[int]) -> int:
        f = [0] * (len(nums) + 2)
        for i, x in enumerate(nums):
            f[i + 2] = max(f[i + 1], f[i] + x)
        return f[-1]
''',
    call='Solution().rob([2, 7, 9, 3, 1])',
    expect=12,
    views=[
        dict(type='text', fn=_formula, h=60),
        dict(type='array', var='nums', label='nums（房屋金额）', pointers={'i': 'orange'},
             color=lambda S, k, v: 'orange' if k == S.get('i') else None,
             dim=lambda S, k, v: 'i' in S and k > S['i'], cell=96, h=200),
        dict(type='array', var='f', label='f（整体右移 2 位：f[i+2] ↔ dfs(i)）', color=_f_color,
             pointers={'i + 2': 'green'}, pointer_labels={'i + 2': 'i+2'}, cell=96, h=210),
        dict(type='custom', draw=_legend, h=46),
    ],
    watch=[('i', 'i', 'orange'), ('x', 'x', 'orange'), ('f[i+1]', 'f[i+1]', 'blue'), ('f[i]+x', 'f[i]+x', 'pink')],
    captions={
        'f = [0]': '`f` 长度 `n+2 = {len(f)}`：前面多两个 0，==防止下标越界==（给 `dfs(-2)`、`dfs(-1)` 留位置）',
        'for i, x in': lambda S, B, ret: (f'看第 `{S.i}` 间房 `x = {S.x}`：偷还是不偷？'
                                          if B.get('i') != S.i else '所有房子都考虑完了'),
        'f[i + 2] = max': _cap_f,
        'return f[-1]': '递归入口 `dfs(n-1)` → 答案 `f[-1]` = =={ret}==（偷 `2 + 9 + 1`）',
    },
    cards=dict(
        one_liner='第 i 间房偷或不偷？递归写出来，再整体右移 2 位翻译成递推',
        complexity='时间 `O(n)`，空间 `O(n)`（可优化到 `O(1)`）',
        problem=['一排房屋，金额为 `nums[i]`；==相邻两间不能同时偷==，求最多偷多少',
                 '示例：`[2,7,9,3,1]` → `12`（偷 `2 + 9 + 1`）'],
        before=[dict(heading='第一步：选或不选，写出记忆化搜索', chapter='② 思路', lines=[
            '`dfs(i)` = 从 `nums[0]` 到 `nums[i]` 最多能偷多少，==从最后一间开始想==',
            '不偷 `nums[i]`：`dfs(i-1)`；偷：上一间不能偷，`dfs(i-2) + nums[i]`',
            '`dfs(i) = max(dfs(i-1), dfs(i-2) + nums[i])`，边界 `i < 0` 时返回 0',
            '同一个 `i` 会被反复递归 → `@cache` 记忆化，`O(n)`',
        ])],
        quote='记忆化搜索会访问 dfs(-2) 和 dfs(-1)，f[-2] 和 f[-1] 下标越界了。解决办法：==在 f 数组的前面插入两个 0==，把 f 数组整体往右偏移 2 位。',
        quote_src='—— 灵茶山艾府题解 · 1:1 翻译成递推',
        idea_heading='第二步：1:1 翻译成递推',
        idea=['偏移后 `dfs(i)` → `f[i+2]`：`f[i+2] = max(f[i+1], f[i] + nums[i])`',
              '边界 `dfs(-2) = dfs(-1) = 0` → `f[0] = f[1] = 0`',
              '入口 `dfs(n-1)` → 答案 `f[n+1]`，即 `f[-1]`；==只有 f 偏移，nums 不偏移=='],
        after=[dict(heading='第三步：空间优化', lines=[
            '算 `f[i+2]` 只用到 `f[i+1]` 和 `f[i]` → 两个变量就够了',
            '`f0, f1 = f1, max(f1, f0 + x)`，答案 `f1`，空间 `O(1)`',
            '答疑：任何偷的顺序都能重排成==从左到右==，所以只需从左往右考虑',
        ])],
        summary=['时间 `O(n)`；`f` 数组 `O(n)`，滚动变量 `O(1)`',
                 '==下标偏移==：`f` 长 `n+2`，`f[i+2]` 对应 `dfs(i)`，`nums[i]` 不偏移',
                 '偷第 i 间时用 `f[i]`（跳过 i-1），不是 `f[i+1]`',
                 '套路：选或不选 → 记忆化搜索 → 1:1 翻译成递推 → 空间优化'],
    ),
)
