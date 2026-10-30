def _txt(S):
    if 'cnt' not in S:
        return '偶数且被 3 整除 ⇔ 被 `lcm(2,3) = 6` 整除'
    if S['cnt'] == 0:
        return '还没有 6 的倍数：`sum = 0`，`cnt = 0`'
    return f"已收集 {S['cnt']} 个 6 的倍数，和 =={S['sum']}==，平均值 = `{S['sum']} // {S['cnt']}` = =={S['sum'] // S['cnt']}=="


def _col(S, i, v):
    if 'x' not in S:
        return None
    cur = S['nums'].index(S['x'])
    if i == cur and S['_line'] < 6:
        return 'blue'
    if v % 6 == 0 and (i < cur or (i == cur and S['_line'] >= 6)):
        return 'green'
    return 'blue' if i == cur else None


CONFIG = dict(
    num=2455, title='可被三整除的偶数的平均值', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='LCM = 6 · 一次遍历',
    tags=[],
    code='''
class Solution:
    def averageValue(self, nums: List[int]) -> int:
        sum = cnt = 0
        for x in nums:
            if x % 6 == 0:
                sum += x
                cnt += 1
        return sum // cnt if cnt else 0
''',
    call='Solution().averageValue([1,3,6,10,12,15])',
    expect=9,
    views=[
        dict(type='text', fn=_txt, size=30, h=100),
        dict(type='array', var='nums', label='nums（蓝 = 当前 x，绿 = 6 的倍数）', cell=110, h=200, color=_col),
    ],
    watch=[('x', 'x', 'blue'), ('sum', 'sum', 'green'), ('cnt', 'cnt', 'orange')],
    captions={
        'sum = cnt = 0': '`sum` 累加 6 的倍数，`cnt` 统计个数，都从 0 开始',
        'for x in nums': lambda S, B, r: ('遍历结束' if S.x == B.get('x') and S.x == S.nums[-1] else f'看下一个数 `x = {S.x}`'),
        'if x % 6 == 0': lambda S, B, r: (f'`{S.x} % 6 = {S.x % 6}` → ==是 6 的倍数==：既是偶数又被 3 整除' if S.x % 6 == 0
                                           else f'`{S.x} % 6 = {S.x % 6} ≠ 0` → 不满足，跳过（{"偶数但不被 3 整除" if S.x % 2 == 0 else "是奇数"}）'),
        'sum += x': '`sum` 加上 `{x}` → `{sum}`',
        'cnt += 1': '个数加一 → `cnt = {cnt}`',
        'return': lambda S, B, r: (f'`cnt = {S.cnt} ≠ 0`，平均值向下取整：`{S.sum} // {S.cnt}` = =={r}==' if S.cnt else '`cnt = 0`：没有满足条件的数 → 返回 `0`，避免除以 0'),
    },
    cards=dict(
        one_liner='偶数又被 3 整除，就是 6 的倍数',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['求 `nums` 中所有 ==能被 3 整除的偶数== 的平均值，结果向下取整',
                 '示例：`[1,3,6,10,12,15]` → `(6 + 12) // 2 = 9`',
                 '没有满足条件的数就返回 `0`'],
        quote='能被 3 和 2 整除的数，就是能被最小公倍数 LCM(3,2)=6 整除的数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['把两个条件合成一个：`x % 6 == 0`',
              '一遍扫描，同时累加和 `sum` 与个数 `cnt`',
              '最后 `sum // cnt` 就是向下取整的平均值；`cnt = 0` 时返回 0'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：`cnt = 0` 时不能除，要特判返回 0',
                 '`sum // cnt` 是整除，对应题目的向下取整',
                 '变量名 `sum` 会遮住内置函数 sum，竞赛里常见，但工程里要避免'],
    ),
)
