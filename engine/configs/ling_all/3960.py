CONFIG = dict(
    num=3960, title='频率平衡子数组', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='枚举子数组 · cnt + cc',
    code='''
class Solution:
    def getLength(self, nums: list[int]) -> int:
        n = len(nums)
        # 所有元素互不相同
        if len(set(nums)) == n:
            return 1

        # 子数组只有一种元素
        ans = same = 0
        for i, x in enumerate(nums):
            same += 1
            if i == n - 1 or x != nums[i + 1]:  # 到达连续相同段的末尾
                ans = max(ans, same)
                same = 0

        for i in range(n):
            # 最优性剪枝：答案不会变大
            if n - i <= ans:
                break

            cnt = defaultdict(int)  # 出现次数
            cc = defaultdict(int)  # 出现次数的出现次数

            for j in range(i, n):
                x = nums[j]
                c = cnt[x]
                if c > 0:
                    cc[c] -= 1
                    if cc[c] == 0:
                        del cc[c]  # 保证我们可以正确计算 cc 的大小
                cnt[x] += 1
                cc[cnt[x]] += 1

                if len(cc) == 2:  # 子数组有两种不同的出现次数
                    c1, c2 = sorted(cc)
                    if c1 * 2 == c2:
                        ans = max(ans, j - i + 1)

        return ans
''',
    call='Solution().getLength([4,1,2,2,3,3])',
    expect=6,
    views=[
        dict(type='array', var='nums', label='nums（框 = 子数组 [i, j]）', cell=90, h=240,
             pointers={'i': 'blue', 'j': 'pink'},
             window=(lambda S: S.get('i') if 'cc' in S else None, lambda S: S.get('j') if 'cc' in S else None)),
        dict(type='map', var='cnt', label='cnt（元素 → 出现次数）', fmt=lambda k, v: f'{k}: {v}', h=130, font=32),
        dict(type='map', var='cc', label='cc（出现次数 → 有几种元素）', fmt=lambda k, v: f'{k}: {v}', h=130, font=32),
        dict(type='text', h=90, size=30, fn=lambda S: (f"`cc` 有 {len(S['cc'])} 种出现次数：{sorted(S['cc'])}" if S.get('cc') else '')),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'if len(set(nums)) == n': '`set` 大小 `{len(set(nums))}` ≠ `n = {n}`，有重复元素，继续',
        'ans = same = 0': '`ans` 先用「只含一种元素」的最长连续段做初值，后面不必再处理这种情况',
        'same += 1': '连续相同段长度 `same` → {same}',
        'ans = max(ans, same)': '到达连续相同段末尾：`ans = max({B.ans}, {B.same}) = {ans}`',
        'same = 0': '开始统计下一段',
        'for i in range(n)': '外层枚举左端点 `i = {i}`',
        'if n - i <= ans': lambda S, B, r: (f'`n − i = {S.n - S.i} <= ans = {S.ans}`：以后的子数组再长也超不过 ans → ==剪枝，直接 break==' if S.n - S.i <= S.ans else f'`n − i = {S.n - S.i} > ans = {S.ans}`：还有可能变长，继续'),
        'cnt = defaultdict': '新的左端点，`cnt` 清空',
        'cc = defaultdict': '`cc` 也清空',
        'for j in range': '内层枚举右端点 `j = {j}`，子数组向右扩大一格',
        'x = nums[j]': '新加入的元素 `x = {x}`',
        'c = cnt[x]': 'x 之前出现了 `{c}` 次',
        'if c > 0': lambda S, B, r: (f'`x` 之前出现过 {S.c} 次 → 要先把 cc 里的旧次数减掉' if S.c > 0 else '`x` 是新元素，cc 里没有旧次数要减'),
        'cc[c] -= 1': '出现 {c} 次的元素少了一种 → `cc[{c}]` = {cc[c]}',
        'if cc[c] == 0': lambda S, B, r: (f'`cc[{S.c}] = 0` → 删掉，才能用 `len(cc)` 数种类' if S.cc.get(S.c, 0) == 0 else f'`cc[{S.c}] = {S.cc[S.c]}` ≠ 0，保留'),
        'cnt[x] += 1': '`cnt[{x}]` → =={cnt[x]}==',
        'cc[cnt[x]] += 1': '出现 {cnt[x]} 次的元素多了一种 → `cc[{cnt[x]}]` = {cc[cnt[x]]}',
        'if len(cc) == 2': lambda S, B, r: (f'`len(cc) = {len(S.cc)}`：恰好两种出现次数，还要检查倍数关系' if len(S.cc) == 2 else f'`len(cc) = {len(S.cc)}` ≠ 2，不满足'),
        'c1, c2 = sorted(cc)': '两种出现次数从小到大：`c1 = {c1}`，`c2 = {c2}`',
        'if c1 * 2 == c2': lambda S, B, r: (f'`{S.c1} × 2 == {S.c2}` → ==是 2 倍，频率平衡==' if S.c1 * 2 == S.c2 else f'`{S.c1} × 2 ≠ {S.c2}`，不平衡'),
        'ans = max(ans, j - i + 1)': '子数组长 `{j - i + 1}`：`ans = max({B.ans}, {j - i + 1}) = {ans}`',
        'return ans': '最长频率平衡子数组 `{ans}`',
    },
    skip=['return 1'],
    cards=dict(
        one_liner='枚举子数组，用「出现次数的出现次数」判断是否 f 与 2f',
        complexity='时间 `O(n²)`，空间 `O(n)`',
        problem=['平衡子数组：只含一种元素，或各元素出现次数只有 `f` 和 `2f` 两种',
                 '求最长的平衡子数组长度，`n ≤ 1000`',
                 '本视频：`[4,1,2,2,3,3]` → `6`（次数 1,1,2,2）'],
        quote='子数组恰好有两种不同的出现次数，且这两种出现次数，一个必须是另一个的两倍。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`cnt` 是元素出现次数，`cc` 是「出现次数的出现次数」，像多重集',
              '`len(cc) == 2` 且小的 ×2 == 大的，就是平衡',
              '优化：先用最长连续段当初值，再用 `n − i <= ans` 剪枝'],
        after=[dict(heading='优化前后的区别', lines=['优化前：每次还要判断 `len(cnt) == 1`', '优化后：先扫一遍求最长连续段，并特判全不同返回 1', '再加最优性剪枝，`O(n²)` 不变但常数更小'])],
        summary=['时间 `O(n²)`，空间 `O(n)`',
                 '易错点：`cc[c]` 减到 0 要 `del`，否则 `len(cc)` 会多算',
                 '只含一种元素的情况已被初值 `ans` 覆盖',
                 '题解还给了「优化前」的写法，本视频用的是优化后的版本'],
    ),
)
