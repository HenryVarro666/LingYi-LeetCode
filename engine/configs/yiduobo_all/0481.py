CONFIG = dict(
    num=481, title='神奇字符串', difficulty='Medium', category='模拟',
    author='yiduobo', technique='按题意模拟 + 边加边计数',
    code='''
class Solution(object):
    def magicalString(self, n):

        if n <= 0:
            return 0

        q = [1]
        pos = 0
        res = 1
        while len(q) < n:
            q.append(3 - q[-1])
            res += 2 - q[-1]
            pos += 1
            now = q[pos]
            if now == 2 and len(q) < n:
                q.append(q[-1])
                res += 2 - q[-1]

        return res
''',
    call='Solution().magicalString(10)',
    expect=5,
    views=[
        dict(type='array', var='q', pointers={'pos': 'blue'}, label='q（pos 指向当前组长度）', h=260,
             color=lambda S, k, v: 'green' if k == len(S['q']) - 1 and S.get('_line') in (14, 15, 17, 18) else None),
        dict(type='text', fn=lambda S: f"`res` = 前 `{len(S['q'])}` 个数里 1 的个数 = =={S['res']}==" if 'res' in S and 'q' in S else '', size=34, h=80),
    ],
    watch=[('n', 'n', 'orange'), ('pos', 'pos', 'blue'), ('res', 'res', 'green')],
    captions={
        'if n <= 0': '`n = {n}`，不会小于等于 0，继续',
        'q = [1]': '从 `[1]` 开始：第一组是 1 个 1',
        'pos = 0': '`pos` 是“头部指针”，指向当前这一组该写几个',
        'res = 1': '`res` 记录 1 的个数，现在有 1 个',
        'while len(q) < n': lambda S, B, r: (f'`len(q) = {len(S.q)} < n = {S.n}` → 继续添加' if len(S.q) < S.n else f'`len(q) = {len(S.q)}` 已经达到 `n = {S.n}` → 结束'),
        'q.append(3 - q[-1])': '先写这一组的第一个数：与末尾 `{B.q[-1]}` 不同，是 `3 − {B.q[-1]}` = =={q[-1]}==',
        'res += 2 - q[-1]': '`2 − {q[-1]}` = `{2 - q[-1]}`：是 1 才加 1，是 2 加 0 → `res = {res}`',
        'pos += 1': '头部指针后移，`pos = {pos}`',
        'now = q[pos]': '`now = q[{pos}] = {now}`：这一组要写 `{now}` 个',
        'if now == 2': lambda S, B, r: (f'`now = 2` 且 `len(q) = {len(S.q)} < n`：这一组还要再写一个' if S.now == 2 and len(S.q) < S.n else (f'`now = {S.now}`：这组只写 1 个，已经写完' if S.now == 1 else f'`now = 2` 但 `len(q) = {len(S.q)}` 已经达到 `n`：不再添加')),
        'q.append(q[-1])': '第二个相同的数：再写一个 `{q[-1]}`',
        'return res': '前 `{n}` 个数里共有 `{res}` 个 1',
    },
    cards=dict(
        one_liner='用头部指针读组长度，尾部追加，同时顺手数 1',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['神奇字符串 `s` 只由 `1`、`2` 组成，各连续相同字符组的长度连起来恰好是 `s` 本身',
                 '`s = 1221121221221121122...`，求前 `n` 个字符中 `1` 的个数',
                 '本视频：`n = 10`，前 10 个是 `1221121221` → `5`'],
        quote='直接按题目要求模拟。每次往字符串尾部添加与当前尾部不同的数字，同时根据字符串头部指针指向的数确定添加的数量，同时更新答案即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`q[-1]` 与新数字不同：`3 - q[-1]` 在 1、2 间切换',
              '`pos` 指向的数是 1 还是 2，决定这一组追加一个还是两个',
              '每追加一个数就用 `2 - 数` 更新 `res`，不用最后再数一遍'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '追加第二个数前要判断 `len(q) < n`，避免多写一个而多算 1',
                 '`q` 的前 3 位靠循环生成（`1`、`2`、`2`），不用像灵神那样预置 `[1,2,2]`',
                 '对比灵神：灵神一次追加整组再最后 `count`；这里逐个追加并实时计数'],
    ),
)
