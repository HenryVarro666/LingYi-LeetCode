_D = lambda S: S['_inner'].get('d')


def _can(S, B, ret):
    i, d, c = S.i, S.d, S.c
    pos = ['百位', '十位', '个位'][i]
    if c <= 0:
        return f'数字 `{d}` 已经用光（`cnt[{d}] = 0`）→ 跳过'
    if i == 0 and d == 0:
        return f'{pos}不能填 `0`（前导零）→ 跳过'
    if i == 2 and d % 2:
        return f'{pos}只能填偶数，`{d}` 是奇数 → 跳过'
    return f'{pos}填 `{d}`：还剩 `{c}` 个，满足要求 → ==可以填=='


CONFIG = dict(
    num=2094, title='找出 3 位偶数', difficulty='Easy', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='回溯：百位、十位、个位逐位填数',
    tags=['灵神核心路线', '灵神题单·链表树与回溯'],
    code='''
class Solution:
    def findEvenNumbers(self, digits: List[int]) -> List[int]:
        cnt = [0] * 10
        for d in digits:
            cnt[d] += 1

        ans = []
        # i=0 百位，i=1 十位，i=2 个位，x 表示当前正在构造的数字
        def dfs(i: int, x: int):
            if i == 3:
                ans.append(x)
                return
            for d, c in enumerate(cnt):
                if c > 0 and (i == 0 and d > 0 or i == 1 or i == 2 and d % 2 == 0):
                    cnt[d] -= 1  # 消耗一个数字 d
                    dfs(i + 1, x * 10 + d)
                    cnt[d] += 1  # 复原
        dfs(0, 0)
        return ans
''',
    call='Solution().findEvenNumbers([2, 2, 0])',
    expect=[202, 220],
    views=[
        dict(type='array', var='cnt', label='cnt[d]：数字 d 还剩几个（下标 = 数字）', cell=64, h=170,
             pointers={_D: 'pink'}, pointer_labels={_D: 'd'},
             color=lambda S, i, v: 'green' if v > 0 else None,
             dim=lambda S, i, v: v == 0),
        dict(type='text', fn=lambda S: ('当前构造 `x = {}`，正在填第 {} 位（{}）'.format(S['_inner'].get('x'), S['_inner'].get('i') + 1, ['百位', '十位', '个位'][S['_inner'].get('i')]) if S['_inner'].get('i', 3) < 3 else '三位都填好了'), size=34),
        dict(type='calls', h=200),
        dict(type='stack', var='ans', label='ans', h=100),
    ],
    watch=[('i', lambda S: S['_inner'].get('i'), 'blue'), ('x', lambda S: S['_inner'].get('x'), 'yellow'),
           ('d', _D, 'pink'), ('ans', 'ans', 'green')],
    skip=['for d, c in enumerate'],
    max_steps=80,
    captions={
        5: '统计数字个数：`cnt[{d}]` = {cnt[d]}',
        'ans = []': '`cnt` 就是==各数字的库存==；填数字时要先看库存',
        'if i == 3': lambda S, B, ret: ('三位都填好了 → `x = {}` 是一个合法答案'.format(S.x) if S.i == 3
                                        else '`i = {}`：还没填满三位，枚举这一位填哪个数字 `d`'.format(S.i)),
        'if c > 0 and': _can,
        'cnt[d] -= 1': '消耗一个数字 `{d}`：`cnt[{d}]` → {cnt[d]}，下一层看不到它',
        'dfs(i + 1': '递归填下一位：`x = {B.x} * 10 + {B.d} = {B.x * 10 + B.d}`',
        '复原': '回溯：把数字 `{d}` 还回库存，`cnt[{d}]` → {cnt[d]}',
        'dfs(0, 0)': '从百位开始：`dfs(0, 0)`',
        'ans.append': '记录答案 `{x}`',
        'return ans': '搜索结束，共 `{len(ret)}` 个。因为按 d 从小到大枚举，==答案天然递增==',
    },
    cards=dict(
        one_liner='换个角度：不枚举数，而是逐位填数字，并限制每位能填什么',
        complexity='时间 `O(n + 10^k)`，空间 `O(k)`（k = 3）',
        problem=['`digits` 里每个数字 0~9，可重复；挑 3 个按任意顺序拼成三位数',
                 '要求==无前导零==、是==偶数==、互不相同，结果升序返回',
                 '本视频：`[2,2,0]` → `[202,220]`'],
        quote='百位数不能填 0。十位数随便填。个位数只能填偶数。用回溯实现上述枚举，注意填的数字个数必须有剩余。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['`cnt[d]` 记库存：填一个就减一，回溯时加回来',
              '`i = 0/1/2` 对应百/十/个位，每位有各自的限制',
              '枚举的是==数字的值==而不是下标，重复数字不会产生重复的数'],
        result='找到 202 和 220，没有奇数、没有前导零 ✓',
        summary=['时间 `O(n + 10^k)`：搜索树是高 3 的 10 叉树',
                 '易错：回溯时要把 `cnt[d]` 加回去，否则后面的分支会缺数字',
                 '`for d, c in enumerate(cnt)` 按 d 从小到大，答案自动有序',
                 '另一种写法：暴力枚举 100~998 的偶数，用 `Counter(...) <= cnt` 判断能否组成'],
    ),
)
