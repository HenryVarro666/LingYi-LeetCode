CONFIG = dict(
    num=3247, title='奇数和子序列的数量', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='奇偶两个状态的 DP（滚动变量）',
    tags=[],
    code='''
class Solution(object):
    def subsequenceCount(self, nums):

        if nums[0] % 2 == 0:
            f, g = 0, 1
        else:
            f, g = 1, 0
        
        mod = 10 ** 9 + 7
        for v in nums[1:]:
            if v % 2 == 0:
                f, g = f + f, g + g + 1
            else:
                f, g = f + g + 1, f + g
        
            f %= mod
            g %= mod

        return f
''',
    call='Solution().subsequenceCount([1, 2, 3, 4, 5])',
    expect=16,
    views=[
        dict(type='text', h=80, fn=lambda S: (
            f"到目前为止：和为奇数的子序列 `f` = =={S['f']}==，和为偶数的子序列 `g` = =={S['g']}==" if 'f' in S and 'g' in S else
            '`f` = 和为奇数的子序列个数，`g` = 和为偶数的子序列个数（非空）')),
        dict(type='array', var='nums', pointers={}, label='nums（当前处理的 v 高亮）', h=200, cell=90,
             color=lambda S, i, v: 'yellow' if 'v' in S and i >= 1 and i == S['nums'].index(S['v']) else None),
        dict(type='text', h=90, fn=lambda S: (
            ('`v` 是偶数：`f = f + f`，`g = g + g + 1`' if S['v'] % 2 == 0 else '`v` 是奇数：`f = f + g + 1`，`g = f + g`') if 'v' in S else '')),
    ],
    watch=[('f', 'f', 'green'), ('g', 'g', 'cyan'), ('v', 'v', 'yellow'), 'mod'],
    captions={
        'if nums[0] % 2 == 0': lambda S, B, r: (f'`nums[0] = {S.nums[0]}` 是偶数 → 单独一个数的子序列和为偶' if S.nums[0] % 2 == 0
                                               else f'`nums[0] = {S.nums[0]}` 是奇数 → 单独一个数的子序列和为奇'),
        'f, g = 0, 1': '偶数：`f = 0`（奇和 0 个），`g = 1`（偶和 1 个）',
        'f, g = 1, 0': '奇数：`f = 1`（奇和 1 个），`g = 0`（偶和 0 个）',
        'mod = ': '答案可能很大，要对 `10^9 + 7` 取模',
        'for v in nums[1:]': '依次考虑后面的数 `v = {v}`：选或不选',
        'if v % 2 == 0': lambda S, B, r: (f'`v = {S.v}` 是偶数：加进任何子序列都不改变奇偶' if S.v % 2 == 0
                                          else f'`v = {S.v}` 是奇数：加进去会让奇偶互换'),
        'f, g = f + f, g + g + 1': '偶数 `v`：`f` = 丢弃 {B.f} + 加入奇和 {B.f} = =={f}==；`g` = {B.g} + {B.g} + 自己单独 1 = =={g}==',
        'f, g = f + g + 1, f + g': '奇数 `v`：`f` = 丢弃 {B.f} + 偶和加入 {B.g} + 自己单独 1 = =={f}==；`g` = 丢弃 {B.g} + 奇和加入 {B.f} = =={g}==',
        'f %= mod': '`f` 取模 → {f}',
        'g %= mod': '`g` 取模 → {g}',
        'return f': '答案是和为奇数的子序列数 `f` = =={f}==',
    },
    max_steps=50,
    cards=dict(
        one_liner='f 记奇数和的个数，g 记偶数和的个数，逐个数转移',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给数组 `nums`，求和为==奇数==的子序列个数，结果对 `10^9 + 7` 取模',
                 '子序列：不改变顺序地删去一些元素，下标不同算不同的子序列',
                 '本视频：`[1,2,3,4,5]` → `16`'],
        quote='令f[index]和g[index]分别表示从下标0到i中和为奇数以及偶数的子序列的数目……注意到这里f和g的每一轮都只和上一轮有关，因此可以使用变量迭代来节省掉数组的空间。',
        quote_src='—— yiduobo 题解原文',
        idea=['新来一个数 `v`：每个旧子序列可以不加它，或者加上它；另外还有「只含 `v`」的子序列',
              '`v` 是偶数：加进去奇偶不变；`v` 是奇数：奇偶互换',
              '所以奇数要写成两种转移，每步只用上一轮的 `f`、`g`，两个变量就够'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：别忘了「只保留 `v` 自己」的那个 `+ 1`；偶数放进 `g`，奇数放进 `f`',
                 '`f, g = f + g + 1, f + g` 是同时赋值，右边用的都是旧值',
                 '原文已是 Python 3 可运行写法，代码未改动'],
    ),
)
