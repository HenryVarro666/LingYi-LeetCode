CONFIG = dict(
    num=2598, title='执行操作后的最大 MEX', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='模 m 同余 · 数组计数',
    tags=['灵神题单', '数学算法', '难度分 1846'],
    code='''
class Solution:
    def findSmallestInteger(self, nums: List[int], m: int) -> int:
        cnt = [0] * m
        for x in nums:
            cnt[x % m] += 1

        i = cnt.index(min(cnt))
        return m * cnt[i] + i
''',
    call='Solution().findSmallestInteger([1,-6,-4,3,5,2,7,9], 3)',
    expect=7,
    views=[
        dict(type='array', var='nums', label='nums（m = 3）', h=170),
        dict(type='array', var='cnt', label='cnt[r]：模 m 余 r 的数有几个', h=190,
             pointers={'i': 'pink'},
             color=lambda S, i, v: 'yellow' if 'x' in S and S.get('x') is not None and i == S['x'] % len(S['cnt']) and '_line' in S and S['_line'] == 6 else None),
        dict(type='text', h=100, size=30,
             fn=lambda S: (f"余 `{S['i']}` 的数最少，只有 =={S['cnt'][S['i']]}== 个 → 前 {S['cnt'][S['i']]} 轮都凑得齐" if 'i' in S
                           else '每个数都能变成同余的 0..m−1 中的一个')),
    ],
    watch=['x', ('i', 'i', 'pink')],
    captions={
        'cnt = [0] * m': '`cnt[r]` 统计模 `m = {m}` 余 `r` 的数有多少个（加减 m 不改变余数）',
        'for x in nums': '看下一个数',
        'cnt[x % m] += 1': '`{x} % {m} = {x % m}`{"（负数在 Python 里也得非负余数）" if x < 0 else ""} → `cnt[{x % m}]` = {cnt[x % m]}',
        'i = cnt.index(min(cnt))': '个数最少的余数是 `i = {i}`，只有 `{cnt[i]}` 个；并列时 `index` 取最小的下标',
        'return': '前 `{cnt[i]}` 轮（每轮 `{m}` 个数 0..m−1）都够用，第 `{cnt[i]+1}` 轮缺 `{i}` → MEX = `{m} * {cnt[i]} + {i}` = =={ret}==',
    },
    cards=dict(
        one_liner='加减 m 不改变余数：缺哪个余数，MEX 就卡在哪',
        complexity='时间 `O(n+m)`，空间 `O(m)`',
        problem=['每步可给任一元素加或减 `value`（记为 m），可操作任意次',
                 '求操作后数组的最大 MEX（缺失的最小非负整数）',
                 '示例：`[1,-10,7,13,6,8], m=5` → `4`'],
        quote='由于同一个数可以加减任意倍的 m，我们可以先把每个 nums[i] 变成与 nums[i] 关于模 m 同余的最小非负整数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['要凑出 0,1,2,…：整数 `k` 需要一个余数为 `k % m` 的数',
              '每个余数最多贡献 `cnt[r]` 次，用完就断了',
              '最少的那个余数 `i` 在第 `cnt[i]` 轮之后缺货，答案 `m*cnt[i]+i`'],
        summary=['时间 `O(n+m)`，空间 `O(m)`',
                 '写法一用哈希表 + while 模拟“消耗”，写法二直接数组公式，更快',
                 '易错：负数取模，Python 的 `%` 已是非负；其他语言要 `(x%m+m)%m`',
                 '`cnt.index(min(cnt))` 并列取最小下标，才能得到最小的缺失值'],
    ),
)
