CONFIG = dict(
    num=374, title='猜数字大小', difficulty='Easy', category='二分算法',
    author='yiduobo', technique='二分答案',
    tags=['灵神题单'],
    setup='''
PICK = 6
NUMS = list(range(1, 11))
def guess(num):
    return 0 if num == PICK else (-1 if num > PICK else 1)
''',
    code='''
class Solution(object):
    def guessNumber(self, n):

        l = 1
        r = n
        while True:
            mid = (l + r) // 2
            res = guess(mid)
            if res == 0:
                return mid
            elif res > 0:
                l = mid + 1
            else:
                r = mid - 1
''',
    call='Solution().guessNumber(10)',
    expect=6,
    views=[
        dict(type='text', size=26, h=60,
             fn=lambda S: (f"候选区间 [`{S['l']}`, `{S['r']}`]" + (f"，刚猜 `{S['mid']}`" if 'mid' in S else '')) if 'r' in S else '1..10 里藏着一个数，只能问 guess(x)'),
        dict(type='array', var=lambda S: list(range(1, 11)), label='候选数字（绿 = 被猜中）', cell=84, h=300,
             pointers={'l-1': 'blue', 'r-1': 'pink', 'mid-1': 'yellow'},
             window=('l-1', 'r-1'), index=False,
             pointer_labels={'l-1': 'l', 'r-1': 'r', 'mid-1': 'mid'},
             color=lambda S, i, v: 'green' if S.get('res') == 0 and 'mid' in S and v == S['mid'] else None,
             dim=lambda S, i, v: 'r' in S and not (S['l'] <= v <= S['r'])),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('mid', 'mid', 'yellow'), ('res', 'res', 'green')],
    captions={
        'l = 1': '数字范围从 1 开始：`l = 1`',
        'r = n': '`r = n = {r}`：答案就在 [1, n]',
        'while True': '一定能猜中，所以循环直到 `return`',
        'mid = ': '猜区间中点 `mid = ({l} + {r}) // 2 = =={mid}==`',
        'res = guess': lambda S, B, r: f'`guess({S.mid}) = {S.res}`：' + ('==猜中=='  if S.res == 0 else ('猜小了（答案更大）' if S.res > 0 else '猜大了（答案更小）')),
        'if res == 0': lambda S, B, r: ('`res == 0`：猜中 → 直接返回 mid' if S.res == 0 else '`res != 0`：没猜中，继续看方向'),
        'elif res > 0': lambda S, B, r: ('`res > 0`：==mid 太小==，答案在右边' if S.res > 0 else '`res < 0`：mid 太大，答案在左边'),
        'l = mid + 1': '`l = mid + 1 = {l}`：mid 已经猜过且偏小，排除 mid 及其左侧',
        'r = mid - 1': '`r = mid - 1 = {r}`：mid 已经猜过且偏大，排除 mid 及其右侧',
        'return mid': '猜中了，答案 `{mid}`',
    },
    cards=dict(
        one_liner='每猜一次，答案范围砍掉一半',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['在 `1..n` 中选了一个数，你每次猜 `x`，接口 `guess(x)` 告诉你方向',
                 '返回 `-1`：猜大了；`1`：猜小了；`0`：猜对了',
                 '本视频：`n = 10`，答案 `6`'],
        quote='经典的问题，直接二分答案即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['答案在 `[l, r]` 里，每次猜中点 `mid`',
              '`guess` 返回 `> 0` 说明 mid 偏小 → `l = mid + 1`',
              '返回 `< 0` 说明偏大 → `r = mid - 1`；mid 已经猜过，所以要 ±1'],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '注意 `guess` 的符号：返回 1 表示答案更大，要往右走',
                 '`l = mid + 1` / `r = mid - 1` 把已猜过的 mid 排除，循环不会卡住',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`'],
    ),
)
