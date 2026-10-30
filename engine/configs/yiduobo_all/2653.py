NUMS = [-3, -1, -2, 2]
K, X = 3, 2


def _pre(f, m):
    s = 0
    while m > 0:
        s += f[m]
        m -= m & -m
    return s


def _wr(S):
    if S.get('_line', 0) >= 36 and 'v' in S:
        return S['nums'].index(S['v']) if 'nums' in S else K - 1
    return K - 1


def _bin(S):
    f = S.get('f')
    if f is None or 'right' not in S:
        return '`f` 是树状数组，下标 `v + 51`：`f` 查询前缀 = 窗口内 `≤ v` 的个数'
    l, r = S['left'], S['right']
    mid = S.get('mid')
    t = f'第 x = `{X}` 小的值在 ==[{l - 51}, {r - 51}]== 里'
    if mid is not None and S.get('_line', 0) >= 16:
        t += f'；试 `mid` 对应值 `{mid - 51}`：`≤ {mid - 51}` 的数有 ==`{_pre(f, mid)}`== 个'
    return t


CONFIG = dict(
    num=2653, title='滑动子数组的美丽值', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='滑动窗口 + 树状数组 + 二分',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针', '难度分 1786'],
    code='''
class Solution(object):
    def getSubarrayBeauty(self, nums, k, x):

        res = [0]
        f = [0] * 102

        def add(index, delta):
            while index <= 101:
                f[index] += delta
                index += index & -index
        
        def get():
            left = 1
            right = 101
            while left < right:
                mid = (left + right) >> 1

                index = mid
                s = 0
                while index > 0:
                    s += f[index]
                    index -= index & -index
                
                if s >= x:
                    right = mid
                else:
                    left = mid + 1
            
            return left

        for v in nums[:k]:
            add(v + 51, 1)

        res = [min(get() - 51, 0)]
        for index, v in enumerate(nums[k:]):
            add(v + 51, 1)
            add(nums[index] + 51, -1)
            res.append(min(get() - 51, 0))
        
        return res
''',
    call=f'Solution().getSubarrayBeauty({NUMS}, {K}, {X})',
    expect=[-2, -1],
    skip=['while index <= 101', 'f[index] += delta', 'index += index & -index', 'index = mid', 's = 0',
          'while index > 0', 's += f[index]', 'index -= index & -index', 'res = [0]', 'f = [0] * 102', 'while left < right', 'mid = (left + right) >> 1', 'right = 101', 'left = 1'],
    max_steps=110,
    views=[
        dict(type='text', fn=_bin, size=26, h=90),
        dict(type='array', var='nums', label='nums（框 = 当前窗口）', cell=90, h=190,
             window=(lambda S: _wr(S) - K + 1, _wr)),
        dict(type='array', var='res', label='res（每个窗口的美丽值）', cell=90, h=140, min_slots=2),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'yellow'), ('s', 's', 'orange'), ('v', 'v')],
    captions={
        'for v in nums[:k]': lambda S, B, r: (f'先把第一个窗口的数放进树状数组：`v = {S.v}`' if S.get('v') != B.get('v') else '第一个窗口放好了'),
        'add(v + 51, 1)': lambda S, B, r: (f'`{S.v}` 进入窗口：树状数组下标 `{S.v} + 51 = {S.v + 51}` 处 +1（偏移 51 保证下标 ≥ 1）' if S._line == 28
                                           else f'新数 `{S.v}` 进入窗口，下标 `{S.v + 51}` 处 +1'),
        'add(nums[index] + 51, -1)': '`{nums[index]}` 离开窗口：下标 `{nums[index] + 51}` 处 -1',
        'for index, v in enumerate(nums[k:])': lambda S, B, r: (f'窗口右移：新数 `{S.v}`，要离开的是 `nums[{S.index}] = {S.nums[S.index]}`' if S.get('index') != B.get('index') or 'index' not in B
                                                               else '窗口都滑完了'),
        'res = [min(get() - 51, 0)]': '第一个窗口：`get()` 二分求第 x 小的值（看下面），再 `min(…, 0)`：不是负数就取 `0`',
        'res.append(min(get() - 51, 0))': '`get()` 二分求这个窗口的第 x 小，再 `min(…, 0)` 追加到 `res`',
        'if s >= x': lambda S, B, r: (f'区间 `[{B.left - 51}, {B.right - 51}]` 取中点 `{S.mid - 51}`：`≤ {S.mid - 51}` 的数有 `{S.s}` 个 ≥ x = `{S.x}` → 第 x 小 ==不超过== 它，往左缩' if S.s >= S.x
                                      else f'区间 `[{B.left - 51}, {B.right - 51}]` 取中点 `{S.mid - 51}`：`≤ {S.mid - 51}` 的数只有 `{S.s}` 个 < x = `{S.x}` → 第 x 小==更大==，往右缩'),
        'right = mid': '`right = mid = {mid}`（值 `{mid - 51}` 可能就是答案，所以保留）',
        'left = mid + 1': '`left = mid + 1 = {left}`（值 `{mid - 51}` 太小，排除）',
        'return left': '区间收成一个值：`left = {left}` → 第 x 小 = `{left} - 51 = {left - 51}`，返回给 `min(…, 0)`',
        'return res': '返回 `{ret}`',
    },
    cards=dict(
        one_liner='前缀个数随值单调不降 → 树状数组数个数，二分找第 x 小',
        complexity='时间 `O(n log U)`，空间 `O(U)`（`U = 101`）',
        problem=['定长 `k` 的每个子数组：第 `x` 小的数若是负数，美丽值就是它，否则 `0`',
                 '示例：`nums = [1,-1,-3,-2,3], k = 3, x = 2` → `[-1,-2,-2]`',
                 '本视频：`[-3,-1,-2,2], k = 3, x = 2` → `[-2,-1]`'],
        quote='我在这里选择的是树状数组加二分的处理方法，利用树状数组记录当前窗口内小于等于某个值的数字的个数，那么这个个数随着数值的增大也是==单调递增==的。',
        quote_src='—— yiduobo 题解原文',
        idea=['值 `v` 映射到下标 `v + 51`，树状数组维护「窗口里每个值的个数」',
              '前缀和 = `≤ v` 的个数，随 `v` 增大单调不降 → 二分',
              '找最小的 `v` 使得 `≤ v` 的个数 `≥ x`；窗口滑动只需两次单点修改'],
        summary=['时间 `O(n log U)`（单次二分 × 树状数组查询），空间 `O(U)`',
                 '易错：下标要偏移 `+51`，树状数组下标从 1 开始',
                 '二分条件 `s >= x` 时 `right = mid`（不 -1），否则 `left = mid + 1`',
                 '最后 `min(第 x 小, 0)`：第 x 小不是负数时美丽值为 `0`',
                 '原文已是 Python 3 可运行写法，未改动；视频里树状数组的内部循环被折叠，只展示二分过程',
                 '对比灵神：直接枚举 `-50 ~ -1` 的计数，`O(nU)`，更简单'],
    ),
)
