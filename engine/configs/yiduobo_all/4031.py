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
    if 'res' not in S or 'p' not in S:
        return None
    p, nums, lo, hi = S['p'], S['nums'], S['lower'], S['upper']
    if p >= len(nums):
        return None
    if S['_line'] in (L_FIRST, L_FIRST + 1):
        return (lo, nums[p] - 1)
    if S['_line'] >= L_LAST:
        return (nums[p] + 1, hi)
    if p + 1 < len(nums):
        return (nums[p] + 1, min(nums[p + 1] - 1, hi))
    return None


L_FIRST = 16
L_LAST = 24


CONFIG = dict(
    num=4031, title='找到所有数组中消失的数字 II', difficulty='Medium', category='模拟',
    author='yiduobo', technique='排序 + 单指针扫描空档', tags=[],
    code='''
class Solution(object):
    def findDisappearedNumbers(self, nums, lower, upper):
        
        nums.sort()
        p = 0
        while p < len(nums) and nums[p] < lower:
            p += 1
        
        if p == len(nums):
            return [[lower, upper]]
        
        if nums[p] > upper:
            return [[lower, upper]]
        
        res = []
        if lower < nums[p]:
            res.append([lower, nums[p] - 1])
        
        while p + 1 < len(nums) and nums[p + 1] <= upper:
            if nums[p + 1] - nums[p] > 1:
                res.append([nums[p] + 1, nums[p + 1] - 1])
            p += 1
        
        if nums[p] < upper:
            res.append([nums[p] + 1, upper])
        
        return res
''',
    call='Solution().findDisappearedNumbers([7, 3, 9, 3, 15], 2, 12)',
    expect=[[2, 2], [4, 6], [8, 8], [10, 12]],
    views=[
        dict(type='array', var='nums', pointers={'p': 'yellow'}, h=190, label='nums（排序后）', cell=80,
             dim=lambda S, i, v: v < S['lower'] or v > S['upper']),
        dict(type='custom', draw=_make_draw(_gap), h=400),
    ],
    watch=[('p', 'p', 'yellow'), ('res', 'res', 'green')],
    captions={
        'nums.sort()': '先排序：`{nums}`，空档只可能出现在相邻两数之间',
        'p = 0': '`p` 是扫描指针',
        'while p < len(nums) and nums[p] < lower': lambda S, B, r: (f'`nums[{S.p}] = {S.nums[S.p]} < lower = {S.lower}`：还在 lower 左边 → 继续往右' if S.p < len(S.nums) and S.nums[S.p] < S.lower else f'`p = {S.p}` 已经找到第一个 `>= lower` 的位置，或者走到头'),
        'p += 1': '跳过小于 lower 的数：`p` → {p}',
        'if p == len(nums)': '`p = {p}`，`len = {len(nums)}`：{"==所有数都小于 lower，整段都缺失==" if p == len(nums) else "还有数落在 lower 右边"}',
        'if nums[p] > upper': '`nums[{p}] = {nums[p]}`，`upper = {upper}`：{"==最小的可用数已经超过 upper，整段都缺失==" if nums[p] > upper else "nums[p] 在区间内，继续切分"}',
        'res = []': '开始收集缺失区间',
        'if lower < nums[p]': '`lower = {lower}`，`nums[p] = {nums[p]}`：{"lower 到 nums[p]-1 都没出现" if lower < nums[p] else "lower 恰好就是 nums[p]，开头没有空档（长度要 > 0）"}',
        'res.append([lower': '开头的缺失 `[{lower}, {nums[p]}-1] = {res[-1]}`',
        'while p + 1 < len(nums)': lambda S, B, r: (f'看 `nums[{S.p+1}] = {S.nums[S.p+1]}` 有没有越过 upper = {S.upper}：没越过 → 继续切' if S.p + 1 < len(S.nums) and S.nums[S.p + 1] <= S.upper else '右边没有数，或者已经越过 upper → 停止切分'),
        'if nums[p + 1] - nums[p] > 1': '`{nums[p+1]} - {nums[p]} = {nums[p+1]-nums[p]}` {">" if nums[p+1]-nums[p]>1 else "≤"} 1 → {"==中间有空档==" if nums[p+1]-nums[p]>1 else "没有空档（重复或相邻）"}',
        'res.append([nums[p] + 1': '空档 `[{nums[p]}+1, {nums[p+1]}-1] = {res[-1]}`',
        'p += 1': '`p` 右移到 {p}',
        'if nums[p] < upper': '`nums[p] = {nums[p]}`，`upper = {upper}`：{"最后一个数还没到 upper，后面还有缺失" if nums[p] < upper else "已经到 upper，结尾没有空档"}',
        'res.append([nums[p] + 1, upper': '结尾的缺失 `[{nums[p]}+1, {upper}] = {res[-1]}`',
        'return res': '按下标顺序生成的区间天然有序，返回 `{res}`',
    },
    cards=dict(
        one_liner='排序后用一根指针扫，每个相邻空档切出一段缺失区间',
        complexity='时间 `O(n log n)`，空间 `O(1)`（不计答案）',
        problem=['给 `nums` 和 `[lower, upper]`，找出区间内没出现在 `nums` 的整数',
                 '连续缺失整数合并成 `[start, end]`，按递增返回，没有则返回空数组',
                 '本视频：`nums=[7,3,9,3,15]`，`[2,12]` → `[[2,2],[4,6],[8,8],[10,12]]`'],
        quote='nums中的某些元素将对[lower, upper]进行若干次的切分。',
        quote_src='—— yiduobo 题解原文',
        idea=['先处理特殊情况：整个 `nums` 都在区间一侧时，直接返回 `[[lower, upper]]`',
              '排序后找到第一个 `nums[p] >= lower`，开头 `lower..nums[p]-1` 是缺失',
              '每次比较 `nums[p]` 和 `nums[p+1]`，越过 upper 就停；最后补 `nums[p]+1..upper`'],
        summary=['时间 `O(n log n)`，空间 `O(1)`（不计答案）',
                 '每一段都要检查长度 `> 0` 才能加入答案',
                 '三种情况：开头空档、中间空档、结尾空档，别漏掉头尾',
                 '对比灵神：灵神加哨兵统一处理头尾；yiduobo 分开特判头尾'],
    ),
)
