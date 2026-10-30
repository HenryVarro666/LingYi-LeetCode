def _phase2(S):
    return S.get('_line') == 20


def _hand(S):
    ln = S.get('_line')
    if ln == 20:
        return '复原：每个数取反（负号只是“访问过”的标记）'
    if 'cur' not in S or ln in (3, 4):
        return '`nxt = cur * 2`（前半）或 `(cur − n) * 2 + 1`（后半）：下标 cur 的数要去的位置'
    x, cur, nxt = S.get('x'), S['cur'], S.get('nxt')
    if ln == 15:
        return f'`{-S["nums"][nxt]}` 放好了；==拿起==原来在下标 {nxt} 的 `x = {x}`'
    if ln == 11:
        return f'环走完：最后拿着的 `{x}` 放回起点 `{S["i"]}`'
    if ln in (9, 10):
        return f'手里拿着 `x = {x}`（原来在下标 {cur}），它要去 ==下标 {nxt}=='
    return f'手里拿着 `x = {x}`（原来在下标 {cur}）'


CONFIG = dict(
    num=1470, title='重新排列数组', difficulty='Easy', category='普通数组',
    author='灵茶山艾府', technique='原地交换 · 沿置换环移动 + 负数标记',
    tags=['List.md', '字节30天'],
    code='''
class Solution:
    def shuffle(self, nums: List[int], n: int) -> List[int]:
        for i, x in enumerate(nums):
            if x < 0:  # 已访问
                continue
            cur = i
            while True:
                # 元素 x 要填入 nums[nxt]
                nxt = cur * 2 if cur < n else (cur - n) * 2 + 1
                if nxt == i:  # 回到起点
                    nums[i] = -x  # 用负数表示访问过
                    break
                # 把 x 填入 nums[nxt]（用负数表示访问过）
                # 同时把原来位于 nxt 的数记为 x
                x, nums[nxt] = nums[nxt], -x
                cur = nxt

        # 复原
        for i, x in enumerate(nums):
            nums[i] = -x

        return nums
''',
    call='Solution().shuffle([2, 5, 1, 3, 4, 7], 3)',
    expect=[2, 3, 5, 4, 1, 7],
    views=[
        dict(type='text', fn=_hand, size=26, h=60),
        dict(type='array', var='nums', label='nums（绿 = 负数 = 已经放到最终位置）', cell=96, h=260,
             pointers={'i': 'blue', 'cur': 'pink', 'nxt': 'green'},
             color=lambda S, i, v: 'green' if v < 0 else None),
        dict(type='text', fn=lambda S: '前半 `x1..xn` 去偶数下标 `2i`，后半 `y1..yn` 去奇数下标 `2(i−n)+1`', size=24, h=50),
        dict(type='array', var=lambda S: [2, 3, 5, 4, 1, 7], label='目标：[x1,y1,x2,y2,x3,y3]', cell=72, h=130),
    ],
    watch=[('i', 'i', 'blue'), ('x', 'x', 'orange'), ('cur', 'cur', 'pink'), ('nxt', 'nxt', 'green'), 'n'],
    skip=['while True', 'break', 'continue', 19],
    captions={
        'for i, x in enumerate(nums)': lambda S, B, ret: (f'看下标 `i = {S.i}`：`x = {S.x}`' if S.get('i') != B.get('i')
                                                          else '所有环都处理完了'),
        'if x < 0': lambda S, B, ret: (f'`x = {S.x} < 0`：已访问（在之前的环里放好了）→ continue' if S.x < 0
                                       else f'`x = {S.x} > 0`：还没访问 → 从 `i = {S.i}` 出发走一个环'),
        'cur = i': '`cur = {cur}`：当前手里的数原来所在的下标',
        'nxt = cur * 2': lambda S, B, ret: (f'`cur = {S.cur} < n`：前半部分 → `nxt = {S.cur} × 2 = {S.nxt}`' if S.cur < S.n
                                            else f'`cur = {S.cur} ≥ n`：后半部分 → `nxt = ({S.cur} − {S.n}) × 2 + 1 = {S.nxt}`'),
        'if nxt == i': lambda S, B, ret: (f'`nxt == i = {S.i}`：==回到起点==，这个环走完了' if S.nxt == S.i
                                          else f'`nxt = {S.nxt} ≠ i = {S.i}`：还没回到起点'),
        11: '环的最后一个数放进起点：`nums[{i}] = -{-nums[i]}`（负数表示访问过）',
        'x, nums[nxt]': lambda S, B, ret: (f'把 `x = {B.x}` 填入 `nums[{S.nxt}]`（记为 `{-B.x}`），'
                                           f'同时==拿起原来的 `{S.x}`== 继续走'),
        'cur = nxt': '`cur = {cur}`：手里的数原来在这里',
        20: lambda S, B, ret: f'复原：`nums[{S.i}] = -({S.x}) = {S.nums[S.i]}`',
        'return nums': '返回 `{ret}`',
    },
    cards=dict(
        one_liner='每个数沿置换环搬到目标位置，用负号标记已访问',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['数组 `nums` 有 `2n` 个元素：`[x1,x2,...,xn,y1,y2,...,yn]`',
                 '把它重新排列成 `[x1,y1,x2,y2,...,xn,yn]` 并返回',
                 '示例：`nums = [2,5,1,3,4,7]`，`n = 3` → `[2,3,5,4,1,7]`'],
        quote='我们可以按照 1→2→4→1 的顺序==走一个环，把环上的每个数移动到其后面的数上==。……考虑到本题 nums[i] 都是正数，我们可以==把访问过的数加个负号==。',
        quote_src='—— 灵茶山艾府题解（方法二：原地交换）',
        idea=['下标 `i` 的数要去 `2i`（前半）或 `2(i−n)+1`（后半）：这是一个==置换==',
              '置换可以拆成若干个环：拿起一个数，放到目标位置，再拿起被挤走的数……',
              '放好的数取负号；遍历到负数说明已在之前的环里处理过'],
        result='运行结束：返回 `[2,3,5,4,1,7]` ✓',
        summary=['时间 `O(n)`：每个元素恰好被标记一次；空间 `O(1)`',
                 '利用题目 `nums[i] ≥ 1`：负号可以当访问标记，最后统一取反复原',
                 '方法一更直接：新建 `ans`，`ans[2i] = nums[i]`，`ans[2i+1] = nums[n+i]`，空间 `O(n)`',
                 '相似题：41. 缺失的第一个正数、1920. 基于排列构建数组'],
    ),
)
