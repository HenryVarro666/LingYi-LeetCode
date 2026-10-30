CONFIG = dict(
    num=2826, title='将三个组排序', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='贪心 + 二分求最长不减子序列', tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1721'],
    code='''
class Solution(object):
    def minimumOperations(self, nums):

        f = [nums[0]]
        for v in nums[1:]:
            if v >= f[-1]:
                f.append(v)
            else:
                left = 0
                right = len(f) - 1
                while left < right:
                    mid = (left + right) // 2
                    if f[mid] > v:
                        right = mid
                    else:
                        left = mid + 1

                f[left] = v

        return len(nums) - len(f)
''',
    call='Solution().minimumOperations([2,1,3,2,1])',
    expect=3,
    views=[
        dict(type='array', var='nums', h=180, label='nums'),
        dict(type='array', var='f', h=220, label='f：当前最长不减子序列（贪心维护）',
             pointers={'left': 'blue', 'right': 'pink'}, window=('left', 'right')),
        dict(type='text', fn=lambda S: f"`len(nums) − len(f) = {len(S['nums'])} − {len(S['f'])}` = =={len(S['nums']) - len(S['f'])}==" if 'f' in S else ''),
    ],
    watch=[('v', 'v', 'yellow'), ('left', 'left', 'blue'), ('right', 'right', 'pink'), ('f', 'f', 'cyan')],
    captions={
        'f = [nums[0]]': '题目等价于：留下最长的不减子序列，其余都改掉。`f` 先放第一个数 `{f[0]}`',
        'if v >= f[-1]': lambda S, B, r: (f'`{S.v} >= {S.f[-1]}`：不小于末尾，直接接在后面' if S.v >= S.f[-1]
                                          else f'`{S.v} < {S.f[-1]}`：接不上，要在 `f` 里找位置替换'),
        'f.append': '`f` 末尾加入 `{v}`，长度变为 {len(f)}',
        'left = 0': '二分区间 `[0, {len(f) - 1}]`：找 `f` 中第一个 `> {v}` 的位置',
        'while left < right': lambda S, B, r: (f'区间 `[{S.left}, {S.right}]` 还没缩成一个点' if S.left < S.right
                                               else f'`left = right = {S.left}`：找到位置'),
        'mid = ': '`mid = ({left} + {right}) // 2 = {mid}`（原文 `/` 在 Python 3 要用 `//`）',
        'if f[mid] > v': lambda S, B, r: (f'`f[{S.mid}] = {S.f[S.mid]} > {S.v}`：答案在左半，`right = mid`' if S.f[S.mid] > S.v
                                          else f'`f[{S.mid}] = {S.f[S.mid]} <= {S.v}`：相等也能接，答案在右半，`left = mid + 1`'),
        'f[left] = v': '用 `{v}` 替换 `f[{left}]`：长度不变，末尾更小，后面更容易接上',
        'return len': '保留 `{len(f)}` 个，需要修改 `{len(nums)} − {len(f)}` = =={len(nums) - len(f)}== 个',
    },
    cards=dict(
        one_liner='要改的最少 = 总数 − 最长不减子序列',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`nums` 每个元素是 1、2 或 3，每次可以删除一个元素',
                 '求让数组变成非递减的最少操作次数',
                 '本视频：`[2,1,3,2,1]` → `3`'],
        quote='为了使得修改的次数最少，就是要让不进行修改的位置最多，那么本题实际上就是要找出原数组中的一个最长的不减子序列。',
        quote_src='—— yiduobo 题解原文',
        idea=['最终数组是 1 在左、2 在中、3 在右，即单调不减',
              '不改的位置越多越好，转成经典的最长不减子序列',
              '贪心：能接就接；接不上就二分，替换第一个比 v 大的数'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`',
                 '不减允许相等：二分找第一个 `> v`，所以 `f[mid] > v` 才收缩右边',
                 '`f` 不一定是真实子序列，只有长度有意义',
                 '对比灵神：灵神用 `bisect_right` 一行完成，且另给值域 3 的 DP'],
    ),
)
