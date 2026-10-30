def _b(x, w=6):
    return format(x, 'b').zfill(w)


def _fn(S):
    if 'x' not in S:
        return ''
    x = S['x']
    s = f"x = `{_b(x)}`"
    if 't' in S:
        s += f"　~x 的 lowbit = `{_b((S['t'] & -S['t']), 6)}`，右移一位 = `{_b((S['t'] & -S['t']) >> 1, 6)}`"
        if S['nums'][S['i']] != x:
            s += f"　→ ans = `{_b(S['nums'][S['i']])}`"
    return s


def _color(S, i, v):
    if 'i' not in S:
        return None
    return 'green' if i < S['i'] else None


CONFIG = dict(
    num=3315, title='构造最小位运算数组 II', difficulty='Medium', category='位运算',
    author='灵茶山艾府', technique='把最右边 0 右边的 1 置为 0',
    tags=['灵神题单·位运算', '难度分 1715'],
    code='''
class Solution:
    def minBitwiseArray(self, nums: List[int]) -> List[int]:
        for i, x in enumerate(nums):
            if x == 2:
                nums[i] = -1
            else:
                t = ~x
                nums[i] ^= (t & -t) >> 1
        return nums
''',
    call='Solution().minBitwiseArray([2,5,11,13,31])',
    expect=[-1, 4, 9, 12, 15],
    views=[
        dict(type='text', fn=_fn, size=28, h=90),
        dict(type='array', var='nums', pointers={'i': 'blue'}, color=_color, label='nums（原地改成答案，绿色 = 已改好）', h=240),
    ],
    watch=[('i', "S.get('i')", 'blue'), ('x', "S.get('x')", 'cyan'), ('t', "S.get('t')", 'orange')],
    captions={
        'for i, x in enumerate': lambda S, B, r: (f'取 `nums[{S.i}] = {S.x}`，二进制 `{format(S.x, "b")}`' if S.nums[S.i] == S.x else '所有数都处理完了，退出循环'),
        'if x == 2': lambda S, B, r: (f'`x = 2` 是偶数：`x | (x+1)` 的最低位一定是 1，不可能等于偶数 → ==无解==' if S.x == 2 else f'`x = {S.x}` 是奇数，有解'),
        'nums[i] = -1': '无解，`nums[{i}] = -1`',
        't = ~x': '取反：`~x` 里最低的 1，就是 `x` 里 ==最右边的 0==。`~x` 的低 6 位是 `{format(t & 63, "06b")}`',
        'nums[i] ^= (t & -t) >> 1': '`t & -t` 取最右边的 0 的位置，右移一位就是它==右边的那个 1==，异或把它置 0：`{x}` → ==`{nums[i]}`==',
        'return nums': '全部改完：`{nums}`',
    },
    cards=dict(
        one_liner='x|(x+1) 是把最右边的 0 变 1，倒推就是把它右边的 1 变 0',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给质数数组 `nums`，对每个 `nums[i]` 找最小的 `ans[i]`',
                 '满足 `ans[i] OR (ans[i]+1) == nums[i]`，找不到填 `-1`',
                 '示例：`[2,3,5,7]` → `[-1,1,4,3]`'],
        quote='可以发现，x | (x+1) 的本质是把二进制最右边的 0 置为 1。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`x=100111`，`x|(x+1)=101111`：最右边的 0 变成了 1',
              '倒推：把 `101111` 里的某个 1 变回 0，最小的是 ==最右边的 0 的右边那个 1==',
              '偶数无解：`x|(x+1)` 最低位一定是 1，质数里只有 `2` 是偶数'],
        summary=['时间 `O(n)`，空间 `O(1)`（原地修改）',
                 '`~x` 的 lowbit 就是 `x` 最右边的 0，右移一位得到要翻转的那个 1',
                 '写法二：`((x+1) & ~x) >> 1` 同样能得到这个 lowbit',
                 '先判 `x == 2`，其余质数都是奇数一定有解'],
    ),
)
