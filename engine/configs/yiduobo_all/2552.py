NUMS = [1, 3, 2, 4, 5]


def _txt(S):
    if 'four' not in S:
        return '`cnt[three]`：以 nums[three] 作 ==3== 的 132 三元组个数；`one`：左边已见的「比 4 小的」个数'
    f = S['four']
    t = S.get('three')
    nums = S['nums']
    if t is None or S.get('_line') not in (10, 11, 12, 13, 15):
        return f"4 = `nums[{f}] = {nums[f]}`，`one = {S.get('one', 0)}`，答案 `res = {S['res']}`"
    rel = '>' if nums[f] > nums[t] else '<'
    return f"4 = `nums[{f}] = {nums[f]}` {rel} 3 = `nums[{t}] = {nums[t]}`；`one = {S['one']}`；`res = {S['res']}`"


CONFIG = dict(
    num=2552, title='统计上升四元组', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='从极值出发 · 枚举 4 再枚举 3',
    tags=['动态规划', '难度分 2433'],
    code='''
class Solution(object):
    def countQuadruplets(self, nums):

        n = len(nums)

        cnt = [0] * n
        res = 0
        for four in range(n):
            one = 0
            for three in range(four):
                if nums[four] > nums[three]:
                    res += cnt[three]
                    one += 1
                else:
                    cnt[three] += one

        return res
''',
    call=f'Solution().countQuadruplets({NUMS})',
    expect=2,
    skip=['for three in range', 'n = len'],
    views=[
        dict(type='array', var='nums', label='nums（粉 = four，蓝 = three）', h=230, cell=90,
             pointers={'four': 'pink', 'three': 'blue'},
             dim=lambda S, i, v: 'four' in S and i > S['four'],
             color=lambda S, i, v: ('green' if 'four' in S and i < S['four'] and i != S.get('three') and v < S['nums'][S['four']] else None)),
        dict(type='array', var='cnt', label='cnt[three]：以 nums[three] 作 3 的 132 个数', h=230, cell=90,
             pointers={'three': 'blue'}, color=lambda S, i, v: 'yellow' if v > 0 else None),
        dict(type='text', h=90, size=28, fn=_txt),
    ],
    watch=[('four', 'four', 'pink'), ('three', 'three', 'blue'), ('one', 'one', 'cyan'), ('res', 'res', 'green')],
    captions={
        'cnt = [0]': '`cnt[three]`：把 `nums[three]` 当作 ==3== 时，已经凑出的 132 三元组个数',
        'res = 0': '`res` 累计 1324 四元组的个数',
        'for four in range': lambda S, B, ret: (f'枚举 4 的下标 `four = {S.four}`（值 {S.nums[S.four]}）' if 'four' not in B or S.four != B.four
                                                else '`four` 枚举完了'),
        'one = 0': '每换一个 4，`one`（4 左边已见的、比 4 小的数）清零',
        'if nums[four] > nums[three]': lambda S, B, ret: (
            f'`nums[{S.four}] = {S.nums[S.four]} > nums[{S.three}] = {S.nums[S.three]}`：3、4 的大小关系对了' if S.nums[S.four] > S.nums[S.three]
            else f'`nums[{S.four}] = {S.nums[S.four]} < nums[{S.three}] = {S.nums[S.three]}`：three 比 four 大：它当 ==3==，four 当 ==2=='),
        'res += cnt[three]': '以它为 3 的 132 有 `cnt[{three}] = {cnt[three]}` 个，配上 4 全是四元组 → `res` = =={res}==',
        'one += 1': '它比 4 小，也是后面某个 3 的「1」候选：`one = {one}`',
        'cnt[three] += one': 'nums[three] > nums[four]：`one` 个更靠前的小数 + 3 + 当前 4 当 2 → 新增 `{one}` 个 132：`cnt[{three}] = {cnt[three]}`',
        'return res': '一共 `{res}` 个',
    },
    max_steps=70,
    cards=dict(
        one_liner='先定 4 的位置，再从左往右一边累加 132、一边累答案',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['`nums` 是 1 到 n 的排列，数 `1324` 形状的四元组：`nums[i] < nums[k] < nums[j] < nums[l]`',
                 '只要求个数，不需要列出来',
                 '本视频：`[1,3,2,4,5]` → `2`'],
        quote='一旦当前的nums[three] > nums[four]，那么由nums[pre_three]，nums[three]，nums[four]这三个位置形成的三元组就是一个132的三元组。',
        quote_src='—— yiduobo 题解原文',
        idea=['「从极值出发」：先枚举最大的 4（`four`），再在它左边枚举 3（`three`）',
              '`nums[four] > nums[three]`：大小关系是 3 < 4，把 `cnt[three]` 个 132 直接记入答案',
              '反过来 `nums[three] > nums[four]`：`four` 当 2，之前比它小的 `one` 个数当 1 → `cnt[three] += one`'],
        summary=['时间 `O(n^2)`，空间 `O(n)`',
                 '`one` 每个 `four` 重新清零，`cnt` 则一直累积',
                 '同一个 three 只在两个分支里二选一：能当 3 配 4，或 4 当 2 补 132',
                 '原文只需删去无关空行，Python 3 直接可运行',
                 '对比灵神：灵神的变量名是 cnt4/cnt3/cnt2，yiduobo 直接用 four/three/one 描述位置'],
    ),
)
