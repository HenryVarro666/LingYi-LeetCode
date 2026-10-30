CONFIG = dict(
    num=2110, title='股票平滑下跌阶段的数目', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='分组循环 · 按右端点计数',
    tags=['分组循环', '难度分 1408'],
    code='''
class Solution:
    def getDescentPeriods(self, prices: List[int]) -> int:
        ans = dec = 0
        for i, p in enumerate(prices):
            if i > 0 and p == prices[i - 1] - 1:
                dec += 1  # 连续递减
            else:
                dec = 1  # 连续递减中断，重新统计
            ans += dec  # dec 是右端点为 i 的连续递减子数组个数
        return ans
''',
    call='Solution().getDescentPeriods([4,3,2,1,5,4,4,3])',
    expect=16,
    views=[
        dict(type='text', fn=lambda S: (f"右端点 `i = {S['i']}` 的递减子数组有 =={S['dec']}== 个，累计 `ans` = {S['ans']}") if 'dec' in S and 'i' in S and S['dec'] > 0 else '', size=30),
        dict(type='array', var='prices', pointers={'i': 'pink'},
             window=(lambda S: S['i'] - S['dec'] + 1 if S.get('dec') else S['i'], 'i'), h=300, cell=90,
             dim=lambda S, k, v: 'i' in S and k > S['i']),
    ],
    watch=[('i', 'i', 'pink'), ('dec', 'dec', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'ans = dec = 0': '`dec`：以当前位置结尾的连续递减段长度；`ans` 累计总数',
        'if i > 0': lambda S, B, r: ('`i = 0`：第一天前面没有价格，单独成段' if S.i == 0 else
                                     (f"`{S.p} == {S.prices[S.i-1]} - 1` → 恰好少 1，递减接上" if S.p == S.prices[S.i-1] - 1
                                      else f"`{S.p}` 不是 `{S.prices[S.i-1]} - 1` → 递减断了")),
        'dec += 1': '递减接上：`dec` → ==`{dec}`==，右端点是 `i` 的合法段多了一个',
        'dec = 1': '断了：只剩 `[{p}]` 自己，`dec` 重置为 ==1==',
        'ans += dec': '右端点为 `{i}` 的递减子数组有 `{dec}` 个，`ans` = {B.ans} + {dec} = =={ans}==',
        'return ans': '一共 `{ans}` 个平滑下降阶段',
    },
    cards=dict(
        one_liner='按右端点分组：以 i 结尾的合法子数组恰好有 dec 个',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['平滑下降阶段：连续若干天，每天价格比前一天恰好少 1',
                 '只有一天也算，求这样的子数组个数',
                 '示例：`[3,2,1,4]` → `7`；本视频：`[4,3,2,1,5,4,4,3]` → `16`'],
        quote='右端点为 i 的连续递减子数组个数就是 dec，加到答案中。',
        quote_src='—— 灵茶山艾府题解',
        idea=['按子数组的==右端点==分组：`[3,2,1]` 结尾的 1 对应 `[3,2,1]`、`[2,1]`、`[1]` 三个',
              '连续递减：`dec += 1`；中断：`dec = 1`',
              '每个位置把 `dec` 累加进答案，不需要额外数组'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：第一天 `i = 0` 要单独算 1 个，所以条件里有 `i > 0`',
                 '易错：必须是恰好少 1，相等或少 2 都算中断',
                 '同类题：3255 长度为 K 的子数组的能量值 II、分组循环专题'],
    ),
)
