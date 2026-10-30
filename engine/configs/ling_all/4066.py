def _idx(S):
    """当前正在处理的相邻对的左下标（nums[k], nums[k+1]）"""
    if 'x' not in S or 'cnt' not in S:
        return None
    ln = S['_line']
    if ln >= 16:
        return None
    k = S['base'] + sum(S['cnt'].values())
    k = k - 1 if ln in (8, 14) else k
    return None if k + 1 >= len(S['nums']) else k


def _idx1(S):
    k = _idx(S)
    return None if k is None else k + 1


def _color(S, i, v):
    k = _idx(S)
    return 'yellow' if k is not None and i in (k, k + 1) else None


def _txt(S):
    if 'cnt' not in S:
        return ''
    best = max(S['cnt'].values(), default=0)
    if S['_line'] >= 16:
        return f'答案 = `base` + `max_cnt` = {S["base"]} + {best} = =={S["base"] + best}=='
    return f'`base` = ==相邻已相等的对数== {S["base"]}，相邻不等的数对里出现最多的有 =={best}== 次'


CONFIG = dict(
    num=4066, title='至多一次替换后的最大相邻相等元素对数', difficulty='Medium', category='模拟',
    author='灵茶山艾府', technique='哈希表统计相邻不等数对', tags=[],
    code='''
class Solution:
    def maxEqualAdjacentPairs(self, nums: list[int]) -> int:
        base = 0
        cnt = defaultdict(int)

        for x, y in pairwise(nums):
            if x == y:
                base += 1
            else:
                # 把 (x,y) 和 (y,x) 都统一为 (x,y)
                if x > y:
                    x, y = y, x
                # 统计相邻且不相等的数对个数
                cnt[(x, y)] += 1

        max_cnt = max(cnt.values(), default=0)
        return base + max_cnt
''',
    call='Solution().maxEqualAdjacentPairs([1,1,2,3,2,2,3])',
    expect=5,
    views=[
        dict(type='array', var='nums', label='nums（黄 = 当前相邻的两个数）', h=190, pointers={}, color=_color),
        dict(type='map', var='cnt', label='cnt：相邻且不相等的数对 (x, y) → 出现次数', fmt=lambda k, v: f'{k}: {v}', h=250, font=30),
        dict(type='text', h=110, size=28, fn=_txt),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), ('base', 'base', 'cyan'), ('max_cnt', 'max_cnt', 'green')],
    captions={
        'base = 0': '`base` 记录不操作时相邻相等的对数',
        'for x, y in pairwise': '看相邻的一对：`({x}, {y})`',
        'if x == y': lambda S, B, r: (f'`{S.x} == {S.y}`：相邻已相等' if S.x == S.y else f'`{S.x} != {S.y}`：相邻不等，值得统计'),
        'base += 1': '`x` 和 `y` 相等：替换后还是 y 和 y 相邻（或都被替换），==不受影响==，直接计入 `base` = {base}',
        'if x > y': lambda S, B, r: f'`({S.x}, {S.y})` 和 `({S.y}, {S.x})` 是同一种数对，统一成小的在前：' + ('需要交换' if S.x > S.y else '已经有序'),
        'x, y = y, x': '交换后 `(x, y) = ({x}, {y})`',
        'cnt[(x, y)] += 1': '数对 `({x}, {y})` 出现 =={cnt[(x, y)]}== 次：把 {x} 换成 {y}（或反过来），这些位置就都==变相等==',
        'max_cnt = max': '只能选一对 `(x, y)` 替换，选出现次数最多的：`max_cnt` = =={max_cnt}==',
        'return base + max_cnt': '答案 = `base + max_cnt` = {base} + {max_cnt} = =={base + max_cnt}==',
    },
    cards=dict(
        one_liner='原本相等的对不受影响，替换只能多救回最常见的那种不等对',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['把所有值为 `x` 的元素换成 `y`（至多一次），求相邻相等的对数最大值',
                 '示例：`[1,2,3,2]` → `2`（把 3 换成 2）',
                 '本视频：`[1,1,2,3,2,2,3]` → `5`'],
        quote='把 nums 中的 x 替换成 y（x≠y）后，只有与 x 相邻的数对的相等关系会发生变化：如果替换前 x 和 y 相邻，那么替换后变成 y 和 y 相邻，答案增大。',
        quote_src='—— 灵茶山艾府题解',
        idea=['不操作的答案 `base` = 相邻相等的对数',
              '替换 x→y：只有相邻值恰为 `(x, y)` 的对会变相等，其余对不变（x 与 z 相邻也不会变相等）',
              '所以增量就是数对 `(x, y)` 的出现次数，取最大即可'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：`(x, y)` 与 `(y, x)` 要统一成同一个 key，否则会少算',
                 '没有不等的相邻对时 `max(..., default=0)`，答案就是 `base`',
                 '本题是 1-indexed 数组的描述，代码里按 0-indexed 的 `pairwise` 处理即可'],
    ),
)
