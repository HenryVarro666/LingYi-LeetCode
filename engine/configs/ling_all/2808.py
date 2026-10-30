CONFIG = dict(
    num=2808, title='使循环数组所有元素相等的最少秒数', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='枚举目标值 · 相邻位置最大间距',
    tags=[],
    code='''
class Solution:
    def minimumSeconds(self, nums: List[int]) -> int:
        pos = defaultdict(list)
        for i, x in enumerate(nums):
            pos[x].append(i)

        ans = n = len(nums)
        for a in pos.values():
            a.append(a[0] + n)
            mx = max(j - i for i, j in pairwise(a))
            ans = min(ans, mx)
        return ans // 2  # 最后再除 2
''',
    call='Solution().minimumSeconds([2, 1, 3, 3, 2, 1, 3])',
    expect=1,
    views=[
        dict(type='array', var='nums', label='nums（绿 = 当前枚举的值 x 出现的位置）', cell=84, h=200,
             color=lambda S, i, v: 'green' if 'a' in S and i < len(S['nums']) and S['nums'][i] == S['nums'][S['a'][0]] else None),
        dict(type='map', var='pos', label='pos[x] = x 出现的下标（末尾补 首位+n 变成非环形）', h=260,
             fmt=lambda k, v: f'{k}: {v}'),
        dict(type='text', size=28, fn=lambda S: (f"相邻最大间距 `mx = {S['mx']}`，扩散耗时 `mx // 2` = =={S['mx'] // 2}==" if 'mx' in S else '')),
    ],
    watch=['n', 'a', ('mx', 'mx', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'pos[x].append': '记录数字 `{x}` 出现在下标 `{i}`：`pos[{x}] = {pos[x]}`',
        'ans = n = len': '`ans` 初值取 `n = {n}`（间距的上界），后面取最小',
        'a.append': '数组是环形的，首尾相邻：末尾补上 `{a[0]} + {n}` = `{a[-1]}`，环就拉直成一条线：`a = {a}`',
        'mx = max': '相邻两个相同数字间距最大的是 =={mx}==；它们同时向中间扩散，耗时 `mx // 2`',
        'ans = min': '枚举的这个数要 `{mx}` 的间距，比较 `min({B.ans}, {mx})` → `ans = {ans}`',
        'return ans': '间距的最小值是 `{ans}`，==最后再除 2== → 最少 =={ret}== 秒',
    },
    cards=dict(
        one_liner='枚举最终的数字，看相邻同数相距最远的那一段',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['每秒每个位置可换成自己或左右邻居的值（环形，同时替换）',
                 '求让整个数组相等的最少秒数',
                 '示例：`[2,1,3,3,2]` → `2`；视频用 `[2,1,3,3,2,1,3]` → `1`'],
        quote='考虑把数字 x「扩散」到其它位置，那么每一秒 x 都可以向左右扩散一位。多个相同数字 x 同时扩散，耗时就取决于相距最远的两个相邻的 x。',
        quote_src='—— 灵茶山艾府题解',
        idea=['最终的数一定在 `nums` 中，枚举它；用哈希表收集每个数的下标',
              '相邻两个 `x` 相距 `d`，从两头同时扩散，`d // 2` 秒碰头',
              '环形：往列表末尾补 `首位 + n`，就变成了普通的相邻间距'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错点：环形首尾也相邻，别忘了补 `a[0] + n`',
                 '先对所有间距取最大、再取最小，==最后统一除 2==',
                 '只有一个相同数时，间距就是 `n`，耗时 `n // 2`'],
    ),
)
