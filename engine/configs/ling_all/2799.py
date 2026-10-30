NUMS = [1, 3, 1, 2, 2, 3]


def _brute(a):
    k = len(set(a))
    return sum(1 for i in range(len(a)) for j in range(i, len(a)) if len(set(a[i:j + 1])) == k)


def _r(S):
    if 'cnt' not in S or 'x' not in S:
        return None
    # 窗口长度 = cnt 的总数；第 10–12 行 out 已减但 left 还没右移
    return S['left'] + sum(S['cnt'].values()) - 1 + (1 if S.get('_line') in (10, 11, 12) else 0)


def _color(S, i, v):
    if 'x' in S and S.get('_line') == 14 and i < S['left']:
        return 'green'
    return None


def _top(S):
    if 'k' not in S:
        return '先求整个数组的不同元素个数 k'
    if 'x' not in S:
        return f"`k = {S['k']}`：子数组越长，不同元素越多 → ==越长越合法=="
    l, r = S['left'], _r(S)
    if S.get('_line') == 14:
        if l == 0:
            return '还没有合法的左端点：本轮 ==0== 个'
        return f"右端点 {r}：左端点取 `0..{l - 1}` 都合法 → 本轮 =={l}== 个"
    kinds = sum(1 for v in S['cnt'].values() if v > 0)
    return f"窗口 `{S['nums'][l:r + 1]}` 有 {kinds} 种元素（需要 {S['k']} 种）"


def _while(S, B, ret):
    r = _r(S)
    w = S.nums[S.left:r + 1]
    if len(S.cnt) == S.k:
        return f'`len(cnt) == k = {S.k}`：`{w}` 是完全子数组 → 右移 left'
    if S.left > 0 and len(set(S.nums[S.left - 1:r + 1])) == S.k:
        return f'`len(cnt) = {len(S.cnt)} < {S.k}`：`{w}` ==恰好不合法==（再往左一位就合法）'
    return f'`len(cnt) = {len(S.cnt)} < {S.k}`：种类还不够，不用缩小'


CONFIG = dict(
    num=2799, title='统计完全子数组的数目', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='不定长滑动窗口 · 越长越合法',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针'],
    code='''
class Solution:
    def countCompleteSubarrays(self, nums: List[int]) -> int:
        k = len(set(nums))
        cnt = defaultdict(int)  # 比 Counter() 快
        ans = left = 0
        for x in nums:
            cnt[x] += 1
            while len(cnt) == k:
                out = nums[left]
                cnt[out] -= 1
                if cnt[out] == 0:
                    del cnt[out]
                left += 1
            ans += left
        return ans
''',
    call=f'Solution().countCompleteSubarrays({NUMS})',
    expect=_brute(NUMS),
    views=[
        dict(type='text', fn=_top, size=28, h=80),
        dict(type='array', var='nums', label='nums（框 = 窗口，绿 = 本轮计入答案的左端点 0..left−1）',
             pointers={'left': 'blue', _r: 'pink'}, pointer_labels={_r: 'right'}, window=('left', _r),
             color=_color, cell=110, h=280),
        dict(type='map', var='cnt', label='cnt（窗口内每个元素的次数）', fmt=lambda k, v: f'{k}: {v}', h=150, font=34),
    ],
    watch=[('k', 'k', 'orange'), ('left', 'left', 'blue'), 'x', ('ans', 'ans', 'green')],
    skip=['out = nums[left]'],
    captions={
        'k = len(set(nums))': '整个数组有 `k = {k}` 种不同元素：子数组也要有 {k} 种',
        'cnt = defaultdict': '`cnt` 统计窗口内每个元素的次数',
        'ans = left = 0': '`ans = 0`，窗口左端点 `left = 0`',
        'for x in nums': lambda S, B, r: ('右端点枚举完毕' if 'x' in B and _r(B) == len(S.nums) - 1
                                          else f'枚举右端点：`{S.x}` 进入窗口'),
        'cnt[x] += 1': '`cnt[{x}]` → {cnt[x]}',
        'while len(cnt) == k': _while,
        'cnt[out] -= 1': '左端 `{out}` 离开窗口：`cnt[{out}]` → {cnt[out]}',
        'if cnt[out] == 0': lambda S, B, r: (f'窗口里没有 {S.out} 了' if S.cnt[S.out] == 0 else f'窗口里还有 {S.out}，种数不变'),
        'del cnt[out]': '删掉 `{out}` → 只剩 {len(cnt)} 种',
        'left += 1': '`left` → {left}',
        'ans += left': lambda S, B, r: ('`left = 0`：还没有完全子数组，`ans` 不变' if S.left == 0
                                        else f'`[{S.left - 1}, {_r(S)}]` 合法，更长的也合法 → `ans += {S.left}` = =={S.ans}=='),
        'return ans': '一共 =={ret}== 个完全子数组',
    },
    max_steps=70,
    cards=dict(
        one_liner='k = 整个数组的种类数；窗口种类到 k 就缩，ans += left',
        complexity='时间 `O(n)`，空间 `O(k)`',
        problem=['==完全子数组==：不同元素个数 = 整个 `nums` 的不同元素个数',
                 '求完全子数组的个数',
                 '示例：`[1,3,1,2,2]` → `4`；`[5,5,5,5]` → `10`',
                 f'本视频：`{NUMS}` → `{_brute(NUMS)}`'],
        quote='当右端点固定在 right 时，左端点在 0,1,2,…,left−1 的所有子数组都是满足要求的，这一共有 left 个。',
        quote_src='—— 灵茶山艾府题解',
        idea=['题干的「整个数组」指 `nums`，先算 `k = len(set(nums))`',
              '子数组越长种类越多：窗口种类 `== k` 就右移 left',
              '退出循环时 `[left−1, right]` 合法 → 左端点 `0..left−1` 都合法'],
        summary=['时间 `O(n)`：left 总共最多右移 n 次',
                 '从未进入内层循环时 `left = 0`，加 0 不影响答案',
                 '`cnt[out]` 到 0 要 `del`，否则 `len(cnt)` 不会变小',
                 '同类：1358、2062、3325（越长越合法）'],
    ),
)
