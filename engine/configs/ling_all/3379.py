def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    nums = S['nums']
    n = len(nums)
    live = S.get('_line') == 4
    cv.text((x0 + 18, y0 + 4), 'nums（循环数组）：弧线 = 从 i 走 nums[i] 步，落脚下标 (i + nums[i]) % n', 24, T['muted'], bold=True)
    cell = min(110, (x1 - x0 - 40) / n)
    sx = x0 + 20 + ((x1 - x0 - 40) - cell * n) / 2
    ya = y0 + 300
    cols = ['blue', 'pink', 'green', 'purple', 'cyan', 'orange']
    for i, v in enumerate(nums):
        X = sx + i * cell
        cv.rect((X + 3, ya, X + cell - 3, ya + cell * 0.8), fill=(50, 58, 70), outline=T['border'], width=2, r=8)
        cv.text((X + cell / 2, ya + cell * 0.4), v, 34, T['text'], anchor='mm', bold=True)
        cv.text((X + cell / 2, ya + cell * 0.8 + 8), i, 20, T['dim'], anchor='mt', mono=True)
    if live:
        for i, v in enumerate(nums):
            t = (i + v) % n
            c = T[cols[i % len(cols)]]
            xa, xb = sx + i * cell + cell / 2, sx + t * cell + cell / 2
            if t == i:
                cv.text((xa, ya - 14), '原地', 20, c, anchor='mb', bold=True)
                continue
            cv.arc_arrow((xa, ya - 6), (xb, ya - 6), 30 + abs(i - t) * cell * 0.28, c, 4)
        yr = ya + cell * 0.8 + 70
        cv.text((x0 + 18, yr), 'result：落脚处的值', 24, T['muted'], bold=True)
        for i, v in enumerate(nums):
            t = (i + v) % n
            X = sx + i * cell
            cv.rect((X + 3, yr + 40, X + cell - 3, yr + 40 + cell * 0.8), fill=T[cols[i % len(cols)]], r=8, alpha=210)
            cv.text((X + cell / 2, yr + 40 + cell * 0.4), nums[t], 34, T['bg'], anchor='mm', bold=True)
        cv.text((x0 + 18, yr + 40 + cell * 0.8 + 16), '例如 i=0：x=3，下标 (0+3)%6=3，result[0]=nums[3]=1', 22, T['dim'])


CONFIG = dict(
    num=3379, title='转换数组', difficulty='Easy', category='模拟',
    author='灵茶山艾府', technique='下标取模', tags=[],
    code='''
class Solution:
    def constructTransformedArray(self, nums: List[int]) -> List[int]:
        n = len(nums)
        return [nums[(i + x) % n] for i, x in enumerate(nums)]
''',
    call='Solution().constructTransformedArray([3,-2,1,1,-3,2])',
    expect=[1, 2, 1, -3, -2, -2],
    views=[
        dict(type='custom', draw=_draw, h=620),
    ],
    watch=['n'],
    captions={
        'n = len': '`n = {n}`：循环数组的长度，取模用',
        'return': '对每个 `i`：落脚下标 `(i + nums[i]) % n`，取 `nums[落脚]`。==正负不用分开判断==：向左就是 `x` 为负。一行推导式一次性算完 → `{ret}`',
    },
    cards=dict(
        one_liner='右移 / 左移统一成 `i + nums[i]`，再对 n 取模',
        complexity='时间 `O(n)`，空间 `O(1)`（返回值不计入）',
        problem=['`nums` 是循环数组；`result[i]` = 从下标 `i` 出发，按 `nums[i]` 的正负向右/向左走 `|nums[i]|` 步后落脚处的值',
                 '`nums[i] == 0` 时落在自己',
                 '示例：`[3,-2,1,1]` → `[1,1,1,3]`；本视频：`[3,-2,1,1,-3,2]` → `[1,2,1,-3,-2,-2]`'],
        quote='操作相当于从下标 i 移动到下标 i+nums[i]。……把下标 i+nums[i] 模 n。比如 n=4，在循环数组中，正数下标 5,9,13,… 都是下标 1，负数下标 −3,−7,−11,… 也都是下标 1。',
        quote_src='—— 灵茶山艾府题解',
        idea=['向左 `|x|` 步 = 下标 `i + x`（`x` 为负），不用分情况',
              '越界了就取模：Python 的 `%` 对负数也返回 `[0, n-1]`',
              '一行列表推导式，`enumerate` 同时拿到 `i` 和 `x`'],
        after=[dict(heading='逐个落脚（n = 6）', lines=[
            '`i=0, x=3` → `(0+3)%6 = 3` → `nums[3] = 1`',
            '`i=1, x=-2` → `(1-2)%6 = 5`（负数绕回末尾）→ `nums[5] = 2`',
            '`i=2, x=1` → `3` → `1`；`i=3, x=1` → `4` → `-3`',
            '`i=4, x=-3` → `(4-3)%6 = 1` → `-2`；`i=5, x=2` → `7%6 = 1` → `-2`',
        ])],
        summary=['时间 `O(n)`，空间 `O(1)`（返回值不计入）',
                 '易错：下标要 `% n`，不是 `% (n-1)`',
                 '易错：`result` 读的是原数组 `nums`，不是边改边读',
                 'Python 取模结果总是非负，不用特判负数；Java/C++ 要写 `((i+x)%n+n)%n`'],
    ),
)
