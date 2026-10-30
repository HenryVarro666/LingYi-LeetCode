NUMS = [1, 2, 3]


def _info(S):
    i = S.get('i')
    if i is None:
        return '`f[i]` = 爬 `i` 个台阶的方案数，每步可爬 `nums` 里的任一个数'
    terms = ' + '.join(f'f[{i - x}]' for x in NUMS if x <= i)
    vals = ' + '.join(str(S['f'][i - x]) for x in NUMS if x <= i)
    done = S.get('_line', 0) >= 9 and S['f'][i] != 0
    return f'`f[{i}] = {terms}`' + (f' = `{vals}` = =={S["f"][i]}==' if done else '')


CONFIG = dict(
    num='LCR 104', title='组合总和 Ⅳ', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='爬楼梯 · 1:1 翻译成递推',
    tags=[],
    code='''
class Solution:
    def combinationSum4(self, nums: List[int], target: int) -> int:
        f = [1] + [0] * target
        for i in range(1, target + 1):
            f[i] = sum(f[i - x] for x in nums if x <= i)
        return f[target]
''',
    call='Solution().combinationSum4([1, 2, 3], 6)',
    expect=24,
    views=[
        dict(type='text', fn=_info, size=26, h=70),
        dict(type='array', var='f', label='f[i]：爬 i 个台阶的方案数（蓝 = i，粉 = 它依赖的 i − x）', h=260, cell=100,
             pointers={'i': 'blue'},
             color=lambda S, k, v: ('blue' if k == S.get('i') else
                                    'pink' if S.get('i') is not None and 0 <= S['i'] - k <= max(NUMS) and (S['i'] - k) in NUMS else None)),
    ],
    watch=[('i', 'i', 'blue'), ('target', 'target', 'yellow'), ('f[target]', 'f[target]', 'green')],
    captions={
        'f = [1] + [0] * target': '`f[0] = 1`：爬 0 个台阶只有「不爬」这 1 种（即递归边界 `dfs(0) = 1`）；其余先置 0',
        'for i in range': lambda S, B, r: (f'算爬 `{S.i}` 个台阶的方案数' if S.i != B.get('i') or 'i' not in B else '`i` 已到 target，循环结束'),
        'f[i] = sum': '最后一步爬 `x` 个台阶，前面就是 `f[i − x]`：`f[{i}]` = =={f[i]}==',
        'return f[target]': '爬 `{target}` 个台阶共 =={ret}== 种（顺序不同算不同）',
    },
    cards=dict(
        one_liner='这题就是爬楼梯：每次从 nums 里选一个数当台阶数',
        complexity='时间 `O(target·n)`，空间 `O(target)`',
        problem=['给不同正整数数组 `nums` 和目标 `target`，求总和为 `target` 的组合个数',
                 '==顺序不同的序列算不同组合==，数字可重复使用',
                 '示例：`[1,2,3]`, `target = 4` → `7`；本视频：`target = 6` → `24`'],
        quote='本题其实就是 70. 爬楼梯，我们每次从 nums 中选一个数，作为往上爬的台阶数，问爬 target 个台阶有多少种方案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`f[i]` = 爬 `i` 个台阶的方案数；考虑==最后一步==爬了 `x`，前面是 `f[i − x]`',
              '70 题就是 `nums = [1, 2]`：`f[i] = f[i-1] + f[i-2]`',
              '边界 `f[0] = 1`，由记忆化搜索的递归边界 `dfs(0) = 1` 翻译而来'],
        summary=['时间 `O(target·n)` = 状态数 × 单状态转移，空间 `O(target)`',
                 '易错：`x <= i` 才能转移，否则下标为负',
                 '进阶：有负数会出现无穷多方案，需限制负数的选取次数',
                 '题解先讲了 `@cache` 记忆化搜索，本视频演示 1:1 翻译后的递推写法'],
    ),
)
