def _txt(S):
    if 'last' not in S:
        return ''
    if 'index' not in S:
        return f"最后一个数不拆，`last = {S['last']}`"
    return f"从倒数第二个往前，`last = {S['last']}` 是后面一段的最小值（首个元素）"


CONFIG = dict(
    num=2366, title='将数组排序的最少替换次数', difficulty='Hard', category='贪心与思维',
    author='yiduobo', technique='倒序 · 取整拆分',
    tags=['灵神题单', '贪心算法', '难度分 2060'],
    code='''
class Solution(object):
    def minimumReplacement(self, nums):

        last = nums[-1]
        res = 0
        for index in range(len(nums) - 2, -1, -1):
            if nums[index] <= last:
                last = nums[index]
            elif nums[index] % last == 0:
                res += nums[index] // last - 1
            else:
                cnt = nums[index] // last
                res += cnt
                last = nums[index] // (cnt + 1)

        return res
''',
    call='Solution().minimumReplacement([4, 10, 3, 7])',
    expect=4,
    views=[
        dict(type='text', fn=_txt, size=34, h=90),
        dict(type='array', var='nums', pointers={'index': 'blue'}, h=300, label='nums（从右往左处理）',
             dim=lambda S, i, v: 'index' in S and i > S['index'],
             color=lambda S, i, v: 'blue' if 'index' in S and i == S['index'] else None),
    ],
    watch=[('index', 'index', 'blue'), ('last', 'last', 'pink'), 'cnt', ('res', 'res', 'green')],
    captions={
        'last = nums[-1]': '最后一个数拆了只会让前面更难，所以不拆：`last = {last}`',
        'res = 0': '`res` 累计拆分次数',
        'for index in range': lambda S, B, r: ('下标走完了，结束循环' if B.get('index') == S.get('index') else f"看 `nums[{S.index}] = {S.nums[S.index]}`，和后面的 `last = {S.last}` 比"),
        'if nums[index] <= last': lambda S, B, r: (f"`{S.nums[S.index]} <= {S.last}` → 不用拆，它成为新的 `last`" if S.nums[S.index] <= S.last else f"`{S.nums[S.index]} > {S.last}` → 比后面大，必须拆"),
        'elif nums[index] % last': lambda S, B, r: (f"`{S.nums[S.index]} % {S.last} == 0` → 刚好拆成若干个 `{S.last}`" if S.nums[S.index] % S.last == 0 else f"`{S.nums[S.index]} % {S.last} = {S.nums[S.index] % S.last}` ≠ 0 → 不能整除，只能拆成 x 和 x+1"),
        'res += nums[index] // last - 1': '拆成 `{nums[index] // last}` 个 `{last}`，操作 `n − 1` 次：`res` = =={res}==',
        'cnt = ': '拆成 `cnt + 1 = {cnt + 1}` 份（q 取最小），先记下 `cnt = {cnt}`',
        'res += cnt': '操作 `cnt` 次：`res` = =={res}==',
        'last = nums[index] // (cnt + 1)': '拆出的最小数 `x = {nums[index]} // {cnt + 1}` = =={last}==，前面的数要跟它比',
        'return res': '最少拆分 `{res}` 次',
    },
    cards=dict(
        one_liner='倒着看，拆出的首个数 x 要尽量大',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['一次操作把一个数换成两个和为它的数',
                 '求让数组非递减的最少操作次数',
                 '示例：`[3,9,3]` → `2`；本视频：`[4,10,3,7]` → `4`'],
        quote='最理想的拆分方式自然是将nums[n - 2]拆分成若干个nums[n - 1]，但是这里有一个前提是nums[n - 2]是nums[n - 1]的倍数。',
        quote_src='—— yiduobo 题解原文',
        idea=['拆出的子数组首元素要尽可能大：既最短，又方便更前面的数',
              '能整除就全拆成 `last`；不能整除就拆成 `x` 和 `x+1`',
              '被拆过的数，前面的数要比较的是拆出的首个元素 `x`，所以用变量 `last` 记着'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`',
                 '易错：拆分后要和 `x`（`last`）比较，不是原来的 `nums[k]`',
                 '对比灵神：灵神用 `(num-1)//m` 统一处理，不分整除与否'],
    ),
)
