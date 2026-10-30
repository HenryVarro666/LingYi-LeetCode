def _make_draw(gap_fn):
    def draw(cv, S, B, box, T):
        x0, y0, x1, y1 = box
        lo, hi = S['lower'], S['upper']
        n = hi - lo + 1
        cv.text((x0 + 18, y0 + 4), f'数轴 [{lo}, {hi}]：红 = nums 里出现，黄 = 正在看的空档，绿 = 已加入答案', 22, T['muted'], bold=True)
        cell = min(78, (x1 - x0 - 40) / n)
        sx = x0 + 20 + ((x1 - x0 - 40) - cell * n) / 2
        top = y0 + 110
        present = set(S['nums'])
        ans = S.get('ans', S.get('res')) or []
        ing = {v for a, b in ans for v in range(a, b + 1)}
        gap = gap_fn(S)
        gset = set(range(gap[0], gap[1] + 1)) if gap and gap[0] <= gap[1] else set()
        for k in range(n):
            v = lo + k
            X = sx + k * cell
            if v in ing:
                fill, tc = T['green'], T['bg']
            elif v in gset:
                fill, tc = T['yellow'], T['bg']
            elif v in present:
                fill, tc = T['red'], T['bg']
            else:
                fill, tc = T['panel2'], T['muted']
            cv.rect((X + 2, top, X + cell - 2, top + cell - 6), fill=fill, r=6)
            cv.text((X + cell / 2, top + (cell - 6) / 2), v, 24, tc, anchor='mm', bold=True)
        y = top + cell + 40
        cv.text((x0 + 18, y), '答案区间：' + (' '.join(f'[{a},{b}]' for a, b in ans) if ans else '（空）'), 26, T['green'], bold=True)
    return draw


def _gap(S):
    if 'i' in S and 'nums' in S and 0 < S['i'] < len(S['nums']):
        return (max(S['nums'][S['i'] - 1] + 1, S['lower']), min(S['nums'][S['i']] - 1, S['upper']))
    return None


CONFIG = dict(
    num=4031, title='找到所有数组中消失的数字 II', difficulty='Medium', category='模拟',
    author='灵茶山艾府', technique='哨兵 + 排序 + 二分找起止', tags=[],
    code='''
class Solution:
    def findDisappearedNumbers(self, nums: list[int], lower: int, upper: int) -> list[list[int]]:
        nums += [lower - 1, upper + 1]
        nums.sort()

        l = bisect_right(nums, lower)
        r = bisect_left(nums, upper)

        ans = []
        for i in range(l, r + 1):
            if nums[i] - nums[i - 1] > 1:
                ans.append([nums[i - 1] + 1, nums[i] - 1])
        return ans
''',
    call='Solution().findDisappearedNumbers([3, 9, 7], 1, 12)',
    expect=[[1, 2], [4, 6], [8, 8], [10, 12]],
    views=[
        dict(type='array', var='nums', pointers={'l': 'cyan', 'r': 'orange', 'i': 'yellow'}, h=190, label='nums（加哨兵、排序后）', cell=80),
        dict(type='custom', draw=_make_draw(_gap), h=400),
    ],
    watch=[('l', 'l', 'cyan'), ('r', 'r', 'orange'), 'i', ('ans', 'ans', 'green')],
    captions={
        'nums += ': '加两个哨兵：`lower-1 = {lower-1}` 在最左，`upper+1 = {upper+1}` 在最右，边界的空档就和中间的统一了',
        'nums.sort()': '排序后相邻两数之间的空档就是缺失的整数：`{nums}`',
        'l = bisect_right': '`l = bisect_right(nums, {lower}) = {l}`：第一个 ==大于 lower== 的数的下标，`nums[l-1]` 是 lower 左边的最后一个',
        'r = bisect_left': '`r = bisect_left(nums, {upper}) = {r}`：第一个 ==大于等于 upper== 的数的下标，空档到它为止',
        'ans = []': '开始收集缺失区间',
        'for i in range': lambda S, B, r: ('遍历完 `i` 到 `r` 的所有相邻对，退出循环' if B.get('i') == S.i else f'`i = {S.i}`：看 `nums[{S.i-1}] = {S.nums[S.i-1]}` 和 `nums[{S.i}] = {S.nums[S.i]}` 之间的空档'),
        'if nums[i] - nums[i - 1] > 1': '`{nums[i]} - {nums[i-1]} = {nums[i]-nums[i-1]}` {">" if nums[i]-nums[i-1]>1 else "≤"} 1 → {"==中间有缺失整数==" if nums[i]-nums[i-1]>1 else "紧挨着，没有空档"}',
        'ans.append': '缺失区间 `[{nums[i-1]}+1, {nums[i]}-1] = {ans[-1]}`，加入答案',
        'return ans': '空档都收集完，返回 `{ans}`',
    },
    cards=dict(
        one_liner='排序后，相邻两数的空档就是缺失区间',
        complexity='时间 `O(n log n)`，空间 `O(1)` 或 `O(n)`',
        problem=['给 `nums` 和区间 `[lower, upper]`，找出区间内没出现在 `nums` 的整数',
                 '连续的缺失整数合并成一个区间 `[start, end]`，按递增返回',
                 '示例：`nums=[3,9,7], [1,12]` → `[[1,2],[4,6],[8,8],[10,12]]`'],
        quote='如果发现 nums[i] - nums[i-1] > 1，那么 [nums[i-1]+1, nums[i]-1] 是一段缺失的整数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['排序后，相邻两数 `a < b` 之间的整数 `a+1 .. b-1` 都没出现',
              '把 `lower-1` 和 `upper+1` 当哨兵放进去，头尾的空档就不用特判',
              '二分找出只和 `[lower, upper]` 有关的起止位置，再遍历相邻对'],
        summary=['时间 `O(n log n)`，瓶颈在排序；空间 `O(1)` 或 `O(n)`',
                 '`bisect_right(nums, lower)`：保证 `nums[l-1] <= lower`，空档从 lower 开始',
                 '`bisect_left(nums, upper)`：保证 `nums[r] >= upper`，空档到 upper 结束',
                 '重复元素差为 0，不会被当作空档；`nums += ...` 会改动传入数组'],
    ),
)
