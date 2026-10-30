def _idx(S):
    """当前正在看的下标：第一轮用 i；第二轮 zip 没有下标，用 (x, valid, mx) 反推"""
    if S['_line'] <= 11:
        return S.get('i')
    if 'x' not in S or 'valid' not in S:
        return None
    nums, rv = S['nums'], S['right_valid']
    for k in range(len(nums)):
        pb = max(nums[:k], default=0)
        pa = max(nums[:k + 1])
        if nums[k] == S['x'] and rv[k] == S['valid'] and S['mx'] in (pb, pa):
            return k
    return None


def _color(S, i, v):
    cur = _idx(S)
    if cur is None:
        return None
    if S['_line'] <= 11:
        if i == cur:
            return 'blue'
        return 'orange' if (i > cur and S['right_valid'][i]) else None
    if i == cur:
        return 'blue'
    return 'green' if i < cur and (S['right_valid'][i] or v in S['ans']) else None


def _text(S):
    if 'mx' not in S:
        return ''
    if S['_line'] <= 11:
        return f"从右往左：右侧最大值 `mx = {S['mx']}`，橙色 = 严格大于右侧所有元素"
    return f"从左往右：左侧最大值 `mx = {S['mx']}`，答案 `ans = {S['ans']}`"


CONFIG = dict(
    num=3912, title='数组中的有效元素', difficulty='Easy', category='动态规划',
    author='灵茶山艾府', technique='前后缀分解 · 两遍维护最大值',
    tags=['灵神题单', '动态规划', '难度分 1273'],
    code='''
class Solution:
    def findValidElements(self, nums: list[int]) -> list[int]:
        # 标记严格大于其右侧所有元素的元素
        n = len(nums)
        right_valid = [False] * n
        mx = 0
        for i in range(n - 1, -1, -1):
            x = nums[i]
            right_valid[i] = x > mx
            mx = max(mx, x)

        ans = []
        mx = 0
        for valid, x in zip(right_valid, nums):
            if valid or x > mx:
                ans.append(x)
            mx = max(mx, x)
        return ans
''',
    call='Solution().findValidElements([1,2,4,2,3,2])',
    expect=[1, 2, 4, 3, 2],
    views=[
        dict(type='text', fn=_text, size=28),
        dict(type='array', var='nums', label='nums', h=260, color=_color),
        dict(type='array', var='right_valid', label='right_valid（严格大于右侧所有元素）', h=200,
             color=lambda S, i, v: 'orange' if v else None),
        dict(type='array', var='ans', label='ans', h=200),
    ],
    watch=[('mx', 'mx', 'purple'), ('x', 'x', 'blue'), ('valid', 'valid', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'right_valid[i] = ': '`{x}` 与右边最大值 `mx = {B.mx}` 比：{"==严格更大，右侧有效==" if right_valid[i] else "不比右边大，右侧不算有效"}',
        'mx = max(mx, x)': '更新最大值 `mx = max({B.mx}, {x}) = {mx}`，后面（或前面）的元素都要和它比',
        'if valid or': '`valid = {valid}`，`x = {x}` 对比左侧最大值 `mx = {mx}`：{"==至少满足一个条件，有效==" if (valid or x > mx) else "两边都不严格更大，无效"}',
        'ans.append': '`{x}` 有效，加入答案：`ans = {ans}`',
        'return ans': '两个方向的条件都查完了，返回 `{ans}`',
    },
    cards=dict(
        one_liner='倒着标记「比右边都大」，正着判断「比左边都大」',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['元素 `nums[i]` 有效：严格大于左侧所有元素，或严格大于右侧所有元素',
                 '首尾元素一定有效，按原顺序返回所有有效元素',
                 '示例：`[1,2,4,2,3,2]` → `[1,2,4,3,2]`'],
        quote='倒序遍历 nums，同时用一个布尔数组记录哪些元素，严格大于其右侧所有元素。……正序遍历 nums，做法同上。',
        quote_src='—— 灵茶山艾府题解',
        idea=['第一遍倒着走，用 `mx` 记录已走过的最大值，`x > mx` 就在 `right_valid` 里标记',
              '第二遍正着走，`mx` 还是同一个套路，`valid or x > mx` 就把它放进答案',
              '`mx` 初值为 0：题目保证元素 ≥ 1，所以首尾一定会被判有效'],
        summary=['时间 `O(n)`，空间 `O(n)`（`right_valid` 数组）',
                 '易错点：必须是「严格大于」，相等不算；`[5,5,5,5]` 只留首尾',
                 '先比较、后更新 `mx`，否则元素会和自己比较',
                 '同类：前后缀分解专题，一遍算后缀、一遍边走边算前缀'],
    ),
)
