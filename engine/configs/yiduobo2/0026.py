NUMS = [1, 1, 2, 3, 3, 3, 4, 4]


def _color(S, i, v):
    if 'now' not in S:
        return None
    if i <= S['now']:
        return 'cyan'
    return None


def _dim(S, i, v):
    return 'index' in S and 'now' in S and S['now'] < i < S['index']


def _inv(S):
    if 'index' not in S or 'now' not in S:
        if 'now' in S:
            return '`res = nums[0..now]`，第一个数一定是 `nums[0]`'
        return '假装另开一个数组 `res`，再证明它可以直接用 `nums` 表示'
    n, i = S['now'], S['index']
    return f"`len(res) = {n + 1}` ==<== `index + 1 = {i + 1}`：改动 `nums[0..{i - 1}]` 不影响后面"


def _for(S, B, ret):
    if 'index' in B and B.index == S.index:
        return f'处理完毕：`res` 就是 `nums[0..{S.now}]`'
    return f'处理 `nums[{S.index}] = {S.nums[S.index]}`，和 `res[-1] = nums[{S.now}] = {S.nums[S.now]}` 比较'


def _if(S, B, ret):
    n, i, a = S.now, S.index, S.nums
    if a[n] != a[i]:
        return f'`res[-1] = {a[n]}` ≠ `{a[i]}` → ==新数字==，加入 res'
    return f'`res[-1] = {a[n]}` = `{a[i]}` → 已经在 res 里了，跳过'


CONFIG = dict(
    num=26, title='删除有序数组中的重复项', difficulty='Easy', category='双指针',
    author='yiduobo', technique='把 nums 前缀当作结果数组 res',
    tags=['热题173', '面试经典150'],
    code='''
class Solution(object):
    def removeDuplicates(self, nums):

        if not nums:
            return 0

        now = 0
        for index in range(1, len(nums)):
            if nums[now] != nums[index]:
                now += 1
                nums[now] = nums[index]

        return now + 1
''',
    call=f'''nums = {NUMS}
k = Solution().removeDuplicates(nums)
k, nums[:k]''',
    expect=(4, [1, 2, 3, 4]),
    views=[
        dict(type='text', fn=_inv, size=27),
        dict(type='array', var='nums', pointers={'now': 'pink', 'index': 'blue'}, window=(0, 'now'),
             color=_color, dim=_dim, h=250, cell=96,
             label='nums（青框 = nums[0..now]，即结果数组 res）'),
        dict(type='array', var=lambda S: S['nums'][:S['now'] + 1] if 'now' in S else None, h=170, cell=96,
             color=lambda S, i, v: 'cyan', label='res = nums[0..now]（只是 nums 的前缀，没有另开数组）'),
    ],
    watch=[('index', 'index', 'blue'), ('now', 'now', 'pink'), ('res[-1]', 'nums[now]', 'cyan'), ('nums[index]', 'nums[index]')],
    captions={
        'if not nums': '`nums` 非空，不走特判（空数组才直接返回 0）',
        'now = 0': '答案的第一个数一定是 `nums[0]`；`now` 是 res 最后一个元素的下标',
        'for index in range': _for,
        'if nums[now] != nums[index]': _if,
        'now += 1': 'res 长度加一：`now` → {now}',
        'nums[now] = nums[index]': '写入 `nums[{now}] = {nums[now]}`：`now ≤ index`，==被覆盖的数早已处理过==',
        'return now + 1': 'res 的长度是 `now + 1 = {ret}`',
    },
    cards=dict(
        one_liner='先假设另开结果数组 res，再发现它能直接放在 nums 前面',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`nums` 非严格递增，==原地==删除重复元素，使每个元素只出现一次',
                 '返回唯一元素个数 `k`，`nums` 前 `k` 个就是去重结果',
                 '示例：`[0,0,1,1,1,2,2,3,3,4]` → `5`',
                 '本视频：`[1,1,2,3,3,3,4,4]` → `4`，前 4 个为 `[1,2,3,4]`'],
        quote='len(res)一定是小于index + 1的……换言之，当我们操作到nums[index]时，==nums[0]到nums[index - 1]即使都改动了也不会产生什么影响==。因此我们直接用nums来表示res。',
        quote_src='—— yiduobo 题解原文',
        idea=['如果能另开数组 `res`：`nums[index] != res[-1]` 就加入 res',
              '处理 `nums[index]` 时，res 最多 `index` 个数 → 写不到 `index` 及后面',
              '所以直接用 `nums[0..now]` 当 res，`now` 维护它的末尾'],
        result='返回 `4`，`nums` 前 4 个为 `[1,2,3,4]` ✓',
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '和 `res[-1]` 即 `nums[now]` 比较，先 `now += 1` 再写入',
                 '返回的是长度 `now + 1`，不是下标 `now`',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串',
                 '对比灵神：灵神 `k` 指向下一个空位、和 `nums[i-1]` 比；yiduobo 和 res 末尾比'],
    ),
)
