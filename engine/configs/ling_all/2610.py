NUMS = [1, 3, 4, 1, 2, 3, 1]


def _draw_nums(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = len(NUMS)
    cell = min(84, (x1 - x0 - 40) / n)
    sx = x0 + 20 + ((x1 - x0 - 40) - cell * n) / 2
    cv.text((x0 + 18, y0 + 2), 'nums（蓝框 = 正在处理的元素，灰 = 已处理）', 22, T['muted'], bold=True)
    cnt = S.get('cnt')
    line = S.get('_line')
    done = None
    if cnt is not None and 'x' in S:
        done = sum(cnt) - (1 if line == 9 else 0)   # 当前元素的下标
    for i, v in enumerate(NUMS):
        X = sx + i * cell
        past = done is not None and i < done
        cur = done is not None and i == done and line != 10
        fill = T['panel2'] if not past else (52, 60, 72)
        cv.rect((X + 4, y0 + 44, X + cell - 4, y0 + 44 + cell - 10), fill=fill, r=10, outline=T['blue'] if cur else T['border'], width=5 if cur else 1)
        cv.text((X + cell / 2, y0 + 44 + cell / 2 - 5), v, 32, T['dim'] if past else T['text'], anchor='mm', bold=True)


def _draw_rows(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    ans = S.get('ans') or []
    cnt = S.get('cnt')
    cv.text((x0 + 18, y0 + 2), 'ans（第几次遇到，就放进第几行）', 22, T['muted'], bold=True)
    cell = 64
    line = S.get('_line')
    hot = None
    if cnt is not None and 'x' in S and line in (7, 8, 9):
        hot = S['x']
    for r, row in enumerate(ans):
        Y = y0 + 44 + r * (cell + 10)
        cv.text((x0 + 22, Y + cell / 2), f'行 {r}', 22, T['dim'], anchor='lm', mono=True)
        for j, v in enumerate(row):
            X = x0 + 110 + j * (cell + 8)
            fresh = (line in (8, 9) and hot == v and j == len(row) - 1 and r == (cnt[hot] - (1 if line == 9 else 0)))
            cv.rect((X, Y, X + cell, Y + cell), fill=T['yellow'] if fresh else T['panel2'], r=10, outline=T['border'])
            cv.text((X + cell / 2, Y + cell / 2), v, 30, T['bg'] if fresh else T['text'], anchor='mm', bold=True)
        if not row:
            cv.rect((x0 + 110, Y, x0 + 110 + cell, Y + cell), outline=T['yellow'], r=10, width=3)


CONFIG = dict(
    num=2610, title='转换二维数组', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='一次遍历 · 第 k 次出现放第 k 行',
    tags=[],
    code='''
class Solution:
    def findMatrix(self, nums: List[int]) -> List[List[int]]:
        ans = []
        cnt = [0] * (len(nums) + 1)
        for x in nums:
            if cnt[x] == len(ans):  # 需要加一行
                ans.append([])
            ans[cnt[x]].append(x)
            cnt[x] += 1
        return ans
''',
    call='Solution().findMatrix([1, 3, 4, 1, 2, 3, 1])',
    expect=[[1, 3, 4, 2], [1, 3], [1]],
    views=[
        dict(type='custom', draw=_draw_nums, h=190),
        dict(type='array', var='cnt', pointers={'x': 'pink'}, label='cnt（下标 = 数值，值 = 已出现次数）', h=190, cell=60,
             color=lambda S, i, v: 'yellow' if S.get('x') == i and S.get('_line') == 9 else None),
        dict(type='custom', draw=_draw_rows, h=330),
    ],
    watch=['x', ('ans', 'ans', 'green')],
    max_steps=60,
    captions={
        'ans = []': '`ans` 存结果的每一行，先一行都没有',
        'cnt = [0]': '`cnt[x]` 记数值 `x` 已经出现了几次，值域是 1 到 n，所以用数组代替哈希表',
        'if cnt[x] == len(ans)': lambda S, B, r: (f'`x = {S.x}` 已出现 `{S.cnt[S.x]}` 次，现有 `{len(S.ans)}` 行：' + ('次数等于行数 → 前面每一行都已有 x，==需要新开一行==' if S.cnt[S.x] == len(S.ans) else '次数小于行数 → 第 ' + str(S.cnt[S.x]) + ' 行还没有 x，直接放')),
        'ans.append([])': '新开一行：现在共 `{len(ans)}` 行',
        'ans[cnt[x]].append(x)': '`x = {x}` 第 `{cnt[x] + 1}` 次出现 → 放进第 `{cnt[x]}` 行（从 0 数）：这一行之前没有 x，不会重复',
        'cnt[x] += 1': '`cnt[{x}]` 加一，`x` 的下一次出现会放到下一行：`cnt[{x}] = {cnt[x]}`',
        'return ans': '行数 = 出现次数最多的数的次数，已是最少：`{ret}`',
    },
    cards=dict(
        one_liner='数 x 第 k 次出现，就放进第 k 行',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['把 `nums` 里的元素分到二维数组，每行元素互不相同',
                 '行数尽可能少，行长度可以不同，答案不唯一',
                 '示例：`[1,3,4,1,2,3,1]` → `[[1,3,4,2],[1,3],[1]]`'],
        quote='一个数出现了多少次，就加到第几行。首次遇到 nums[i]=1，加到第一行。再次遇到 1，加到第二行。这样既可以保证每行不会有相同元素，又可以保证用到的行数是最小的。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['`cnt[x]` 记 x 已出现几次，它同时就是 x 下一次要去的行号',
              '行不够就 `ans.append([])`，保证 `cnt[x]` 行一定存在',
              '出现最多的数决定行数，所以行数是最少的'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错点：先放入 `ans[cnt[x]]`，再让 `cnt[x] += 1`，顺序反了会错一行',
                 '值域在 `[1, n]`，`cnt` 用数组比哈希表快',
                 '灵神方法一：用 Counter，每轮把所有不同元素各取一个放一行，再把次数减一'],
    ),
)
