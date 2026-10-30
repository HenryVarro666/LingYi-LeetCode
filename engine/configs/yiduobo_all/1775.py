CONFIG = dict(
    num=1775, title='通过最少操作次数使数组的和相等', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='大和数组减、小和数组加，按幅度贪心', tags=['灵神题单', '贪心与思维', '难度分 1850'],
    code='''
class Solution(object):
    def minOperations(self, nums1, nums2):

        l1 = len(nums1)
        l2 = len(nums2)
        if l1 > l2 * 6 or l2 > l1 * 6:
            return -1
        
        s1 = sum(nums1)
        s2 = sum(nums2)

        if s1 == s2:
            return 0
        
        if s1 > s2:
            ma = nums1
            mi = nums2
        else:
            mi = nums1
            ma = nums2
        
        ma_cnt = {}
        for num in ma:
            ma_cnt[num] = ma_cnt.get(num, 0) + 1
        
        mi_cnt = {}
        for num in mi:
            mi_cnt[num] = mi_cnt.get(num, 0) + 1
        
        diff = abs(s1 - s2)
        res = 0
        for num in range(5):
            cnt = ma_cnt.get(6 - num, 0) + mi_cnt.get(num + 1, 0)
            if cnt * (5 - num) < diff:
                diff -= cnt * (5 - num)
                res += cnt
            else:
                res += diff // (5 - num)
                if diff % (5 - num) != 0:
                    res += 1
                break
        
        return res
''',
    call='Solution().minOperations([3,1], [4,4,5,3])',
    expect=3,
    views=[
        dict(type='array', var=lambda S: S['ma'] if 'ma' in S else S['nums1'], label='和大的数组 ma（大数往下减）', h=140,
             color=lambda S, i, v: 'orange' if 'ma' in S else None),
        dict(type='array', var=lambda S: S['mi'] if 'mi' in S else S['nums2'], label='和小的数组 mi（小数往上加）', h=140,
             color=lambda S, i, v: 'green' if 'mi' in S else None),
        dict(type='map', var=lambda S: S['ma_cnt'] if 'ma_cnt' in S else {}, label='ma_cnt', h=120),
        dict(type='map', var=lambda S: S['mi_cnt'] if 'mi_cnt' in S else {}, label='mi_cnt', h=120),
        dict(type='text', fn=lambda S: (f"还差 `diff` = =={S['diff']}==，已操作 `res` = {S['res']} 次" if 'res' in S and 'diff' in S else '')),
    ],
    skip=['for num in ma', 'for num in mi', 'ma_cnt[num]', 'mi_cnt[num]', 'ma_cnt = {}', 'mi_cnt = {}', 'l1 = len', 'l2 = len', 'res = 0'],
    watch=[('diff', 'diff if "diff" in dir() else None', 'pink'), ('num', 'num if "num" in dir() else None', 'blue'), ('res', 'res if "res" in dir() else None', 'green')],
    captions={
        'if l1 > l2 * 6': '长度 `{l1}`、`{l2}`：一边全 6、另一边全 1 也追不上才无解，这里{"无解" if l1 > l2 * 6 or l2 > l1 * 6 else "有解"}',
        's1 = sum': '`s1 = {s1}`',
        's2 = sum': '`s2 = {s2}`',
        'if s1 == s2': '`s1 = {s1}`，`s2 = {s2}`：{"已经相等，不用操作" if s1 == s2 else "不等，需要操作"}',
        'if s1 > s2': '哪个和更大？`{s1} > {s2}` → {"nums1 是 ma" if s1 > s2 else "nums2 是 ma"}',
        'ma = ': '`ma` 是和大的那个：要把它的大数往下减',
        'mi = ': '`mi` 是和小的那个：要把它的小数往上加',
        'diff = abs': '用两个哈希表统计 ma、mi 里各值的个数：`ma_cnt = {ma_cnt}`，`mi_cnt = {mi_cnt}`；和的差 `diff = {diff}`，要削到 0',
        'cnt = ma_cnt': '这一档幅度 `5 − num = {5 - num}`：`ma` 的 `{6 - num}`（减到 1）和 `mi` 的 `{num + 1}`（加到 6）各算一个，共 `{cnt}` 个',
        'if cnt * (5 - num) < diff': '`{cnt}×{5 - num} = {cnt * (5 - num)}` 与 `diff = {diff}`：{"不够，这一档全用上" if cnt * (5 - num) < diff else "够了，只需要其中一部分"}',
        'diff -= cnt': '全部操作后 `diff` 减少 `{cnt}×{5 - num}`，→ =={diff}==',
        'res += cnt': '这 `{cnt}` 个数都操作，`res` → =={res}==',
        'res += diff //': '剩下 `diff={diff}`，每次最多减 `{5 - num}`：`diff // {5 - num}` = {diff // (5 - num)} 次，`res` → {res}',
        'if diff % (5 - num)': '`diff % {5 - num} = {diff % (5 - num)}`：{"除不尽，还要多一次" if diff % (5 - num) != 0 else "刚好整除"}',
        'res += 1': '多操作一次，`res` → =={res}==',
        'break': '差距已能填平，结束枚举',
        'return res': '最少操作 =={res}== 次',
    },
    cards=dict(
        one_liner='和大的数组往下减，和小的往上加，从最大幅度开始用',
        complexity='时间 `O(n+m)`，空间 `O(1)`',
        problem=['两个数组元素都在 `1~6`，每次可把任意一个数改成 `1~6` 内任意值',
                 '求让两数组和相等的最少操作次数，不可能返回 `-1`',
                 '示例：`[6,6]` 与 `[1]` → `3`'],
        quote='为了使得操作次数最少，那么显然应该从ma中的6和mi中的1开始进行操作，而接下来则是5和2，4和3，以此类推。',
        quote_src='—— yiduobo 题解原文',
        idea=['先判无解：长度 `m` 对 `n`，取值范围 `[m,6m]` 与 `[n,6n]` 要有交集',
              '设 `ma` 为和大的，`mi` 为和小的：==减 ma 里的大数、加 mi 里的小数==',
              '枚举 `num=0..4`：一次操作能缩小 `5-num`，先用幅度大的；够填就算 `diff/(5-num)` 向上取整'],
        summary=['时间 `O(n+m)`，空间 `O(1)`',
                 '易错：剩余差 `diff` 除不尽时要多加一次',
                 '易错：开头先判无解，相等直接返回 0',
                 '对比灵神：灵神把两边变化量合成一个 cnt 数组；yiduobo 分成 ma_cnt / mi_cnt 两个哈希表',
                 '原文为 Python 2 写法，`res += diff / (5 - num)` 的整数除法已改为 `//`'],
    ),
)
