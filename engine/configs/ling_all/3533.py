_I = lambda S: S['_inner'].get('i')


def _txt(S):
    I = S['_inner']
    if 's' not in I:
        return '`dfs(s, x)`：`s` = 还没填的下标集合，`x` = 已拼接的数 mod k'
    n = len(S['nums'])
    s, x = I['s'], I['x']
    used = [S['nums'][j] for j in range(n) if not s >> j & 1]
    return f'`s = {s:0{n}b}`（剩余 {[S["nums"][j] for j in range(n) if s >> j & 1]}），已填 {used}，拼接数 mod {S["k"]} = `{x}`'


CONFIG = dict(
    num=3533, title='判断连接可整除性', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='排序 + 状压记忆化暴搜',
    tags=['灵神题单', '动态规划', '难度分 2257'],
    code='''
class Solution:
    def concatenatedDivisibility(self, nums: List[int], k: int) -> List[int]:
        nums.sort()
        pow10 = [10 ** len(str(x)) for x in nums]

        ans = []
        @cache  # 充当 vis
        def dfs(s: int, x: int) -> bool:
            if s == 0:
                return x == 0
            # 枚举在 s 中的下标 i
            for i, (p10, v) in enumerate(zip(pow10, nums)):
                if s & (1 << i) and dfs(s ^ (1 << i), (x * p10 + v) % k):
                    ans.append(v)
                    return True
            return False

        if not dfs((1 << len(nums)) - 1, 0):
            return []
        ans.reverse()  # nums[i] 是倒序加入答案的，所以要反转
        return ans
''',
    call='Solution().concatenatedDivisibility([7, 4, 5, 2], 2)',
    expect=[2, 5, 7, 4],
    views=[
        dict(type='text', fn=_txt, h=80),
        dict(type='array', var='nums', label='nums（排序后；绿 = 已填，粉 = 正在尝试的 i）', cell=76, h=190,
             pointers={_I: 'pink'}, pointer_labels={_I: 'i'},
             color=lambda S, i, v: 'green' if 's' in S['_inner'] and not S['_inner']['s'] >> i & 1 else None),
        dict(type='calls', h=250),
        dict(type='stack', var='ans', label='ans（倒序加入）', h=100),
    ],
    watch=[('s', "_inner.get('s')"), ('x', "_inner.get('x')"), 'ans'],
    skip=['pow10 = ', 'ans = []', 'for i, (p10, v)', 'return True'],
    captions={
        'nums.sort()': '==先排序==：从小到大枚举，第一个找到的就是字典序最小的数组',
        '@cache': '`@cache` 充当 `vis`：同一个 `(s, x)` 只搜一次',
        'if s == 0': lambda S, B, r: ('`s = 0`：数字全部填完，只有 `x == 0` 才整除' if S.s == 0 else f'`s = {S.s}` 还有数字没填，继续往下搜'),
        'return x == 0': '全填完了：拼接数 mod k = `{B.x}` → ==`{B.x == 0}`==',
        'if s & (1 << i)': lambda S, B, r: (
            f'`nums[{B.i}] = {B.nums[B.i]}` 不在 `s` 里（已填过）→ 跳过' if not B.s >> B.i & 1 else
            f'按下标从小到大试 `nums[{B.i}] = {B.nums[B.i]}`：新余数 `({B.x} × {B.p10} + {B.v}) % {B.k} = {(B.x * B.p10 + B.v) % B.k}`，递归下一位'),
        'ans.append(v)': '子树返回 True：==`{v}` 是这一位的数==，立刻返回 True 不再搜别的分支，倒序加入 `ans`',
        'return False': '`s = {B.s}` 下所有数都试过，凑不出 → 返回 False（这个状态以后也不会成功）',
        'if not dfs': '入口 `dfs(U, 0)`：`U` = 全集 `{(1 << len(nums)) - 1}`，余数 0 开始',
        'ans.reverse()': '最内层先 append，所以 ==ans 是倒序的==，反转得 `{ans[::-1]}`',
        'return ans': '返回字典序最小的排列 `{ans}`',
    },
    max_steps=75,
    cards=dict(
        one_liner='排序后暴搜第一个可行排列，再用 vis 剪掉重复状态',
        complexity='时间 `O(n·k·2^n)`，空间 `O(k·2^n)`',
        problem=['给正整数数组 `nums` 和 `k`，把 `nums` 重新排列后依次拼接成十进制数',
                 '要求这个数能被 `k` 整除，返回==字典序最小的排列==（不是拼接数最小）',
                 '无解返回 `[]`；示例：`[3,12,45], k=5` → `[3,12,45]`；本视频用 `[7,4,5,2], k=2`'],
        quote='首先读清楚题目，要计算的是字典序最小的数组，不是拼接后的数。为了让字典序最小，我们要从小到大枚举。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`nums` 从小到大排序，类似全排列的暴搜：每一位按顺序试',
              '只维护「剩余集合 `s`」和「拼接数 mod k = `x`」，拼接就是 `x×10^L + v`',
              '不同顺序可能到达同一个 `(s, x)`，用 `@cache` 记下，重复到达必然失败'],
        summary=['时间 `O(nk·2^n)`：状态 `O(k·2^n)` 个，每个枚举 n 个下标',
                 '返回的是==数组==字典序最小，所以要先排序再从小到大试',
                 '答案是递归返回时 append 的，==要 reverse==',
                 '`@cache` 把「找到就返回 True」的搜索变成对状态只算一次',
                 '思考题：改成拼接数字最小，需要自定义比较 `a+b < b+a` 排序'],
    ),
)
