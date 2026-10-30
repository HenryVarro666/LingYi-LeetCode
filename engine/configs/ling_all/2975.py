CONFIG = dict(
    num=2975, title='移除栅栏得到的正方形田地的最大面积', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='哈希集合求交集',
    tags=[],
    code='''
from typing import Set


class Solution:
    def f(self, a: List[int], mx: int) -> Set[int]:
        a += [1, mx]
        a.sort()
        # 计算 a 中任意两个数的差，保存到哈希集合中
        return set(y - x for x, y in combinations(a, 2))

    def maximizeSquareArea(self, m: int, n: int, hFences: List[int], vFences: List[int]) -> int:
        MOD = 1_000_000_007
        h_set = self.f(hFences, m)
        v_set = self.f(vFences, n)

        ans = max(h_set & v_set, default=0)
        return ans * ans % MOD if ans else -1
''',
    call='Solution().maximizeSquareArea(7, 6, [2,4], [3])',
    expect=25,
    views=[
        dict(type='text', size=26, fn=lambda S: (f"交集 = `{sorted(S['h_set'] & S['v_set'])}`，最大边长 =={max(S['h_set'] & S['v_set'], default=0)}==" if 'h_set' in S and 'v_set' in S else '栅栏位置加上两条外框，任选两条的距离都可能是边长')),
        dict(type='array', var='a', label='a（栅栏位置，含外框 1 和 mx）', cell=84, h=190),
        dict(type='set', var='h_set', label='h_set：水平方向可得的边长', fmt=lambda x: str(x), h=190),
        dict(type='set', var='v_set', label='v_set：垂直方向可得的边长', fmt=lambda x: str(x), h=190),
    ],
    watch=['mx', 'ans'],
    captions={
        'a += [1, mx]': '外框栅栏不能删但可以当边界：把 `1` 和 `{mx}` 加进来 → `{a}`',
        'a.sort()': '排序，方便按位置看：`{a}`',
        'return set(y - x': lambda S, B, r: f'任意两条栅栏（中间的全拆掉）的距离都是候选边长 → ==`{sorted(r)}`==',
        'MOD = ': '答案可能很大，最后对 `10^9+7` 取模',
        'h_set = self.f': '水平方向：候选边长集合 `h_set = {sorted(h_set)}`',
        'v_set = self.f': '垂直方向：候选边长集合 `v_set = {sorted(v_set)}`',
        'ans = max(': '两个集合的交集 `{sorted(h_set & v_set)}` 里取最大 → 边长 `ans = {ans}`（交集为空则为 0）',
        'return ans * ans': lambda S, B, r: (f'正方形面积 `{S.ans}²` 取模 = =={r}==' if S.ans else '交集为空，拼不出正方形 → `-1`'),
    },
    cards=dict(
        one_liner='横竖分开算：各自求出所有可能的边长，取交集的最大值',
        complexity='时间 `O(h² + v²)`，空间 `O(h² + v²)`',
        problem=['田地里有一些水平栅栏和垂直栅栏，外框的四条栅栏不能移除',
                 '移除若干栅栏后，求能形成的最大==正方形==面积（对 `10^9+7` 取模），拼不出返回 `-1`',
                 '本视频：`m=7, n=6, hFences=[2,4], vFences=[3]` → `25`'],
        quote='对于水平栅栏，任意两个栅栏之间的距离（中间的栅栏全部删除）都可能是正方形的边长，存到一个哈希表 hSet 中。',
        quote_src='—— 灵茶山艾府题解',
        idea=['水平、垂直互不影响：各自把外框 `1`、`mx` 加进去，枚举任意两条的差',
              '正方形的边长必须==两个方向都能取到==：求 `h_set & v_set`',
              '交集最大值的平方就是答案，交集为空返回 `-1`'],
        summary=['时间、空间都是 `O(h² + v²)`',
                 '别忘了把外框 `1` 和 `m`/`n` 加进栅栏列表',
                 '平方之后再取模；交集为空要返回 `-1`，不是 0',
                 '`max(..., default=0)` 处理交集为空；`a += ...` 会改动传入的列表',
                 '代码开头补了 `from typing import Set`（引擎没预置 Set，作者代码本身未改）',
                 '相似题：1465 切割后面积最大的蛋糕、2943'],
    ),
)
