NUMS = [2, 3, 3, 2, 3]
M = 6


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = len(NUMS)
    cv.text((x0 + 18, y0 + 4), f'nums（m = {M}）：看每一对相邻数的和', 24, T['muted'], bold=True)
    cell = min(110, (x1 - x0 - 40) / n)
    sx = x0 + 20 + ((x1 - x0 - 40) - cell * n) / 2
    top = y0 + 140
    sums = [NUMS[i] + NUMS[i + 1] for i in range(n - 1)]
    first = next((i for i, v in enumerate(sums) if v >= M), None)
    for i, v in enumerate(NUMS):
        X = sx + i * cell
        hit = first is not None and i in (first, first + 1)
        cv.rect((X + 4, top, X + cell - 4, top + cell - 8), fill=T['green'] if hit else T['panel'], outline=T['border'], r=10)
        cv.text((X + cell / 2, top + (cell - 8) / 2), v, 36, T['bg'] if hit else T['text'], anchor='mm', bold=True)
        cv.text((X + cell / 2, top + cell + 4), i, 20, T['dim'], anchor='mt', mono=True)
    for i, v in enumerate(sums):
        X = sx + (i + 1) * cell
        ok = v >= M
        col = T['green'] if ok else T['muted']
        cv.text((X, top - 30), f'{v}', 30, col, anchor='mm', bold=True)
        cv.text((X, top - 62), '≥ m' if ok else '< m', 20, col, anchor='mm')
    msg = (f'第一对和 ≥ m 的是 `{NUMS[first]} + {NUMS[first + 1]} = {sums[first]}`：==它就是「核心」==，其余元素从两端一个一个剥掉'
           if first is not None else '没有任何一对 ≥ m → false')
    cv.rich(x0 + 24, top + cell + 70, msg, x1 - x0 - 48, size=30, color=T['text'], accent=T['yellow'])


CONFIG = dict(
    num=2811, title='判断是否能拆分数组', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='脑筋急转弯 · 相邻两数之和',
    tags=['灵神题单·贪心与思维', '难度分 1543'],
    code='''
class Solution:
    def canSplitArray(self, nums: List[int], m: int) -> bool:
        return len(nums) <= 2 or any(x + y >= m for x, y in pairwise(nums))
''',
    call=f'Solution().canSplitArray({NUMS}, {M})',
    expect=True,
    views=[dict(type='custom', draw=_draw, h=420)],
    watch=[('m', 'm', 'yellow')],
    captions={'return len(nums)': 'n = 5 > 2，所以要看 `any(...)`：相邻对 `(2,3)` 和 5 < 6，`(3,3)` 和 ==6 ≥ 6== → 找到核心，返回 `True`'},
    cards=dict(
        one_liner='n ≥ 3 时，只要有一对相邻数之和 ≥ m，就能像剥洋葱一样拆完',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['把数组不断一分为二，直到拆成 `n` 个长度为 1 的数组',
                 '每次拆出的两个子数组都要「好」：长度为 1，或元素和 `≥ m`',
                 '示例：`nums=[2,3,3,2,3]`，`m=6` → `true`'],
        quote='无论按照何种方式分割，一定会在某个时刻，分割出一个长为 2 的子数组。如果 nums 中任何长为 2 的子数组的元素和都小于 m，那么无法满足要求。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`n ≤ 2` 一刀就拆完，直接满足',
              '`n ≥ 3`：必有一刻出现长为 2 的子数组，它的和必须 `≥ m`',
              '反过来：有这样一对「核心」，就从首尾一个一个剥掉元素',
              '剩下的子数组包含核心，和 `≥ m`，每次都合法',
              '问题变成：有没有相邻两数之和 `≥ m`'],
        after=[dict(heading='剥洋葱演示', lines=['核心 `[3, 3]`（和 6 ≥ m）在下标 1、2', '先剥最左的 `2`：剩 `[3,3,2,3]`，和 11 ≥ m', '再剥最右的 `3`：剩 `[3,3,2]`，和 8 ≥ m', '再剥 `2`：剩 `[3,3]`，和 6 ≥ m；最后一刀拆成 `[3]` `[3]`']),],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：别漏掉 `n ≤ 2` 的特判，此时没有拆分限制',
                 '`pairwise(nums)` 产生相邻对 `(nums[i], nums[i+1])`，`any` 找到第一个满足的就停',
                 '这是一行代码，核心在于证明：数组元素都是正数，剥洋葱时和只增不减'],
    ),
)
