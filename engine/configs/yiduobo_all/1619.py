CONFIG = dict(
    num=1619, title='删除某些元素后的数组均值', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='快速选择第 k 小',
    code='''
class Solution(object):
    def trimMean(self, arr):
        n = len(arr)
        k = n // 20
        l = self.search(arr, 0, n - 1, k)
        r = self.search(arr, 0, n - 1, n - k + 1)
        cnt_l = cnt_r = 0
        tot = 0.0
        for num in arr:
            if num < l:
                cnt_l += 1
            elif num > r:
                cnt_r += 1
            else:
                tot += num

        return (tot - (k - cnt_l) * l - (k - cnt_r) * r) / (n - k - k)

        
    def search(self, arr, l, r, k):
        if l == r:
            return arr[l]

        mid = arr[(l + r) // 2]
        i = l
        j = r
        while i <= j:
            while i <= r and arr[i] < mid:
                i += 1
            while j >= l and arr[j] > mid:
                j -= 1
            if i <= j:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1
                j -= 1

        if j - l + 1 >= k:
            return self.search(arr, l, j, k)
        elif i - l >= k:
            return arr[l + k - 1]
        else:
            return self.search(arr, i, r, k - (i - l))
''',
    call='Solution().trimMean([6,2,7,5,1,2,0,3,10,2,5,0,5,5,0,8,7,6,8,0])',
    expect=4.0,
    views=[
        dict(type='array', var='arr', pointers={'i': 'blue', 'j': 'pink'}, window=('l', 'r'), h=260, cell=60,
             color=lambda S, i, v: ('green' if (S.get('l') is not None and False) else None)),
        dict(type='calls', h=200),
        dict(type='text', fn=lambda S: (f"去掉最小 `{S['k']}` 个和最大 `{S['k']}` 个，`k = n // 20 = {S['k']}`；下界 `l = {S['l']}`，上界 `r = {S['r']}`" if 'r' in S and 'k' in S and 'n' in S and 'tot' in S else ''), size=26),
    ],
    watch=['k', 'l', 'r', 'cnt_l', 'cnt_r', ('tot', 'tot', 'green')],
    captions={
        'k = n // 20': '要去掉前 5% 小和前 5% 大：`k = {n} // 20 = {k}`',
        'l = self.search(arr, 0, n - 1, k)': '快速选择：求第 `{k}` 小的数，记为 `l` = =={l}==',
        'r = self.search(arr, 0, n - 1, n - k + 1)': '第 k 大 = 第 `n-k+1` 小：求出 `r` = =={r}==',
        'if l == r': lambda S, B, ret: ('区间只剩一个数 → 它就是答案' if S.l == S.r else f'区间 `[{S.l}, {S.r}]` 还有多个数，继续划分'),
        'mid = arr[': '取中间的数当基准 `mid` = =={mid}==',
        'while i <= j': '`i <= j`：还没划分完' ,
        'while i <= r and arr[i] < mid': '`i` 右移，跳过比 mid 小的数，已在左侧',
        'while j >= l and arr[j] > mid': '`j` 左移，跳过比 mid 大的数，已在右侧',
        'arr[i], arr[j] = arr[j], arr[i]': '`i` 处不小于 mid、`j` 处不大于 mid → 交换，放到各自的一侧',
        'if j - l + 1 >= k': lambda S, B, ret: (f'左半 `[{S.l}..{S.j}]` 有 `{S.j - S.l + 1}` 个数 >= k={S.k}：第 k 小在左半，只递归左边' if S.j - S.l + 1 >= S.k else f'左半只有 `{S.j - S.l + 1}` 个数 < k={S.k}，往下判断'),
        'elif i - l >= k': lambda S, B, ret: (f'`i - l = {S.i - S.l}` >= k：第 k 小落在中间等于 mid 的部分，直接取 `arr[{S.l + S.k - 1}]`' if S.i - S.l >= S.k else f'`i - l = {S.i - S.l}` < k：第 k 小在右半'),
        'return self.search(arr, l, j, k)': '递归左半 `[{l}, {j}]`',
        'return arr[l + k - 1]': '找到第 `{k}` 小：`{ret}`',
        'return self.search(arr, i, r, k - (i - l))': '去掉左边 `{i - l}` 个，递归右半 `[{i}, {r}]`，找第 `{k - (i - l)}` 小',
        'for num in arr': '一趟遍历，按和 l、r 的大小关系分类',
        'if num < l': '`{num} < l={l}`？ → 属于要被去掉的最小部分，计数',
        'elif num > r': '`{num} > r={r}`？ → 属于要被去掉的最大部分，计数',
        'tot += num': '`l <= {num} <= r`：参与求和，`tot` = {tot}',
        'return (tot': '`l` 和 `r` 本身可能有重复：被去掉的个数不足 k 时要从 tot 里补扣。均值 = ==({tot} - {k - cnt_l}×{l} - {k - cnt_r}×{r}) / {n - k - k}== = {ret}',
    },
    cards=dict(
        one_liner='先找第 k 小和第 k 大，再一趟遍历求平均',
        complexity='时间 `O(n)`（快速选择，平均），空间 `O(log n)` 递归栈',
        problem=['给定长度为 `n`（20 的倍数）的数组 `arr`，去掉最小的 5% 和最大的 5% 的元素',
                 '返回剩余元素的平均值',
                 '示例：20 个数 `[6,2,7,5,1,2,0,3,10,2,5,0,5,5,0,8,7,6,8,0]` → `4.0`'],
        quote='不妨设k = n / 20，题目就是要求去除掉arr中前k小的数以及前k大的数。那么可以先找出题目中第k小的数以及第k大的数，然后一趟遍历，根据arr中的数与这两个数的大小关系来决定是否需要去除。',
        quote_src='—— yiduobo 题解原文',
        idea=['排序再去头尾是 `O(n log n)`，作者想要更优',
              '第 k 大 = 第 `n-k+1` 小，用快排的划分思想：每次只递归包含答案的一边',
              '得到 `l`、`r` 后遍历：`<l` 和 `>r` 的计数，其余求和；重复值用计数补扣'],
        summary=['时间平均 `O(n)`，空间 `O(log n)`',
                 '易错：`l`、`r` 本身可能重复出现多次，要用 `k - cnt_l` 补扣掉多余的',
                 '`search` 会原地交换 `arr`，第二次查找是在被打乱的数组上进行',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`（`n // 20`、`(l + r) // 2`），最后求均值的 `/` 保持不变',
                 '直接排序去头尾也能过，快速选择是更优做法'],
    ),
)
