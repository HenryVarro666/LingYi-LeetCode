NUMS = [1, 2, 3, 1, 2, 1]


def _color(S, i, v):
    if 'i' not in S:
        return None
    if i == S['i']:
        return 'blue'
    x = S.get('x')
    if x is not None and S['_line'] in (5, 6) and x in S['last'] and i == S['last'][x]:
        return 'pink'
    return None


def _gap(S):
    if 'i' not in S or S['_line'] not in (5, 6):
        return '枚举右边的 `nums[i]`，在哈希表里查它==上一次出现的位置=='
    x, i = S['x'], S['i']
    if x not in S['last']:
        return f'`{x}` 之前没出现过 → 不可能和左边配对'
    d = i - S['last'][x]
    return f"`i - last[{x}] = {i} - {S['last'][x]} = {d}` " + ('`≤ k = 2` → ==找到了==' if d <= S['k'] else '`> k = 2` → 太远了')


def _if_cap(S, B, ret):
    x, i = S.x, S.i
    if x not in S.last:
        return f'`{x}` 不在 `last` 中：它是第一次出现'
    d = i - S.last[x]
    if d <= S.k:
        return f'`{x}` 上次出现在 `{S.last[x]}`，距离 `{d} ≤ k` → 满足条件'
    return f'`{x}` 上次出现在 `{S.last[x]}`，距离 `{d} > k` → 不满足'


def _set_cap(S, B, ret):
    x, i = S.x, S.i
    if x in B.last:
        return f'更新 `last[{x}] = {i}`：==只保留最近一次==，以后离右边更近（旧的 `{B.last[x]}` 没用了）'
    return f'记录 `last[{x}] = {i}`：给右边的数查询'


CONFIG = dict(
    num=219, title='存在重复元素 II', difficulty='Easy', category='哈希',
    author='灵茶山艾府', technique='枚举右，维护左 · 哈希表记上一次出现的位置',
    tags=['面试经典150'],
    code='''
class Solution:
    def containsNearbyDuplicate(self, nums: List[int], k: int) -> bool:
        last = {}
        for i, x in enumerate(nums):
            if x in last and i - last[x] <= k:
                return True
            last[x] = i
        return False
''',
    call=f'Solution().containsNearbyDuplicate({NUMS}, 2)',
    expect=True,
    views=[
        dict(type='text', fn=_gap, size=26, h=60),
        dict(type='array', var='nums', label='nums（蓝 = i，粉 = last[x]，框 = 与 i 距离 ≤ k 的范围）', cell=100, h=230,
             pointers={'i': 'blue'}, color=_color,
             window=(lambda S: max(0, S['i'] - S['k']) if 'i' in S else None, lambda S: S['i'] if 'i' in S else None)),
        dict(type='map', var='last', label='last：数字 → 上一次出现的下标', h=200, font=34, fmt=lambda k, v: f'{k} → {v}'),
    ],
    watch=[('i', 'i', 'blue'), ('x', 'x'), ('k', 'k')],
    captions={
        'last = {}': '`last[x]` 记录 `x` ==上一次出现的位置==（下标）',
        'for i, x in enumerate': lambda S, B, ret: (f'枚举右：`i = {S.i}`，`x = {S.x}`' if 'i' in S and S.i != B.get('i')
                                                    else '遍历结束'),
        'if x in last and': _if_cap,
        'return True': '`nums[{last[x]}] == nums[{i}] == {x}`，下标差 `{i - last[x]} ≤ k` → 返回 ==True==',
        'last[x] = i': _set_cap,
        'return False': '遍历完也没找到 → 返回 False',
    },
    cards=dict(
        one_liner='遍历时用哈希表记每个数上一次出现的位置',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['整数数组 `nums` 和整数 `k`：是否存在两个==不同的下标== `i`、`j`',
                 '满足 `nums[i] == nums[j]` 且 `abs(i - j) <= k`？',
                 '示例：`[1,2,3,1], k = 3` → `true`；`[1,2,3,1,2,3], k = 2` → `false`'],
        quote='我们可以在遍历 nums 的同时，用一个哈希表 last 记录==每个数 x 上一次出现的位置==（下标）last[x]。',
        quote_src='—— 灵茶山艾府题解「方法一：枚举右，维护左」',
        idea=['枚举右边的 `nums[i]`，左边离它==最近==的相同元素在 `last[x]`',
              '`i - last[x] <= k` 就找到了；否则更新 `last[x] = i`',
              '本视频：`nums = [1,2,3,1,2,1], k = 2`'],
        after=[dict(heading='答疑：为什么只看左边？', lines=[
            '如果 `x` 右边也有相等的 `nums[j]`',
            '遍历到 `nums[j]` 时，`last[x] = i`，会判断 `j - i <= k`',
            '==相邻的相同元素都会被检查到==，不会漏掉']),
               dict(heading='方法二：定长滑动窗口', lines=[
            '等价于：有没有长为 `min(k+1, n)` 的子数组包含相同元素',
            '哈希集合维护窗口；`x` ==进窗口前==先查是否已在集合中',
            '`i >= k` 时移出 `nums[i-k]`；空间降到 `O(min(k, n))`'])],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '先判断再更新：`last[x] = i` 写在判断前面就成了自己和自己比',
                 '为什么覆盖旧下标？==离右边越近越好==，更早的下标不会更优',
                 '「枚举右，维护左」是两数之和（第 1 题）同款套路'],
    ),
)
