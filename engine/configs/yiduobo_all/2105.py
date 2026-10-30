def _water(S):
    if 'now_a' not in S:
        return ''
    return f"Alice 罐里 =={S['now_a']}== / {S['capacityA']}　Bob 罐里 =={S['now_b']}== / {S['capacityB']}　已加水 =={S['res']}== 次"


CONFIG = dict(
    num=2105, title='给植物浇水 II', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='两侧向中间模拟',
    tags=['灵神题单·滑动窗口与双指针', '难度分 1507'],
    code='''
class Solution(object):
    def minimumRefill(self, plants, capacityA, capacityB):

        l = 0
        r = len(plants) - 1
        now_a = capacityA
        now_b = capacityB
        res = 0
        while l < r:
            if now_a < plants[l]:
                now_a = capacityA
                res += 1
            now_a -= plants[l]

            if now_b < plants[r]:
                now_b = capacityB
                res += 1
            now_b -= plants[r]
        
            l += 1
            r -= 1

        if l == r:
            if now_a >= now_b:
                if now_a < plants[l]:
                    res += 1
            elif now_b < plants[l]:
                res += 1

        return res
''',
    call='Solution().minimumRefill([2,4,5,3,4], 5, 6)',
    expect=3,
    views=[
        dict(type='text', fn=_water, h=60),
        dict(type='array', var='plants', pointers={'l': 'blue', 'r': 'pink'}, h=300, label='plants（每株需要的水量）'),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), 'now_a', 'now_b', ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 记加水次数',
        'while l < r': lambda S, B, ret: (f'`l = {S.l} < r = {S.r}`：两人还没碰面，同时各浇一株' if S.l < S.r
                                          else f'`l = {S.l}`，`r = {S.r}`：碰面或错开，模拟结束'),
        'now_a = capacityA': lambda S, B, ret: (f'Alice 水罐一开始是满的：`now_a = {S.now_a}`' if 'res' not in S else f'Alice 水壶加满：`now_a = {S.now_a}`'),
        'now_a -= plants[l]': 'Alice 浇水：`now_a -= {plants[l]}` → {now_a}',
        'if now_b < plants[r]': '`now_b = {now_b}` 对 `plants[{r}] = {plants[r]}`：=={"不够，先加满" if now_b < plants[r] else "够了，直接浇"}==',
        'now_b = capacityB': lambda S, B, ret: (f'Bob 水罐一开始是满的：`now_b = {S.now_b}`' if 'res' not in S else f'Bob 水壶加满：`now_b = {S.now_b}`'),
        'now_b -= plants[r]': 'Bob 浇水：`now_b -= {plants[r]}` → {now_b}',
        'res += 1': '加水一次：`res` → {res}',
        'l += 1': 'Alice 往右一步：`l` → {l}',
        'r -= 1': 'Bob 往左一步：`r` → {r}',
        'if l == r': lambda S, B, ret: ('`l == r`：两人到了同一株，要看谁水多' if S.l == S.r
                                        else '`l != r`：植物是偶数株，没有共同的那一株'),
        'if now_a >= now_b': '`now_a = {now_a}`，`now_b = {now_b}`：=={"Alice 水不少于 Bob，由 Alice 浇" if now_a >= now_b else "Bob 水更多，由 Bob 浇"}==',
        'if now_a < plants[l]': lambda S, B, ret: (
            f'`now_a = {S.now_a}` 对 `plants[{S.l}] = {S.plants[S.l]}`：' + ('==不够，先加满==' if S.now_a < S.plants[S.l] else '够了，直接浇')
            if S.l < S.r else
            f'同一株：`now_a = {S.now_a}` 对 `plants[{S.l}] = {S.plants[S.l]}`：' + ('==不够，需加水==' if S.now_a < S.plants[S.l] else '够了')),
        'elif now_b < plants[l]': '`now_b = {now_b}` 对 `plants[{l}] = {plants[l]}`：=={"不够，需加水" if now_b < plants[l] else "够了"}==',
        'return res': '一共加水 `{res}` 次',
    },
    cards=dict(
        one_liner='直接模拟：从两侧向中间走，相遇时先比水量',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['Alice 从左、Bob 从右同时给植物浇水，水罐初始是满的',
                 '水不够就先加满再浇；到同一株时，水多的人浇，同样多则 Alice',
                 '求加水总次数，如 `[2,4,5,3,4], 5, 6`'],
        quote='若最后alice和bob相遇在同一个位置，需要优先判断二者谁剩下的水更多，然后再判断是否需要加水。',
        quote_src='—— yiduobo 题解原文',
        idea=['按题目过程模拟：`l`、`r` 同时向中间走',
              '`now_a`、`now_b` 记剩余水量，不够就加满、`res += 1`',
              '循环后若 `l == r`，先比谁水多，再看那个人够不够'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：加满水后仍要扣掉这株的水量',
                 '易错：相遇那株先比 `now_a >= now_b`（相等归 Alice），再判断是否加水',
                 '原文为 Python 2 写法，逻辑无需改动，直接运行'],
    ),
)
