_M = lambda S: S.get('self.max_num')
_R = lambda S: S.get('self.res')


def _txt(S):
    if 'now' not in S:
        return ''
    return f'当前选出的数 OR 起来 `now = {S["now"]:03b}`（{S["now"]}），历史最大 `max_num = {S.get("self.max_num")}`，个数 `res = {S.get("self.res")}`'


def _cap_if(S, B, ret):
    if S.level == len(S.nums):
        return f'`level = {S.level}` = 数组长度：一个子集选完了，OR 值 `now = {S.now}`'
    return f'`level = {S.level}` < {len(S.nums)}：还要决定 `nums[{S.level}] = {S.nums[S.level]}` 选不选'


CONFIG = dict(
    num=2044, title='统计按位或能得到最大值的子集数目', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='不剪枝的暴力 dfs，边搜边更新最大值',
    tags=['灵神核心路线', '灵神题单·动态规划'],
    code='''
class Solution(object):
    def countMaxOrSubsets(self, nums):

        self.max_num = 0
        self.res = 0
        self.dfs(0, 0, nums)

        return self.res

    def dfs(self, level, now, nums):
        if level == len(nums):
            if now > self.max_num:
                self.max_num = now
                self.res = 1
            elif now == self.max_num:
                self.res += 1
            return

        self.dfs(level + 1, now | nums[level], nums)
        self.dfs(level + 1, now, nums)
''',
    call='Solution().countMaxOrSubsets([3, 5, 1])',
    expect=2,
    views=[
        dict(type='text', h=90, fn=_txt, size=24),
        dict(type='array', var='nums', label='nums（箭头 = 当前要决定的数）', h=140, cell=80, pointers={'level': 'blue'}),
        dict(type='calls', h=300, hide=('nums',)),
    ],
    watch=[('level', 'level', 'blue'), ('now', 'now', 'cyan'), ('max_num', _M, 'green'), ('res', _R, 'yellow')],
    skip=['self.max_num = 0', 'self.res = 0'],
    captions={
        'self.dfs(0, 0, nums)': '从 `dfs(0, 0)` 开始：不剪枝，把每个子集的 OR 都算出来，边搜边记最大值和个数',
        'if level == len(nums)': _cap_if,
        'if now > self.max_num': lambda S, B, r: (
            f'`now = {S.now} > max_num = {S["self.max_num"]}` → ==出现更大的 OR==，更新最大值' if S.now > S['self.max_num']
            else f'`now = {S.now}` 没有超过 `max_num = {S["self.max_num"]}`，再看是否相等'),
        'self.max_num = now': '`max_num` 更新为 `{self.max_num}`',
        'self.res = 1': '最大值换了，旧的计数作废：`res` 重新从 `1` 数起',
        'elif now == self.max_num': lambda S, B, r: (f'`now = {S.now}` 等于 `max_num` → 又一个达到最大值的子集' if S.now == S['self.max_num'] else f'`now = {S.now}` 小于 `max_num = {S["self.max_num"]}` → 不算'),
        'self.res += 1': '`res` 加一 → `{self.res}`',
        'self.dfs(level + 1, now | nums[level], nums)': '`nums[{level-1}] = {nums[level-1]}`：先试==选==它，`now` 变成 `{now}`',
        'self.dfs(level + 1, now, nums)': '这一支回溯完毕，再试==不选== `nums[{level-1}]`：`now` 保持 `{now}`',
        'return self.res': '全部枚举完：最大 OR 是 `{self.max_num}`，个数 `{self.res}`',
    },
    max_steps=100,
    cards=dict(
        one_liner='数据很小，直接 dfs 枚举全部子集，边搜边更新最大值',
        complexity='时间 `O(2^n)`，空间 `O(n)`',
        problem=['求 `nums` 子集按位或的最大值，返回能得到最大值的非空子集个数',
                 '下标不同视为不同子集',
                 '本视频：`[3,5,1]` → `2`（最大 OR 是 `7`）'],
        quote='在这里使用暴力dfs枚举每种组合反而比状态压缩动态规划更快一点。具体实现上就是最常规不带任何剪枝的dfs。',
        quote_src='—— yiduobo 题解原文',
        idea=['先想到按位 DP / 状压 DP，但 `n ≤ 16`，直接 `2^16` 个子集更省事',
              '`dfs(level, now)`：每个数选（OR 进 `now`）或不选',
              '到叶子比较：`now` 更大就重置 `max_num` 和 `res = 1`；相等就 `res += 1`'],
        summary=['时间 `O(2^n)`，空间 `O(n)`',
                 '叶子里要 ==三种情况==：更大（重置计数）、相等（加一）、更小（忽略）',
                 '初值 `max_num = 0`：空集 OR 为 0，但 `nums[i] ≥ 1`，所以空集不会被算进去',
                 '对比灵神：灵神先求 `total_or`，OR 到顶就整段 `2^(n-i)` 直接累加']
    ),
)
