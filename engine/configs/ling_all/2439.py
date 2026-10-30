def _txt(S):
    if 'limit' not in S:
        return ''
    s = f"猜上界 `limit = {S['limit']}`：要让所有数都 `≤ {S['limit']}`"
    if 'extra' in S:
        s += f"。从右往左，手上多出的积木 `extra = ` =={S['extra']}=="
    return s


def _col(S, i, v):
    if 'i' not in S or '_inner' not in S or 'new_num' not in S['_inner']:
        return None
    if i == S['i']:
        return 'orange' if S['new_num'] > S['limit'] else 'green'
    return None


def _f(S):
    if 'new_num' not in S.get('_inner', {}):
        return ''
    i = S['i']
    return f"`nums[{i}] + extra = {S['nums'][i]} + {S['_inner'].get('extra', 0)}`  →  `new_num = ` =={S['new_num']}=="


CONFIG = dict(
    num=2439, title='最小化数组中的最大值', difficulty='Medium', category='二分算法',
    author='灵茶山艾府', technique='二分答案 + 积木往左堆',
    tags=['二分答案', '难度分 1965'],
    code='''
class Solution:
    def minimizeArrayValue(self, nums: List[int]) -> int:
        def check(limit: int) -> bool:
            extra = 0
            for i in range(len(nums) - 1, 0, -1):
                new_num = nums[i] + extra  # 把多出的积木堆到 nums[i] 上
                extra = max(new_num - limit, 0)  # 如果 new_num - limit > 0，那么多出的积木继续丢给左边
            return nums[0] + extra <= limit

        return bisect_left(range(max(nums)), True, lo=nums[0], key=check)
''',
    call='Solution().minimizeArrayValue([3,7,1,6,2])',
    expect=5,
    views=[
        dict(type='text', fn=_txt),
        dict(type='bars', var='nums', pointers={'i': 'blue'}, label='nums（积木堆）', h=330, color=_col),
        dict(type='text', fn=_f),
    ],
    watch=['limit', ('extra', 'extra', 'orange'), ('i', 'i', 'blue'), ('new_num', 'new_num', 'cyan')],
    max_steps=70,
    captions={
        'return bisect_left': lambda S, B, r: ('二分答案：`check(limit)` 判断「所有数能否都压到 `limit` 以内」，`limit` 越大越容易。下面逐个试' if r is None
                                               else f'二分结束：最小可行的上界是 =={r}=='),
        'extra = 0': '还没有多出的积木：`extra = 0`',
        'for i in range': lambda S, B, r: (f"`i` 走完了，剩下 `nums[0]` 单独判断" if B.get('i') == S.i
                                           else f"从右往左，到 `i = {S.i}`：多出的积木只能往左边送"),
        'new_num = ': '`nums[{i}]` 加上右边送来的 `{B.extra}` → `new_num = {new_num}`',
        'extra = max': lambda S, B, r: (f"`new_num = {S.new_num} > limit = {S.limit}` → 多出 `{S.extra}`，继续丢给 `nums[{S.i - 1}]`" if S.extra > 0
                                        else f"`new_num = {S.new_num} ≤ limit = {S.limit}` → 没有多余，`extra = 0`"),
        'return nums[0]': lambda S, B, r: (f"`nums[0] + extra = {S.nums[0]} + {S.extra} = {S.nums[0] + S.extra} ≤ {S.limit}` → ==可行==，上界可以再小" if r
                                           else f"`nums[0] + extra = {S.nums[0]} + {S.extra} = {S.nums[0] + S.extra} > {S.limit}` → ==不可行==，`nums[0]` 没法再往右送"),
    },
    cards=dict(
        one_liner='最小化最大值就是二分答案：猜上界，积木从右往左堆',
        complexity='时间 `O(n log U)`，空间 `O(1)`',
        problem=['可以把 `nums[i]` 的 1 个单位移到 `nums[i-1]`，次数不限',
                 '求操作后数组最大值的最小值',
                 '示例：`[3,7,1,6]` → `5`；本视频用 `[3,7,1,6,2]` → `5`'],
        quote='「最小化最大值」就是二分答案的代名词。我们猜测一个上界 limit，即要求操作后所有元素均不超过 limit。',
        quote_src='—— 灵茶山艾府题解',
        idea=['把 `nums[i]` 看成积木堆，多出的积木可以一路往左搬',
              '从右往左模拟：`nums[i] > limit` 就把多出的 `extra` 丢给左边',
              '最后 `nums[0]` 再加上 `extra` 若不超过 `limit`，这个上界可行；`nums[0]` 不能往右送'],
        summary=['二分开区间：下界 `nums[0]-1` 不可行（`nums[0]` 减不掉），上界 `max(nums)` 一定可行',
                 '`check` 不改 `nums`，只用 `extra` 变量，空间 `O(1)`',
                 '方法二：前缀平均数上取整的最大值，`max((s + i) // (i + 1) ...)`，`O(n)`',
                 '上取整公式：`ceil(a/b) = (a+b-1)//b`',
                 '同类题：2560、2616、2513'],
    ),
)
