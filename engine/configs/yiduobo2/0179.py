NUMS = [3, 30, 34, 5, 9]


def _in_cmp(S):
    return 'x' in S and 'y' in S


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), 'cmp(x, y)：比较两种拼接顺序（等长字符串，字典序 = 数值大小）', 24, T['muted'], bold=True)
    if _in_cmp(S):
        x, y = str(S['x']), str(S['y'])
        xy, yx = x + y, y + x
        big = xy > yx
        cx = x0 + (x1 - x0) / 2
        for k, (lab, s, win) in enumerate((('str(x) + str(y)', xy, big), ('str(y) + str(x)', yx, not big))):
            Y = y0 + 60 + k * 100
            cv.text((cx - 60, Y + 36), lab, 26, T['muted'], anchor='rm', mono=True)
            w = cv.tlen(s, 40, mono=True) + 40
            cv.rect((cx - 30, Y, cx - 30 + w, Y + 72), fill=T['green'] if win else T['panel2'], r=10, outline=T['border'])
            cv.text((cx - 10, Y + 36), s, 40, T['bg'] if win else T['text'], anchor='lm', mono=True, bold=True)
        first, second = (x, y) if big else (y, x)
        cv.text((cx, y0 + 290), f'{first} 应该排在 {second} 前面', 30, T['green'], anchor='mm', bold=True)
    elif S.get('_line') in (5, 8) and isinstance(S.get('nums'), list):
        cv.text((x0 + 24, y0 + 60), '排序结束：相邻两个数都满足 x+y > y+x', 26, T['text'])
        nums = S['nums']
        for k in range(len(nums) - 1):
            a, b = str(nums[k]), str(nums[k + 1])
            cv.text((x0 + 40, y0 + 104 + k * 40), f'{a}+{b} = {a + b}  >  {b + a} = {b}+{a}', 24, T['code'], mono=True)


def _cap_if(S, B, ret):
    x, y = str(S.x), str(S.y)
    xy, yx = x + y, y + x
    if xy > yx:
        return f'`"{xy}" > "{yx}"`：x 在前拼出来更大'
    return f'`"{xy}" < "{yx}"`：y 在前拼出来更大'


CONFIG = dict(
    num=179, title='最大数', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='证明传递性 + 自定义比较排序',
    tags=['字节30天', '热题173'],
    setup='from functools import cmp_to_key',
    code='''
class Solution(object):
    def largestNumber(self, nums):
        nums = sorted(nums, key=cmp_to_key(self.cmp))

        if max(nums) == 0:
            return '0'
        else:
            return ''.join([str(x) for x in nums])

    def cmp(self, x, y):
        if str(x) + str(y) > str(y) + str(x):
            return -1
        return 1
''',
    call=f'Solution().largestNumber({NUMS})',
    expect='9534330',
    views=[
        dict(type='array', var='nums', label='nums（蓝 = x，粉 = y；排序结束后变成新顺序）', cell=100, h=160,
             color=lambda S, i, v: ('blue' if v == S['x'] else 'pink' if v == S['y'] else None) if _in_cmp(S)
             else ('green' if S.get('_line') in (5, 8) else None)),
        dict(type='custom', draw=_draw, h=360),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink')],
    captions={
        'nums = sorted': 'Python 3 的 `sorted` 不再接受 cmp 函数，用 `cmp_to_key(self.cmp)` 包一层；排序时反复调用 `cmp`',
        'if str(x) + str(y)': _cap_if,
        'return -1': '返回 `-1`：==x = {x} 排在 y = {y} 前面==',
        'return 1': '返回 `1`：==y = {y} 排在 x = {x} 前面==',
        'if max(nums) == 0': lambda S, B, r: (f'排好了：`{S.nums}`。`max(nums) = {max(S.nums)}`，不全是 0'
                                              if max(S.nums) else '全是 0 → 答案是 "0"'),
        "return ''.join": '按顺序拼接：返回 =={ret}==',
    },
    cards=dict(
        one_liner='先证明“x+y > y+x 则 x 在前”有传递性，再放心排序',
        complexity='时间 `O(n log n · L)`，空间 `O(n · L)`（L 为数字位数）',
        problem=['给一组非负整数 `nums`，重新排列顺序（每个数不可拆分），拼成==最大的整数==',
                 '结果可能很大，返回字符串',
                 '示例：`[10,2]` → `"210"`；`[3,30,34,5,9]` → `"9534330"`'],
        quote='这说明如果nums[0]排在nums[1]之前较优，同时nums[1]排在nums[2]之前较优，那么==一定有nums[0]排在nums[2]之前较优==。于是我们可以将nums排好序，然后依次拼接起来就好了。',
        quote_src='—— yiduobo 题解原文',
        idea=['`a·10^l1 + b > b·10^l0 + a` ⇔ `a(10^l1 − 1) > b(10^l0 − 1)`',
              '两个这样的不等式==相乘==，约掉 `b(10^l1 − 1)`，就得到 a、c 之间的不等式',
              '有传递性才能排序；有逆序对就交换，答案一定更大 → 排好序就是最优'],
        result='拼接 `9 5 34 3 30` → `"9534330"`',
        summary=['时间 `O(n log n · L)`：每次比较要拼接字符串',
                 '易错：全是 0 时要返回 `"0"`，这里用 `max(nums) == 0` 判断',
                 '易错：`cmp` 返回负数表示 x 在前，别写反',
                 '原文为 Python 2 写法：`sorted(nums, self.cmp)` 改用 `cmp_to_key` 包装，删去文档字符串',
                 '对比灵神：用 `f(s) = x/(10^n − 1)` 化成实数比较来证传递性'],
    ),
)
