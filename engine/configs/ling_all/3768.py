CONFIG = dict(
    num=3768, title='固定长度子数组中的最小逆序对数目', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='定长滑窗 + 离散化值域树状数组',
    tags=['树状数组', '难度分 2158'],
    code='''
class FenwickTree:
    def __init__(self, n: int):
        self.tree = [0] * (n + 1)  # 使用下标 1 到 n

    # a[i] 增加 val
    # 1 <= i <= n
    # 时间复杂度 O(log n)
    def update(self, i: int, val: int) -> None:
        t = self.tree
        while i < len(t):
            t[i] += val
            i += i & -i

    # 计算前缀和 a[1] + ... + a[i]
    # 1 <= i <= n
    # 时间复杂度 O(log n)
    def pre(self, i: int) -> int:
        t = self.tree
        res = 0
        while i > 0:
            res += t[i]
            i &= i - 1
        return res

class Solution:
    def minInversionCount(self, nums: List[int], k: int) -> int:
        # 离散化
        sorted_nums = sorted(set(nums))
        mp = {x: i for i, x in enumerate(sorted_nums, 1)}  # 树状数组下标从 1 开始
        for i, x in enumerate(nums):
            nums[i] = mp[x]

        t = FenwickTree(len(sorted_nums))
        inv = 0
        ans = inf

        for i, x in enumerate(nums):
            # 1. 入
            t.update(x, 1)
            inv += min(i + 1, k) - t.pre(x)  # 窗口大小 - (<=x 的元素个数) = (>x 的元素个数)

            left = i + 1 - k
            if left < 0:  # 尚未形成第一个窗口
                continue

            # 2. 更新答案
            ans = min(ans, inv)
            if ans == 0:  # 已经最小了，无需再计算
                break

            # 3. 出
            out = nums[left]
            inv -= t.pre(out - 1)  # < out 的元素个数
            t.update(out, -1)

        return ans
''',
    call='Solution().minInversionCount([3,2,1,4], 3)',
    expect=1,
    views=[
        dict(type='array', var='nums', label='nums（已离散化成名次；蓝 = 当前窗口）',
             h=150,
             color=lambda S, i, v: 'blue' if S.get('_line', 0) >= 37 and 'self' not in S.get('_inner', {}) and S['i'] - S['k'] < i <= S['i'] else None),
        dict(type='array', var=lambda S: S['t'] if isinstance(S.get('t'), list) else (S['t'].tree if 't' in S else None), label='树状数组 tree：窗口内各名次的出现次数（前缀和）', h=140,
             color=lambda S, i, v: 'yellow' if 9 <= S.get('_line', 0) <= 23 and i == S.get('_inner', {}).get('i') else None),
        dict(type='text', fn=lambda S: (f"窗口逆序对 ==inv = {S['inv']}==，目前最小 ans = {S['ans']}" if 'inv' in S and S.get('_line', 0) >= 41 else ('树状数组：update 沿 `i += i & -i` 向上更新，pre 沿 `i &= i - 1` 向左拼前缀和' if 9 <= S.get('_line', 0) <= 23 else '【窗口滑动时 O(log n) 维护逆序对个数】')), h=60),
    ],
    watch=['i', 'x', 'inv', 'ans'],
    captions={
        'sorted_nums = sorted': '离散化：`sorted_nums = {sorted_nums}`，只需要相对大小',
        'mp = {x': '`mp = {mp}`：值 → 名次（从 1 开始）',
        'nums[i] = mp[x]': '`nums[{i}]` 换成名次 `{nums[i]}`',
        't = FenwickTree': '建值域树状数组，下标 = 名次',
        'inv = 0': '`inv` 维护窗口内逆序对个数',
        't.update(x, 1)': lambda S, B, r: f"`nums[{B.i}]` = {B.x} 进入窗口，在树状数组里记一次",
        'inv += min': lambda S, B, r: f"窗口大小 `min({B.i}+1, {B.k})` 减去 `<= {B.x}` 的个数（pre 查），就是窗口里大于 {B.x} 的个数，加到 `inv`",
        'left = i + 1 - k': '此时窗口里的逆序对 `inv` = =={inv}==；窗口左端下标 `left = i + 1 - k = {left}`',
        'if left < 0': lambda S, B, r: ('窗口还没满，继续往右扩' if S.left < 0 else f'窗口 `[{S.left}, {S.i}]` 已满，可以更新答案'),
        'ans = min': '`ans = min({B.ans}, {inv}) = {ans}`',
        'if ans == 0': lambda S, B, r: ('已经是 0，不可能更小，提前结束' if S.ans == 0 else f'`ans = {S.ans}` 还不是 0，继续滑'),
        'out = nums[left]': '窗口左端 `nums[{left}] = {out}` 要离开',
        'inv -= t.pre': lambda S, B, r: f"离开的 {B.out} 在最左，带走的逆序对 = 窗口里比它小的个数，用 `pre({B.out} - 1)` 查，从 `inv` 里减掉",
        't.update(out, -1)': '把 `{out}` 从树状数组里去掉，窗口右移',
        'self.tree = [0]': '树状数组，初始全 0',
        't[i] += val': '`tree[{i}]` 加 `{val}`',
        'i += i & -i': '`i += i & -i` → {i}：跳到下一个会管到当前位置的格子',
        'res += t[i]': '累加 `tree[{i}]`，`res` = {res}',
        'i &= i - 1': '`i &= i - 1` → {i}：去掉最低位的 1，继续向左拼前缀和',
        'return res': '前缀和 = `{res}`',
        'return ans': '所有窗口里最小的逆序对数 = `{ans}`',
    },
    skip=['for i, x in enumerate', 'self.tree = [0]', 'def ', 'while i < len', 'while i > 0', 'res = 0', 't = self.tree', 'continue', 'break'],
    max_steps=130,
    cards=dict(
        one_liner='窗口进一个、出一个，用树状数组实时修正逆序对数',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['数组 `nums` 和整数 `k`',
                 '逆序对：`i < j` 且 `nums[i] > nums[j]`',
                 '求所有长度为 `k` 的子数组里，逆序对最少的是多少',
                 '示例：`[3,1,2,5,4]`，`k=3` → `0`；本视频用 `[3,2,1,4]` → `1`'],
        quote='元素 x 进入窗口时，inv 增加了窗口内的大于 x 的元素个数。元素 x 离开窗口时，inv 减少了窗口内的小于 x 的元素个数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['定长滑窗：入窗口的元素在最右，贡献「窗口内比它大的个数」个逆序对',
              '出窗口的元素在最左，带走「窗口内比它小的个数」个逆序对',
              '数值很大但只看相对大小：先离散化成名次，再用值域树状数组数个数'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错：入窗口用 `min(i+1, k)` 当窗口大小；窗口没满不更新答案',
                 '先「入」再算答案再「出」，三步顺序不能乱',
                 'ans 为 0 就可以提前 break；也可用 SortedList 写法（本视频未演示）',
                 '这里把 `nums` 原地改成了名次，注意后面读到的都是名次'],
    ),
)
