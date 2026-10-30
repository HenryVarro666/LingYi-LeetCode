CONFIG = dict(
    num=2772, title='使数组中的所有元素都等于零', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='最左非零元素 · 差分数组',
    tags=['灵神题单', '常用数据结构', '难度分 2029'],
    code='''
class Solution(object):
    def checkArray(self, nums, k):

        n = len(nums)
        f = [0] * n
        now = 0

        for index, v in enumerate(nums):
            now += f[index]
            if v < now:
                return False
            
            delta = v - now
            if delta > 0 and index + k > n:
                return False
            
            now = v
            if index + k < n:
                f[index + k] -= delta

        return True
''',
    call='Solution().checkArray([2,2,3,1,1,0], 3)',
    expect=True,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 当前下标 index）', pointers={'index': 'blue'}, h=200),
        dict(type='text', fn=lambda S: (f"`now` = 已经被减掉的量 `{S['now']}`，`v = {S['v']}`" + (f"，还要新减 `delta = {S['delta']}`" if S.get('_line', 0) >= 13 and S.get('_line', 0) <= 18 else '') if 'v' in S and 'now' in S else ''), h=60),
        dict(type='array', var='f', label='f（差分：到 index+k 处让 now 回落 delta）', h=190, cell=90),
    ],
    watch=['index', 'v', 'now', 'delta'],
    captions={
        'f = [0]': '`f[i]` 记录：到下标 `i` 时已有的减法效果要回落多少',
        'now = 0': '`now`：前面操作已经让当前位置被减掉的总量（保持当前值不再变）',
        'for index, v': lambda S, B, r: ('全部遍历完，没有无解的情况' if 'index' in B and B.index == S.index else f'看第 `{S.index}` 个数 `v = {S.v}`'),
        'now += f[index]': '先把差分加上：有的操作到这里结束了，`now` 变成 `{now}`',
        'if v < now': lambda S, B, r: (f'`v = {S.v} < now = {S.now}`：已经被减得比自己还多，无解 → `False`' if S.v < S.now else f'`v = {S.v} >= now = {S.now}`：没减过头'),
        'delta = v - now': '还差 `{v} - {now} = {delta}` 次才能减到 0：必须由以它为左端的区间补上',
        'if delta > 0': lambda S, B, r: (f'要补 `{S.delta}` 次但 `index + k = {S.index + S.k} > n = {len(S.nums)}`：后面放不下区间 → `False`' if S.delta > 0 and S.index + S.k > len(S.nums) else ('`delta = 0`：这个数不用补' if S.delta == 0 else f'`index + k = {S.index + S.k} <= n`：可以补')),
        'now = v': '补完后，这个位置被减掉的总量刚好等于 `v`：`now = {v}`',
        'f[index + k] -= delta': lambda S, B, r: f'区间到 `index + k = {S.index + S.k}` 前结束：`f[{S.index + S.k}]` 减 `{S.delta}`，`now` 到那里要回落',
        'if index + k < n': lambda S, B, r: (f'`{S.index + S.k} < {len(S.nums)}`：区间结束位置还在数组内，记到 `f` 里' if S.index + S.k < len(S.nums) else f'`{S.index + S.k} >= {len(S.nums)}`：区间一直延伸到末尾，不用记'),
        'return True': '所有位置都能减到 0 → `True`',
    },
    cards=dict(
        one_liner='最左的非零数只能靠以它为左端的区间减',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['每次选长度为 `k` 的子数组，每个元素减 `1`，可操作任意次',
                 '问能否把数组变成全 `0`',
                 '示例：`nums=[2,2,3,1,1,0], k=3` → `true`'],
        quote='对于数组中最左侧的非0元素，就只能选择以该元素为左边界的长度为k的子数组来执行若干次减法，而这个次数就是这个元素的值。',
        quote_src='—— yiduobo 题解原文',
        idea=['无解有两种：某个元素被减成负数；最后 `k-1` 个元素里还有非零',
              '每个位置的修改都来自它左边，所以不需要线段树，普通差分就够',
              '`now` 表示当前位置已被减掉的量，`f[index+k]` 处让它回落'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`v < now` 是减过头；`delta > 0 且 index + k > n` 是区间放不下',
                 '`now = v` 这一步容易漏：补完后当前位置被减到 0，后续看的是剩余量',
                 '原文为 Python 2 风格，本题代码无需改动'],
    ),
)
