
def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    nums = S['nums']
    w = max(v.bit_length() for v in nums)
    n = len(nums)
    cw, rh, lw = 78, 56, 150
    sx = x0 + 30 + lw
    top = y0 + 92
    cv.text((x0 + 18, y0 + 6), '逐个或进 res：只要这一列出现过 1，res 该位就是 1（黄 = 当前数，蓝 = 已合并）', 24, T['muted'], bold=True)
    for b in range(w):
        cv.text((sx + b * cw + cw / 2, top - 10), f'2^{w - 1 - b}', 18, T['dim'], anchor='mb', mono=True)
    cur = None
    if 'num' in S:
        cur = nums.index(S['num'])
    res = S.get('res', 0)
    def pref(k):
        r = 0
        for v in nums[:k + 1]:
            r |= v
        return r
    done = -1
    if cur is not None:
        done = cur if res == pref(cur) else cur - 1
    for r, v in enumerate(nums):
        y = top + r * rh
        used = r <= done
        iscur = r == cur
        cv.text((x0 + 30, y + rh / 2), f'nums[{r}]={v}', 24, T['yellow'] if iscur else (T['text'] if used else T['muted']), anchor='lm', mono=True, bold=iscur)
        for b in range(w):
            bit = (v >> (w - 1 - b)) & 1
            X = sx + b * cw
            if bit:
                fill = T['yellow'] if iscur else (T['blue'] if used else T['panel2'])
                tc = T['bg'] if (iscur or used) else T['muted']
            else:
                fill, tc = T['panel2'], T['dim']
            cv.rect((X + 4, y + 4, X + cw - 4, y + rh - 4), fill=fill, r=8, alpha=255 if (used or iscur) else 150)
            cv.text((X + cw / 2, y + rh / 2), bit, 26, tc, anchor='mm', bold=True, mono=True)
    yc = top + n * rh + 12
    cv.line([(x0 + 30, yc - 4), (sx + w * cw, yc - 4)], T['border'], 2)
    cv.text((x0 + 30, yc + rh / 2 + 4), 'res 二进制', 24, T['green'], anchor='lm', bold=True)
    for b in range(w):
        bit = (res >> (w - 1 - b)) & 1
        X = sx + b * cw
        cv.rect((X + 4, yc + 8, X + cw - 4, yc + rh), fill=(T['green'] if bit else T['panel2']), r=8)
        cv.text((X + cw / 2, yc + rh / 2 + 4), bit, 26, T['bg'] if bit else T['dim'], anchor='mm', bold=True, mono=True)
    cv.text((sx + w * cw + 30, yc + rh / 2 + 4), f'= {res}', 34, T['green'], anchor='lm', bold=True, mono=True)


CONFIG = dict(
    num=2317, title='操作后的最大异或和', difficulty='Medium', category='位运算',
    author='yiduobo', technique='读懂操作 · 全体按位或',
    tags=['灵神题单', '位运算', '难度分 1679'],
    code='''
class Solution(object):
    def maximumXOR(self, nums):

        res = 0
        for num in nums:
            res |= num
        
        return res
''',
    call='Solution().maximumXOR([3, 2, 4, 6])',
    expect=7,
    views=[
        dict(type='custom', draw=_draw, h=420),
        dict(type='array', var='nums', h=120, label='nums', cell=70,
             color=lambda S, i, v: 'yellow' if 'num' in S and i == S['nums'].index(S['num']) else None),
    ],
    watch=['num', ('res', 'res', 'green')],
    captions={
        'res = 0': '`res = 0`：或运算的单位元，一开始哪一位都没出现过 1',
        'for num in nums': lambda S, B, r: ('nums 取完了，循环结束' if B.get('num') == S.num and 'num' in B else f'取出 `num = {S.num}`：看它在哪些位上有 1'),
        'res |= num': '`res |= num`：{B.res} | {num} → =={res}==。res 里为 1 的位 = 至少有一个数在这一位是 1',
        'return res': '每一位只要出现过 1，就能把多余的 1 擦掉只留一个 → 答案 `{res}`',
    },
    cards=dict(
        one_liner='操作只能把 1 擦成 0：有 1 的位，都能保留成答案的 1',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['一次操作：选任意 `x` 和下标 `i`，令 `nums[i] = nums[i] & (nums[i] ^ x)`',
                 '操作次数不限，求所有数异或值的最大可能',
                 '示例：`[3,2,4,6]` → `7`'],
        quote='这个操作可以选择让num[i]中任意位上的1变为0，次数不限。',
        quote_src='—— yiduobo 题解原文',
        idea=['`&` 只对值为 1 的位生效；`x` 在这位取 1，异或后这位变 0，与原值相与仍是 0',
              '所以能把 `nums[i]` 任意位上的 1 变 0，0 却变不成 1',
              '某位上没有 1：答案这位只能是 0；有 1：删到只剩一个，这位就是 1',
              '这恰好是把所有数 ==或== 起来'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：别把操作当成“任意修改”，它只能把 1 变 0',
                 '最大异或和 = 所有数按位或，二进制每位都取到能取的 1',
                 '原文为 Python 2 风格（`class Solution(object)`），代码无需改动',
                 '对比灵神：灵神分四个“提示”逐步推出，最后用 `reduce(or_, nums)`'],
    ),
)
