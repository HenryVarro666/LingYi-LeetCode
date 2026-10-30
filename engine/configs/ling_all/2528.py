def _range_txt(S):
    if 'low' in S and 'sum_d' in S:
        return f"猜答案 `low = {S['low']}`：能否用 ≤ `k = {S['k']}` 座新电站让每座城市电量 ≥ `low`？已建 `{S.get('built', 0)}` 座"
    if 'left' in S and 'right' in S and 'power' in S:
        return f"二分（开区间）：`left = {S['left']}` 满足，`right = {S['right']}` 不满足"
    return '先算每座城市的初始电量 `power`'


CONFIG = dict(
    num=2528, title='最大化城市的最小电量', difficulty='Hard', category='二分算法',
    author='灵茶山艾府', technique='二分答案 + 差分 + 从左往右贪心',
    tags=['二分算法', '常用数据结构', '难度分 2236'],
    code='''
class Solution:
    def maxPower(self, stations: List[int], r: int, k: int) -> int:
        n = len(stations)
        # 前缀和
        s = list(accumulate(stations, initial=0))
        # 初始电量
        power = [s[min(i + r + 1, n)] - s[max(i - r, 0)] for i in range(n)]

        def check(low: int) -> bool:
            diff = [0] * n  # 差分数组
            sum_d = built = 0
            for i, p in enumerate(power):
                sum_d += diff[i]  # 累加差分值
                m = low - (p + sum_d)
                if m <= 0:
                    continue
                # 需要在 i+r 额外建造 m 个供电站
                built += m
                if built > k:  # 不满足要求
                    return False
                # 把区间 [i, i+2r] 增加 m
                sum_d += m  # 由于 diff[i] 后面不会再访问，我们直接加到 sum_d 中
                if (right := i + r * 2 + 1) < n:
                    diff[right] -= m
            return True

        # 开区间二分
        mn = min(power)
        left, right = mn + k // n, mn + k + 1
        while left + 1 < right:
            mid = (left + right) // 2
            if check(mid):
                left = mid
            else:
                right = mid
        return left
''',
    call='Solution().maxPower([1,2,4,5,0], 1, 3)',
    expect=5,
    max_steps=68,
    views=[
        dict(type='text', fn=_range_txt, size=26, h=60),
        dict(type='array', var='stations', label='stations（原始电站数）', h=130),
        dict(type='array', var='power', label='power（初始电量）', h=150,
             pointers={'i': 'blue'},
             color=lambda S, i, v: ('yellow' if 'low' in S and 'sum_d' in S and S.get('i') == i and S['low'] > v + S['sum_d'] else None)),
        dict(type='array', var='diff', label='diff（差分：到这里失效的电量）', h=150, pointers={'i': 'blue'}),
    ],
    watch=['low', 'i', 'p', 'sum_d', 'm', 'built', 'k', 'left', 'right', 'mid'],
    captions={
        's = list(accumulate': '前缀和 `s = {s}`，区间和 O(1)',
        'power = [': '城市 i 被 `[i-r, i+r]` 的电站覆盖：初始电量 `power = {power}`',
        'diff = [0] * n': '新一轮判定：差分数组清零',
        'sum_d += diff[i]': '累加差分，`sum_d = {sum_d}` = 前面新建电站对城市 `{i}` 的贡献',
        'm = low - (p + sum_d)': '城市 `{i}` 实际电量 `{p} + {sum_d}`，目标 `{low}` → 还缺 `m = {m}`',
        'if m <= 0': lambda S, B, ret: ('不缺电，跳过' if S.m <= 0 else f'缺 `{S.m}`，必须补'),
        'built += m': '在 `i+r = {i + r}` 处建 `{m}` 座（越靠右越能覆盖后面的城市），累计 `built = {built}`',
        'if built > k': lambda S, B, ret: (f'`built = {S.built} > k = {S.k}`：额外电站不够 → ==low 不可行==' if S.built > S.k else f'`built = {S.built} ≤ k = {S.k}`，还够用'),
        'return False': '这个 `low` 做不到 → 返回 False',
        'sum_d += m': '电站覆盖 `[i, i+2r]`，当前城市立刻 +{m}，`sum_d = {sum_d}`',
        'diff[right] -= m': '`right = {i + 2*r + 1}` 处这批电站失效：`diff[{i + 2*r + 1}] -= {m}`',
        'return True': '每座城市都 ≥ `low` 且 `built ≤ k` → 返回 True',
        'mn = min': '最小初始电量 `mn = {mn}`',
        'left, right': '`left = mn + k//n = {left}`（均摊必满足），`right = mn + k + 1 = {right}`（必不满足）',
        'while left + 1 < right': lambda S, B, ret: (f'区间 `({S.left}, {S.right})` 里还有候选，继续' if S.left + 1 < S.right else f'`left + 1 = right`，收敛，答案 `{S.left}`'),
        'mid = (left + right)': '猜 `mid = {mid}`',
        'if check(mid)': '调用 `check({mid})`：能否让每座城市电量都 ≥ {mid}？',
        'left = mid': '`{mid}` 可行 → 答案 ≥ mid：`left = {left}`',
        'right = mid': '`{mid}` 不可行 → 答案 < mid：`right = {right}`',
        'return left': '`left` 就是最大的可行 low：`{left}`',
    },
    cards=dict(
        one_liner='二分猜最小电量，从左到右贪心补电站，差分维护覆盖',
        complexity='时间 `O(n log k)`，空间 `O(n)`',
        problem=['`stations[i]` 是城市 i 的电站数，每座电站给距离 ≤ `r` 的城市供电',
                 '再建 `k` 座电站，让==电量最小的城市==电量尽量大',
                 '示例：`[1,2,4,5,0], r=1, k=2` → `5`','本视频取 `k = 3`，答案同为 `5`'],
        quote='我们需要在二分之前，用 stations 计算每个城市的初始电量 power。……建造的电站越靠右越好，尽可能多地覆盖没遍历到的城市。',
        quote_src='—— 灵茶山艾府题解',
        idea=['电量要求越松越容易满足 → ==二分猜 low==',
              '判定：从左往右，缺多少补多少，电站建在 `i+r`，覆盖 `[i, i+2r]`',
              '「区间 +m」用差分数组，边做边累加前缀和'],
        summary=['时间 `O(n log k)`，空间 `O(n)`',
                 '开区间二分：左端 `mn + k//n` 必可行，右端 `mn + k + 1` 必不可行',
                 '易错：差分下标 `i + 2r + 1` 要判断是否越界',
                 '本视频用写法一（前缀和）；写法二用滑动窗口求 power，库函数写法用 bisect_left',
                 '同类：差分 + 贪心的「最小操作次数」题'],
    ),
)
