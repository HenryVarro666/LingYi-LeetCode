def _txt(S):
    if 'p' not in S:
        return ''
    nums = S['nums']
    if 'q' in S and S['_line'] >= 12 and S['p'] < len(nums):
        p, q = S['p'], S['q']
        if 'index' in S and S['_line'] >= 14:
            i = S['index']
            return f"`nums[{i}]` 在 `({i} - {p} + 1) × ({q} - {i} + 1) − 1` = =={(i-p+1)*(q-i+1)-1}== 个长度 ≥ 2 的子数组里"
        return f"连续段 `nums[{p}:{q+1}]` = =={nums[p:q+1]}=="
    return ''


CONFIG = dict(
    num=3284, title='连续子数组的和', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='贡献法 · 切分连续段',
    tags=[],
    code='''
class Solution(object):
    def getSum(self, nums):

        mod = 10 ** 9 + 7
        res = sum(nums) % mod

        p = 0
        while p < len(nums):
            if p + 1 == len(nums) or abs(nums[p] - nums[p + 1]) != 1:
                p += 1
            else:
                q = p + 1
                diff = nums[q] - nums[p]
                while q + 1 < len(nums) and nums[q + 1] - nums[q] == diff:
                    q += 1
                for index in range(p, q + 1):
                    res += nums[index] * ((index - p + 1) * (q - index + 1) - 1)
                    res %= mod
                
                p = q
        
        return res
''',
    call='Solution().getSum([3, 4, 5, 4, 3])',
    expect=75,
    views=[
        dict(type='text', fn=_txt, size=26),
        dict(type='array', var='nums', label='nums（蓝框 = 当前连续段 p..q）', cell=84,
             pointers={'p': 'blue', 'q': 'pink'},
             window=('p', 'q'),
             color=lambda S, i, v: 'yellow' if 'index' in S and i == S['index'] and S['_line'] >= 14 else None),
    ],
    watch=[('p', 'p', 'blue'), ('q', 'q', 'pink'), ('index', 'index', 'yellow'), ('res', 'res', 'green')],
    captions={
        'res = sum': '先把所有长度为 1 的子数组算上，它们的和就是 `sum(nums)`：`res = {res}`',
        'while p <': lambda S, B, ret: (f'`p = {S.p}`：从这里找一段尽量长的连续数组' if S.p < len(S.nums) else f'`p = {S.p} == len(nums)`，所有位置都处理完，循环结束'),
        'if p + 1 ==': lambda S, B, ret: (f"`p = {S.p}` 已是最后一个元素，或与下一个差的绝对值不是 1 → ==不能延伸=="
                                       if S.p + 1 == len(S.nums) or abs(S.nums[S.p] - S.nums[S.p + 1]) != 1
                                       else f"`|nums[{S.p}] - nums[{S.p+1}]| = 1` → 连续，可以向右延伸"),
        'p += 1': '单个元素没有长度 ≥ 2 的连续数组，`p` 后移到 `{p}`',
        'q = p + 1': '至少 `nums[p], nums[p+1]` 两个元素：`q = {q}`',
        'diff =': '这一段的公差 `diff = {diff}`（只能全是 +1 或全是 −1）',
        'while q + 1': lambda S, B, ret: (f"`nums[{S.q+1}] - nums[{S.q}] = {S.nums[S.q+1]-S.nums[S.q]}` 等于 `diff` → ==继续延伸=="
                                       if S.q + 1 < len(S.nums) and S.nums[S.q+1] - S.nums[S.q] == S.diff
                                       else '到末尾，或差值变了 → ==这一段到 `q` 结束=='),
        'q += 1': '延伸一格：`q = {q}`',
        'for index': lambda S, B, ret: ('这一段的下标都枚举完了' if 'index' in B and S.index == B.index else f'枚举 `p..q` 内的每个下标，算它的贡献：`index = {S.index}`'),
        'res += nums': '`nums[{index}]` 出现在 `({index} - {p} + 1) × ({q} - {index} + 1) - 1` = `{(index-p+1)*(q-index+1)-1}` 个长度 ≥ 2 的子数组中，`res = {B.res} + {nums[index]} × {(index-p+1)*(q-index+1)-1}` = {B.res + nums[index]*((index-p+1)*(q-index+1)-1)}',
        'res %= mod': '对 `10^9 + 7` 取模，防止溢出：`res = {res}`',
        'p = q': '这一段处理完；下一段从 `q` 开始，因为 `nums[q]` 还可能是下一段的起点（如 `5,4`）',
        'return': '长度 1 的和 + 各连续段的贡献 = ==`{ret}`==',
    },
    cards=dict(
        one_liner='切出尽量长的连续段，用贡献法算段内所有子数组的和',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['数组 `arr` 的相邻差全是 `+1`，或全是 `-1`，称为连续数组；长度 1 也算',
                 '给整数数组 `nums`，求所有连续子数组的「元素之和」的总和（模 `10^9 + 7`）',
                 '示例：`[3, 4, 5, 4, 3]` → `75`'],
        quote='对于p到q之间的下标index，其所在子数组的左边界可以在p到index之间，一共有index - p + 1种可行的取值；而右边界则可以在index到q之间，一共有q - index + 1种可行的取值。',
        quote_src='—— yiduobo 题解',
        idea=['连续数组的子数组仍然连续 → 先把 `nums` 切成尽量长的连续段',
              '贡献法：`nums[index]` 在 `(index-p+1) × (q-index+1)` 个子数组里，减 1 去掉长度为 1 的那个',
              '长度 1 的子数组统一用 `sum(nums)` 一次加上，避免 `[3,4]`、`[4,3]` 里的 `4` 重复计算'],
        summary=['时间 `O(n)`：每段处理一次，`p = q` 让相邻段只共享端点',
                 '易错：`[3,4,3]` 不连续，但 `[3,4]` 和 `[4,3]` 各自连续',
                 '易错：长度 1 的子数组只能算一次，所以段内要减 1',
                 '每次累加后都取模 `10^9 + 7`'],
    ),
)
