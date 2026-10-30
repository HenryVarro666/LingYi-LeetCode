CONFIG = dict(
    num=1103, title='分糖果 II', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='数学公式 · 按列求和',
    code='''
class Solution:
    def distributeCandies(self, candies: int, n: int) -> List[int]:
        m = int((sqrt(8 * candies + 1) - 1) / 2)
        k, extra = divmod(m, n)
        ans = [k * (k - 1) // 2 * n + k * (i + 1) +
               (k * n + i + 1 if i < extra else 0)
               for i in range(n)]
        ans[extra] += candies - m * (m + 1) // 2
        return ans
''',
    setup='from math import sqrt',
    call='Solution().distributeCandies(20, 4)',
    expect=[6, 7, 3, 4],
    max_steps=40,
    views=[
        dict(type='text', size=30, fn=lambda S: (f"能完整发出的次数 `m = {S['m']}`，满足 `1+2+…+m ≤ {S['candies']}`" if 'm' in S else '')),
        dict(type='text', size=30, fn=lambda S: (f"整轮 `k = {S['k']}`，多出 `extra = {S['extra']}` 个人再拿一颗" if 'extra' in S else '')),
        dict(type='array', var='ans', label='ans（每个小朋友的糖果数）', pointers={'extra': 'pink'}, h=260,
             color=lambda S, i, v: 'green' if 'extra' in S and i == S['extra'] else None),
    ],
    watch=['candies', 'n', ('m', 'm', 'blue'), ('k', 'k', 'cyan'), ('extra', 'extra', 'pink')],
    captions={
        'm = int': '`1+2+…+m = m(m+1)/2 ≤ {candies}` 解得 `m = {m}`：前 `m` 次都能发「足够」的糖果',
        'divmod': '`m = {m}` 次分给 `{n}` 人：整整 `k = {k}` 轮，余下 `extra = {extra}` 次',
        'ans = [': lambda S, B, r: f'每列求和：`k(k-1)/2·n + k(i+1)`，前 `extra` 个人再加 `kn+i+1`，得 `{S.ans}`',
        'ans[extra] +=': '最后不够的 `{candies} - {m}×{m+1}/2 = {candies - m * (m + 1) // 2}` 颗，全给第 `extra` 个人 → `{ans}`',
        'return': '返回 `{ret}`，总和刚好 `{candies}`',
    },
    cards=dict(
        one_liner='先算出能发满多少次，再按列用等差数列求和',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`candies` 颗糖，`n` 个小朋友排队，第 `i` 次发 `i` 颗，到队尾回到队首',
                 '剩下的糖不够就全部给当前的人，返回每人糖数',
                 '示例：`candies=10, n=3` → `[5,2,3]`；本视频：`20, 4` → `[6,7,3,4]`'],
        quote='如果第 i 次循环分给小朋友 i 颗糖果，则称作分出了「足够」的糖果。假设最后在第 m 次循环分出了足够的糖果（第 m+1 次循环糖果个数不够）',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['`m(m+1)/2 ≤ candies`，解一元二次不等式得 `m`',
              '`m` 次发了 `k` 整轮，再多 `extra` 次；第 `i` 列是等差数列，直接套公式',
              '最后一次不足的余数，加到 `ans[extra]`'],
        summary=['时间 `O(n)`，空间 `O(1)`；方法一直接模拟，循环 `O(√candies)` 次',
                 '易错点：余数那一份给的是下标 `extra`，不是 `extra-1`',
                 '`i < extra` 的人多拿 `kn+i+1`，`i = extra` 的人拿余数',
                 '数据范围小，两种写法实际速度差不多'],
    ),
)
