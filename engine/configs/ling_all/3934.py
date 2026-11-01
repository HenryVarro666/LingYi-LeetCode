def _pair(S):
    nums = S['nums']
    sa = S.get('sa')
    if not sa:
        return '把每个数拆成 3 个字节，用后缀数组库函数排序后缀' if S['_line'] <= 11 else ''
    if 'rk' in S and S['rk'] > 0 and 'j' in S and S['_line'] in range(35, 41):
        a, b = sa[S['rk']], sa[S['rk'] - 1]
        return f'排名 {S["rk"]} 的后缀 `{nums[a:]}` vs 排名 {S["rk"] - 1} 的后缀 `{nums[b:]}`，已匹配 h = =={S["h"]}=='
    return '按字典序排好的后缀：' + ' < '.join(str(nums[p:]) for p in sa)


def _ih(S):
    return S['i'] + S['h'] if 'j' in S and 31 < S['_line'] < 39 and S['i'] + S['h'] < S['n'] else None


def _jh(S):
    return S['j'] + S['h'] if 'j' in S and 34 < S['_line'] < 39 and S['j'] + S['h'] < S['n'] else None


def _rk_ptr(S):
    return S['rk'] if 'rk' in S and S['_line'] <= 41 else None


CONFIG = dict(
    num=3934, title='最短唯一子数组', difficulty='Hard', category='字符串',
    author='灵茶山艾府', technique='后缀数组 + 高度数组（Go 原文转写）',
    tags=['灵神题单', '字符串', '难度分 2163'],
    setup='''
def suffix_array(b):
    # 对应 Go 里 suffixarray.New(tmp).sa：字节串所有后缀按字典序排序后的起点
    return sorted(range(len(b)), key=lambda i: b[i:])
''',
    code='''
class Solution:
    def smallestUniqueSubarray(self, nums: List[int]) -> int:
        n = len(nums)
        # 把 1 个 int 拆成 3 个 byte（题目保证 nums[i] <= 1e5），从而可以调用库函数计算后缀数组
        tmp = bytearray()
        for x in nums:
            tmp += bytes([x >> 16 & 255, x >> 8 & 255, x & 255])

        _sa = suffix_array(bytes(tmp))

        sa = []
        for p in _sa:
            if p % 3 == 0:  # 是 3 的倍数的 _sa[i] 就对应着 nums 的 sa[i]
                sa.append(p // 3)

        # 计算后缀名次数组
        # 后缀 nums[i:] 位于后缀字典序中的第 rank[i] 个
        # 相当于 sa 的反函数，即 rank[sa[i]] = i
        rank = [0] * n
        for i, p in enumerate(sa):
            rank[p] = i

        # 计算高度数组（也叫 LCP 数组）
        # height[0] = 0（哨兵）
        # height[i] = LCP(nums[sa[i]:], nums[sa[i-1]:])  (i > 0)
        # 从 LCP0 到 LCP1，我们只去掉了 nums[0] 和 nums[sa[rank[0]-1]] 这两个数
        # 所以 LCP1 >= LCP0 - 1
        # 这样就能加快 LCP 的计算了（类似滑动窗口）
        height = [0] * n
        h = 0
        for i, rk in enumerate(rank):
            if h > 0:
                h -= 1
            if rk > 0:
                j = sa[rk - 1]
                while i + h < n and j + h < n and nums[i + h] == nums[j + h]:
                    h += 1
            height[rk] = h

        ans = n
        for i, h in enumerate(height):
            # 对于后缀 nums[sa[i]:]，其长为 uniqueLength 的前缀是唯一的
            uniqueLength = h + 1
            if i < n - 1:
                uniqueLength = max(h, height[i + 1]) + 1
            # 注意 uniqueLength 不能超过后缀 nums[sa[i]:] 的长度
            if uniqueLength <= n - sa[i]:
                ans = min(ans, uniqueLength)
        return ans
''',
    call='Solution().smallestUniqueSubarray([1, 1, 2, 2, 1])',
    expect=2,
    views=[
        dict(type='text', fn=_pair, size=22),
        dict(type='array', var='nums', label='nums（蓝 = 后缀 i 的比较位置，粉 = 前一名后缀的比较位置）', cell=84, h=150,
             pointers={_ih: 'blue', _jh: 'pink'}, pointer_labels={_ih: 'i+h', _jh: 'j+h'}),
        dict(type='array', var='sa', label='sa（第 k 小的后缀从哪里开始）', cell=84, h=150,
             pointers={_rk_ptr: 'blue'}, pointer_labels={_rk_ptr: 'rk'}),
        dict(type='array', var='height', label='height（与前一名后缀的 LCP）', cell=84, h=150,
             color=lambda S, k, v: 'green' if 'uniqueLength' in S and 'i' in S and k == S['i'] and S['_line'] >= 45 else None),
    ],
    watch=[('i', 'i', 'blue'), ('rk', 'rk', 'cyan'), ('h', 'h', 'orange'), ('uniqueLength', 'uniqueLength', 'pink'), ('ans', 'ans', 'green')],
    skip=['n = len(nums)', 'tmp = bytearray()', 'rank = [0] * n', 'height = [0] * n', 'for x in nums', 'h = 0', 'for p in _sa', 'tmp += bytes', 'if p % 3 == 0', 'for i, p in enumerate(sa)', 'h += 1',
          'for i, h in enumerate(height)', 'uniqueLength = h + 1', 'if i < n - 1', 'uniqueLength = max', 'sa = []'],
    captions={
        '_sa = suffix_array': '每个数拆成 3 个字节 → `{list(tmp)}`；对字节串求后缀数组 `_sa = {_sa}`（共 {len(_sa)} 个后缀）',
        'sa.append(p // 3)': '`_sa` 里 3 的倍数 `{p}` 才是 nums 的后缀起点 → `{p} // 3`，`sa = {sa}`（其余位置在某个数中间，丢掉）',
        'rank[p] = i': '`rank[{p}] = {i}`：后缀 `nums[{p}:]` 排第 {i}',
        'for i, rk in enumerate(rank)': lambda S, B, ret: ('所有后缀的 LCP 都算完了，`height` 就绪' if B.get('i') == S.i and 'rk' in B else f'处理后缀 `nums[{S.i}:]`，它排第 `rk = {S.rk}`'),
        'h -= 1': '上个后缀去掉首个数后，LCP ==至少还剩 h-1== → 回退 1 即可，`h = {h}`',
        'if rk > 0': lambda S, B, ret: ('`rk > 0`：有前一名后缀' if S.rk > 0 else '`rk = 0` 是最小后缀，没有前一名，`height` 记 0'),
        'j = sa[rk - 1]': '前一名后缀从 `j = {j}` 开始比',
        'while i + h < n': lambda S, B, ret: (f'`nums[{S.i + S.h}] = {S.nums[S.i + S.h]}` == `nums[{S.j + S.h}]` → `h` 加一再比' if S.i + S.h < S.n and S.j + S.h < S.n and S.nums[S.i + S.h] == S.nums[S.j + S.h] else f'不再相等（或到头）：LCP = `{S.h}`'),
        'height[rk] = h': '`height[{rk}] = {h}`',
        'ans = n': '`ans` 初值 `n = {n}`（整个数组一定唯一）；开始看每个后缀的最短唯一前缀',
        'if uniqueLength <= n - sa[i]': lambda S, B, ret: (f'后缀 `nums[{S.sa[S.i]}:]`：与前一名 LCP = {S.h}' + (f'，与后一名 LCP = {S.height[S.i + 1]}' if S.i < S.n - 1 else '，没有后一名') + f' → 最短唯一前缀长 `{S.uniqueLength}`；' + (f'≤ 后缀长度 {S.n - S.sa[S.i]}，可用' if S.uniqueLength <= S.n - S.sa[S.i] else f'> 后缀长度 {S.n - S.sa[S.i]}，后缀不够长，不算')),
        'ans = min': '`ans = min(.., {uniqueLength})` → `{ans}`',
        'return ans': '最短唯一子数组长度 `{ans}`',
    },
    max_steps=110,
    cards=dict(
        one_liner='每个后缀的最短唯一前缀 = 与前后邻居的最大 LCP + 1',
        complexity='时间 `O(n)`（库函数 SA-IS），空间 `O(n)`',
        problem=['求 `nums` 里 ==只出现一次== 的子数组的最小长度',
                 '示例：`[3,3,3]` → `3`；`[2,1,2,3,3]` → `1`',
                 '本视频：`[1,1,2,2,1]` → `2`'],
        quote='后缀 sa[i] 与其他后缀的最长公共前缀，来自它和 sa[i-1]、sa[i+1] 的 LCP，二者取最大',
        quote_src='—— 灵茶山艾府题解（节选）',
        idea=['后缀数组把相似的后缀排在一起，一个后缀的最长重复前缀只可能来自前一名或后一名',
              '所以后缀 `sa[i]` 的最短唯一前缀长 `max(height[i], height[i+1]) + 1`',
              '长度不能超过后缀本身（`≤ n - sa[i]`）；取所有后缀的最小值'],
        result='长度 1 的子数组都重复，`[1,2]` 等长度 2 的唯一 → 返回 `2` ✓',
        summary=['原文为 Go，已按原逻辑逐行转写；Go 里用 `suffixarray` 拿 sa，Python 在 setup 里用排序后缀的等价函数 `suffix_array` 代替（作者代码不变）',
                 '拆成 3 个字节是为了套字节串的库函数，取 `p % 3 == 0` 的位置还原',
                 '易错：`uniqueLength` 不能超过后缀长度，超过说明这个前缀不存在',
                 '也可以二分答案 + 字符串哈希，`O(n log n)`'],
    ),
)
