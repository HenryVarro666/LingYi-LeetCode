NUMS = [1, 2, 0, 4, 3, 5]


def _goal(S):
    t = S.get('target')
    if not t or len(t) < len(NUMS):
        return '目标：0 在最前（`0 1 2 … n−1`）或 0 在最后（`1 2 … n−1 0`），两种都要算，取小的'
    fin = [0] * len(t)
    for v, pos in t.items():
        fin[pos] = v
    name = '方案 A：0 在最前' if t[0] == 0 else '方案 B：0 在最后'
    return f'=={name}==，目标排列 `{fin}`'


def _info(S):
    if 'cnt' not in S:
        return ''
    z = '已用过 0 所在的环' if S.get('zero_flag') else '还没遇到 0 所在的环'
    return f'本方案已累计 `cnt = {S["cnt"]}`，{z}'


def _color(S, i, v):
    vis = S.get('vis')
    if vis is None or 'target' not in S:
        return None
    if i in vis:
        return 'orange' if v == 0 else 'green'
    return None


CONFIG = dict(
    num=2459, title='通过移动项目到空白区域来排序数组', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='置换环计数 · 0 在最前 / 最后两种目标',
    tags=['数组'],
    code='''
class Solution(object):
    def sortArray(self, nums):

        n = len(nums)

        def check():
            vis = set()
            cnt = 0
            zero_flag = False

            for index in range(n):
                if index not in vis and target[nums[index]] != index:
                    vis.add(index)
                    cnt += 1
                    p = target[nums[index]]
                    while p not in vis:
                        vis.add(p)
                        p = target[nums[p]]
                        cnt += 1

                    if not zero_flag and target[0] in vis:
                        cnt -= 1
                        zero_flag = True
                    else:
                        cnt += 1

            return cnt

        target = {}
        for index in range(n):
            target[index] = index
        res = check()

        for index in range(1, n):
            target[index] = index - 1
        target[0] = n - 1
        res = min(res, check())

        return res
''',
    call=f'Solution().sortArray({NUMS})',
    expect=2,
    views=[
        dict(type='text', fn=_goal, size=26, h=70),
        dict(type='array', var='nums', label='nums（绿 = 已走过的错位位置，橙 = 空白 0 所在的位置）', cell=90, h=190,
             pointers={'index': 'blue', 'p': 'pink'}, color=_color),
        dict(type='map', var='target', label='target：数值 → 它应该去的位置', fmt=lambda k, v: f'{k}→{v}', h=130, font=28),
        dict(type='text', fn=_info, size=28, h=60),
    ],
    watch=[('index', 'index', 'blue'), ('p', 'p', 'pink'), ('cnt', 'cnt', 'green'), ('zero_flag', 'zero_flag', 'orange'), ('res', 'res', 'cyan')],
    skip=['n = len', 'vis = set()', 'def check', 'zero_flag = False', 'target = {}', 30, 31, 34, 35, 'vis.add('],
    captions={
        'cnt = 0': '`cnt` 统计这种目标下需要的移动次数',
        'for index in range(n)': lambda S, B, r: ('所有位置都看完了，这个方案算完' if 'index' in B and B.index == S.index else f'看位置 `{S.index}`：现在放着 `{S.nums[S.index]}`，它应该去 `{S.target[S.nums[S.index]]}`'
                                                  ),
        'if index not in vis and target': lambda S, B, r: (
            f'位置 `{S.index}` 已在某个环里，跳过' if S.index in S.vis
            else f'`{S.nums[S.index]}` 已经在正确位置，不用动' if S.target[S.nums[S.index]] == S.index
            else f'`{S.nums[S.index]}` 站错了位置，且没处理过 → 顺着「占位」关系走出一个环'),
        'cnt += 1': lambda S, B, r: f'环里多了一个位置：`cnt = {S.cnt}`' if S._line != 25 else f'环里不含 0 → 要多花 2 次（先和 0 换一次，最后换回来）：`cnt = {S.cnt}`（= k + 1）',
        'p = target[nums[index]]': '`p` = 起点那个数应该去的位置，也就是下一个被占的位置',
        'while p not in vis': lambda S, B, r: (f'`p = {S.p}` 还没走过 → 继续沿环走' if S.p not in S.vis else f'`p = {S.p}` 已走过 → 环闭合了'),
        'p = target[nums[p]]': lambda S, B, r: f'`p` 跳到下一个被占的位置 `{S.p}`',
        'if not zero_flag and target[0] in vis': lambda S, B, r: (
            f'这个环包含 0 的目标位置 `{S.target[0]}` → 有空位，不用额外代价（长度 k 的环只要 k − 1 次）'
            if (not S.zero_flag) and S.target[0] in S.vis else '不含 0 的环，或 0 的环已经算过'),
        'cnt -= 1': '含 0 的环：k 个位置只需 `k − 1` 次交换，扣掉 1：`cnt = {cnt}`',
        'zero_flag = True': '0 所在的环只扣一次，用 `zero_flag` 记下',
        'return cnt': '这个目标下共需要 `{cnt}` 次移动',
        'res = check()': '先算方案 A：目标是 0 在最前',
        'target[0] = n - 1': '换成方案 B：每个数 `v` 的目标位置改为 `v − 1`，0 的目标位置改为最后一位 `n − 1`',
        'res = min(res, check())': '方案 A 需要 `{res}` 次；再算方案 B（0 在最后），最后取较小的',
        'return res': '最少移动次数 `{res}`',
    },
    max_steps=100,
    cards=dict(
        one_liner='按置换环数交换次数：含 0 的环 k − 1，不含 0 的环 k + 1',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`nums` 是 `0 … n−1` 的排列，`0` 表示空白区域',
                 '每次操作==只能把某个数移到空白处==（和 0 交换）',
                 '要排成 `0,1,…,n−1`，或 `1,…,n−1,0`，求最少操作次数',
                 '本视频：`[1,2,0,4,3,5]` → `2`'],
        quote='对于一个长度为k的环，若其包含空白区域，那么其交换次数不变，依然是k - 1；若其不包含空白区域，就需要先进行一次额外操作，将环中某个数与空白区域交换……因此其所需的交换次数就是k + 1。',
        quote_src='—— yiduobo 题解原文',
        idea=['先忽略「只能和 0 换」：没在正确位置的数，占位关系会连成环，长度 `k` 的环要 `k − 1` 次交换',
              '现在只能和 0 换：==环里有 0 就照常 `k − 1`==；没有 0 就多出 2 次，共 `k + 1`',
              '合法排列有两种（0 在最前 / 最后），目标位置 `target` 不同，各算一遍取最小'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：两种目标要分别算，不能只算一种',
                 '错位环的长度含 0 的位置时，只能抵消一次（`zero_flag`），0 只在一个环里',
                 '已经在正确位置的数组成长度 1 的环，不要计入',
                 '原文已是 Python 3 可运行的写法，未做修改'],
    ),
)
