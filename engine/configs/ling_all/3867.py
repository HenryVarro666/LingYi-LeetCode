CONFIG = dict(
    num=3867, title='数对的最大公约数之和', difficulty='Medium', category='模拟',
    author='灵茶山艾府', technique='按题意模拟 · 前缀最大值 + 排序配对',
    code='''
class Solution:
    def gcdSum(self, nums: List[int]) -> int:
        n = len(nums)
        pre = [0] * n
        mx = 0
        for i, x in enumerate(nums):
            mx = max(mx, x)
            pre[i] = gcd(x, mx)

        pre.sort()
        return sum(gcd(pre[i], pre[-1 - i]) for i in range(n // 2))
''',
    call='Solution().gcdSum([3,6,2,8,4,9])',
    expect=4,
    views=[
        dict(type='array', var='nums', pointers={'i': 'blue'}, h=200, label='nums'),
        dict(type='array', var='pre', pointers={'i': 'pink'}, h=200, label='pre = prefixGcd',
             color=lambda S, k, v: 'green' if S.get('_line') is not None and k == S.get('i') and v else None),
    ],
    watch=[('i', 'i', 'blue'), ('x', 'x', 'blue'), ('mx', 'mx', 'orange')],
    captions={
        'mx = 0': '`mx` 记录前缀最大值',
        'mx = max': '前缀最大值：`mx = max({B.mx}, {x}) = {mx}`',
        'pre[i] = gcd': '`pre[{i}] = gcd({x}, {mx}) = {pre[i]}`',
        'pre.sort()': '按非递减排序：`pre = {pre}`',
        'return sum': lambda S, B, r: '最小配最大：' + '，'.join(
            f'gcd({S.pre[k]}, {S.pre[-1-k]}) = {gcd(S.pre[k], S.pre[-1-k])}' for k in range(len(S.pre) // 2)) + f'，总和 =={r}==',
    },
    cards=dict(
        one_liner='题目怎么说就怎么做：先造 prefixGcd，排序，首尾配对',
        complexity='时间 `O(n log U + n log n)`，空间 `O(n)`',
        problem=['`prefixGcd[i] = gcd(nums[i], 前缀最大值)`',
                 '把 `prefixGcd` 排序后，最小配最大、次小配次大……',
                 '求所有数对 gcd 之和；n 为奇数时中间元素忽略',
                 '示例：`[3,6,2,8]` → `5`'],
        quote='题目怎么说，我们就怎么做。把题目要求翻译成代码即可。',
        quote_src='—— 灵茶山艾府题解',
        idea=['遍历时顺手维护 `mx`，`pre[i] = gcd(x, mx)`',
              '排序后第 `i` 个与倒数第 `i+1` 个配对：`pre[i]` 和 `pre[-1-i]`',
              '只配 `n // 2` 对，奇数时中间那个自然被忽略'],
        summary=['时间 `O(n log U + n log n)`，空间 `O(n)`',
                 '易错点：先用当前 `x` 更新 `mx`，再算 gcd',
                 '配对对数是 `n // 2`，不要多算中间元素'],
    ),
)
