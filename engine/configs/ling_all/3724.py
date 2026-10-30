def _idx(S):
    if 'x' not in S or 'nums1' not in S:
        return None
    a, b = S['nums1'], S['nums2']
    for i in range(len(a)):
        if (min(a[i], b[i]), max(a[i], b[i])) == (S['x'], S['y']):
            return i
    return None


def _col1(S, i, v):
    return 'blue' if _idx(S) == i else None


def _col2(S, i, v):
    if i == len(S['nums2']) - 1:
        return 'yellow'
    return 'blue' if _idx(S) == i else None


def _txt(S):
    if 'target' not in S:
        return ''
    t = f"`target = {S['target']}`（nums2 最后一个数，要追加到 nums1 末尾）"
    return t


def _txt2(S):
    if 'x' not in S:
        return ''
    x, y, t = S['x'], S['y'], S['target']
    mn = S.get('mn')
    rel = '在 [x,y] 内 → 顺带追加，代价 0' if x <= t <= y else ('target < x → 代价 x - target' if t < x else 'target > y → 代价 target - y')
    s = f"区间 `[{x}, {y}]`：{rel}"
    if mn is not None and mn != float('inf'):
        s += f"；当前 `mn = {mn}`"
    return s


CONFIG = dict(
    num=3724, title='转换数组的最少操作次数', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='分类讨论：顺带追加 target',
    tags=['灵神题单', '难度分 1790'],
    code='''
# 手写 min max 更快
min = lambda a, b: b if b < a else a
max = lambda a, b: b if b > a else a

class Solution:
    def minOperations(self, nums1: List[int], nums2: List[int]) -> int:
        target = nums2[-1]
        ans = 1  # 把元素追加到 nums1 的末尾需要一次操作
        mn = inf
        for x, y in zip(nums1, nums2):
            if x > y:
                x, y = y, x  # 保证 x <= y，简化后续逻辑
            ans += y - x
            # 如果 target 在 [x,y] 中，那么在从 x 变成 y 的过程中，可以顺带把 target 追加到 nums1 的末尾，代价为 0
            # 如果 target < x，代价为 x-target
            # 如果 target > y，代价为 target-y
            if mn > 0:  # 如果 target 还不在任何 [x,y] 中，则计算
                mn = min(mn, max(x - target, target - y))
        return ans + max(mn, 0)  # 如果 target 在 [x,y] 中，上面可能会算出负数
''',
    call='Solution().minOperations([1,3,6], [2,4,5,3])',
    expect=4,
    views=[
        dict(type='array', var='nums1', label='nums1', color=_col1, h=190),
        dict(type='array', var='nums2', label='nums2（黄色 = target）', color=_col2, h=190),
        dict(type='text', fn=_txt, h=50),
        dict(type='text', fn=_txt2, h=60),
    ],
    watch=['target', 'x', 'y', ('ans', 'ans', 'green'), ('mn', 'mn', 'orange')],
    skip=['min = lambda', 'max = lambda'],
    captions={
        'target = nums2[-1]': 'nums2 比 nums1 多一个，多出来的就是最后一个数：`target = {target}`',
        'ans = 1': '追加操作固定要 1 次：`ans = 1`',
        'mn = inf': '`mn` 记录「额外调整 target 的最小代价」，先设无穷大',
        'for x, y in zip': lambda S, B, r: ('zip 配完了，循环结束' if ('x' in B and B.x == S.x and B.y == S.y) else f'配对 `nums1[i] = {S.x}` → `nums2[i] = {S.y}`'),
        'x, y = y, x': lambda S, B, r: f'`x = {B.x} > y = {B.y}` → 交换，保证 `x <= y`：区间 `[{S.x}, {S.y}]`',
        'ans += y - x': '这一对必须挪 `y - x` 步：`ans += {y} - {x}` → =={ans}==',
        'if mn > 0': lambda S, B, r: (f'`mn = {S.mn}` > 0：target 还没被任何区间覆盖，继续算' if B.mn > 0
                                      else f'`mn = {S.mn}`：target 已被某个 `[x,y]` 覆盖，顺带追加，不用再算'),
        'mn = min(mn': '代价 `max(x - target, target - y)` = `max({x - target}, {target - y})` = {max(x - target, target - y)}；`mn` → =={mn}==（≤ 0 表示 target 在 [x,y] 内）',
        'return ans': '`ans + max(mn, 0)` = `{ans} + {max(mn, 0)}` = =={ret}==；`max(mn, 0)` 把负数（target 在区间内）归零',
    },
    cards=dict(
        one_liner='挪 x 到 y 的途中，顺带把 target 追加过去',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`nums1` 长 `n`，`nums2` 长 `n+1`；操作：某个数 `+1`、`-1`、或把它追加到末尾',
                 '求把 `nums1` 变成 `nums2` 的最少操作次数',
                 '示例：`[1,3,6]` → `[2,4,5,3]`，答案 `4`'],
        quote='贪心地想，能不能在从 x 变成 y 的过程中，顺带把 target 追加到 nums1 的末尾？',
        quote_src='—— 灵茶山艾府题解',
        idea=['恰好追加一个数，其余 `nums1[i]` 必须一一变成 `nums2[i]`，各付 `|x - y|` 步',
              '追加的那个数最终要变成 `target`：选某个 `x` 在变成 `y` 的路上追加',
              '`target` 在 `[x,y]` 内代价 0；在左边付 `x - target`；在右边付 `target - y`',
              '对所有 `(x,y)` 取最小代价'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '追加操作本身还要 `+1`，别漏掉：`ans = 1`',
                 '`target` 在区间内时会算出负数，最后用 `max(mn, 0)` 归零',
                 '原文开头手写了 `min`/`max`（比内置更快），本视频照搬',
                 '思考题：`nums2` 更长或可插到任意位置怎么做'],
    ),
)
