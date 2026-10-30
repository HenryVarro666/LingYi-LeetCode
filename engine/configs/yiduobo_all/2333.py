CONFIG = dict(
    num=2333, title='最小差值平方和', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='差值排序，逐层削平', tags=['灵神题单', '贪心与思维', '难度分 2011'],
    code='''
class Solution(object):
    def minSumSquareDiff(self, nums1, nums2, k1, k2):

        k = k1 + k2
        n = len(nums1)
        diff = sorted([abs(nums1[index] - nums2[index]) for index in range(n)], reverse=True)

        p = n - 1
        for index in range(n - 1):
            if (index + 1) * (diff[index] - diff[index + 1]) <= k:
                k -= (index + 1) * (diff[index] - diff[index + 1])
            else:
                p = index
                break

        if p == n - 1 and k >= diff[-1] * n:
            return 0

        delta = k // (p + 1)
        k %= (p + 1)
        res = 0

        for index in range(k):
            res += (diff[p] - delta - 1) ** 2
        for index in range(k, p + 1):
            res += (diff[p] - delta) ** 2
        for index in range(p + 1, n):
            res += diff[index] ** 2
        
        return res
''',
    call='Solution().minSumSquareDiff([11,1,10,5,2], [1,10,3,1,1], 4, 3)',
    expect=138,
    views=[
        dict(type='bars', var=lambda S: S['diff'] if 'diff' in S else [], label='diff[i] = |nums1[i] − nums2[i]|（从大到小）', h=400,
             pointers={'index': 'blue'},
             color=lambda S, i, v: 'pink' if 'p' in S and i <= S['p'] and 'delta' in S else None),
        dict(type='text', fn=lambda S: (f"剩余操作 `k` = =={S['k']}==" + (f"；前 `{S['p']+1}` 个各减 `{S['delta']}`" if 'delta' in S else '')), size=30),
    ],
    watch=['k', ('p', 'p if "p" in dir() else None', 'pink'), ('index', 'index if "index" in dir() else None', 'blue'), ('res', 'res if "res" in dir() else None', 'green')],
    captions={
        'k = k1 + k2': '`nums1[i] + 1` 等价于 `nums2[i] − 1`：操作次数合并，`k = {k}`',
        'n = len': '`n = {n}`',
        'diff = sorted': '`diff` 取绝对值并从大到小排：`{diff}`；问题变成「diff 至多减 k 次」',
        'p = n - 1': '`p` 记录「最终被削平的前缀」的末尾，默认是最后一个',
        'if (index + 1) *': '把前 `{index + 1}` 个削到 `{diff[index + 1]}` 需要 `{index + 1}×({diff[index]}−{diff[index + 1]}) = {(index + 1) * (diff[index] - diff[index + 1])}`，`k = {k}`：{"够，整体削平" if (index + 1) * (diff[index] - diff[index + 1]) <= k else "不够，到此为止"}',
        'k -= (index + 1)': '用掉这些操作，`k` → =={k}==',
        'p = index': '`p = {p}`：前 `{p + 1}` 个数能一起削平，剩下的 `k` 平分给它们',
        'if p == n - 1 and': '`p` 在末尾时，还要看能否全削成 0：`k = {k}` 对 `diff[-1]×n = {diff[-1] * n}` → {"能，返回 0" if p == n - 1 and k >= diff[-1] * n else "不能"}',
        'delta = k //': '剩下 `k={k}` 平分给 `{p + 1}` 个数：每个再减 `delta = {delta}`',
        'k %= (p + 1)': '余数 `k = {k}`：这 `{k}` 个数再多减 1',
        'res += (diff[p] - delta - 1)': '多减 1 的数：`({diff[p]}−{delta}−1)^2`，`res` → {res}',
        'res += (diff[p] - delta) **': '只减 delta 的数：`({diff[p]}−{delta})^2`，`res` → {res}',
        'res += diff[index] ** 2': '后面没动过的数：`diff[{index}]^2`，`res` → {res}',
        'return res': '最小平方和 =={res}==',
    },
    cards=dict(
        one_liner='k 很大不能逐次减：把最大的几个整层削平',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['两个数组，`nums1` 最多改 `k1` 次，`nums2` 最多改 `k2` 次，每次 ±1',
                 '求修改后 `(nums1[i]-nums2[i])^2` 之和的最小值',
                 '示例：`[1,4,10,12],[5,8,6,9],k1=1,k2=1` → `43`'],
        quote='对nums1[i]加一就相当于对nums2[i]减一。令diff[i] = abs(nums1[i] - nums2[i])，那么问题就可以转化为给出一共k = k1 + k2次操作，每次可以将diff数组中的某个数减去1。',
        quote_src='—— yiduobo 题解原文',
        idea=['证明：`x<y` 时减 y 比减 x 的平方和降得更多，所以==每次减最大的==',
              '排序后：先把 `diff[0]` 减到 `diff[1]`，再两个一起减到 `diff[2]`……',
              '前 `index+1` 个削平到 `diff[index+1]` 要 `(index+1)×差` 次；k 不够就平分，余数个多减 1'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错：`k` 可达 `1e9`，必须按「整层」削平，不能一次次减',
                 '易错：`p` 在末尾且 `k >= diff[-1]*n` 时可全削成 0，直接返回 0',
                 '对比灵神：灵神加哨兵 0 统一处理；yiduobo 单独判断「全削为 0」的情况',
                 '原文为 Python 2 写法，`delta = k / (p + 1)` 的整数除法已改为 `//`'],
    ),
)
