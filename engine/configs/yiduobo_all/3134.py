CONFIG = dict(
    num=3134, title='找出唯一性数组的中位数', difficulty='Hard', category='滑动窗口与双指针',
    author='yiduobo', technique='二分中位数 + 变长滑窗数「大于等于 mid」',
    tags=['灵神题单·滑动窗口与双指针', '灵神题单·二分算法', '难度分 2451'],
    code='''
class Solution(object):
    def medianOfUniquenessArray(self, nums):

        n = len(nums)
        m = (n + 1) * n // 2

        left = 1
        right = n

        while left < right:
            mid = (left + right + 1) // 2
            freq = {}
            p = 0
            cnt = 0

            for index, v in enumerate(nums):
                while p < n and len(freq) < mid:
                    freq[nums[p]] = freq.get(nums[p], 0) + 1
                    p += 1

                if len(freq) < mid:
                    break

                cnt += n - p + 1
                freq[v] -= 1
                if freq[v] == 0:
                    freq.pop(v)

            if cnt <= m // 2:
                right = mid - 1
            else:
                left = mid
        
        return left
''',
    call='Solution().medianOfUniquenessArray([4,3,5,4])',
    expect=2,
    views=[
        dict(type='array', var='nums', label='nums（框 = 窗口 [index, p)，p 是右边界的下一格）', pointers={'index': 'blue', 'p': 'pink'},
             window=(lambda S: S.get('index', 0), lambda S: min(S.get('p', 0), len(S['nums'])) - 1), cell=100, h=230,
             dim=lambda S, i, v: 'index' in S and 'p' in S and not (S['index'] <= i < S['p'])),
        dict(type='map', var='freq', label='freq（窗口内每个数的次数）', fmt=lambda k, v: f'{k}: {v}', h=130, font=34),
        dict(type='text', h=110, size=30,
             fn=lambda S: (f"二分区间 [{S['left']}, {S['right']}]，猜 `mid` = =={S['mid']}==；累计 `cnt` = {S['cnt']}，门槛 `m // 2` = {S['m']//2}"
                           if 'mid' in S and 'cnt' in S else
                           (f"共 `m` = {S['m']} 个子数组，二分 distinct 值范围 [1, {S['n']}]" if 'm' in S else ''))),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'orange'), ('index', 'index', 'cyan'),
           ('p', 'p', 'yellow'), ('cnt', 'cnt', 'green')],
    captions={
        'm = (n + 1)': '子数组共 `m = n(n+1)/2` = =={m}== 个，逐个枚举不可行，要二分中位数',
        'left = 1': '中位数是某个 distinct 值，范围在 `[1, n]`：`left = 1`，`right = n`',
        'while left < right': lambda S, B, r: (f'`left = {S.left} < right = {S.right}`，区间还没收缩完' if S.left < S.right
                                               else f'`left = right = {S.left}` → 二分结束'),
        'mid = (left': '猜中位数 `mid = ({left} + {right} + 1) // 2` = =={mid}==（向上取整，因为分支里是 `left = mid`）',
        'freq = {}': '`freq` 记录窗口 `nums[index:p]` 里每个数的次数',
        'p = 0': '`p` 是窗口右边界（开区间），只会向右',
        'cnt = 0': '`cnt` 统计 distinct 值 ==大于等于 mid== 的子数组个数',
        'while p < n and len(freq) < mid': lambda S, B, r: (
            f'`p = {S.p} < n` 且 `len(freq) = {len(S.freq)} < mid = {S.mid}` → 窗口里的数还不够 `mid` 种，右扩'
            if S.p < S.n and len(S.freq) < S.mid else
            (f'窗口已有 `{len(S.freq)}` 种数 ≥ `mid = {S.mid}` → 停止右扩' if len(S.freq) >= S.mid else f'`p` 到末尾了，不能再扩')),
        'freq[nums[p]]': '`nums[{p-1}] = {nums[p-1]}` 进入窗口，`p` → {p}',
        'if len(freq) < mid': lambda S, B, r: (f'`len(freq) = {len(S.freq)} < mid = {S.mid}`：就算扩到末尾也凑不够 → ==break==，之后的起点更不可能'
                                               if len(S.freq) < S.mid else f'`len(freq) = {len(S.freq)} ≥ mid = {S.mid}` → 窗口够了'),
        'cnt += n - p + 1': '起点 `{index}`、终点 `p-1..n-1` 的子数组 distinct 都 ≥ {mid}，共 `{n} - {p} + 1` = =={n - p + 1}== 个 → `cnt = {cnt}`',
        'freq[v] -= 1': '起点右移前，把 `nums[{index}] = {v}` 移出窗口：次数 → {freq[v]}',
        'freq.pop': '`{v}` 次数为 0，从 freq 删掉，窗口剩 `{len(freq)}` 种数；不删的话 `len(freq)` 会虚高',
        'break': '直接结束这一轮统计，`cnt` 保持 {cnt}',
        'if cnt <= m // 2': lambda S, B, r: (f'`cnt = {S.cnt} ≤ m // 2 = {S.m // 2}`：distinct ≥ {S.mid} 的太少 → `mid` ==猜大了==，`right = mid - 1`'
                                              if S.cnt <= S.m // 2 else f'`cnt = {S.cnt} > m // 2 = {S.m // 2}`：distinct ≥ {S.mid} 的足够多 → `mid` 可行，`left = mid`'),
        'right = mid - 1': '`right` → {right}',
        'left = mid': '`left` → {left}',
        'return left': '`left = right`，中位数 = =={left}==',
    },
    skip=['freq = {}', 'p = 0', 'cnt = 0', 'p += 1', 'freq[v] == 0', 'for index, v', 'right = n'],
    max_steps=50,
    cards=dict(
        one_liner='先算出子数组总数定下中位位置，再二分中位数、滑窗数「≥ mid」的子数组',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['对 `nums` 所有非空子数组，取各自的不同元素个数，排序成「唯一性数组」，求中位数（偶数个取较小的）',
                 '示例：`[4,3,5,4]` → `[1,1,1,1,2,2,2,3,3,3]` → `2`'],
        quote='唯一性数组中大于等于中位数的元素数目必然要大于等于m // 2，也就是说在这里可以尝试利用二分法来寻找这个中位数。',
        quote_src='—— yiduobo 题解原文',
        idea=['`m = n(n+1)/2` 个子数组已知，逐个枚举太慢 → ==二分 distinct 值==',
              '统计「distinct ≥ mid」的子数组：参考第 340 题，变长窗口先右扩到恰好 `mid` 种数',
              '这时终点在 `p-1..n-1` 的子数组都满足，一共 `n-p+1` 个；再移走起点继续'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '`mid` 要向上取整 `(left+right+1)//2`，否则 `left = mid` 会死循环',
                 '数的是「≥ mid」，所以 `cnt <= m // 2` 时 mid 偏大，缩 `right`',
                 '原文已是 Python 3 可运行写法，代码未改动',
                 '对比灵神：灵神数「≤ upper」并和第 k 小比较；yiduobo 数「≥ mid」并和 m//2 比较'],
    ),
)
