CONFIG = dict(
    num=2607, title='使子数组元素和相等', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='裴蜀定理 + 中位数贪心', tags=['灵神题单', '数学算法', '难度分 2071'],
    code='''
class Solution:
    def makeSubKSumEqual(self, arr: List[int], k: int) -> int:
        k = gcd(k, len(arr))
        ans = 0
        for i in range(k):
            b = sorted(arr[i::k])
            mid = b[len(b) // 2]
            ans += sum(abs(x - mid) for x in b)
        return ans
''',
    call='Solution().makeSubKSumEqual([1,9,4,2,7,3,5,8], 6)',
    expect=19,
    views=[
        dict(type='array', var='arr', h=200, label='arr（循环数组）',
             color=lambda S, i, v: ('blue' if i % S['k'] == S['i'] else None) if 'i' in S and 'b' in S and S.get('_line', 0) >= 6 else None),
        dict(type='array', var='b', h=200, label='b = 这一组排序后'),
        dict(type='text', h=100, fn=lambda S: f"中位数 `mid` = =={S['mid']}==，本组代价 `{sum(abs(x - S['mid']) for x in S['b'])}`" if 'mid' in S and 'b' in S else ''),
    ],
    watch=['k', 'i', 'mid', ('ans', 'ans', 'green')],
    captions={
        'k = gcd': '数组既有周期 `n` 又有周期 `k`，必有周期 `gcd`（裴蜀定理）→ `k = {k}`，下标模 `k` 同余的数必须相等',
        'b = sorted': '第 `{i}` 组：下标模 `{k}` 余 `{i}` 的数，排序得 `{b}`',
        'mid = ': '中位数贪心：全变成中位数最省，`mid = b[{len(b)//2}] = {mid}`',
        'ans += ': '本组每个数变成 `{mid}` 的代价 = `{sum(abs(x - mid) for x in b)}`，累计 `ans = {ans}`',
        'return ans': '各组互不影响，总代价 =={ret}==',
    },
    cards=dict(
        one_liner='循环数组按 gcd(k, n) 分组，每组都变成中位数',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['循环数组 `arr`，每次可把一个元素 `+1` 或 `-1`',
                 '要使所有长为 `k` 的子数组和都相等，求最少运算次数',
                 '示例：`[1,4,1,3]`, `k=2` → `1`'],
        quote='一个循环数组如果既有周期 n，又有周期 k，则必然有周期 gcd(n,k)。',
        quote_src='—— 灵茶山艾府题解',
        idea=['相邻两个长 `k` 的子数组和相等 ⇒ `a[i] = a[i+k]`',
              '循环后再由裴蜀定理，等价于 `a[i] = a[i+gcd(n,k)]`',
              '按 `i % gcd` 分组，每组变成中位数，距离和最小'],
        summary=['时间 `O(n log n)`，排序可换快速选择做到 `O(n)`',
                 '易错：别忘了循环数组，要先 `k = gcd(k, n)`',
                 '中位数贪心取 `b[len(b)//2]`',
                 '相似题：462 最小操作次数使数组元素相等 II'],
    ),
)
