def _state(S):
    if 'left' not in S:
        return f"找 nums 中==下标最小且 ≥ {S['target']}== 的数" if 'target' in S else ''
    l, r = S['left'], S['right']
    s = f"答案范围 `[{l}, {r}]`"
    if 'mid' in S and l < r + 1 and S['mid'] < len(S['nums']):
        x, t = S['nums'][S['mid']], S['target']
        s += f"   ·   nums[{S['mid']}] = =={x}== {'=' if x == t else ('<' if x < t else '>')} {t}"
    return s


def _eq(S, B, ret):
    x, t = S.nums[S.mid], S.target
    if x == t:
        return f'`nums[{S.mid}] = {x} == {t}`：找到 target，==直接返回 mid=='
    return f'`nums[{S.mid}] = {x} ≠ {t}`：没碰上 target，再看大小关系'


def _lt(S, B, ret):
    x, t = S.nums[S.mid], S.target
    if x < t:
        return f'`{x} < {t}`：mid 及左边都比 target 小 → ==答案位于 mid + 1 到 right 之间=='
    return f'`{x} > {t}`：答案位于 left 到 mid 之间，==mid 还有可能成为答案=='


def _same(S, B, ret):
    if B.left == B.right:
        return f'`left == right == {B.left}`：范围只剩一个位置，==它就是答案==，直接返回'
    return f'`left = {B.left}`，`right = {B.right}`：范围里还有多个位置 → 继续二分'


CONFIG = dict(
    num=35, title='搜索插入位置', difficulty='Easy', category='二分查找',
    author='yiduobo', technique='特判末尾 + 二分（right = mid 保留候选）',
    code='''
class Solution(object):
    def searchInsert(self, nums, target):
        if not nums:
            return 0
        if target > nums[-1]:
            return len(nums)

        left = 0
        right = len(nums) - 1
        while left <= right:
            if left == right:
                return left
            else:
                mid = (right + left) // 2
                if nums[mid] == target:
                    return mid
                elif nums[mid] < target:
                    left = mid + 1
                else:
                    right = mid
''',
    call='Solution().searchInsert([1,3,5,6,8,10,12], 9)',
    expect=5,
    views=[
        dict(type='text', fn=_state, size=28),
        dict(type='array', var='nums', pointers={'left': 'blue', 'right': 'pink', 'mid': 'yellow'},
             window=('left', 'right'), cell=110, h=300,
             dim=lambda S, i, v: 'left' in S and not (S['left'] <= i <= S['right']),
             color=lambda S, i, v: 'green' if 'left' in S and S['left'] == S['right'] == i else None),
        dict(type='text', size=25, lines=2, h=100,
             text='比较 `nums[mid]` 和 `target`：`==` 返回 mid；`<` 则 `left = mid + 1`\n'
                  '`>` 则 `right = mid`（==mid 可能是答案，不能写 mid - 1==）'),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'yellow'),
           ('nums[mid]', 'nums[mid]'), ('target', 'target')],
    skip=['left = 0', 'while left <= right'],
    captions={
        'if not nums': '特判空数组（本例非空）',
        'if target > nums[-1]': '`{target} > nums[-1] = {nums[-1]}`？不成立。==只有比最后一个数还大，才插到末尾== `len(nums)`',
        'right = len(nums)': '否则答案一定在 `[{left}, {right}]` 里：下标最小且 `≥ {target}` 的数必然存在',
        'if left == right': _same,
        'mid = (right + left)': '`mid = ({right} + {left}) // 2 = {mid}`，考察 `nums[{mid}] = {nums[mid]}`',
        'if nums[mid] == target': _eq,
        'elif nums[mid] < target': _lt,
        'left = mid + 1': '`left = mid + 1 = {left}`：扔掉 mid 及左边，范围变成 `[{left}, {right}]`',
        'right = mid': '`right = mid = {right}`，==不是 mid - 1==：保留 mid 这个候选，范围变成 `[{left}, {right}]`',
    },
    cards=dict(
        one_liner='找下标最小的 ≥ target 的数；大于时 right = mid，把 mid 留作候选',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['有序、无重复数组 `nums` 和 `target`：找到就返回下标，否则返回==按顺序插入的位置==',
                 '要求 `O(log n)`',
                 '示例：`[1,3,5,6]`, `5` → `2`；`2` → `1`；`7` → `4`'],
        quote='如果nums[mid] > target，那么说明答案位于left到mid之间。==需要注意这里mid还是有可能成为答案的，因此此时right = mid而不是mid - 1。==',
        quote_src='—— yiduobo 题解原文',
        idea=['题目要找 nums 中==下标最小，且大于等于 target== 的数',
              '先特判：target 比最后一个数还大 → 直接返回 `len(nums)`；否则答案在 `[0, n-1]`',
              '`==` 返回 mid；`<` 时 `left = mid + 1`；`>` 时 `right = mid`；只剩一个位置就返回它'],
        result='返回 `5`：`10` 是第一个 `≥ 9` 的数，9 应插在下标 5 ✓',
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '原文为 Python 2 写法：整数除法 `/` 已改为 `//`，并删去了 `"""type"""` 文档字符串',
                 '`right = mid` 不能写成 `mid - 1`：mid 可能就是插入位置',
                 '`left == right` 时立刻返回，所以 `right = mid` 不会死循环',
                 '必须先特判 `target > nums[-1]`：答案 `n` 不在 `[0, n-1]` 里'],
    ),
)
