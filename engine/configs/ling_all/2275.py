def _bin(S):
    x = S.get('x')
    if x is None or 'i' not in S:
        return '把每个数拆成二进制位，给每一位上的 1 计数'
    return f"当前 `x` = `{x:b}`（剩余的高位），正在统计第 =={S['i']}== 位（从低到高）；每位的计数 = 该位是 1 的数的个数"


CONFIG = dict(
    num=2275, title='按位与结果大于零的最长组合', difficulty='Medium', category='位运算',
    author='灵茶山艾府', technique='拆位 · 统计每位 1 的个数',
    tags=['灵神题单', '难度分 1642'],
    code='''
class Solution:
    def largestCombination(self, candidates: List[int]) -> int:
        cnt = [0] * 24
        for x in candidates:
            i = 0
            while x:
                cnt[i] += x & 1
                x >>= 1
                i += 1
        return max(cnt)
''',
    call='Solution().largestCombination([5,6,7,4])',
    expect=4,
    views=[
        dict(type='text', fn=_bin, h=70),
        dict(type='array', var='candidates', label='candidates', h=150,
             ),
        dict(type='array', var='cnt', label='cnt[i]：第 i 位是 1 的数的个数', h=200, cell=36,
             pointers={'i': 'pink'},
             color=lambda S, i, v: 'green' if v and v == max(S['cnt']) else None),
    ],
    watch=['x', ('i', 'i', 'pink'), ('max(cnt)', 'max(cnt)', 'green')],
    captions={
        'cnt = [0]': '`cnt[i]` 记录「第 i 位是 1 的数」有多少个；`10^7 < 2^24`，开 24 位够用',
        'for x in candidates': lambda S, B, r: (f'取下一个数 `x = {S.x}`，二进制 `{S.x:b}`' if S.x else '所有数都统计完了，`cnt` 里每个位置就是该位上 1 的个数'),
        'i = 0': '从最低位（第 0 位）开始看',
        'while x': lambda S, B, r: (f'`x = {S.x}` 还不是 0，还有高位没统计' if S.x else '`x` 变成 0，高位都没有 1 了 → 这个数统计完'),
        'cnt[i] += x & 1': '`x & 1` = {x & 1}：第 {i} 位是 1 就让 `cnt[{i}]` +1 → =={cnt[i]}==',
        'x >>= 1': '`x` 右移一位，下一位变成最低位：`x` = {x}',
        'i += 1': '换到第 `{i}` 位',
        'return max(cnt)': '为什么取最大？AND>0 ⇔ 某一位全是 1；选「该位是 1」的所有数即可 → 最多 `{max(cnt)}` 个',
    },
    cards=dict(
        one_liner='AND 大于 0，就一定有某一位全是 1：枚举这一位',
        complexity='时间 `O(n log U)`，空间 `O(log U)`',
        problem=['从 `candidates` 里选一个子序列，使所有元素按位与 `> 0`',
                 '返回满足条件的最长子序列长度',
                 '示例：`[16,17,71,62,12,24,14]` → `4`；本视频用 `[5,6,7,4]` → `4`'],
        quote='既然要求 AND 大于 0，那么这个 AND 值中，一定有一个比特位是 1。枚举这个比特位。',
        quote_src='—— 灵茶山艾府题解',
        idea=['如果 AND 的第 i 位是 1，选的数第 i 位也必须全是 1',
              '所以答案 = ==每一位上 1 的个数的最大值==',
              '写法二：遍历一次，同时给 24 个位计数'],
        summary=['时间 `O(n log U)`，空间 `O(log U)`',
                 '写法一：`max(sum(x >> i & 1 for x in candidates) for i in range(m))`，枚举位再遍历数组，结果一样',
                 '易错：`while x` 里会修改 `x`，只是循环变量的拷贝，不影响原数组',
                 '思考题：改成「子数组」要用拆位 + 双指针 / 滑窗'],
    ),
)
