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


def _pre(S):
    pre = [0]
    for v in S['nums']:
        pre.append(pre[-1] + v)
    return pre


def _fresh(S):
    """pre_sum 已经加上了当前的 x"""
    p = _cur(S)
    return p is not None and 'pre_sum' in S and S['pre_sum'] == _pre(S)[p + 1]


def _prev_min(S):
    """今天之前的最低价 = min(s[0..p])，也就是本轮更新 min_pre_sum 之前的值"""
    return min(_pre(S)[:_cur(S) + 1])


def _best_l(S):
    if not _fresh(S):
        return None
    pre, m = _pre(S), _prev_min(S)
    return max(k for k in range(_cur(S) + 1) if pre[k] == m)


def _best_r(S):
    return _cur(S) if _best_l(S) is not None else None


def _profit(S):
    if not _fresh(S):
        return ''
    a, b = S['pre_sum'], _prev_min(S)
    return f'利润 = 今天的价 `{a}` − 之前最低价 `{b}` = =={a - b}==（以 `x` 结尾的最大子数组和）'


def _chart(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    pre = _pre(S)
    n = len(pre) - 1
    p = _cur(S)
    if p is not None:
        j, seen = p + 1, p                      # 今天是 s[j]；s[0..p] 是之前的价格
    elif getattr(S['nums'], 'pos', None) is not None:
        j, seen = None, n                       # 遍历结束
    else:
        j, seen = None, (0 if 'min_pre_sum' in S else -1)
    lo, hi = min(pre), max(pre)
    cv.text((x0 + 18, y0 + 4), '前缀和 = 股价折线   蓝 = 之前的价格   粉 = 今天   绿线 = 之前的最低价', 22, T['muted'], bold=True)
    L, R = x0 + 80, x1 - 50
    top, bot = y0 + 64, y1 - 40

    def X(k):
        return L + (R - L) * k / n

    def Y(v):
        return bot - (bot - top) * (v - lo) / max(1, hi - lo)
    for v in range(lo, hi + 1):
        cv.line([(L - 16, Y(v)), (R + 16, Y(v))], T['border'], 1)
        if (v - lo) % 2 == 0 or hi - lo <= 8:
            cv.text((L - 30, Y(v)), str(v), 20, T['dim'], anchor='rm', mono=True)
    cv.line([(X(k), Y(pre[k])) for k in range(n + 1)], T['dim'], 3)
    mn = S.get('min_pre_sum')
    if mn is not None:
        cv.dashed((L - 16, Y(mn)), (R + 16, Y(mn)), T['green'], 3)
        cv.text((L - 14, Y(mn) - 6), 'min_pre_sum', 18, T['green'], anchor='lb', bold=True)
    fresh = _fresh(S)
    if fresh:
        xa, pm = X(j), _prev_min(S)
        if pre[j] != pm:
            cv.arrow((xa + 26, Y(pm)), (xa + 26, Y(pre[j]) + (8 if pre[j] > pm else -8)), T['orange'], 4, 14)
        cv.text((xa + 36, (Y(pm) + Y(pre[j])) / 2), f'{pre[j] - pm}', 26, T['orange'], anchor='lm', bold=True)
    for k in range(n + 1):
        cx, cy = X(k), Y(pre[k])
        r, c = 10, None
        if k == j and fresh:
            r, c = 14, T['pink']
        elif k <= seen:
            c = T['blue']
        if mn is not None and k <= seen and pre[k] == mn and not (k == j and fresh):
            r, c = 13, T['green']
        if c:
            cv.d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=c)
        else:
            cv.d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=T['panel'], outline=T['dim'], width=3)
        cv.text((cx, bot + 12), f's{k}', 18, T['pink'] if k == j else T['muted'], anchor='mt', mono=True)


CONFIG = dict(
    num=53, title='最大子数组和', difficulty='Medium', category='普通数组',
    author='灵茶山艾府', technique='前缀和 + 贪心（买卖股票视角）',
    code='''
class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        ans = -inf
        min_pre_sum = pre_sum = 0
        for x in nums:
            pre_sum += x  # 当前的前缀和
            ans = max(ans, pre_sum - min_pre_sum)  # 减去前缀和的最小值
            min_pre_sum = min(min_pre_sum, pre_sum)  # 维护前缀和的最小值
        return ans
''',
    setup=SETUP,
    call='Solution().maxSubArray(Nums([-2, 1, -3, 4, -1, 2, 1, -5, 4]))',
    expect=6,
    views=[
        dict(type='array', var='nums', label='nums', cell=76, pointers={_cur: 'pink'}, pointer_labels={_cur: 'x'},
             window=(_best_l, _best_r), window_color='orange'),
        dict(type='text', fn=_profit),
        dict(type='custom', draw=_chart, h=360),
    ],
    watch=['x', 'pre_sum', ('min_pre_sum', 'min_pre_sum', 'green'), ('ans', 'ans', 'orange')],
    captions={
        'ans = -inf': '答案可能是负数（比如全是负数），所以初始化成 `-inf`',
        'min_pre_sum = pre_sum = 0': '前缀和从 `s0 = 0` 开始：空前缀也能当「买入价」',
        'for x in nums': lambda S, B, ret: (f'下一天：`x = {S.x}`' if _cur(S) is not None else '`nums` 遍历完了'),
        'pre_sum += x': lambda S, B, ret: f'`pre_sum = {B.pre_sum} + ({S.x}) = {S.pre_sum}`：今天的股价（卖出价）',
        'ans = max': lambda S, B, ret: (
            f'今天卖出最多赚 `{S.pre_sum} − ({S.min_pre_sum}) = {S.pre_sum - S.min_pre_sum}`'
            f'（子数组 `nums[{max(k for k in range(_cur(S) + 1) if _pre(S)[k] == S.min_pre_sum)}..{_cur(S)}]`）'
            f' → `ans = {S.ans}`'),
        'min_pre_sum = min': lambda S, B, ret: (
            f'今天的价 `{S.pre_sum}` 更低 → `min_pre_sum = {S.min_pre_sum}`。==先算利润、再更新最低价=='
            if S.min_pre_sum != B.min_pre_sum else
            f'最低价还是 `{S.min_pre_sum}`（今天的 `{S.pre_sum}` 不更低）'),
        'return ans': '最大子数组和 =={ret}==',
    },
    cards=dict(
        one_liner='子数组和 = 两个前缀和之差：今天的股价减去之前的最低价',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['找出和最大的==连续子数组==（至少含一个元素），返回它的和',
                 '示例：`nums = [-2,1,-3,4,-1,2,1,-5,4]` → `6`（子数组 `[4,-1,2,1]`）'],
        quote='由于子数组的元素和等于两个前缀和的差，所以求出 nums 的前缀和，问题就变成 121. 买卖股票的最佳时机 了。本题子数组不能为空，相当于一定要交易一次。',
        quote_src='—— 灵茶山艾府题解「方法一：前缀和 + 贪心」',
        idea=['前缀和 = 股价；一边遍历一边维护==前缀和的最小值==（最低买入价）',
              '当前前缀和 − 最小前缀和 = ==以当前元素结尾==的最大子数组和（今天卖出的最大利润）',
              '==先算利润，再更新最低价==：相当于不能同一天买入又卖出（子数组不能为空）'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`ans` 初始化成 `-inf`：全是负数时答案是负的',
                 '顺序反了会把空子数组的和 `0` 算进答案',
                 '不能直接用「最大前缀和 − 最小前缀和」：最大的可能在左边（如 `[1,-2]`）',
                 '题解方法二：动态规划 `f = max(f, 0) + x`，`ans = max(ans, f)`'],
    ),
)
