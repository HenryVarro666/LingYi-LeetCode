NUMS = [2, 7, 9, 3, 1]          # 演示输入（金额互不相同，可由 num 反查下标）
FX = [0, 0]                      # FX[k + 2] = f[k]；前两个 0 是「还没有房子」
for _x in NUMS:
    FX.append(max(FX[-2] + _x, FX[-1]))


def _phase(S, B):
    """返回 (k, done)：当前看第 k 家；done 表示这一家的 f[k] 已经滚动进 last_one"""
    if 'num' not in S:
        return -1, True
    k = NUMS.index(S['num'])
    return k, ('num' in B and B['num'] == S['num'])


def _roll(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    if 'last_one' not in S:
        cv.text((x0 + 18, y0 + 44), '（变量尚未创建）', 24, T['dim'])
        return
    k, done = _phase(S, B)
    top = k if done else k - 1          # 已知的最后一个 f 下标
    n = len(NUMS)
    cell = 100
    sx = x0 + 20 + (x1 - x0 - 40 - cell * (n + 2)) / 2
    cv.text((x0 + 18, y0 + 4), 'f[i] = 前 i 家最多偷多少（最左两格：还没有房子，算 0）', 24, T['muted'], bold=True)
    y = y0 + 50
    lo_idx = top                         # last_one 对应的 f 下标
    lt_idx = top - 1                     # last_two 对应的 f 下标
    for j in range(-2, n):
        X = sx + (j + 2) * cell
        known = j <= top
        fill = T['panel2']
        if j == lo_idx:
            fill = T['blue']
        elif j == lt_idx:
            fill = T['pink']
        if j < 0:
            cv.rect((X + 6, y, X + cell - 6, y + 80), fill=fill if fill != T['panel2'] else None,
                    outline=T['border'], width=2, r=10)
        else:
            cv.rect((X + 6, y, X + cell - 6, y + 80), fill=fill, outline=T['border'], width=1, r=10)
        if known:
            cv.text((X + cell / 2, y + 40), FX[j + 2], 32, T['bg'] if fill != T['panel2'] else T['text'],
                    anchor='mm', bold=True)
        else:
            cv.text((X + cell / 2, y + 40), '?', 30, T['dim'], anchor='mm', bold=True)
        cv.text((X + cell / 2, y + 88), f'f[{j}]' if j >= 0 else '—', 18, T['dim'], anchor='mt', mono=True)
    for j, name, c, dy in [(lt_idx, 'last_two', 'pink', 30), (lo_idx, 'last_one', 'blue', 0)]:
        X = sx + (j + 2) * cell + cell / 2
        cv.tri_up(X, y + 122, 10, T[c])
        cv.text((X, y + 138 + dy), name, 22, T[c], anchor='mt', bold=True)
    if k >= 0 and not done:
        X = sx + (k + 2) * cell
        cv.rect((X + 4, y - 4, X + cell - 4, y + 84), outline=T['green'], width=4, r=12)
        cv.text((X + cell / 2, y - 8), '下一个', 20, T['green'], anchor='mb', bold=True)


def _formula(cv, S, B, box, T):
    if 'num' not in S:
        s = '只和前两个状态有关 → ==滚动==：`last_two`、`last_one` 初始都为 0' if 'last_one' in S else ''
    else:
        k, done = _phase(S, B)
        rolled = done and (B.get('last_one'), B.get('last_two')) != (S['last_one'], S['last_two'])
        V = B if rolled else S
        if done and not rolled:
            s = f"已看完 {k + 1} 家：`last_one = {S['last_one']}`"
        else:
            s = (f"`f[{k}] = max(last_two + num, last_one)` = max({V['last_two']} + {V['num']}, {V['last_one']}) = "
                 f"=={max(V['last_two'] + V['num'], V['last_one'])}==")
    if s:
        cv.rich(box[0] + 22, box[1] + 8, s, box[2] - box[0] - 44, size=28, accent=(45, 212, 191), max_lines=2, line_gap=1.4)


def _cap_roll(S, B, ret):
    lt, lo, num = B.last_two, B.last_one, B.num
    rob = lt + num
    pick = '偷' if rob > lo else '不偷'
    return (f'偷这家：`last_two + num = {lt} + {num} = {rob}`；不偷：`last_one = {lo}` → =={pick}==；'
            f'同时赋值：`last_one = {S.last_one}`，`last_two` 接过旧的 `{lo}`')


CONFIG = dict(
    num=198, title='打家劫舍', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='线性 DP + 滚动变量',
    code='''
class Solution(object):
    def rob(self, nums):
        if not nums:
            return 0

        last_two = last_one = 0
        for num in nums:
            last_one, last_two = max(last_two + num, last_one), last_one

        return last_one
''',
    call=f'Solution().rob({NUMS})',
    expect=12,
    views=[
        dict(type='custom', draw=_formula, h=60),
        dict(type='array', var='nums', label='nums（房屋金额）',
             color=lambda S, k, v: 'green' if 'num' in S and v == S['num'] else None,
             dim=lambda S, k, v: 'num' in S and k > NUMS.index(S['num']), cell=100, h=190),
        dict(type='custom', draw=_roll, h=330),
    ],
    watch=[('num', 'num', 'green'), ('last_two', 'last_two', 'pink'), ('last_one', 'last_one', 'blue')],
    captions={
        'if not nums': '特判：没有房子直接返回 0',
        'last_two = last_one = 0': '`f[i]` 只和 `f[i-1]`、`f[i-2]` 有关 → 只留两个变量，初始都是 0',
        'for num in nums': lambda S, B, ret: (f'下一家 `num = {S.num}`：此刻 `last_two = f[i-2] = {S.last_two}`，'
                                              f'`last_one = f[i-1] = {S.last_one}`'
                                              if B.get('num') != S.num else '所有房子都看完了'),
        'last_one, last_two = max': _cap_roll,
        'return last_one': '`last_one` 就是 `f[n-1]`：最多偷 =={ret}==',
    },
    cards=dict(
        one_liner='偷第 i 家就不能偷 i-1 家：f[i] = max(f[i-2] + nums[i], f[i-1])，再滚动起来',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['一排房屋，金额为 `nums[i]`；==相邻两间不能同时偷==，求最多偷多少',
                 '示例：`[2,7,9,3,1]` → `12`（偷 `2 + 9 + 1`）'],
        quote='由于这里状态转移只与前两个数有关，于是可以滚动起来。==需要注意的是滚动时要么需要记录其中一个状态，要么使用python同时赋值的写法==。',
        quote_src='—— yiduobo 题解',
        idea=['`f[i]` = 前 i 家能偷到的最大金额',
              '偷第 i 家 → 不能偷 i-1 家：`f[i-2] + nums[i]`；不偷 → `f[i-1]`',
              '`f[i] = max(f[i-2] + nums[i], f[i-1])`，只用到前两项 → 两个变量滚动'],
        after=[dict(heading='为什么要「同时赋值」', lines=[
            '新 `last_two` 应该等于==旧的== `last_one`',
            '若分两行先改 `last_one`，再写 `last_two = last_one` 就拿到了==新值==',
            'Python 先算出右边整个元组，再一起赋给左边 → 不需要临时变量',
        ])],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '原文为 Python 2 写法：本题仅删去 docstring，其余未改',
                 '边界：原文写 `f[0] = nums[0]`、`f[1] = max(nums[0], nums[1])`；代码用两个 0 起步省掉特判',
                 '滚动时注意顺序：用同时赋值，或先用临时变量记下旧值'],
    ),
)
