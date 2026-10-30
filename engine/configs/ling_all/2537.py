CODE = '''
class Solution:
    def countGood(self, nums: List[int], k: int) -> int:
        cnt = defaultdict(int)  # 比 Counter() 快
        ans = left = pairs = 0
        for x in nums:
            pairs += cnt[x]
            cnt[x] += 1
            while pairs >= k:
                cnt[nums[left]] -= 1
                pairs -= cnt[nums[left]]
                left += 1
            ans += left
        return ans
'''
_L = CODE.strip('\n').split('\n')


def _ln(txt):
    return [i + 1 for i, s in enumerate(_L) if txt in s][0]


def _right(S):
    """当前窗口右端点（x 在 nums 里的下标）"""
    if 'left' not in S or 'cnt' not in S or 'x' not in S:
        return None
    w = sum(S['cnt'].values())
    ln = S['_line']
    if ln in (_ln('for x in nums'), _ln('pairs += cnt[x]'), _ln('cnt[nums[left]] -= 1'), _ln('pairs -= cnt')):
        return S['left'] + w
    return S['left'] + w - 1


class _Named:
    def __init__(self, f, name):
        self.f, self.name = f, name

    def __call__(self, S):
        return self.f(S)

    def __str__(self):
        return self.name

    __repr__ = __str__


def _left(S):
    return S['left'] if 'left' in S and 'x' in S else None


def _txt(S):
    if 'pairs' not in S:
        return '`pairs` = 窗口里相等数对的个数，目标：`pairs >= k` 才合法'
    x = S.get('x')
    ln = S['_line']
    if x is None:
        return ''
    if ln in (_ln('while pairs'),) and S['pairs'] >= S['k']:
        return f"`pairs = {S['pairs']} >= k = {S['k']}`：窗口合法，==缩小左端点=="
    return f"`pairs = {S['pairs']}`　`left = {S['left']}`　已累计 `ans = {S['ans']}`"


CONFIG = dict(
    num=2537, title='统计好子数组的数目', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='不定长滑窗 · 越长越合法',
    tags=['灵神题单', '难度分 1892'],
    code=CODE,
    call='Solution().countGood([3,1,4,3,2,2,4], 2)',
    expect=4,
    views=[
        dict(type='array', var='nums', label='nums（框 = 窗口 [left, right]，right 是正在移入的 x）', cell=100, h=250,
             pointers={'left': 'blue', _Named(_right, 'right'): 'pink'}, window=(_left, _right)),
        dict(type='map', var='cnt', label='cnt（窗口内每个数的出现次数）', fmt=lambda k, v: f'{k}: {v}', h=170, font=34),
        dict(type='text', h=100, size=30, fn=_txt),
    ],
    watch=[('x', 'x', 'pink'), ('left', 'left', 'blue'), ('pairs', 'pairs', 'orange'), ('k', 'k'), ('ans', 'ans', 'green')],
    captions={
        'cnt = defaultdict': '`cnt` 记窗口内每个数出现几次',
        'ans = left = pairs = 0': '`pairs` = 窗口里 ==相等数对== 的个数；`left` = 窗口左端点',
        'for x in nums': lambda S, B, ret: ('遍历结束，所有右端点都枚举完了' if 'x' in S and S.left + sum(S.cnt.values()) == len(S.nums) else f'枚举右端点：`x = {S.x}` 准备移入窗口'),
        'pairs += cnt[x]': '窗口里已有 `{cnt[x]}` 个 `{x}`，新来的 `{x}` 和它们各成一对 → `pairs` 增加 `{cnt[x]}`，变成 ==`{pairs}`==',
        'cnt[x] += 1': '`{x}` 的次数加一 → `cnt[{x}] = {cnt[x]}`',
        'while pairs >= k': lambda S, B, ret: (f'`pairs = {S.pairs} >= k = {S.k}`：窗口已合法，可以缩左端点' if S.pairs >= S.k
                                               else f'`pairs = {S.pairs} < k = {S.k}`：不合法了，停止缩小'),
        'cnt[nums[left]] -= 1': '移出 `nums[{left}] = {nums[left]}`：先把它的次数减一 → `{cnt[nums[left]]}`',
        'pairs -= cnt[nums[left]]': '它和窗口里剩下的 `{cnt[nums[left]]}` 个同值元素各成一对，一起消失 → `pairs = {pairs}`',
        'left += 1': '`left` 右移到 `{left}`',
        'ans += left': lambda S, B, ret: ('`left = 0`：连 `[0, right]` 都不合法 → 这个右端点贡献 `0`' if S.left == 0 else f'退出循环时 `[left, right]` 不合法，但上一轮的 `[left-1, right]` 合法 → ==越长越合法==，起点取 `0 ~ {S.left - 1}` 都行，共 `{S.left}` 个 → `ans = {S.ans}`'),
        'return ans': '返回 `{ans}`',
    },
    max_steps=90,
    cards=dict(
        one_liner='枚举右端点，缩到刚好不合法：左边 left 个起点全部合法',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['数组里至少有 `k` 对下标 `(i, j)`，`i < j` 且 `arr[i] == arr[j]` 的子数组叫==好子数组==',
                 '统计 `nums` 里好子数组的个数',
                 '示例：`nums = [3,1,4,3,2,2,4], k = 2` → `4`'],
        quote='如果窗口中有 c 个元素 x，再进来一个 x，会新增 c 个相等数对。如果窗口中有 c 个元素 x，再去掉一个 x，会减少 c-1 个相等数对。',
        quote_src='—— 灵茶山艾府题解',
        idea=['哈希表 `cnt` 维护窗口里每个数的次数，`pairs` 维护相等数对数',
              '子数组越长越容易好 → 右端点固定时，合法的左端点是一个前缀 `0 ~ left-1`',
              '外层枚举右端点；`pairs >= k` 就缩左端点，退出后 `ans += left`'],
        summary=['时间 `O(n)`：left 总共只右移 n 次',
                 '易错：移出元素时==先减次数再减 pairs==（减的是 c-1，即减完之后的 cnt）',
                 '`ans += left` 统计的是右端点固定时的合法左端点个数',
                 '同类题：2962、3325、3258 等“越长越合法”滑窗'],
    ),
)
