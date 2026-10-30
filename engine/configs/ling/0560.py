# setup 里的 Nums 只是普通 list，额外记下 for 循环当前走到的下标 pos（仅用于画图，不影响代码逻辑）
SETUP = '''
class Nums(list):
    def __init__(self, it):
        super().__init__(it)
        self.live = True
    def __iter__(self):
        return self._walk() if self.live else list.__iter__(self)
    def _walk(self):
        for i in range(len(self)):
            self.pos = i
            yield list.__getitem__(self, i)
        self.pos = len(self)
    def __deepcopy__(self, memo):
        c = Nums(list.__iter__(self))
        c.__dict__.update(self.__dict__)
        c.live = False
        return c
'''


def _cur(S):
    nums = S.get('nums')
    p = getattr(nums, 'pos', None)
    return p if p is not None and p < len(nums) else None


def _chart(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    nums, k = S['nums'], S['k']
    n = len(nums)
    pre = [0]
    for v in nums:
        pre.append(pre[-1] + v)
    p = _cur(S)
    j = p + 1 if p is not None else None
    cnt = S.get('cnt') or {}
    counted = sum(cnt.values())
    s = S.get('s')
    target = s - k if (j is not None and s == pre[j]) else None
    vals = pre + [v - k for v in pre]
    lo, hi = min(vals), max(vals)
    cv.text((x0 + 18, y0 + 4), '前缀和 s[j] 折线   蓝 = 已存进 cnt   粉 = 当前 s[j]   绿 = 能配对的 s[i]', 22, T['muted'], bold=True)
    L, R = x0 + 90, x1 - 60
    top, bot = y0 + 70, y1 - 44

    def X(jj):
        return L + (R - L) * jj / n

    def Y(v):
        return bot - (bot - top) * (v - lo) / max(1, hi - lo)
    for v in range(lo, hi + 1):
        cv.line([(L - 20, Y(v)), (R + 20, Y(v))], T['border'], 1)
        cv.text((L - 34, Y(v)), str(v), 22, T['dim'], anchor='rm', mono=True)
    cv.line([(X(jj), Y(pre[jj])) for jj in range(n + 1)], T['dim'], 3)
    if target is not None:
        cv.dashed((L - 20, Y(target)), (R + 20, Y(target)), T['green'], 3)
        cv.text((R + 24, Y(target)), f's−k', 20, T['green'], anchor='lm', bold=True)
    for jj in range(n + 1):
        cx, cy = X(jj), Y(pre[jj])
        match = target is not None and jj < j and jj < counted and pre[jj] == target
        r, c = 11, None
        if jj == j:
            r, c = 15, T['pink']
        elif match:
            r, c = 14, T['green']
        elif jj < counted:
            c = T['blue']
        if c:
            cv.d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=c)
        else:
            cv.d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=T['panel'], outline=T['dim'], width=3)
        cv.text((cx, cy - r - 4), str(pre[jj]), 22, c or T['dim'], anchor='mb', bold=True)
        cv.text((cx, bot + 14), f's[{jj}]', 20, T['pink'] if jj == j else T['muted'], anchor='mt', mono=True)


CONFIG = dict(
    num=560, title='和为 K 的子数组', difficulty='Medium', category='子串',
    author='灵茶山艾府', technique='前缀和 + 哈希表（枚举右，维护左）',
    code='''
class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        cnt = defaultdict(int)
        cnt[0] = 1  # s[0]=0 单独统计
        ans = s = 0
        for x in nums:
            s += x
            ans += cnt[s - k]
            cnt[s] += 1
        return ans
''',
    setup=SETUP,
    call='Solution().subarraySum(Nums([1, 1, -1, 1, -1]), 1)',
    expect=6,
    views=[
        dict(type='array', var='nums', label='nums（粉色箭头 = 当前的 x）', cell=76,
             pointers={_cur: 'pink'}, pointer_labels={_cur: 'x'}),
        dict(type='custom', draw=_chart, h=330),
        dict(type='map', var=lambda S: {a: b for a, b in S['cnt'].items() if b} if 'cnt' in S else None,
             label='cnt：前缀和 → 出现次数（只显示非 0 项）', fmt=lambda a, b: f's={a} 有 {b} 个', h=110),
    ],
    watch=['x', 's', ('s - k', 's - k', 'green'), ('ans', 'ans', 'orange')],
    captions={
        'cnt = defaultdict': '`cnt[v]` = 左边有几个前缀和等于 `v`；`defaultdict` 查不到时返回 0',
        'cnt[0] = 1': '空前缀 `s[0] = 0` 也要先存进去：==否则从 nums[0] 开始的子数组配不上对==',
        'ans = s = 0': '`s` 是一边走一边算的前缀和，`ans` 是答案，都从 0 开始',
        'for x in nums': lambda S, B, ret: (f'枚举右端点：取下一个数 `x = {S.x}`' if _cur(S) is not None
                                            else '`nums` 遍历完了，循环结束'),
        's += x': lambda S, B, ret: f'`s = {B.s} + ({S.x}) = {S.s}`：这就是当前的 `s[{_cur(S) + 1}]`',
        'ans += cnt': '找左边等于 `s − k = {s - k}` 的前缀和：有 `cnt[{s - k}] = {cnt[s - k]}` 个 → ==新增 {cnt[s - k]} 个子数组==，`ans = {ans}`',
        'cnt[s] += 1': '查完再把 `s = {s}` 存进去：`cnt[{s}] = {cnt[s]}`，留给右边的 `s[j]` 配对',
        'return ans': '遍历结束：和为 `k` 的子数组一共 =={ret}== 个',
    },
    cards=dict(
        one_liner='枚举右端点，用哈希表数一数左边有几个前缀和等于 s − k',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给整数数组 `nums` 和整数 `k`，统计==和为 k 的子数组==的个数',
                 '子数组 = 连续、非空的一段；`nums` 里==可能有负数==',
                 '示例：`nums = [1,1,-1,1,-1], k = 1` → `6`'],
        quote='把 `s[j] − s[i] = k` 移项，得 `s[i] = s[j] − k`。枚举当前的前缀和 `s[j]`，看看曾经有多少个前缀和等于 `s[j] − k`（配对）。',
        quote_src='—— 灵茶山艾府题解「枚举右，维护左」',
        idea=['子数组和 = 两个前缀和之差：`nums[i..j-1]` 的和 = `s[j] − s[i]`',
              '这就是「两数之和」：==枚举右边的 s[j]，用哈希表维护左边==',
              '暴力是两重循环；保留外层枚举 `j`，内层换成 `O(1)` 查表 → 不重不漏'],
        summary=['时间 `O(n)`，空间 `O(n)`：每个数只进出哈希表一次',
                 '`cnt[0] = 1` 不能漏：空前缀 `s[0] = 0`，否则「前缀本身」这种子数组算不到',
                 '==先更新 ans，再更新 cnt==：反过来时 `k = 0` 会和自己配对（如 `[2], k = 0`）',
                 '有负数 → 窗口和不单调，==不能用滑动窗口==',
                 '题解另两种写法：先建好 `s` 数组再遍历；或循环里先存 `cnt[s]` 再加 `x`'],
    ),
)
