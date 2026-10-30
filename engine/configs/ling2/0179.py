from functools import cmp_to_key as _ck

CASES = [[10, 2], [3, 30, 34, 5, 9], [0, 0]]


def _replay(arr):
    """重放排序过程，记录每一次 lambda 比较（lambda 不会被逐行追踪）"""
    log = []

    def cmp(a, b):
        log.append((a, b))
        return int(b + a) - int(a + b)
    sorted(arr, key=_ck(cmp))
    return log


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    line = S.get('_line')
    cv.text((x0 + 18, y0 + 4), '排序时的每一次比较：拼接 a+b 和 b+a，大的那种顺序留下', 24, T['muted'], bold=True)
    if line == 4 and isinstance(B.get('nums'), list):
        log = _replay(B['nums'])
        cv.text((x0 + 24, y1 - 34), f"排序前 nums = {B['nums']}", 22, T['muted'], mono=True)
        colw = (x1 - x0 - 40) / (2 if len(log) > 5 else 1)
        for k, (a, b) in enumerate(log):
            X = x0 + 24 + (k // 5) * colw if len(log) > 5 else x0 + 24
            Y = y0 + 50 + (k % 5) * 60
            ab, ba = a + b, b + a
            first = a if int(ab) >= int(ba) else b
            sign = '>' if int(ab) > int(ba) else ('=' if ab == ba else '<')
            cv.text((X, Y), f'{a}+{b}={ab} {sign} {ba}={b}+{a}', 22, T['text'], mono=True)
            cv.text((X + 6, Y + 26), f'→ "{first}" 排前面' if ab != ba else '→ 一样大，谁前都行', 19,
                    T['green'], bold=True)
    elif line == 3:
        cv.text((x0 + 24, y0 + 56), '先把数字转成字符串，方便拼接：', 24, T['text'])
        cv.text((x0 + 24, y0 + 96), '"3" + "30" = "330"，"30" + "3" = "303"', 26, T['code'], mono=True)
    elif line == 5:
        nums = S.get('nums') or []
        if nums and nums[0] == '0':
            cv.text((x0 + 24, y0 + 56), '排序后最大的都是 "0" → 全是 0', 26, T['text'])
            cv.text((x0 + 24, y0 + 96), '答案是 "0"，不能返回 "00"', 26, T['orange'], bold=True)
        else:
            cv.text((x0 + 24, y0 + 56), '按排好的顺序直接拼接：', 26, T['text'])
            cv.text((x0 + 24, y0 + 96), ' + '.join(f'"{x}"' for x in nums), 26, T['code'], mono=True)


def _cap_sort(S, B, ret):
    return f'按自定义规则排序：`a+b > b+a` 时 lambda 返回负数 → ==a 排在前面==，排完 `{S.nums}`'


def _cap_ret(S, B, ret):
    if S.nums[0] == '0':
        return f'`nums[0] == "0"`：最大的都是 0，说明==全是 0== → 返回 `"0"` 而不是 `"{"".join(S.nums)}"`'
    return f'拼接排好序的 nums → 返回 =={ret}=='


CONFIG = dict(
    num=179, title='最大数', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='自定义排序（交换论证）',
    tags=['字节30天', '热题173'],
    setup='from functools import cmp_to_key',
    code='''
class Solution:
    def largestNumber(self, nums: List[int]) -> str:
        nums = list(map(str, nums))
        nums.sort(key=cmp_to_key(lambda a, b: int(b + a) - int(a + b)))
        return "0" if nums[0] == "0" else ''.join(nums)
''',
    call=f'[Solution().largestNumber(nums) for nums in {CASES}]',
    expect=['210', '9534330', '0'],
    views=[
        dict(type='array', var='nums', label='nums（当前）', cell=96, h=150,
             color=lambda S, i, v: 'green' if S.get('_line') in (4, 5) else None),
        dict(type='custom', draw=_draw, h=320),
    ],
    watch=[('nums', 'nums', 'green')],
    captions={
        'nums = list(map': '新的一组输入：先把每个数==转成字符串==，`nums = {nums}`',
        'nums.sort': _cap_sort,
        'return': _cap_ret,
    },
    cards=dict(
        one_liner='排序规则：a+b > b+a 就让 a 排在 b 前面',
        complexity='时间 `O(n log n log U)`，空间 `O(n log U)`',
        problem=['给一组非负整数 `nums`，重新排列顺序（每个数不可拆分），拼成==最大的整数==',
                 '结果可能很大，返回字符串',
                 '示例：`[10,2]` → `"210"`；`[3,30,34,5,9]` → `"9534330"`',
                 '本视频依次跑三组：`[10,2]`、`[3,30,34,5,9]`、`[0,0]`'],
        quote='如果 nums = [a,b]，只有两个元素，怎么做？比较 a+b 和 b+a 谁大谁小即可。……==把上述规则作为排序时比大小的策略==，把 nums 排序后，拼接 nums 即为最优解。',
        quote_src='—— 灵茶山艾府题解',
        idea=['两个数：比较 `a+b` 和 `b+a`（字符串拼接）即可',
              '推广成排序规则，需要证明两件事：规则==有传递性==、排序结果==最优==',
              '`cmp_to_key`：返回负数表示 a 在前，所以写 `int(b + a) - int(a + b)`'],
        result='三组答案：`"210"`、`"9534330"`、`"0"`',
        after=[dict(heading='为什么这样排序是对的（原文证明）', lines=[
            '传递性：设 x 长 n 位、y 长 m 位，`x+y > y+x` ⇔ `x·10^m + y > y·10^n + x`',
            '⇔ `x/(10^n − 1) > y/(10^m − 1)`',
            '记 `f(s) = x/(10^n − 1)`，就是循环小数 `0.xxx…`',
            '比较拼接 = 比较实数 `f(s)`，实数有传递性 → ==规则没有矛盾==',
            '最优性（反证）：最优解若有相邻 `f(s_i) < f(s_i+1)`，交换后更大，矛盾',
        ])],
        summary=['时间 `O(n log n log U)`：排序比较 `O(n log n)` 次，每次 `O(log U)`',
                 '易错：全是 0 时答案是 `"0"`，看 `nums[0] == "0"` 即可',
                 '易错：不能直接按字符串字典序排，`"3"` 和 `"30"` 会排错',
                 '同类：3309. 连接二进制表示可形成的最大数值'],
    ),
)
