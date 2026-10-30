CONFIG = dict(
    num=900, title='RLE迭代器', difficulty='Medium', category='设计',
    author='yiduobo', technique='模拟 · 下标 + 已用个数',
    code='''
class RLEIterator(object):

    def __init__(self, A):
        self.A = A[:]
        self.used_num = 0
        self.now = 0

    def next(self, n):
        while self.now < len(self.A) and self.used_num + n > self.A[self.now]:
            n -= self.A[self.now] - self.used_num
            self.used_num = 0
            self.now += 2
        
        if self.now == len(self.A):
            return -1
        
        self.used_num += n
        return self.A[self.now + 1]
''',
    call='it = RLEIterator([3,8,0,9,2,5])\n[it.next(2), it.next(1), it.next(1), it.next(2)]',
    expect=[8, 8, 5, -1],
    views=[
        dict(type='array', var='self.A', h=250, label='A（偶数位 = 次数，奇数位 = 数字）',
             pointers={'self.now': 'blue'}),
        dict(type='text', size=32, fn=lambda S: (f"当前段：`{S['self.A'][S['self.now']]}` 个 `{S['self.A'][S['self.now']+1]}`，已用 ==`{S['self.used_num']}`==" if S['self.now'] < len(S['self.A']) else '所有段都用完了') if 'self.A' in S else ''),
        dict(type='text', size=32, fn=lambda S: f"本次要取 n = ==`{S['n']}`==" if 'n' in S and 'self.A' in S else ''),
    ],
    watch=['n', ('now', 'self.now', 'blue'), ('used_num', 'self.used_num', 'orange')],
    captions={
        4: '把压缩数组 `A` 拷贝一份：`[次数, 数字, 次数, 数字 ...]`',
        5: '`used_num`：当前段已经取走了几个',
        6: '`now`：当前段在 `A` 中的下标（指向次数）',
        'while self.now': lambda S, B, r: (f'当前段剩 `{S["self.A"][S["self.now"]] - S["self.used_num"]}` 个，要取 `{S["n"]}` 个：用掉后 `{S["self.used_num"]+S["n"]}` > `{S["self.A"][S["self.now"]]}`？ ==这段不够== → 吃光它，跳到下一段'
                                          if S['self.now'] < len(S['self.A']) and S['self.used_num'] + S['n'] > S['self.A'][S['self.now']]
                                          else ('`now` 已经走出数组：没有数了' if S['self.now'] >= len(S['self.A']) else f'当前段剩余够用（`{S["self.used_num"]} + {S["n"]} ≤ {S["self.A"][S["self.now"]]}`）→ 不用再跳段')),
        10: '这一段剩下的全吃掉，还欠 `n = {n}` 个',
        11: '换新段，已用个数清零',
        12: '`now` 跳两位到下一段（次数、数字各占一位）→ {self.now}',
        'if self.now == len': lambda S, B, r: ('`now` 等于 `len(A)`：所有段都吃完了 → 返回 `-1`' if S['self.now'] == len(S['self.A']) else '还有段可用 → 继续'),
        'self.used_num += n': '这一段够用：已用个数加 `n` → `{self.used_num}`',
        'return self.A': '返回当前段的数字 `{ret}`',
    },
    cards=dict(
        one_liner='用「段下标 + 已用个数」模拟，不展开原数组',
        complexity='`next` 均摊 `O(1)`，空间 `O(n)`',
        problem=['`A` 是行程编码：偶数位 `A[2i]` 次数，奇数位 `A[2i+1]` 是数字',
                 '`next(n)`：取走接下来 `n` 个数，返回最后取走的那个；不够则返回 `-1`',
                 '本视频：`A = [3,8,0,9,2,5]`，依次 `next(2),(1),(1),(2)` → `8, 8, 5, -1`'],
        quote='直接按照题目意思进行模拟即可。使用两个变量now和used_num分别表示当前处于A数组的哪个下标，以及当前下标对应的数已经使用了多少个。',
        quote_src='—— yiduobo 题解原文',
        idea=['`now` 指向当前段的次数，`used_num` 是这段已经取走的个数',
              '这段不够（`used_num + n > A[now]`）：吃光它，`n` 减去剩余，`now += 2`',
              '这段够了：`used_num += n`，返回这一段的数字'],
        summary=['每段最多跳过一次，`next` 均摊 `O(1)`',
                 '易错点：次数为 0 的段要直接跳过（本例的 `0, 9`）',
                 '`now == len(A)` 才返回 `-1`，不是 `>`，因为每次只加 2',
                 '用 `>`（不是 `>=`）判断不够：刚好吃完这段时仍停在这段，数字照样返回'],
    ),
)
