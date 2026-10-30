NUMS = [1, 3, 2, 3, 3]
K = 2

TRACK = '''
class KList(list):  # 快照用的普通 list（带上下标 k）
    pass

class TList(list):  # 只用于动画：记录 for 循环当前遍历到的下标 k
    def __iter__(self):
        for k in range(len(self)):
            self.k = k
            yield list.__getitem__(self, k)
        self.k = None

    def __deepcopy__(self, memo):
        c = KList(list.copy(self))
        c.k = getattr(self, 'k', -1)
        return c
'''


def _r(S):
    if S.get('_line', 0) < 5:
        return None
    k = getattr(S.get('nums'), 'k', None)
    return k if isinstance(k, int) and k >= 0 else None


def _left(S):
    return S.get('left') if _r(S) is not None else None


def _settled(S):
    line = S.get('_line', 0)
    return line == 12 or (line == 8 and S.get('cnt_mx') != K)


def _color(S, i, v):
    r = _r(S)
    if r is None:
        return 'orange' if v == max(NUMS) and S.get('_line', 0) >= 4 else None
    if i < S.get('left', 0) and i <= r and _settled(S):
        return 'green'
    if v == max(NUMS) and S.get('left', 0) <= i <= r:
        return 'orange'
    return None


def _dim(S, i, v):
    r = _r(S)
    return r is not None and i > r


def _formula(S, B):
    r = _r(S)
    if r is None:
        if 'mx' in S and S.get('_line', 0) >= 4:
            return f'`mx = max(nums) = {S.mx}`，要统计 `{S.mx}` 至少出现 `k = {K}` 次的子数组'
        return '先求整个数组的最大值 `mx`'
    left = S.get('left', 0)
    if not _settled(S):
        if S.get('cnt_mx') == K and S.get('_line', 0) in (8, 9, 10, 11):
            return f'窗口 `[{left}, {r}]` 里有 `{K}` 个 mx，仍然合法 → ==继续右移 left=='
        return f'`x = {S.x}` 进入窗口，`cnt_mx = {S.cnt_mx}`'
    if left == 0:
        return f'右端点 `right = {r}`：窗口里 `mx` 不足 `{K}` 个，==没有==合法左端点'
    subs = ', '.join(str(NUMS[l:r + 1]).replace(' ', '') for l in range(left))
    return f'右端点 `right = {r}`：左端点 `0~{left - 1}` 都合法（==绿色==）→ {subs}'


def _while(S, B, ret):
    if S.cnt_mx == K:
        return f'窗口里 `mx` 出现 `{S.cnt_mx}` 次 `== k` → 太“合法”了，==右移 left== 直到不足 k 次'
    return f'`cnt_mx = {S.cnt_mx} < k` → 窗口 `[{S.left}, {_r(S)}]` 不满足，停止收缩'


CONFIG = dict(
    num=2962, title='统计最大元素出现至少 K 次的子数组', difficulty='Medium', category='滑动窗口',
    author='灵茶山艾府', technique='「越长越合法」型滑动窗口',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution:
    def countSubarrays(self, nums: List[int], k: int) -> int:
        mx = max(nums)
        ans = cnt_mx = left = 0
        for x in nums:
            if x == mx:
                cnt_mx += 1
            while cnt_mx == k:
                if nums[left] == mx:
                    cnt_mx -= 1
                left += 1
            ans += left
        return ans
''',
    setup=TRACK,
    call=f'Solution().countSubarrays(TList({NUMS}), {K})',
    expect=6,
    views=[
        dict(type='array', var='nums', h=230,
             label='nums（橙 = 窗口中的 mx，绿 = 当前右端点的合法左端点，青框 = 窗口 [left, right]）',
             pointers={'left': 'blue', _r: 'pink'}, pointer_labels={_r: 'right'},
             window=(_left, _r), color=_color, dim=_dim, cell=110),
        dict(type='text', fn=_formula, size=26, h=120, lines=3),
    ],
    watch=[('x', 'x', 'pink'), ('left', 'left', 'blue'), ('cnt_mx', 'cnt_mx', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'mx = max(nums)': '注意：最大元素指==整个数组==的最大值，`mx = {mx}`',
        'ans = cnt_mx = left': '`cnt_mx`：窗口里 `mx` 的个数；`left`：窗口左端点',
        'for x in nums': lambda S, B, ret: (f'右端点移到 `right = {_r(S)}`，`x = {S.x}` 进入窗口' if _r(S) is not None
                                            else '右端点枚举完毕'),
        'if x == mx': lambda S, B, ret: (f'`x = {S.x} == mx` → 计数加一' if S.x == S.mx
                                         else f'`x = {S.x} ≠ mx = {S.mx}` → 计数不变'),
        'cnt_mx += 1': '`cnt_mx = {cnt_mx}`',
        'while cnt_mx == k': _while,
        'if nums[left] == mx': lambda S, B, ret: (f'`nums[{S.left}] = {S.nums[S.left]}` 是 mx → 移出后计数减一'
                                                  if S.nums[S.left] == S.mx
                                                  else f'`nums[{S.left}] = {S.nums[S.left]}` 不是 mx → 计数不变'),
        'cnt_mx -= 1': '`cnt_mx = {cnt_mx}`：窗口里的 mx 少了一个',
        'left += 1': '`left` → {left}',
        'ans += left': lambda S, B, ret: (
            f'`[left−1, right]` 合法，==更长的也合法== → 左端点 `0~{S.left - 1}` 共 `{S.left}` 个，`ans = {S.ans}`'
            if S.left else '`left = 0`：以它为右端点的子数组==都不合法==，`ans` 不变'),
        'return ans': '返回 `ans = {ret}`',
    },
    cards=dict(
        one_liner='窗口刚好不合法时，左边多出来的 left 个起点全都合法',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['统计子数组个数：==整个数组的最大值==在子数组中至少出现 `k` 次',
                 '示例：`nums = [1,3,2,3,3], k = 2` → `6`',
                 '`[1,3,2,3] [1,3,2,3,3] [3,2,3] [3,2,3,3] [2,3,3] [3,3]`'],
        quote='当右端点固定在 right 时，左端点在 0,1,2,…,left−1 的所有子数组都是满足要求的，这一共有 left 个，加到答案中。',
        quote_src='—— 灵茶山艾府题解',
        idea=['子数组==越长越合法==：包含的 mx 越多越能满足要求',
              '`cnt_mx == k` 时不断右移 `left`，直到 mx 的个数 ==小于 k==',
              '此时 `[left−1, right]` 合法，再往左延长也合法 → `ans += left`'],
        result='右端点为 3 时加 2，为 4 时加 4，共 `6` 个 ✓',
        summary=['时间 `O(n)`：`left` 总共最多右移 n 次',
                 '易错：mx 是==整个数组==的最大值，不是子数组的',
                 '易错：内层循环条件是 `cnt_mx == k`，退出后加的是 `left` 而不是 `right−left+1`',
                 '模板：「越长越合法」→ 收缩到刚好不合法，答案加 `left`'],
    ),
)
