
def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    nums = S['nums']
    w = max(v.bit_length() for v in nums)
    n = len(nums)
    cw, rh, lw = 78, 56, 150
    sx = x0 + 30 + lw
    top = y0 + 92
    cv.text((x0 + 18, y0 + 6), '逐个异或进 res：两个 1 相遇变 0，一个 1 变 1（黄 = 当前数，蓝 = 已合并）', 24, T['muted'], bold=True)
    for b in range(w):
        cv.text((sx + b * cw + cw / 2, top - 10), f'2^{w - 1 - b}', 18, T['dim'], anchor='mb', mono=True)
    cur = None
    if 'num' in S:
        cur = nums.index(S['num'])
    res = S.get('res', 0)
    def pref(k):
        r = 0
        for v in nums[:k + 1]:
            r ^= v
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
    num=2527, title='查询数组异或美丽值', difficulty='Medium', category='位运算',
    author='yiduobo', technique='对称性分类 · 全体异或',
    tags=['灵神题单', '位运算', '难度分 1550'],
    code='''
class Solution(object):
    def xorBeauty(self, nums):

        res = 0
        for num in nums:
            res ^= num
        
        return res
''',
    call='Solution().xorBeauty([3, 5, 12, 9])',
    expect=3,
    views=[
        dict(type='custom', draw=_draw, h=420),
        dict(type='array', var='nums', h=120, label='nums', cell=70,
             color=lambda S, i, v: 'yellow' if 'num' in S and i == S['nums'].index(S['num']) else None),
    ],
    watch=['num', ('res', 'res', 'green')],
    captions={
        'res = 0': '`res = 0`：0 异或任何数都等于那个数，是异或的“单位元”',
        'for num in nums': lambda S, B, r: ('nums 取完了，循环结束' if B.get('num') == S.num and 'num' in B else f'取出 `num = {S.num}`：它在三元组里有 `i=j=k` 这一种不会被抵消的情况'),
        'res ^= num': '`res ^= num`：{B.res} ^ {num} → =={res}==。同一位上两个 1 抵消成 0，只剩奇数个 1 的位是 1',
        'return res': '其余五类三元组都成对抵消为 0，答案就是全体异或 `{res}`',
    },
    cards=dict(
        one_liner='三元组里 i、j、k 地位等价：除了 i=j=k，其余成对抵消',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`(nums[i] | nums[j]) & nums[k]` 叫有效值，对所有 `(i, j, k)` 三元组求异或',
                 '返回这个异或美丽值',
                 '示例：`[1,4]` → `5`；本视频 `[3,5,12,9]` → `3`'],
        quote='乍一看感觉是与数位操作有关的问题，不过注意到本题最终是计算异或值，且参与最终异或运算的中间结果所需的三元组(i, j, k)中的i、j、k是完全等价的',
        quote_src='—— yiduobo 题解原文',
        idea=['先利用 i、j、k 的等价，==按“谁和谁相同”分五类==讨论',
              '三者两两不同、`i=j≠k`、`i=k≠j` 等：总能配出一个有效值相同的“镜像”三元组 → 异或为 0',
              '只有 `i=j=k` 找不到镜像，`(x|x)&x = x` → 答案是 ==所有 nums 异或==',
              '于是一个循环 `res ^= num` 就够了'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '核心：相同值异或为 0，配对出来的三元组全部消掉',
                 '易错：别去枚举 `n^3`，`n` 最大 `10^5`',
                 '原文为 Python 2 风格（`class Solution(object)`），代码无需改动',
                 '对比灵神：他一行 `reduce(xor, nums)`，并补充了拆位法；这里是分类讨论的推导'],
    ),
)
