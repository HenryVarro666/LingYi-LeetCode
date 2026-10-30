def _txt(S):
    if 'right' not in S:
        return '先排序：排序不改变「两数之和」，所以不影响答案'
    l, r, t = S['left'], S['right'], S['target']
    if l >= r:
        return f'`left = {l} >= right = {r}`，两指针相遇，结束'
    s = S['nums'][l] + S['nums'][r]
    if s < t:
        return f'`{S["nums"][l]} + {S["nums"][r]} = {s} < {t}`：left 与 `[{l+1}, {r}]` 里每个数都合法，共 =={r-l}== 对'
    return f'`{S["nums"][l]} + {S["nums"][r]} = {s} >= {t}`：right 太大，和谁配都不行'


CONFIG = dict(
    num=2824, title='统计和小于目标的下标对数目', difficulty='Easy', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='排序 + 相向双指针',
    tags=['滑动窗口与双指针', '三、单序列双指针'],
    code='''
class Solution:
    def countPairs(self, nums: List[int], target: int) -> int:
        nums.sort()
        ans = left = 0
        right = len(nums) - 1
        while left < right:
            if nums[left] + nums[right] < target:
                ans += right - left
                left += 1
            else:
                right -= 1
        return ans
''',
    call='Solution().countPairs([-6,2,5,-2,-7,-1,3], -2)',
    expect=10,
    views=[
        dict(type='text', fn=_txt, h=70),
        dict(type='array', var='nums', pointers={'left': 'blue', 'right': 'pink'}, window=('left', 'right'), h=300,
             dim=lambda S, i, v: 'right' in S and not (S['left'] <= i <= S['right'])),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), 'target', ('ans', 'ans', 'green')],
    captions={
        'nums.sort()': '只关心两数之和，==顺序不影响答案==，先排序：`{nums}`',
        'right = len': '`right = len(nums) - 1 = {right}`，左右指针分别指向最小和最大',
        'while left < right': lambda S, B, r: (f'`left = {S.left} < right = {S.right}`，还有数对没算' if S.left < S.right
                                                else f'`left = {S.left} >= right = {S.right}`：指针相遇，结束'),
        'if nums[left] + nums[right] < target': '`{nums[left]} + {nums[right]} = {nums[left]+nums[right]}` 与 `target = {target}` 比较 → {"小于" if nums[left]+nums[right] < target else "不小于"}',
        'ans += right - left': '有序：left 与 `[left+1, right]` 里任何数相加都 `< target` → 一次加 `{right} - {left}` = {right-left} 对，`ans` = =={ans}==',
        'left += 1': 'left 的所有搭档都数完了 → `left` 右移到 {left}',
        'right -= 1': 'right 与 `[left, right-1]` 里任何数相加都 `>= target` → 扔掉 right，`right` 左移到 {right}',
        'return ans': '一共 =={ans}== 对',
    },
    cards=dict(
        one_liner='排序后相向双指针：一次数一批合法数对',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['数组 `nums`，数 `i < j` 且 `nums[i] + nums[j] < target` 的下标对个数',
                 '示例：`nums=[-6,2,5,-2,-7,-1,3]`，`target=-2` → `10`'],
        quote='从数组中选两个数，我们只关心这两个数的和是否小于 target。由于 a+b=b+a，无论如何排列数组元素，都不会影响加法的结果。',
        quote_src='—— 灵茶山艾府题解',
        idea=['既然顺序无关，先排序，再用相向双指针（同 167 两数之和 II）',
              '`nums[left] + nums[right] < target`：left 与区间内所有数都合法，一次加 `right - left`',
              '否则 right 太大，后面不再考虑它，`right -= 1`'],
        summary=['时间 `O(n log n)`（瓶颈在排序），空间 `O(1)`',
                 '易错：加的是 `right - left`，不是 1；数完后移动的是 left',
                 '条件是严格小于，等于 target 要走 else 分支',
                 '同类题：167 两数之和 II、15 三数之和'],
    ),
)
