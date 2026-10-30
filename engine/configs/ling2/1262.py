NUMS = [3, 6, 5, 1, 8]


def _v(v):
    return '-inf' if v == float('-inf') else str(v)


def _color(S, r, c, v):
    if S.get('_line') == 7 and 'j' in S:
        i, j, x = S['i'], S['j'], S['x']
        if (r, c) == (i + 1, j):
            return 'yellow'
        if (r, c) == (i, (j + x) % 3):
            return 'pink'
        if (r, c) == (i, j):
            return 'blue'
    if S.get('_line') == 8 and (r, c) == (len(S['f']) - 1, 0):
        return 'green'
    return None


def _text(S):
    if S.get('_line') == 7:
        return '`f[i+1][j] = max(f[i][j], f[i][(j+x)%3] + x)`：==不选 x== 或 ==选 x=='
    return '`f[i+1][j]`：从前 i+1 个数中选，所选之和 s 满足 (s + j) ==能被 3 整除== 时 s 的最大值'


def _for_i(S, B, ret):
    if 'i' in B and B.i == S['i']:
        return '所有数都考虑完了'
    x = S['x']
    return f'考虑 `nums[{S["i"]}] = {x}`（`{x} mod 3 = {x % 3}`），算出第 `{S["i"] + 1}` 行'


def _trans(S, B, ret):
    i, j, x, f = S['i'], S['j'], S['x'], S['f']
    k = (j + x) % 3
    no, yes = f[i][j], f[i][k]
    if x % 3 == 0 and yes != float('-inf'):
        return f'`{x}` 是 3 的倍数，余数不变，==不选白不选==：`f[{i}][{j}] + {x}` → `f[{i + 1}][{j}]` = =={_v(f[i + 1][j])}=='
    yes_s = f'`f[{i}][{k}] + {x}` = {_v(yes)} + {x} = {_v(yes + x)}' if yes != float('-inf') else f'`f[{i}][{k}]` 是 -inf（非法）'
    return f'不选：`f[{i}][{j}]` = {_v(no)}；选：{yes_s} → `f[{i + 1}][{j}]` = =={_v(f[i + 1][j])}=='


CONFIG = dict(
    num=1262, title='可被三整除的最大和', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='选或不选：记忆化搜索 1:1 翻译成递推',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution:
    def maxSumDivThree(self, nums: List[int]) -> int:
        f = [[-inf] * 3 for _ in range(len(nums) + 1)]
        f[0][0] = 0
        for i, x in enumerate(nums):
            for j in range(3):
                f[i + 1][j] = max(f[i][j], f[i][(j + x) % 3] + x)
        return f[-1][0]
''',
    call=f'Solution().maxSumDivThree({NUMS!r})',
    expect=18,
    views=[
        dict(type='text', fn=_text, h=60, size=24),
        dict(type='array', var='nums', label='nums', cell=90, pointers={'i': 'cyan'}, h=170),
        dict(type='table', var='f', label='f（黄 = 正在算，蓝 = 不选 x，粉 = 选 x）', cell=110, h=470,
             rows=lambda S: ['∅'] + [str(v) for v in S['nums']],
             cols=['j=0', 'j=1', 'j=2'], color=_color),
    ],
    watch=[('i', 'i', 'cyan'), ('x', 'x'), ('j', 'j', 'yellow')],
    skip=['for j in range(3)'],
    captions={
        'f = [[-inf]': '`f` 有 `n + 1 = {len(f)}` 行：多出的第 0 行对应递归边界 `dfs(-1, j)`',
        'f[0][0] = 0': '`f[0] = [0, -inf, -inf]`：什么都不选，和为 0 合法；==-inf 表示非法方案==',
        'for i, x in': _for_i,
        'f[i + 1][j] = max': _trans,
        'return f[-1][0]': '答案 `f[n][0]`（翻译自 `dfs(n-1, 0)`）= =={ret}==',
    },
    cards=dict(
        one_liner='选或不选：f[i+1][j] = max(不选 x, 选 x)，-inf 自动排除非法方案',
        complexity='时间 `O(nk)`，空间 `O(nk)`，`k = 3`',
        problem=['整数数组 `nums`（元素都是正数）',
                 '选出若干个数，使它们的和==能被 3 整除==，求最大的和',
                 '示例：`[3,6,5,1,8]` → `18`（选 3、6、1、8）'],
        quote='用「选或不选」的思路，考虑最后一个数 x = nums[n-1]……==如果 x mod 3 = 0，选 x 不影响结果，一定要选（不选白不选）==。',
        quote_src='—— 灵茶山艾府题解：方法二 动态规划',
        idea=['`dfs(i, j)`：从 `nums[0..i]` 中选数，已选的数之和 mod 3 = j',
              '不选 x：`dfs(i-1, j)`；选 x：`dfs(i-1, (j+x)%3) + x`',
              '去掉「递」只留「归」：在上面加一排，`f[0] = [0, -inf, -inf]`'],
        summary=['时间 `O(nk)`，空间 `O(nk)`；滚动数组可优化到 `O(k)`',
                 '`-inf` 表示非法方案，取 `max` 时被自动排除',
                 '把 `j` 定义成「已选」之和 mod 3，就不用处理 `(j - x) mod 3 < 0`',
                 '方法一贪心：s mod 3 = 1 时去掉一个余 1 的或两个余 2 的最小数',
                 'DP 比贪心适用性更广：把 3 换成 4、5 也能直接用'],
    ),
)
