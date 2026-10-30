def _c(S, i, j, v):
    if 'd' in S and 'i' in S and i == S['i'] and j == S['d'] and S['x'] is not None:
        return 'yellow'
    return 'green' if v else None


CONFIG = dict(
    num=3153, title='所有数对中数位差之和', difficulty='Medium', category='位运算',
    author='灵茶山艾府', technique='拆位 + 枚举右维护左',
    tags=['灵神题单·位运算', '难度分 1645'],
    code='''
class Solution:
    def sumDigitDifferences(self, nums: List[int]) -> int:
        ans = 0
        cnt = [[0] * 10 for _ in str(nums[0])]
        for k, x in enumerate(nums):
            i = 0
            while x:
                x, d = divmod(x, 10)
                ans += k - cnt[i][d]
                cnt[i][d] += 1
                i += 1
        return ans
''',
    call='Solution().sumDigitDifferences([13, 23, 12])',
    expect=4,
    views=[
        dict(type='array', var='nums', pointers={'k': 'blue'}, h=170, label='nums（k = 当前数，前面 k 个数已入表）',
             color=lambda S, i, v: 'blue' if 'k' in S and i == S['k'] else None,
             dim=lambda S, i, v: 'k' in S and i > S['k']),
        dict(type='table', var='cnt', h=230, cell=64, label='cnt[位][数字]：这一位上数字出现次数（黄 = 刚查/更新）',
             rows=lambda S: ['个位', '十位'][:len(S['cnt'])], cols=list(range(10)), color=_c),
        dict(type='text', size=30, fn=lambda S: (f"第 `{S['k']}` 个数，前面有 `{S['k']}` 个；这一位数字 `{S['d']}` 已出现 `{S['cnt'][S['i']][S['d']]}` 次 → 不同的有 =={S['k'] - S['cnt'][S['i']][S['d']]}== 个") if 'd' in S and 'i' in S and S['i'] < len(S['cnt']) and S['x'] is not None else ''),
    ],
    watch=[('k', 'k', 'blue'), ('x', 'x', 'pink'), ('d', 'd', 'yellow'), ('i', 'i', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'cnt = [[0]': '每个数位一行 `cnt`，每行 10 格统计 0~9 出现次数；共 `{len(cnt)}` 位',
        'for k, x': lambda S, B, r: ('所有数都处理完，退出循环' if S.k == len(S.nums) - 1 and S.x == 0 and B.k == S.k else f'枚举右边的数 `x = nums[{S.k}]`，左边已经处理过的有 `{S.k}` 个（枚举右、维护左）'),
        'i = 0': '从个位开始拆，`i` 表示当前是第几位',
        'while x': lambda S, B, r: (f'`x = {S.x}` 还没拆完 → 继续拆下一位' if S.x else '`x = 0`：所有数位拆完，换下一个数'),
        'divmod': '拆出个位 `d = {d}`，剩下的 `x = {x}` 留给更高位',
        'ans +=': '前面共 `{k}` 个数，其中 `{cnt[i][d]}` 个这一位也是 `{d}` → 不同的 `{k} − {cnt[i][d]}` = =={k - cnt[i][d]}==，`ans` 累加为 {ans}',
        'cnt[i][d] += 1': '==先加答案再更新 cnt==：现在才把自己放进表，不然会和自己配对',
        'i += 1': '下一位：`i` → {i}',
        'return': '所有位上的不同数对都累加完：`ans = {ans}`',
    },
    cards=dict(
        one_liner='把每个数位拆开，只数这一位上「不同的数对」',
        complexity='时间 `O(n log U)`，空间 `O(D log U)`',
        problem=['数组 `nums` 里所有数的位数相同；两个数的数位差 = 同一位置上数字不同的个数',
                 '求所有数对的数位差之和',
                 '示例：`[13,23,12]` → `4`'],
        quote='横看成岭侧成峰，换一个角度，把每一位拆开：计算个位数中的不同数对个数；计算十位数中的不同数对个数……',
        quote_src='—— 灵茶山艾府题解',
        idea=['每一位彼此独立：总和 = 各位「不同数对个数」之和',
              '遍历到 `d = a[k]` 时，前面 `k` 个数里有 `cnt[d]` 个与它相同',
              '所以有 `k − cnt[d]` 个不同，直接加进答案'],
        summary=['时间 `O(n log U)`，空间 `O(D log U)`，`D = 10`',
                 '==先更新 ans，再更新 cnt==：否则下标相同的数对也被算进来（`nums=[1]` 会得到 −1）',
                 '另一种写法：总对数 `m·n(n−1)/2` 减去每位上「相同的数对」，同 1512 好数对',
                 '`cnt` 的行数取自 `nums[0]` 的位数，因为所有数位数相同'],
    ),
)
