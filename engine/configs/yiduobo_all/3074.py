CONFIG = dict(
    num=3074, title='重新分装苹果', difficulty='Easy', category='贪心算法',
    author='yiduobo', technique='箱子降序 · 边加边扣',
    tags=['灵神题单', '从最小/最大开始贪心', '难度分 1198'],
    code='''
class Solution(object):
    def minimumBoxes(self, apple, capacity):

        capacity.sort(reverse=True)
        p = 0
        s = 0
        for v in apple:
            s += v
            while s > capacity[p]:
                s -= capacity[p]
                p += 1
        
        return p + 1
''',
    call='Solution().minimumBoxes([3,2,4,1], [2,5,1,4,3])',
    expect=3,
    views=[
        dict(type='array', var='apple', label='apple（逐个包裹倒进来）', h=170,
             color=lambda S, i, v: ('blue' if 'v' in S and S['apple'].index(S['v']) == i else None)),
        dict(type='array', var='capacity', label='capacity（降序）：p 指向当前箱子', pointers={'p': 'pink'}, h=250,
             color=lambda S, i, v: ('green' if 'p' in S and i < S['p'] else None),
             dim=lambda S, i, v: 'p' in S and i > S['p']),
        dict(type='text', fn=lambda S: f"当前箱子 `capacity[{S['p']}] = {S['capacity'][S['p']]}`，手里苹果 s = ==`{S['s']}`==" if 'p' in S and 's' in S else '', size=32, h=110),
    ],
    watch=[('p', 'p', 'pink'), ('s', 's', 'yellow'), ('v', 'v', 'blue')],
    captions={
        'capacity.sort': '同一包裹可拆开 → 想少用箱子，就==先用大箱子==：`{capacity}`',
        'p = 0': '`p` 指向正在装的箱子',
        's = 0': '`s`：当前这个箱子里已经装了多少',
        's += v': '倒入一个包裹：`s` = {B.s} + {v} = =={s}==',
        'while s > capacity[p]': lambda S, B, r: (f'`s = {S.s} > capacity[{S.p}] = {S.capacity[S.p]}`：装不下 → 这个箱子装满，换下一个' if S.s > S.capacity[S.p] else f'`s = {S.s} <= capacity[{S.p}] = {S.capacity[S.p]}`：当前箱子装得下，看下一个包裹'),
        's -= capacity[p]': '装满第 `{p}` 个箱子，剩下的 `s` = =={s}== 放进下一个箱子',
        'p += 1': '换箱子：`p` → {p}',
        'return p + 1': '`p` 从 0 开始，实际用了 `p + 1` = =={p+1}== 个箱子',
    },
    cards=dict(
        one_liner='箱子从大到小排，苹果一路倒，装满就换箱子',
        complexity='时间 `O(m log m + n)`，空间 `O(1)`',
        problem=['`apple[i]` 是第 `i` 个包裹的苹果数，`capacity[j]` 是箱子容量',
                 '包裹里的苹果可以分到不同箱子，求最少箱子数',
                 '本视频：`apple=[3,2,4,1]`，`capacity=[2,5,1,4,3]` → `3`'],
        quote='应该尽量选择容积大的箱子才能使得最终答案最小，于是只需先将箱子按大小从大到小排序，然后遍历苹果，按箱子容积从大到小的顺序填装苹果即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['先给箱子降序，大箱子排前面',
              '遍历包裹，把苹果累加到 `s`（当前箱子里的量）',
              '`s` 超过容量就装满这个箱子，余量留给下一个'],
        summary=['时间 `O(m log m + n)`，空间 `O(1)`',
                 '`while` 而不是 `if`：一个大包裹可能跨好几个箱子',
                 '最后返回 `p + 1`：最后一个箱子也算',
                 '对比灵神：灵神先求总和再逐箱扣减；yiduobo 按包裹逐个倒入',
                 '原文为 Python 2 风格，无需改动即可运行'],
    ),
)
