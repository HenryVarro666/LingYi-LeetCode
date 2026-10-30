def _bin(x):
    return format(x, 'b')


def _row(S):
    if 'pre' not in S:
        return ''
    return f"前缀或 `pre = {_bin(S['pre'])}`　最大或值 `ans = {S['ans']}`"


CONFIG = dict(
    num=2680, title='最大或值', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='前后缀分解 · 只改一个数',
    tags=['灵神题单·动态规划', '难度分 1912'],
    code='''
class Solution:
    def maximumOr(self, nums: List[int], k: int) -> int:
        n = len(nums)
        # suf[i] 表示 nums[i+1:] 的 OR
        suf = [0] * n
        for i in range(n - 2, -1, -1):
            suf[i] = suf[i + 1] | nums[i + 1]

        # pre 表示 nums[:i] 的 OR
        ans = pre = 0
        for x, suf_or in zip(nums, suf):
            ans = max(ans, pre | (x << k) | suf_or)
            pre |= x
        return ans
''',
    call='Solution().maximumOr([6,4,5], 1)',
    expect=15,
    views=[
        dict(type='array', var='nums', label='nums', pointers={'i': 'blue'}),
        dict(type='array', var='suf', label='suf[i] = nums[i+1:] 的 OR', pointers={'i': 'pink'}),
        dict(type='text', fn=_row, size=36),
    ],
    watch=[('x', 'x', 'blue'), ('pre', 'pre', 'cyan'), ('suf_or', 'suf_or', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'n = len': '`n = {n}`',
        'suf = [0] * n': '`suf[i]` 存 `nums[i]` ==右边==所有数的 OR，最后一个右边没有数，是 0',
        'for i in range(n - 2': '从右往左算后缀或，`i = {i}`',
        'suf[i] = suf[i + 1]': '`suf[{i}]` = `suf[{i + 1}] | nums[{i + 1}]` = {suf[i]}，也就是 `nums[{i}]` 右边所有数的 OR',
        'ans = pre = 0': '`pre` 是 `x` 左边所有数的 OR（一边遍历一边算），`ans` 记最大值',
        'for x, suf_or in zip': '枚举把 `x = {x}` 左移 `k` 位（==只改一个数就够了==，雨露均沾不如集中）',
        'ans = max': '改 `{x}`：`pre | (x << k) | suf_or` = `{pre} | {x << k} | {suf_or}` = {pre | (x << k) | suf_or}；`ans` → {ans}',
        'pre |= x': '把 `x` 并入前缀或，给下一个数用：`pre` → {pre}',
        'return ans': '枚举完所有数，最大或值 `{ans}`',
    },
    cards=dict(
        one_liner='k 次翻倍全给同一个数，再用前后缀或 O(1) 算出其余数',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['每次操作可把一个数乘 2，最多 `k` 次',
                 '求 `nums[0] | nums[1] | ... | nums[n-1]` 的最大值',
                 '示例：`[12,9], k=1` → `30`；本视频：`[6,4,5], k=1` → `15`'],
        quote='把「乘 2」分配给多个数（雨露均沾），不如只分配给一个数，这样能得到更长（更大）的答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['要让答案最大，先让二进制长度最长 → 乘 2 全部给同一个数',
              '枚举是哪个数左移 `k` 位：其余数的 OR = 左边 `pre` | 右边 `suf`',
              '`suf` 先预处理，`pre` 边遍历边算（前后缀分解，同 238 题）'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '不一定选最大的数：如 6 和 4，把 4 左移更优（6=110 的 1 不被浪费）',
                 '`x << k` 是一次性左移 k 位，不是循环 k 次',
                 '方法二：用 `all_or ^ x | fixed` 去掉 x，空间优化到 `O(1)`'],
    ),
)
