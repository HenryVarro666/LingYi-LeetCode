NUMS = [2, 3, 4, 2, 5]


def _txt(S):
    if 'v' not in S:
        return '按「最后两个数的奇偶」把子序列分成 4 类，再加上长度为 1 的 odd / even'
    return f'当前 `v = {S["v"]}`（=={"偶" if S["v"] % 2 == 0 else "奇"}数==）：只会更新「以它的奇偶结尾」的那两类'


def _mat(S):
    return [[S['even_even'], S['even_odd']], [S['odd_even'], S['odd_odd']]]


def _hl(S, r, c, v):
    if 'v' not in S or S.get('_line', 0) < 10:
        return None
    if S['v'] % 2 == 0:
        return 'yellow' if c == 0 else None
    return 'yellow' if c == 1 else None


CONFIG = dict(
    num=3686, title='稳定子序列的数量', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='最后两个数的奇偶 · 四类状态',
    tags=['灵神题单', '动态规划', '难度分 1969'],
    code='''
class Solution(object):
    def countStableSubsequences(self, nums):
        
        odd = 0
        even = 0
        odd_odd = 0
        odd_even = 0
        even_odd = 0
        even_even = 0
        mod = 10 ** 9 + 7

        for v in nums:
            if v % 2 == 0:
                even_even = (even_even + even + odd_even) % mod
                odd_even = (odd_even + odd + even_odd + odd_odd) % mod
                even += 1
            else:
                odd_odd = (odd_odd + odd + even_odd) % mod
                even_odd = (even_odd + even + odd_even + even_even) % mod
                odd += 1

        return (len(nums) + odd_odd + odd_even + even_odd + even_even) % mod
''',
    call=f'Solution().countStableSubsequences({NUMS})',
    expect=29,
    max_steps=70,
    views=[
        dict(type='array', var='nums', label='nums', h=160, cell=80),
        dict(type='text', fn=_txt, size=26, h=70),
        dict(type='table', var=_mat, label='长度 ≥ 2 的稳定子序列（行 = 倒数第二个，列 = 最后一个）', h=230, cell=100,
             rows=['偶 …', '奇 …'], cols=['… 偶', '… 奇'], color=_hl),
        dict(type='text', fn=lambda S: f"长度为 1 的：`odd = {S['odd']}`，`even = {S['even']}`", size=24, h=50),
    ],
    watch=[('odd', 'odd', 'orange'), ('even', 'even', 'blue'), ('odd_odd', 'odd_odd', 'orange'),
           ('odd_even', 'odd_even', 'pink'), ('even_odd', 'even_odd', 'cyan'), ('even_even', 'even_even', 'blue')],
    captions={
        4: '`odd`、`even`：长度为 1 的子序列（奇数 / 偶数）个数',
        6: '后四个变量：倒数第二个、最后一个数的奇偶组合各有多少个稳定子序列',
        10: '结果可能很大，取模 `10^9 + 7`',
        12: '依次考虑每个数，新数只影响以它结尾的那些子序列',
        13: '`{v} % 2 = {v % 2}` → {"偶数，只更新 even_even / odd_even" if v % 2 == 0 else "奇数，只更新 odd_odd / even_odd"}',
        14: '`even_even` 只能从「末尾是偶」转移：加 `even + odd_even`；==不能接 even_even，否则三连偶==：`{even_even}`',
        15: '`odd_even` 可接在任何以奇数结尾的后面：`odd + even_odd + odd_odd`：`{odd_even}`（==先更新依赖别人的 even_even==）',
        16: '单个偶数多了一个：`even = {even}`',
        18: '`odd_odd` 只能接在 `odd`、`even_odd` 后面，不能接 `odd_odd` 自己：`{odd_odd}`',
        19: '`even_odd` 可接在任何以偶数结尾的后面：`even + odd_even + even_even`：`{even_odd}`',
        20: '单个奇数多了一个：`odd = {odd}`',
        22: '长度为 1 的共 `len(nums) = {len(nums)}` 个，再加四类长度 ≥ 2 的 → =={ret}==',
    },
    cards=dict(
        one_liner='只看最后两个数的奇偶，就能判断能否再接一个数',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['子序列里不存在连续三个奇偶性相同的元素，称为稳定子序列',
                 '求非空稳定子序列数目，对 `10^9 + 7` 取模',
                 '示例：`[2,3,4,2]` → `14`；本视频：`[2,3,4,2,5]` → `29`'],
        quote='添加新元素时，只需要考虑添加的元素的奇偶性，以及子序列中最后两个元素的奇偶性，就能判断能否将这个元素加入到子序列中。',
        quote_src='—— yiduobo 题解原文（改写自开头的推导）',
        idea=['用 `odd_odd / odd_even / even_odd / even_even` 记「最后两个数」的奇偶',
              '长度为 1 的子序列单独记 `odd` / `even`，因为它们还没有「倒数第二个」',
              '`odd_odd` 不能再接奇数；`even_odd` 本身就不是三连，可接任何偶数结尾的'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：变量迭代要==先更新依赖别人的项==（`odd_odd` / `even_even`），再更新其他项',
                 '最终答案 = `len(nums)`（所有单元素）+ 四类长度 ≥ 2 的',
                 '原文已是 Python 3 可运行的写法，未做修改',
                 '对比灵神：灵神按「末尾连续几个同奇偶」分类，只要 4 个状态且不用单独记长度 1'],
    ),
)
