def _txt(S):
    ln = S.get('_line', 0)
    if 'res' in S and ln >= 23 and 'index' in S:
        i = S['index']
        return f"`nums[{i}] = {S['nums'][i]}`：`left[{i}] × right[{i}] = {S['left'][i]} × {S['right'][i]}` = =={S['left'][i] * S['right'][i]}=="
    if 'first' in S and 'index' in S and 16 <= ln <= 18:
        return f"从右往左：`nums[{S['index']}]` 往右最近的 `v+1` 在哪？没有就是 `n`；`right` 记 `位置差`"
    if 'last' in S and 'index' in S and 9 <= ln <= 11:
        return f"从左往右：`nums[{S['index']}]` 往左最近的 `v` 或 `v+1` 在哪？没有就是 `-1`；`left` 记 `位置差`"
    return '数每个 v 当「较小数」的子数组个数 = left × right'


def _col(name):
    def f(S, i, v):
        ln = S.get('_line', 0)
        if name == 'left' and 'index' in S and 9 <= ln <= 11 and i == len(S['left']) - 1:
            return 'green'
        if name == 'right' and 16 <= ln <= 19 and 'index' in S and 'res' not in S:
            return 'green' if ln != 19 and i == len(S['right']) - 1 else None
        if 'res' in S and ln >= 23 and 'index' in S and i == S['index']:
            return 'blue'
        return None
    return f


CONFIG = dict(
    num=2763, title='所有子数组中不平衡数字之和', difficulty='Hard', category='贪心与思维',
    author='yiduobo', technique='贡献法 · 左右各扫一遍',
    tags=['灵神题单', '难度分 2700'],
    code='''
class Solution(object):
    def sumImbalanceNumbers(self, nums):

        n = len(nums)

        last = {}
        left = []
        for index in range(n):
            v = nums[index]
            left.append(index - max(last.get(v + 1, -1), last.get(v, -1)))
            last[v] = index

        first = {}
        right = []
        for index in range(n - 1, -1, -1):
            v = nums[index]
            right.append(first.get(v + 1, n) - index)
            first[v] = index
        right.reverse()

        res = 0
        for index in range(n):
            res += left[index] * right[index]
        
        return res - n * (n + 1) // 2
''',
    call='Solution().sumImbalanceNumbers([1,3,3,3,5])',
    expect=8,
    views=[
        dict(type='text', fn=_txt, size=24, h=60),
        dict(type='array', var='nums', h=170, label='nums',
             color=lambda S, i, v: 'blue' if 'index' in S and i == S['index'] and 'v' in S else None),
        dict(type='array', var='left', h=175, label='left[i]：左边界可选个数', color=_col('left')),
        dict(type='array', var='right', h=175, label='right[i]：右边界可选个数（倒着填，最后 reverse）', color=_col('right')),
        dict(type='map', var='last', h=130, label='last：值 → 最近出现下标'),
        dict(type='map', var='first', h=130, label='first：值 → 最近出现下标（从右往左）'),
    ],
    watch=['index', 'v', ('res', 'res', 'green')],
    captions={
        'n = len(nums)': '`n = {n}`',
        'last = {}': '`last`：从左往右扫，记录每个值最近一次出现的下标',
        'left = []': '`left[i]`：以 `nums[i]` 当较小数时，左端点有多少种选法',
        'first = {}': '`first`：从右往左扫，记录每个值最近出现的下标',
        'right = []': '`right[i]`：右端点有多少种选法（倒着收集）',
        'left.append': '左边最近的 `v+1` 或 `v` 在 `{max(last.get(v + 1, -1), last.get(v, -1))}` → 左端点可选 `index − ({max(last.get(v + 1, -1), last.get(v, -1))})` = =={left[-1]}== 个',
        'right.append': '右边最近的 `v+1` 在 `{first.get(v + 1, n)}`（没有就是 `n`）→ 右端点可选 `{first.get(v + 1, n)} − {index}` = =={right[-1]}== 个',
        'last[v] = index': '`last[{v}] = {index}`',
        'first[v] = index': '`first[{v}] = {index}`',
        'right.reverse()': '`right` 是倒着填的，翻转回来：`{right}`',
        'v = nums[index]': '`v = nums[{index}] = {v}`',
        'res = 0': '`res` 累计所有贡献',
        'res += left': '`res += left[{index}] × right[{index}]` = `{left[index]} × {right[index]}` → =={res}==',
        'return res': '每个子数组的最大值被当成了「较小数」，多算一次：`res − n(n+1)/2 = {res} − {n * (n + 1) // 2}` = =={ret}==',
        8: lambda S, B, r: ('`left` 求完了' if 'index' in B and S['index'] == B.index == len(S['nums']) - 1 else f"从左往右：`index = {S['index']}`"),
        15: lambda S, B, r: ('`right` 求完了' if 'index' in B and S['index'] == B.index == 0 else f"从右往左：`index = {S['index']}`"),
        22: lambda S, B, r: ('贡献累加完了' if 'index' in B and S['index'] == B.index == len(S['nums']) - 1 else f"逐个累加：`index = {S['index']}`"),
    },
    cards=dict(
        one_liner='较小数 v 的贡献 = 左边界个数 × 右边界个数',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['子数组的「不平衡数字」= 排序后相邻差 `> 1` 的位置数；求 `nums` 所有子数组的不平衡数字之和',
                 '示例：`[1,3,3,3,5]` → `8`',
                 '`n ≤ 1000`，`1 ≤ nums[i] ≤ n`'],
        quote='可以想办法计算出数组中每个数在作为不平衡关系中的较小数时对答案产生的贡献，从而在O(n)的时间内得到最终答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['先想暴力：左端点固定向右扩，新加 `x` 时看 `x−1`、`x+1` 是否已存在，分五种情况改个数',
              '观察后改成「按较小数算贡献」：`left` 看左边最近的 `v` 或 `v+1`，`right` 只看右边最近的 `v+1`',
              '只让最左边的 `v` 产生贡献，避免重复值多算；最后减去子数组总数 `n(n+1)/2`'],
        summary=['时间 `O(n)`，空间 `O(n)`（两个字典 + 两个数组）',
                 '`left` 同时看 `v` 和 `v+1`，`right` 只看 `v+1`：保证相同的 `v` 只有最左边那个计数',
                 '最后要减 `n(n+1)/2`：每个子数组的最大值被当成「较小数」多算一次',
                 '原文为 Python 2 写法，`n * (n + 1) / 2` 是整数除法，已改为 `//`',
                 '对比灵神：灵神靠 `idx` 数组 + `right` 数组，`x−1` 当较小数；yiduobo 用字典，看 `v+1`'],
    ),
)
