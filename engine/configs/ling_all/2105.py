def _water(S):
    if 'a' not in S:
        return ''
    return f"Alice 罐里 =={S['a']}== / {S['capacityA']}　Bob 罐里 =={S['b']}== / {S['capacityB']}　已灌满 =={S['ans']}== 次"


CONFIG = dict(
    num=2105, title='给植物浇水 II', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='相向双指针 · 模拟',
    tags=['灵神题单·滑动窗口与双指针', '难度分 1507'],
    code='''
class Solution:
    def minimumRefill(self, plants: List[int], capacityA: int, capacityB: int) -> int:
        ans = 0
        a, b = capacityA, capacityB
        i, j = 0, len(plants) - 1
        while i < j:
            # Alice 给植物 i 浇水
            if a < plants[i]:
                # 没有足够的水，重新灌满水罐
                ans += 1
                a = capacityA
            a -= plants[i]
            i += 1
            # Bob 给植物 j 浇水
            if b < plants[j]:
                # 没有足够的水，重新灌满水罐
                ans += 1
                b = capacityB
            b -= plants[j]
            j -= 1
        # 如果 Alice 和 Bob 到达同一株植物，那么当前水罐中水更多的人会给这株植物浇水
        if i == j and max(a, b) < plants[i]:
            # 没有足够的水，重新灌满水罐
            ans += 1
        return ans
''',
    call='Solution().minimumRefill([2,4,5,3,4], 5, 6)',
    expect=3,
    views=[
        dict(type='text', fn=_water, h=60),
        dict(type='array', var='plants', pointers={'i': 'blue', 'j': 'pink'}, h=300, label='plants（每株需要的水量）',
             ),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), 'a', 'b', ('ans', 'ans', 'green')],
    captions={
        'a, b = capacityA': '两人都从满罐开始：`a = {a}`，`b = {b}`',
        'i, j = 0': 'Alice 从左 `i = 0`，Bob 从右 `j = {j}`，同时往中间走',
        'while i < j': lambda S, B, ret: (f'`i = {S.i} < j = {S.j}`：两人还没碰面，各浇一株' if S.i < S.j
                                          else f'`i = {S.i}`，`j = {S.j}`：两人碰面或错开，循环结束'),
        'if a < plants[i]': '`a = {a}` 对 `plants[{i}] = {plants[i]}`：=={"不够，要先灌满" if a < plants[i] else "够了，直接浇"}==',
        'ans += 1': '重新灌满水罐，次数 `ans` → {ans}',
        'a = capacityA': 'Alice 灌满：`a = {capacityA}`',
        'a -= plants[i]': '灌完要==立刻浇水==：`a -= {plants[i]}` → {a}',
        'i += 1': 'Alice 走向下一株：`i` → {i}',
        'if b < plants[j]': '`b = {b}` 对 `plants[{j}] = {plants[j]}`：=={"不够，要先灌满" if b < plants[j] else "够了，直接浇"}==',
        'b = capacityB': 'Bob 灌满：`b = {capacityB}`',
        'b -= plants[j]': '`b -= {plants[j]}` → {b}',
        'j -= 1': 'Bob 走向前一株：`j` → {j}',
        'if i == j and': lambda S, B, ret: (
            f'两人到了同一株 `plants[{S.i}] = {S.plants[S.i]}`：水多的人来浇，`max(a, b) = {max(S.a, S.b)}` → =={"仍不够，要灌满" if max(S.a, S.b) < S.plants[S.i] else "够了"}=='
            if S.i == S.j else '`i != j`：没有碰到同一株（偶数株），无需额外处理'),
        'return ans': '一共重新灌满 `{ans}` 次',
    },
    cards=dict(
        one_liner='两人从两头同时走，谁水不够谁灌满',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['Alice 从左往右、Bob 从右往左给植物浇水，同时进行，水罐初始是满的',
                 '水够就必须浇；不够先灌满再浇。到同一株时，水多的人浇（相同则 Alice）',
                 '求重新灌满水罐的总次数，如 `[2,4,5,3,4], 5, 6`'],
        quote='灌满水后要立刻浇水，不能跳过。',
        quote_src='—— 灵茶山艾府题解',
        idea=['用 `a`、`b` 记两个罐里的水，`i`、`j` 是两人的位置',
              '循环里各浇一株：水不够就 `ans += 1` 并灌满，再扣掉水量',
              '循环结束若 `i == j`，水更多的人浇，仍不够才再灌一次'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：灌满后别忘了接着 `-= plants[i]`，不能跳过这株',
                 '易错：同一株只由水更多的人浇，用 `max(a, b) < plants[i]` 判断',
                 '这是「相向双指针」的模拟题，对比 yiduobo 的写法：结束后用 `now_a >= now_b` 分情况'],
    ),
)
