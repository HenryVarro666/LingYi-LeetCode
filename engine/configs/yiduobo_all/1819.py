CONFIG = dict(
    num=1819, title='序列中不同最大公约数的数目', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='筛法式枚举 · 倍数子序列的 gcd',
    tags=['灵神题单·数学算法', '难度分 2540'],
    code='''
class Solution(object):
    def countDifferentSubsequenceGCDs(self, nums):

        num_set = set(nums)
        max_num = max(nums)
        res = 0
        for gcd in range(1, max_num + 1):
            now_gcd = None
            for now in range(gcd, max_num + 1, gcd):
                if now in num_set:
                    if now_gcd is None:
                        now_gcd = now
                    else:
                        x, y = now_gcd, now
                        while x:
                            x, y = y % x, x
                        now_gcd = y
            
            if now_gcd == gcd:
                res += 1

        return res
''',
    call='Solution().countDifferentSubsequenceGCDs([2, 3])',
    expect=3,
    skip=['while x:', 'x, y = y % x, x'],
    views=[
        dict(type='text', h=70, size=30, fn=lambda S: (f"候选 `gcd = {S['gcd']}`：已挑出的倍数的 gcd = `{S.get('now_gcd')}`" if 'gcd' in S and 'now_gcd' in S and S['_line'] >= 10 else '')),
        dict(type='array', var='[1 if k in num_set else 0 for k in range(max_num + 1)]', label='数轴 0..max：1 = 这个数在 nums 中', cell=72, h=260,
             pointers={'gcd': 'blue', 'now': 'pink'},
             color=lambda S, i, v: 'green' if v else None),
    ],
    watch=[('gcd', 'gcd', 'blue'), ('now', 'now', 'pink'), ('now_gcd', 'now_gcd', 'cyan'), ('res', 'res', 'green')],
    captions={
        'num_set = set': '用集合 `num_set` 快速判断某个数在不在 nums 中',
        'max_num = max': '`max_num = {max_num}`：枚举范围 1..max_num',
        'res = 0': '`res` 统计有多少个数能成为某个子序列的最大公约数',
        'for gcd in range': '枚举候选最大公约数 `gcd = {gcd}`',
        'now_gcd = None': '`now_gcd`：把 `gcd` 的倍数里属于 nums 的数拎出来后，它们的最大公约数；还没拎到任何数就是 `None`',
        'for now in range': '按筛法的做法，依次检查 `gcd`、`2gcd`、`3gcd` ... → `now = {now}`',
        'if now in num_set': lambda S, B, ret: (f'`{S.now}` 在 nums 中 → 它是 `{S.gcd}` 的倍数，拎出来' if S.now in S.num_set else f'`{S.now}` 不在 nums 中 → 跳过'),
        'if now_gcd is None': lambda S, B, ret: ('这是拎到的第一个数 → `now_gcd = now`' if S.now_gcd is None else f'已经有 `now_gcd = {S.now_gcd}`，要和 `{S.now}` 再求最大公约数'),
        'now_gcd = now': '`now_gcd = {now_gcd}`',
        'x, y = now_gcd, now': '辗转相除：求 `gcd({now_gcd}, {now})`',
        'now_gcd = y': '辗转相除结束，`now_gcd = {now_gcd}`',
        'if now_gcd == gcd': lambda S, B, ret: (f'`now_gcd = {S.now_gcd} == gcd = {S.gcd}` → ==这些倍数的 gcd 恰好是 {S.gcd}，存在这样的子序列==' if S.now_gcd == S.gcd else f'`now_gcd = {S.now_gcd}` ≠ `gcd = {S.gcd}` → 倍数的 gcd 还是更大，凑不出 {S.gcd}'),
        'res += 1': '`res = {res}`',
        'return res': '一共 `{res}` 个不同的最大公约数',
    },
    cards=dict(
        one_liner='枚举每个数当候选 gcd，拎出它的倍数，看 gcd 能不能凑到它',
        complexity='时间 `O(M log M)`（`M = max(nums)`），空间 `O(n)`',
        problem=['求 `nums` 所有非空子序列的最大公约数中，==不同的值==有几个',
                 '示例：`[2,3]` → `3`（2、3、1）'],
        quote='对于当前枚举到的数gcd，若nums中存在某个序列的最大公约数为gcd，那么这个序列中的数必然都是gcd的倍数。',
        quote_src='—— yiduobo 题解原文',
        idea=['`n` 太大不能两两枚举数对，但 `nums` 的值域可以枚举',
              '像筛法一样检查 `gcd, 2gcd, 3gcd, ...` 是否在 `nums` 中，全部拎出来',
              '拎出来的数的 gcd 恰好等于 `gcd`，就说明存在这样的子序列'],
        summary=['枚举量是 `M/1 + M/2 + ... + M/M`，约 `O(M log M)`',
                 '拎出所有倍数求 gcd：倍数越多 gcd 越小，所以用全部倍数判断就够',
                 '易错点：`now_gcd` 初值 `None`，不能当 0 处理；最后要和 `gcd` 比较',
                 '代码里变量 `gcd` 是候选值，辗转相除是内联写的（`while x`）',
                 '对比灵神：yiduobo 不限制 `i ≤ U/3`，也不提前 `break`'],
    ),
)
