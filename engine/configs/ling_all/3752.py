CONFIG = dict(
    num=3752, title='字典序最小和为目标值且绝对值是排列的数组', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='负数主导 · 从大到小贪心选负',
    tags=['灵神题单·贪心与思维', '难度分 1827'],
    code='''
class Solution:
    def lexSmallestNegatedPerm(self, n: int, target: int) -> List[int]:
        mx = n * (n + 1) // 2
        if abs(target) > mx or (mx - target) % 2:
            return []
        neg_s = (mx - target) // 2  # 取负号的元素（的绝对值）之和

        ans = [0] * n
        l, r = 0, n - 1
        # 从 1,2,...,n 中选一些数，元素和等于 neg_s
        # 为了让负数部分的字典序尽量小，从大往小选
        for x in range(n, 0, -1):
            if neg_s >= x:
                neg_s -= x
                ans[l] = -x
                l += 1
            else:
                # 大的正数填在末尾
                ans[r] = x
                r -= 1
        return ans
''',
    call='Solution().lexSmallestNegatedPerm(5, 1)',
    expect=[-5, -2, 1, 3, 4],
    views=[
        dict(type='text', size=26, fn=lambda S: (
            f"`mx = {S['mx']}`，`neg_s = {S['neg_s']}`（还要从没选的数里凑出的负数绝对值之和）" if 'neg_s' in S else
            (f"`mx = {S['mx']}`" if 'mx' in S else ''))),
        dict(type='array', var='ans', label='ans（蓝 = 负数从左填，粉 = 正数从右填）', cell=96,
             pointers={'l': 'blue', 'r': 'pink'},
             color=lambda S, i, v: 'blue' if v < 0 else ('pink' if v > 0 else None), h=300),
    ],
    watch=['x', 'neg_s', ('l', 'l', 'blue'), ('r', 'r', 'pink')],
    captions={
        'mx = n': '`mx = 1+2+…+n = {mx}`：全取正数时的和（全取负数则是 `-{mx}`）',
        'if abs(target)': lambda S, B, r: (f'`|target| = {abs(S.target)} > {S.mx}` 或奇偶不同 → 无解' if abs(S.target) > S.mx or (S.mx - S.target) % 2
                                           else f'`|target| = {abs(S.target)} ≤ {S.mx}`，且 `mx - target = {S.mx - S.target}` 是偶数 → 有解'),
        'neg_s = (mx': '`pos + neg = mx`，`pos - neg = target` → `neg_s = (mx - target)/2 = {neg_s}`',
        'ans = [0]': '先造一个长 `n` 的数组，负数从左边填，正数从右边填',
        'l, r =': '`l` 指向负数区的下一个位置，`r` 指向正数区的下一个位置',
        'for x in': '从大到小枚举 `x`：越大的数取负，越能让开头更小',
        'if neg_s >= x': lambda S, B, r: (f'`neg_s = {S.neg_s} ≥ x = {S.x}` → ==选 {S.x} 作负数==' if S.neg_s >= S.x
                                          else f'`neg_s = {S.neg_s} < x = {S.x}` → 装不下，{S.x} 只能当正数'),
        'neg_s -= x': '`neg_s` 还要凑 `{neg_s}`',
        'ans[l] = -x': '`-{x}` 放到最左的空位 `ans[{B.l}]`',
        'l += 1': '`l` → {l}',
        'ans[r] = x': '大的正数填在末尾：`ans[{B.r}] = {x}`，这样正数区从小到大',
        'r -= 1': '`r` → {r}',
        'return ans': '`neg_s` 刚好减到 `{neg_s}`，答案 `{ans}`',
    },
    cards=dict(
        one_liner='负数越大越靠前，从大往小贪心凑出负数之和',
        complexity='时间 `O(n)`，空间 `O(1)`（不计返回值）',
        problem=['给正整数 `n` 和整数 `target`，把 `1..n` 排成数组并给部分数加负号',
                 '要求元素和等于 `target`，且字典序最小；无解返回 `[]`',
                 '示例：`n = 3, target = 0` → `[-3,1,2]`；本视频：`n = 5, target = 1`'],
        quote='要让字典序最小，第一个数越小越好。所以负数要填在前面，所以本题是==负数主导==的，应围绕 neg_s 贪心，而不是 pos_s。',
        quote_src='—— 灵茶山艾府题解',
        idea=['设取负的数之和为 `neg_s`，则 `neg_s = (S - target) / 2`，`S - target` 必须是偶数，且 `|target| ≤ S`',
              '第一个数取 `≤ neg_s` 的最大的 `x`，`-x` 就最小；然后 `neg_s -= x`，重复',
              '没选的数不加负号，从小到大排在后面（代码里从 `r` 倒着填）'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '无解条件：`|target| > n(n+1)/2` 或 `n(n+1)/2 - target` 是奇数',
                 '有解时一定能凑出：`1..n` 的子集和覆盖 `[0, S]` 的所有整数，贪心不会卡住',
                 '易错：要围绕负数的和贪心，而不是正数的和'],
    ),
)
