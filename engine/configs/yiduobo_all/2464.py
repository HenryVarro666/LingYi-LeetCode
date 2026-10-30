def _nums_color(S, k, v):
    if 'i' not in S or 'j' not in S:
        return None
    if S['j'] <= k <= S['i']:
        return 'yellow' if k in (S['i'], S['j']) else 'blue'
    return None


def _f_color(S, k, v):
    if 'j' in S and S.get('j', 0) > 0 and k == S['j'] - 1:
        return 'cyan'
    if 'i' in S and k == S['i']:
        return 'yellow'
    return None


CONFIG = dict(
    num=2464, title='有效分割中的最少子数组数目', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='划分型 DP · 枚举最后一段',
    tags=['灵神题单·动态规划', '灵神题单·数学算法'],
    code='''
class Solution(object):
    def validSubarraySplit(self, nums):

        def gcd(x, y):
            while y:
                x, y = y, x % y
            return x

        n = len(nums)
        f = [-1] * n
        for i in range(n):
            for j in range(i + 1):
                if gcd(nums[i], nums[j]) > 1 and (j == 0 or f[j - 1] != -1):
                    if j == 0:
                        f[i] = 1
                    elif f[i] == -1 or f[i] > f[j - 1] + 1:
                        f[i] = f[j - 1] + 1
        
        return f[-1]
''',
    call='Solution().validSubarraySplit([2,6,3,4,3])',
    expect=2,
    skip=['def gcd', 'while y', 'x, y = y, x % y', 'return x', 'n = len(nums)', 'for j in range(i + 1)'],
    max_steps=80,
    views=[
        dict(type='text', fn=lambda S: (f"最后一段 `nums[{S['j']}..{S['i']}]`：首 `{S['nums'][S['j']]}`、尾 `{S['nums'][S['i']]}`，公约数 `{__import__('math').gcd(S['nums'][S['i']], S['nums'][S['j']])}`" if 'j' in S and 'i' in S and S['j'] <= S['i'] else '`f[i]`：`nums[0..i]` 分成合法段的最少段数，`-1` = 分不了'), size=26, h=60),
        dict(type='array', var='nums', label='nums（黄 = 最后一段的首尾，蓝 = 段内）', h=210, cell=84,
             pointers={'j': 'pink', 'i': 'blue'}, color=_nums_color),
        dict(type='array', var='f', label='f（青 = f[j-1]，黄 = 正在算的 f[i]）', h=210, cell=84, color=_f_color),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('f[i]', 'f[i]', 'yellow')],
    captions={
        'f = [-1] * n': '`f[i]` 先全设成 `-1`：表示==还没有合法分法==',
        'for i in range': lambda S, B, ret: (f'算 `f[{S.i}]`：`nums[0..{S.i}]` 最少能分成几段' if S.get('i') != B.get('i') or 'i' not in B else '全部算完'),
        'if gcd(': lambda S, B, ret: (
            f'最后一段 `nums[{S.j}..{S.i}]` 首尾 `{S.nums[S.j]}`、`{S.nums[S.i]}` 的 `gcd = {__import__("math").gcd(S.nums[S.i], S.nums[S.j])}`'
            + ('，==不互质==' if __import__("math").gcd(S.nums[S.i], S.nums[S.j]) > 1 else '，互质 → 这一段不合法')
            + (('，前面 `f[%d] = %d`' % (S.j - 1, S.f[S.j - 1])) if S.j > 0 and __import__("math").gcd(S.nums[S.i], S.nums[S.j]) > 1 else '')),
        'if j == 0': '`j = {j}`：{"最后一段从头开始，整个前缀就是一段 → 只需 1 段" if j == 0 else "前面还有部分，要接在 f[j-1] 后面"}',
        'f[i] = 1': '整个 `nums[0..{i}]` 作为一段：`f[{i}]` = ==1==',
        'elif f[i] == -1': '`f[{i}] = {f[i]}`，候选 `f[{j - 1}] + 1 = {f[j-1] + 1}` → {"更小或还没有，采用" if f[i] == -1 or f[i] > f[j-1] + 1 else "不更优，保留"}',
        'f[i] = f[j - 1] + 1': '`f[{i}] = f[{j - 1}] + 1` = =={f[i]}==',
        'return f[-1]': '`f[{n - 1}]` = =={ret}==：整个数组最少分成 `{ret}` 段',
    },
    cards=dict(
        one_liner='枚举最后一段的起点：首尾不互质才合法',
        complexity='时间 `O(n^2 log U)`，空间 `O(n)`',
        problem=['把 `nums` 分成若干连续子数组，要求每段==首尾元素的最大公约数 > 1==',
                 '返回最少段数；分不了返回 `-1`',
                 '示例：`[2,6,3,4,3]` → `2`（`[2,6]` + `[3,4,3]`）'],
        quote='令f[i]表示以nums[i]结尾的前缀可以得到的最少划分，那么对于f[i]，不妨考虑划分出来的最后这个子数组……若nums[i]与nums[j]不互质，那么就有f[i] = min(f[i], f[j - 1] + 1)。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i]`：前缀 `nums[0..i]` 的最少段数，`-1` 表示无解',
              '枚举最后一段 `nums[j..i]`：首尾 `gcd > 1` 才合法',
              '`j = 0` 时前面没有别的段，直接 `f[i] = 1`；否则 `f[j-1] + 1`，且 `f[j-1]` 必须有解'],
        result='`[2,6]` + `[3,4,3]` → 最少 2 段 ✓',
        summary=['时间 `O(n^2 log U)`：双重循环 × `gcd`；空间 `O(n)`',
                 '易错：`j = 0` 时没有 `f[j-1]`，要单独当作 1 段',
                 '`f[j-1] == -1` 时不能转移，否则会算出错误的段数',
                 '原文本身可在 Python 3 运行，未修改'],
    ),
)
