M = 5
GROUPS = [1, 1, 2, 2, 3, 4]


def _txt(S):
    inn = S.get('_inner', {})
    if 'left' in inn:
        left = inn['left']
        c = inn.get('cnt')
        rest = ' '.join(f'余{k + 1}×{v}' for k, v in enumerate(c) if v) if c is not None else ''
        return f'`left = {left}`（已卖出 mod {S["m"]}）；还没安排：{rest or "无"}' + ('  → ==left=0，这批顾客开心==' if left == 0 else '')
    if 'ans' in S:
        return f'已经开心的组 `ans = {S["ans"]}`；`cnt[x]`：余数为 x 的组数（0 在最前，x 和 m−x 配对）'
    return '只关心「卖出个数 mod m」：余数相同的组可以互换'


CONFIG = dict(
    num=1815, title='得到新鲜甜甜圈的最多组数', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='取模分组 + 配对 + 记忆化搜索',
    tags=['难度分 2559'],
    code='''
class Solution:
    def maxHappyGroups(self, m: int, groups: List[int]) -> int:
        ans = 0
        cnt = [0] * m
        for x in groups:
            x %= m
            if x == 0:
                ans += 1  # 直接排在最前面
            elif cnt[-x]:
                cnt[-x] -= 1  # 配对
                ans += 1
            else:
                cnt[x] += 1

        @cache  # 记忆化
        def dfs(left: int, cnt: Tuple[int]) -> int:
            res = 0
            cnt = list(cnt)
            for x, c in enumerate(cnt):  # 枚举顾客
                if c:  # cnt[x] > 0
                    cnt[x] -= 1
                    res = max(res, (left == 0) + dfs((left + x + 1) % m, tuple(cnt)))  # x 从 0 开始，这里要 +1
                    cnt[x] += 1
            return res
        return ans + dfs(0, tuple(cnt[1:]))  # 转成 tuple 这样能记忆化
''',
    call=f'Solution().maxHappyGroups({M}, {GROUPS})',
    expect=3,
    views=[
        dict(type='array', var='groups', label='groups', h=130, cell=80),
        dict(type='array', var=lambda S: list(S['cnt']), label='cnt（顶层：下标 = 余数；dfs 里：下标 x 表示余数 x+1）', h=200, cell=80,
             pointers={'x': 'blue'}),
        dict(type='calls', h=230),
        dict(type='text', fn=_txt, size=26, h=90),
    ],
    watch=[('ans', 'ans', 'green'), ('x', 'x', 'blue'), ('left', 'left', 'orange'), ('res', 'res', 'pink')],
    skip=['for x in groups', 'for x, c in enumerate', 'if c:', 'cnt = list(cnt)', 'res = 0'],
    captions={
        'ans = 0': '`ans` 统计开心的组数',
        'cnt = [0] * m': '`cnt[r]`：模 `m = {m}` 余 `r` 的组数',
        'x %= m': '只关心余数：`{B.x} % {m}` = `{x}`（买 1 个和买 m+1 个没区别）',
        'if x == 0': lambda S, B, r: ('余 0：这批顾客==正好买完整批==，排在最前面都开心' if S.x == 0 else f'`x = {S.x} ≠ 0`，要和别的组配对'),
        'ans += 1  # 直接': '余 0 的组直接排最前面 → `ans = {ans}`',
        'elif cnt[-x]': lambda S, B, r: (f'有余 `{-S.x % S.m}` 的组（`{S.x} + {-S.x % S.m} = {S.m}`）→ ==配对：一组买完，下一组开心==' if S.cnt[-S.x]
                                         else f'没有余 `{-S.x % S.m}` 的组可配，先记下 `x = {S.x}`'),
        'cnt[-x] -= 1': '配对：把余 `{-x % m}` 的一组用掉 → `cnt[{-x % m}] = {cnt[-x]}`',
        'ans += 1  # 配对': '这一对里有一批开心 → `ans = {ans}`',
        13: '没配上，余 `{x}` 的组数加一 → `cnt[{x}] = {cnt[x]}`',
        'def dfs': '`dfs(left, cnt)`：已卖出 mod m 为 `left`，剩余各余数的组数为 `cnt`；加 `@cache` 避免重复算',
        'return ans + dfs': '剩下无法配对的最多 4 种余数，交给记忆化搜索：`dfs(0, {tuple(B.cnt[1:])})`',
        'cnt[x] -= 1': '选一批余 `{x + 1}` 的顾客来（下标 x 对应余数 x+1）：剩 `cnt[{x}] = {cnt[x]}`',
        'res = max(res': lambda S, B, r: (f'`left = {B.left}`：' + ('==为 0，这批顾客开心 +1==' if B.left == 0 else '不为 0，这批不开心')
                                          + f'；再看子问题 `dfs({(B.left + B.x + 1) % B.m}, ...)`（该状态算过则直接取缓存）'),
        23: '子问题返回，这一层 `res = {res}`；恢复现场：`cnt[{x}]` 加回 → {cnt[x]}',
        'return res': lambda S, B, r: f'`left = {S.left}` 这一层最多开心 `{r}` 批',
    },
    max_steps=90,
    cards=dict(
        one_liner='只看余数：先配对，剩下至多 4 种余数交给记忆化搜索',
        complexity='时间 `O(m^2 (n/m)^(m/2))`，空间 `O(m (n/m)^(m/2))`',
        problem=['每批烤 `batchSize` 个甜甜圈，卖完才能烤下一批；一批顾客的第一位拿到的不是剩下的，这组就开心',
                 '可以任意安排各组到来的顺序，求==最多多少组开心==',
                 '本视频：`batchSize = 5, groups = [1,1,2,2,3,4]` → `3`'],
        quote='把 0 排在前面后，剩下的顾客，尽可能地两两一对安排。例如把 1 和 m-1 排在一起，2 和 m-2 排在一起……每一对中都有一批开心的顾客。',
        quote_src='—— 灵茶山艾府题解',
        idea=['只关心「卖出个数 mod m」，所以按 `groups[i] % m` 分组计数',
              '余 0 的直接排最前；余 `x` 和余 `m-x` 配成一对，每对贡献 1 个开心',
              '剩下至多 4 种余数：`dfs(left, cnt)` 枚举下一批顾客，==`left == 0` 就开心==；`@cache` + `tuple` 记忆化'],
        summary=['时间 `O(m^2 (n/m)^(m/2))`，最坏约 2.8 万个状态',
                 '易错：`cnt` 切掉了下标 0，所以 dfs 里下标 `x` 对应余数 `x+1`',
                 '易错：`cnt` 要转成 `tuple` 才能进 `@cache`；递归里修改后要恢复',
                 '题解先给不配对的基础记忆化写法，再加配对优化；本视频演示优化后的写法（还有位运算打包状态的写法）',
                 '同类：状压 DP 题单 §9.7'],
    ),
)
