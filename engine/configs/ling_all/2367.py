CONFIG = dict(
    num=2367, title='等差三元组的数目', difficulty='Easy', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='同向三指针', tags=['三指针'],
    code='''
class Solution:
    def arithmeticTriplets(self, nums: List[int], diff: int) -> int:
        ans, i, j = 0, 0, 1
        for x in nums:  # x = nums[k]
            while nums[j] + diff < x:
                j += 1
            if nums[j] + diff > x:
                continue
            while nums[i] + diff * 2 < x:
                i += 1
            if nums[i] + diff * 2 == x:
                ans += 1
        return ans
''',
    call='Solution().arithmeticTriplets([0,1,4,6,7,10], 3)',
    expect=2,
    views=[
        dict(type='text', fn=lambda S: (f"k 指向 `{S['x']}`：要找 j 对应 ==`{S['x'] - S['diff']}`==，i 对应 ==`{S['x'] - 2 * S['diff']}`==" if 'x' in S else f"diff = {S['diff']}：三个数依次相差 diff"), size=30),
        dict(type='array', var='nums', h=330,
             pointers={'i': 'blue', 'j': 'pink', 'nums.index(x)': 'green'}, pointer_labels={'nums.index(x)': 'k'},
             color=lambda S, idx, v: ('green' if 'x' in S and v == S['x'] and S['nums'].index(S['x']) == idx else None)),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('x(k)', 'x', 'green'), ('ans', 'ans', 'green')],
    captions={
        'ans, i, j = 0': '`ans = 0`，`i = 0`，`j = 1`：三个指针都只会往右走',
        'for x in nums': '枚举 k：`x = nums[k] = {x}`',
        'while nums[j] + diff < x': '`nums[j] + diff = {nums[j]} + {diff}` 和 `x = {x}` 比：{"还不够大 → j 右移" if nums[j] + diff < x else "不小于 x，j 停下"}',
        'j += 1': '`nums[j] + diff` 比 x 小，j 不可能是中间项 → `j` → {j}',
        'if nums[j] + diff > x': lambda S, B, r: (f'`{S.nums[S.j]} + {S.diff} = {S.nums[S.j] + S.diff} > {S.x}`：==没有数==能做 x 的前一项 → 跳过这个 x' if S.nums[S.j] + S.diff > S.x else f'`nums[j] + diff == x`：中间项找到了，接着找 i'),
        'continue': '`j` 停在比 x 大的位置，说明 `x - diff` 不在数组里，换下一个 x',
        'while nums[i] + diff * 2 < x': '`nums[i] + 2*diff = {nums[i] + diff * 2}` 和 `x = {x}` 比：{"太小 → i 右移" if nums[i] + diff * 2 < x else "不小于 x，i 停下"}',
        'i += 1': '最小项还不够，`i` 只增不减 → {i}',
        'if nums[i] + diff * 2 == x': lambda S, B, r: (f'`{S.nums[S.i]} + {2 * S.diff} == {S.x}`：==成立==，(i, j, k) 构成等差三元组' if S.nums[S.i] + S.diff * 2 == S.x else f'`{S.nums[S.i]} + {2 * S.diff} = {S.nums[S.i] + 2 * S.diff} != {S.x}`：i 这一项对不上，不是三元组'),
        'ans += 1': '找到一组：`ans` → {ans}',
        'return ans': '共 `{ans}` 个等差三元组',
    },
    cards=dict(
        one_liner='k 往右走，i、j 跟着只增不减，三指针各走一遍',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['严格递增数组 `nums`，找 `i<j<k` 使 `nums[j]-nums[i]==diff` 且 `nums[k]-nums[j]==diff`',
                 '返回这样的三元组个数',
                 '示例：`[0,1,4,6,7,10]`，`diff=3` → `2`'],
        quote='遍历 k 时，i 和 j 只增不减，因此可以用类似同向双指针的做法来移动指针。',
        quote_src='—— 灵茶山艾府题解',
        idea=['枚举 `x = nums[k]`，j 右移到 `nums[j] + diff >= x`',
              '等于 x 才去移动 i，直到 `nums[i] + 2*diff >= x`',
              '数组严格递增，所以 k 变大时 i、j 都不会回头'],
        summary=['时间 `O(n)`：`i += 1` 和 `j += 1` 总共不超过 `n` 次',
                 '没判断 `j<k`：一旦 `j=k`，`nums[j]+diff>=x` 必然成立，循环会停下',
                 '灵神还给了哈希表写法：一边查 `x-diff` 和 `x-2*diff`，一边插入 x',
                 '题单位置：滑动窗口与双指针 · 三指针'],
    ),
)
