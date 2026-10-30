def _rev(x):
    return int(bin(x)[2:][::-1], 2)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    nums = S.get('nums')
    if nums is None:
        return
    done = S.get('_line', 0) >= 4
    cv.text((x0 + 18, y0 + 4), '每个数：二进制 → 反转 → 反射值（排序键 = (反射值, 原值)）', 24, T['muted'], bold=True)
    cols = [('x', 90), ('bin(x)', 190), ('反转后', 190), ('反射值', 120)]
    rh = min(64, (y1 - y0 - 120) / (len(nums) + 1))
    X0 = x0 + 30
    yy = y0 + 56
    xx = X0
    for name, w in cols:
        cv.text((xx + w / 2, yy), name, 22, T['muted'], anchor='mm', bold=True)
        xx += w
    yy += rh
    for k, x in enumerate(nums):
        b = bin(x)[2:]
        r = b[::-1]
        vals = [str(x), b, r, str(_rev(x))]
        colors = [T['text'], T['cyan'], T['pink'], T['green'] if done else T['yellow']]
        xx = X0
        if done:
            cv.rect((X0 - 8, yy - rh / 2 + 3, xx + sum(w for _, w in cols) - 8, yy + rh / 2 - 3), fill=T['panel2'], r=6)
        for (name, w), v, c in zip(cols, vals, colors):
            cv.text((xx + w / 2, yy), v, 26, c, anchor='mm', bold=True, mono=True)
            xx += w
        cv.text((xx + 10, yy), f'#{k + 1}', 20, T['dim'], anchor='lm')
        yy += rh
    cv.text((X0, y1 - 28), '已按键排序：反射值相同的，原值小的在前' if done else '排序前：保持输入顺序', 22,
            T['green'] if done else T['muted'], anchor='lm', bold=True)


CONFIG = dict(
    num=3769, title='二进制反射排序', difficulty='Easy', category='位运算',
    author='灵茶山艾府', technique='自定义排序键', tags=['灵神题单', '难度分 1364'],
    code='''
class Solution:
    def sortByReflection(self, nums: List[int]) -> List[int]:
        # O(1) 反转见另一份代码【Python3 位运算】
        nums.sort(key=lambda x: (int(bin(x)[2:][::-1], 2), x))
        return nums
''',
    call='Solution().sortByReflection([3, 6, 5, 8, 12])',
    expect=[8, 3, 6, 12, 5],
    views=[
        dict(type='array', var='nums', h=150, label='nums',
             color=lambda S, i, v: 'green' if S.get('_line', 0) >= 4 else None),
        dict(type='custom', draw=_draw, h=420),
    ],
    watch=[('nums', 'nums', 'green')],
    captions={
        'nums.sort': lambda S, B, r: ('排序键 `(反射值, x)`：先比反射值，相同再比原值。结果 `' + str(S.nums) + '`，'
                                      '如 3、6、12 的反射值都是 3，按原值 ==3 < 6 < 12== 排'),
        'return nums': '`nums` 已原地排好，返回 `{nums}`',
    },
    cards=dict(
        one_liner='自己造排序键：先比二进制反转值，再比原值',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['二进制反射 = 把正整数的二进制（不含前导零）反转，再转回十进制',
                 '按反射值升序排；反射值相同，==原值小的在前==',
                 '示例：`[3,6,5,8]` → `[8,3,6,5]`；本视频：`[3,6,5,8,12]`'],
        quote='用库函数 O(1) 得到二进制反转后的结果。Python 需要手写。',
        quote_src='—— 灵茶山艾府题解',
        idea=['Python 里 `bin(x)[2:]` 去掉 `0b`，`[::-1]` 反转，`int(.., 2)` 转回十进制',
              '`key` 返回元组 `(反射值, x)`：元组比较天然就是「先比第一项，相同再比第二项」',
              '这样一行 `sort` 就把题目的两条规则都实现了'],
        summary=['时间 `O(n log n)`（每个数的反转是 `O(1)` 级位数），空间 `O(1)`（忽略排序栈）',
                 '易错点：反转要==忽略前导零==，不能固定按 32 位反转后直接用（8 → 1000 → 0001）',
                 '另一种写法：用 190 题的位运算反转 `reverseBits(x) >> (32 - x.bit_length())`，同样 `O(1)`',
                 '相关：190. 颠倒二进制位'],
    ),
)
