NUMS = [3, 8, 5, 6, 2, 7]


def _col(S, i, v):
    if 'i' not in S:
        return None
    if i == S['i']:
        return 'yellow'
    if i > S['i']:
        return 'green' if v % 2 == 0 else 'purple'
    return None


def _dim(S, i, v):
    return 'i' in S and i < S['i']


def _txt(S):
    if 'i' not in S:
        return '从右往左扫：`cnt[0]` = 右边偶数个数，`cnt[1]` = 右边奇数个数'
    return f'右侧（i 之后）：偶数 =={S["cnt"][0]}== 个，奇数 =={S["cnt"][1]}== 个'


CONFIG = dict(
    num=3917, title='统计下标的相反奇偶性得分', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='倒序遍历 · 维护奇偶计数',
    tags=['灵神核心路线', '灵神题单·常用数据结构'],
    code='''
class Solution:
    def countOppositeParity(self, nums: list[int]) -> list[int]:
        n = len(nums)
        ans = [0] * n
        cnt = [0] * 2
        for i in range(n - 1, -1, -1):
            x = nums[i] % 2  # x 的奇偶性
            ans[i] = cnt[1 - x]  # 查询右侧奇偶性不等于 x 的元素个数 
            cnt[x] += 1
        return ans
''',
    call=f'Solution().countOppositeParity({NUMS})',
    expect=[3, 2, 2, 1, 1, 0],
    views=[
        dict(type='array', var='nums', label='nums（黄 = 当前 i；右侧：绿 = 偶数，紫 = 奇数）', pointers={'i': 'yellow'},
             color=_col, dim=_dim, cell=100, h=230),
        dict(type='array', var='cnt', label='cnt[0] 偶数个数 / cnt[1] 奇数个数', cell=100, h=180,
             color=lambda S, i, v: 'green' if i == 0 else 'purple'),
        dict(type='array', var='ans', label='ans', cell=100, h=180,
             color=lambda S, i, v: 'orange' if 'i' in S and i >= S['i'] and S.get('_line') != 7 else None),
        dict(type='text', fn=_txt, size=30, h=80),
    ],
    watch=[('i', 'i', 'yellow'), 'x'],
    captions={
        'ans = [0] * n': '答案数组 `ans` 先全填 0',
        'cnt = [0] * 2': '`cnt[0]` / `cnt[1]`：==已遍历（右侧）==的偶数 / 奇数个数',
        'for i in range': lambda S, B, ret: (f'从右往左：`i = {S.i}`，此时 cnt 恰好统计了 i 右侧的元素'
                                             if 'i' not in B or S.i != B.i else '遍历结束'),
        'x = nums[i] % 2': lambda S, B, ret: f'x 的奇偶性：`nums[{S.i}] = {S.nums[S.i]}` 是{"奇" if S.x else "偶"}数 → `x = {S.x}`',
        'ans[i] = cnt[1 - x]': lambda S, B, ret: (f'查询右侧奇偶性不等于 x 的元素个数：右边{"偶" if S.x else "奇"}数有 '
                                                  f'`cnt[{1 - S.x}] = {S.ans[S.i]}` 个 → `ans[{S.i}] = {S.ans[S.i]}`'),
        'cnt[x] += 1': lambda S, B, ret: f'`nums[{S.i}]` 也进入「右侧」，供左边的元素查询：`cnt[{S.x}]` → {S.cnt[S.x]}',
        'return ans': '返回 `{ret}`',
    },
    cards=dict(
        one_liner='倒着扫，边扫边数右边有几个奇数、几个偶数',
        complexity='时间 `O(n)`，空间 `O(1)`（返回值不计）',
        problem=['下标 i 的分数 = 满足 `i < j` 且 `nums[i]`、`nums[j]` ==奇偶性不同==的 j 的个数',
                 '返回每个下标的分数组成的数组',
                 '示例：`[1,2,3,4]` → `[2,1,1,0]`'],
        quote='从右到左遍历 nums，==维护遍历过的奇数个数和偶数个数==。根据 nums[i] 的奇偶性，查询其右侧的偶数个数或奇数个数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['「枚举右，维护左」的镜像版：枚举 i，==维护右边==的统计量',
              '`x = nums[i] % 2`，奇偶相反的那一类就是 `cnt[1 − x]`',
              '先查询再把自己加入 cnt，避免把自己算进去'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '顺序：==先算 `ans[i]`，再 `cnt[x] += 1`==',
                 '`1 − x` 把 0/1 翻转，省掉 if 判断',
                 '同类：§0.1 枚举右维护左，例如 1. 两数之和'],
    ),
)
