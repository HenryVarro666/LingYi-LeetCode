_NUMS = [10, 1, 2, 7, 1, 3]


def _pick(S):
    inner = S.get('_inner', {})
    return inner.get('i') if 'cnt' in inner else None


def _state(S):
    if 'left' not in S:
        return ''
    l, r = S['left'], S['right']
    if 'mid' in S and (S.get('_line', 0) <= 12 or S.get('_line') in (16, 17)):
        return f'开区间 `({l}, {r})`，猜答案 `mid = {S["mid"]}`：能选出 ==cnt >= p== 个差值 `<= mid` 的数对吗？'
    return f'开区间 `({l}, {r})`：`left` 一定不行，`right` 一定行'


CONFIG = dict(
    num=2616, title='最小化数对的最大差值', difficulty='Medium', category='二分算法',
    author='灵茶山艾府', technique='二分答案 + 排序后贪心配对',
    tags=['难度分 2155'],
    code='''
class Solution:
    def minimizeMax(self, nums: List[int], p: int) -> int:
        nums.sort()
        def check(mx: int) -> bool:
            cnt = i = 0
            while i < len(nums) - 1:
                if nums[i + 1] - nums[i] <= mx:  # 选 nums[i] 和 nums[i+1]
                    cnt += 1
                    i += 2
                else:  # 不选 nums[i]
                    i += 1
            return cnt >= p

        left, right = -1, nums[-1] - nums[0]
        while left + 1 < right:
            mid = (left + right) // 2
            if check(mid):
                right = mid
            else:
                left = mid
        return right
''',
    call=f'Solution().minimizeMax({_NUMS}, 2)',
    expect=1,
    views=[
        dict(type='text', fn=_state, h=60),
        dict(type='array', var='nums', label='nums（排序后；蓝 = 当前 i，绿 = 刚选的一对，暗 = 已扫过）', cell=84, h=210,
             pointers={'i': 'blue'},
             dim=lambda S, i, v: 'cnt' in S['_inner'] and i < S['_inner']['i'],
             color=lambda S, i, v: 'green' if 'cnt' in S['_inner'] and S['_line'] == 8 and S['_inner']['i'] <= i <= S['_inner']['i'] + 1 else None),
        dict(type='text', fn=lambda S: (f'已选 `cnt = {S["_inner"]["cnt"]}` 对，目标 `p = {S["p"]}`' if 'cnt' in S['_inner'] else ''), h=60),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'yellow'), 'cnt', 'i', ('p', 'p')],
    skip=['cnt = i = 0'],
    captions={
        'nums.sort()': '先排序：配对时==选相邻的数==差最小，例如 `[1,2,3,4]` 选 (1,2)(3,4) 优于 (1,3)(2,4) → `{nums}`',
        'left, right = -1': '开区间二分：`left = -1` 一定不行（差不会是负数），`right = {right}` = 最大值 − 最小值，一定行',
        'while left + 1 < right': lambda S, B, r: (f'`left + 1 = {B.left + 1} < right = {B.right}`：区间里还有没判断的数，继续' if B.left + 1 < B.right
                                                   else f'`left + 1 = {B.left + 1} == right`：区间收拢，答案就是 `right = {B.right}`'),
        'mid = (left + right)': '猜一个最大差值 `mid = ({left} + {right}) // 2 = {mid}`，交给 `check` 判断',
        'while i < len(nums) - 1': lambda S, B, r: (f'`i = {S.i}`：还有 `nums[i+1]` 可以配，继续' if S.i < len(S.nums) - 1
                                                    else f'`i = {S.i}`：没有下一个数了，配对结束'),
        'if nums[i + 1] - nums[i] <= mx': lambda S, B, r: (
            f'`{S.nums[S.i + 1]} − {S.nums[S.i]} = {S.nums[S.i + 1] - S.nums[S.i]} <= {S.mx}` → 能配，==直接选这一对==（贪心：最小的两个数能配就配）'
            if S.nums[S.i + 1] - S.nums[S.i] <= S.mx else
            f'`{S.nums[S.i + 1]} − {S.nums[S.i]} = {S.nums[S.i + 1] - S.nums[S.i]} > {S.mx}` → 配不了，`nums[{S.i}]` 只能放弃'),
        'cnt += 1': '选了一对：`cnt = {cnt}`',
        'i += 2': '两个数都用掉了：`i` 跳到 {i}',
        'i += 1': '不选 `nums[i]`：`i` 右移到 {i}',
        'return cnt >= p': '`cnt = {cnt}`，`p = {p}` → ==`{ret}`==：{"够了，mx 可行" if ret else "不够，mx 太小"}',
        'right = mid': '`check({mid})` 成立 → 答案 `<= {mid}`，==右端点收到 mid==：`right = {right}`',
        'left = mid': '`check({mid})` 不成立 → 答案 `> {mid}`，==左端点移到 mid==：`left = {left}`',
        'return right': '开区间二分：`check` 为真时更新的是 right，最后就返回 right = =={right}==',
    },
    max_steps=110,
    cards=dict(
        one_liner='二分猜最大差值，排序后相邻配对贪心数一数',
        complexity='时间 `O(n log n + n log U)`，空间 `O(1)`',
        problem=['给整数数组 `nums` 和整数 `p`，选 `p` 个不相交的下标对',
                 '让这 `p` 个对的==差值最大值==尽量小，返回这个最小值',
                 '示例：`[10,1,2,7,1,3]`，`p = 2` → `1`'],
        quote='假设数对差值 <= mx。mx 越大，要求就越宽松，越能找到 p 个数对；mx 越小，要求就越苛刻，越不能找到 p 个数对。据此，可以二分猜答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['最小化最大值 → ==二分答案==：mx 越大越容易凑出 p 对',
              '判定时先排序，==能选 nums[0]、nums[1] 就直接选==（灵神用 f(n) = f(n-2)+1 证明）',
              '不能配就跳过 nums[i]，一遍扫描数出最多能配几对'],
        summary=['时间 `O(n log n + n log U)`，U 为最大值减最小值；空间 `O(1)`',
                 '开区间二分：左端点 `-1`，右端点 `nums[-1] - nums[0]`，check 为真就更新 right',
                 '易错：配对后 `i += 2`，不配才 `i += 1`；`p = 0` 时答案是 0',
                 '另一种写法：只在排序后的相邻差值数组里二分，与值域无关，`O(n log n)`',
                 '库函数写法：`bisect_left(range(...), True, key=check)`'],
    ),
)
