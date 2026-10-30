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
    author='yiduobo', technique='奇偶性 · 和与差同奇偶', tags=['灵神题单', '贪心与思维', '难度分 1200'],
    code='''
class Solution(object):
    def countPartitions(self, nums):
        
        if sum(nums) % 2 == 0:
            return len(nums) - 1
        return 0
''',
    call='Solution().countPartitions([4,1,3,6,2])',
    expect=4,
    views=[dict(type='custom', draw=_draw, h=520)],
    watch=[('n', 'len(nums)'), ('S', 'sum(nums)'), ('S % 2', 'sum(nums) % 2')],
    captions={
        'if sum(nums) % 2 == 0': '`sum(nums) = {sum(nums)}`，除以 2 余 `{sum(nums) % 2}`：总和是偶数吗？是 → 任意切点都满足；不是就跳过，最后返回 0',
        'return len(nums) - 1': '总和为偶数，`n − 1 = {len(nums) - 1}` 个切点全部可行，返回 =={ret}==',
        'return 0': '总和为奇数，没有可行的分区，返回 0',
    },
    cards=dict(
        one_liner='x−y 为偶数 ⇔ x+y 为偶数：看总和就够了',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['在下标 `index` 处把 `nums` 分成前后两个子数组，求两边和之差为偶数的分法数',
                 '`index` 取值 `0` 到 `n − 2`',
                 '本视频：`[4,1,3,6,2]` → `4`'],
        quote='对于两个整数x和y而言，若x - y为偶数，那么x + y也必然为偶数。',
        quote_src='—— yiduobo 题解原文',
        idea=['两子数组之差为偶数，等价于两者之和（即 nums 之和）为偶数',
              '反过来，总和 `s` 偶时，差 `2 * x − s` 的奇偶只依赖 `s`',
              '所以 `s` 偶：==任意 index 都行，共 n−1 种==；`s` 奇：答案 0'],
        after=[dict(heading='总和为奇数的情形', lines=['例如 `[1,2,2]`，总和 `s = 5` 是奇数',
                '任何切法：差 `2 * x − 5` 都是奇数',
                '`if` 不成立，直接落到 `return 0`',
                '这时和差都是奇数，没有可行方案'])],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：切点个数是 `n − 1`',
                 '原文为 Python 2 风格，代码无需修改',
                 '对比灵神：灵神直接写 `2L − S` 的奇偶；yiduobo 先用「差与和同奇偶」转换'],
    ),
)
