TRACK = '''
class KList(list):
    pass

class TList(list):  # 只用于动画：记录 for 循环当前遍历到的下标 k
    def __iter__(self):
        for k in range(len(self)):
            self.k = k
            yield list.__getitem__(self, k)
        self.k = None

    def __deepcopy__(self, memo):
        c = KList(list.copy(self))
        c.k = getattr(self, 'k', -1)
        return c
'''


def _k(S):
    k = getattr(S.get('nums'), 'k', None)
    return k if isinstance(k, int) and k >= 0 else None


def _color(S, i, v):
    k = _k(S)
    if k is None:
        return 'orange' if v == 0 else None
    if i == k and v == 0:
        return 'yellow'
    if i <= k and v > 0:
        return 'blue'
    if v == 0:
        return 'orange'
    return None


def _txt(S):
    if 'pre' not in S or _k(S) is None:
        return '数组里的 `0` 是候选起点；非 0 是砖块'
    pre, tot = S['pre'], S['total']
    return f'左边砖块和 `pre` = =={pre}==，右边 `total − pre` = =={tot - pre}==，差 `{abs(pre * 2 - tot)}`'


CONFIG = dict(
    num=3354, title='使数组元素等于零', difficulty='Easy', category='动态规划',
    author='灵茶山艾府', technique='前缀和 · 小球打砖块',
    tags=['动态规划', '专题：前后缀分解'],
    code='''
class Solution:
    def countValidSelections(self, nums: List[int]) -> int:
        total = sum(nums)
        ans = pre = 0
        for x in nums:
            if x:
                pre += x
            elif pre * 2 == total:
                ans += 2
            elif abs(pre * 2 - total) == 1:
                ans += 1
        return ans
''',
    setup=TRACK,
    call='Solution().countValidSelections(TList([1,0,2,0,3]))',
    expect=2,
    views=[
        dict(type='text', fn=_txt, h=70),
        dict(type='array', var='nums', pointers={_k: 'yellow'}, pointer_labels={_k: 'x'}, color=_color, h=300,
             label='nums（橙 = 候选起点，蓝 = 已累计进 pre 的砖块）'),
    ],
    watch=[('total', 'total', 'purple'), ('pre', 'pre', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'total = sum': '`total` = 所有砖块总数 = =={total}==；后缀和 = `total − pre`，不用再存数组',
        'for x in nums': lambda S, B, r: (f'枚举到 `x = {S.x}`' if _k(S) is not None else '数组遍历完毕'),
        'if x:': lambda S, B, r: (f'`x = {S.x}` 非 0：是砖块，不能当起点，只累计进前缀和' if S.x
                                  else '`x = 0`：可以当起点，比较左右两边的砖块和'),
        'pre += x': '`pre += {x}` → =={pre}==（左边砖块总数）',
        'elif pre * 2 == total': '`pre × 2 = {pre*2}`，`total = {total}`：'
                                 '{"相等 → 左右一样多，向左向右都行" if pre*2==total else "不相等，再看差是不是 1"}',
        'ans += 2': '左右砖块数相同 → 初始方向左右皆可，`ans += 2` → =={ans}==',
        'elif abs': '`|pre×2 − total| = {abs(pre*2-total)}`：'
                    '{"差 1 → 只有一个方向能打光，" if abs(pre*2-total)==1 else "差不是 1 → 打不光，这个 0 不能当起点"}',
        'ans += 1': '前后差恰好 1 → 方向只能朝较多的一侧，`ans += 1` → =={ans}==',
        'return ans': '共 `{ans}` 种有效选择',
    },
    cards=dict(
        one_liner='小球打砖块：起点左右的砖块数之差不能超过 1',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['从某个 `nums[curr] = 0` 出发，选方向走；遇到正数就减 1 并掉头',
                 '走出数组后若全为 0，这个（起点，方向）有效；数有效方案数',
                 '示例：`[1,0,2,0,3]` → `2`'],
        quote='每打掉一个砖块，小球的移动方向就要反向，所以要想打掉所有砖块，起始位置左右的砖块个数之差不能超过 1。',
        quote_src='—— 灵茶山艾府题解',
        idea=['把数组看成「小球打砖块」，每打一块就反向，左右轮流打',
              '遍历时维护前缀和 `pre`，后缀和 = `total − pre`',
              '遇到 0：相等 `+2`，差 1 `+1`，其余不能当起点'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：只有 `nums[i] = 0` 的位置才能当起点，非 0 只累计前缀和',
                 '写法二：`ans += max(2 - abs(pre*2 - total), 0)`，把三个分支合成一个公式',
                 '同类：前后缀分解，枚举分割点时用 total 减前缀得到后缀'],
    ),
)
