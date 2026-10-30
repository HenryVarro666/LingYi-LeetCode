def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    a = S['nums']
    n = len(a)
    tot = sum(a)
    cv.text((x0 + 20, y0 + 8), f'nums = {a}，总和 S = {tot}（{"偶数" if tot % 2 == 0 else "奇数"}）', 28, T['text'], bold=True)
    cv.text((x0 + 20, y0 + 56), '每个分区：左和 L、右和 S−L、差 = 2L − S', 24, T['muted'])
    rh = 78
    for i in range(n - 1):
        L = sum(a[:i + 1])
        d = L - (tot - L)
        y = y0 + 110 + i * rh
        ok = d % 2 == 0
        col = T['green'] if ok else T['red']
        cv.text((x0 + 30, y), f'i={i}', 26, T['muted'], mono=True)
        cv.text((x0 + 130, y), f'{a[:i+1]} | {a[i+1:]}', 26, T['text'], mono=True)
        cv.text((x0 + 130, y + 36), f'{L} − {tot - L} = {d}', 22, col, mono=True)
        cv.text((x1 - 40, y), '偶' if ok else '奇', 30, col, anchor='rt', bold=True)


CONFIG = dict(
    num=3432, title='统计元素和差值为偶数的分区方案', difficulty='Easy', category='贪心算法',
    author='灵茶山艾府', technique='奇偶性分析 · 一行结论', tags=['灵神题单', '难度分 1200'],
    code='''
class Solution:
    def countPartitions(self, nums: List[int]) -> int:
        return 0 if sum(nums) % 2 else len(nums) - 1
''',
    call='Solution().countPartitions([10,10,3,7,6])',
    expect=4,
    views=[dict(type='custom', draw=_draw, h=520)],
    watch=[('n', 'len(nums)'), ('S', 'sum(nums)'), ('S % 2', 'sum(nums) % 2')],
    captions={
        'return 0 if': '总和 `S = {sum(nums)}`，`S % 2 = {sum(nums) % 2}`：偶数 → 差 `2L − S` 全是偶数，每个分区都行，答案 `n − 1 = {len(nums) - 1}`；奇数则全部不行，答案 0',
    },
    cards=dict(
        one_liner='差 = 2L − S，奇偶只取决于总和 S',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['在 `i` 处把数组切成左右两个非空子数组，求左右两边元素和之差为偶数的切法数',
                 '示例：`[10,10,3,7,6]` → `4`',
                 '`[1,2,2]` → `0`；`[2,4,6,8]` → `3`'],
        quote='题目要求 L − (S−L) = 2L − S 是偶数。由于 2L 一定是偶数，所以只需关注 S 的奇偶性。',
        quote_src='—— 灵茶山艾府题解',
        idea=['设总和 `S`，左边和 `L`，右边就是 `S − L`',
              '`2L` 恒为偶数 → 差的奇偶 = `S` 的奇偶',
              '`S` 偶：==全部 n−1 个分区都满足==；`S` 奇：一个都不满足'],
        before=[dict(heading='先看一个例子', lines=['`[10,10,3,7,6]`，总和 `S = 36`',
                '分区 `[10] | [10,3,7,6]`：`10 − 26 = −16`，偶数',
                '换别的切点，差始终是偶数，和切在哪无关'])],
        after=[dict(heading='总和为奇数的例子', lines=['`[1,2,2]`：总和 `S = 5`，奇数',
                '切 `[1] | [2,2]`：`1 − 4 = −3`，奇数',
                '切 `[1,2] | [2]`：`3 − 2 = 1`，奇数',
                '所以答案是 `0`'])],
        summary=['时间 `O(n)`（求和），空间 `O(1)`',
                 '分区数是 `n − 1`，不是 `n`：左右都要非空',
                 '结论与切点 `i` 无关，所以不用枚举',
                 '同类：奇偶性脑筋急转弯（如 3875、2396）'],
    ),
)
