NUMS, K = [2, 2, 3, 1, 2, 4], 6


def _color(S, i, v):
    if 'i' not in S:
        return None
    if S['left'] <= i <= S['i']:
        return 'green' if S['_line'] == 12 else 'blue'
    return None


def _top(S):
    if 'i' not in S:
        return f'`k = {K}`：不同元素和越大越容易 ≥ k → ==越长越合法==，求最短'
    l, i = S['left'], S['i']
    keys = sorted(x for x, c in S['cnt'].items() if c > 0)
    expr = ' + '.join(map(str, keys)) if keys else '0'
    ok = S['s'] >= K
    return f"窗口 `[{l}, {i}]` 的不同元素：`{expr} = {S['s']}` " + (f'≥ {K}，==满足==' if ok else f'< {K}')


def _while(S, B, ret):
    if S.s >= S.k:
        return f'`s = {S.s} ≥ {S.k}`：窗口满足要求 → 先更新答案，再试着缩短'
    return f'`s = {S.s} < {S.k}`：窗口不满足（或已缩到不满足），继续扩右端点'


CONFIG = dict(
    num=3795, title='不同元素和至少为 K 的最短子数组长度', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='不定长滑动窗口 · 求最短',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针'],
    code='''
class Solution:
    def minLength(self, nums: List[int], k: int) -> int:
        cnt = defaultdict(int)
        s = left = 0
        ans = inf

        for i, x in enumerate(nums):
            # 1. 入
            cnt[x] += 1
            if cnt[x] == 1:
                s += x

            while s >= k:
                # 2. 更新答案
                ans = min(ans, i - left + 1)

                # 3. 出
                out = nums[left]
                cnt[out] -= 1
                if cnt[out] == 0:
                    s -= out
                left += 1

        return ans if ans < inf else -1
''',
    call=f'Solution().minLength({NUMS}, {K})',
    expect=2,
    views=[
        dict(type='text', fn=_top, size=28, h=80),
        dict(type='array', var='nums', label='nums（框 = 窗口 [left, i]，绿 = 正在用来更新答案）',
             pointers={'left': 'blue', 'i': 'pink'}, window=('left', 'i'), color=_color, cell=120, h=300),
        dict(type='map', var='cnt', label='cnt（窗口内每个元素的出现次数）', fmt=lambda k, v: f'{k}: {v}', h=150, font=34),
    ],
    watch=[('left', 'left', 'blue'), ('i', 'i', 'pink'), ('s', 's', 'orange'), 'out', ('ans', 'ans', 'green')],
    captions={
        'cnt = defaultdict': '`cnt` 记录窗口内每个元素出现几次',
        's = left = 0': '`s`：窗口内==不同==元素之和；`left = 0`',
        'ans = inf': '`ans = inf`，表示还没找到',
        'for i, x in': lambda S, B, r: ('右端点枚举完毕' if 'i' in B and B.i == S.i
                                        else f'枚举右端点 `i = {S.i}`，`x = {S.x}` 进入窗口'),
        'cnt[x] += 1': '`cnt[{x}]` → {cnt[x]}',
        'if cnt[x] == 1': lambda S, B, r: (f'`cnt[{S.x}] == 1`：{S.x} ==第一次==出现在窗口里，要计入和' if S.cnt[S.x] == 1
                                           else f'`cnt[{S.x}] = {S.cnt[S.x]}`：窗口里已经有 {S.x}，==重复的不计入=='),
        's += x': '`s = {B.s} + {x} = {s}`',
        'while s >= k': _while,
        'ans = min(': '窗口 `[{left}, {i}]` 长 `{i - left + 1}`：`ans = min({B.ans}, {i - left + 1})` = =={ans}==',
        'out = nums[left]': '左端点 `nums[{left}] = {out}` 准备离开窗口',
        'cnt[out] -= 1': '`cnt[{out}]` → {cnt[out]}',
        'if cnt[out] == 0': lambda S, B, r: (f'`cnt[{S.out}] == 0`：窗口里==没有 {S.out} 了==，要从和里减掉' if S.cnt[S.out] == 0
                                             else f'`cnt[{S.out}] = {S.cnt[S.out]}`：窗口里还有 {S.out}，和不变'),
        's -= out': '`s = {B.s} − {out} = {s}`',
        'left += 1': '`left` → {left}',
        'return ans if': '最短长度为 =={ret}==',
    },
    cards=dict(
        one_liner='209 题的滑窗 + 哈希表计数：只有次数 0↔1 时才改窗口和',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给数组 `nums` 和整数 `k`，求子数组的==最小长度==',
                 '要求子数组中==不同==值之和（重复只算一次）至少为 `k`；不存在返回 `-1`',
                 '示例：`[2,2,3,1], k = 4` → `2`；本视频 `[2,2,3,1,2,4], k = 6` → `2`'],
        quote='元素 x 进入窗口后，如果 x 在窗口内的出现次数==等于 1==，把 x 加到窗口元素和中。元素 x 离开窗口后，如果出现次数==等于 0==，把 x 从窗口元素和中减掉。',
        quote_src='—— 灵茶山艾府题解',
        idea=['元素都是正数：窗口越长，不同元素和越大 → ==越长越合法==',
              '模板三步：入 → 满足时更新答案 → 出，直到不满足',
              '重复元素不能重复计入，所以用 `cnt` 判断第一次/最后一次'],
        summary=['时间 `O(n)`：left 总共最多右移 n 次；空间 `O(n)`',
                 '易错：更新答案要放在 while ==里面==，出窗口之前',
                 '易错：出窗口时先 `cnt[out] -= 1` 再判断是否为 0',
                 '`ans` 初始 `inf`，最后没找到要返回 `-1`',
                 '前置题：209 长度最小的子数组'],
    ),
)
