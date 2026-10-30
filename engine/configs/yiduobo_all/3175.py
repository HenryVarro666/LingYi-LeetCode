CONFIG = dict(
    num=3175, title='找到连续赢 K 场比赛的第一位玩家', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='单调栈 · 下一个更大元素', tags=[],
    code='''
class Solution(object):
    def findWinningPlayer(self, skills, k):

        n = len(skills)
        f = [-1] * n
        stack = []
        for index, v in enumerate(skills):
            while stack and skills[stack[-1]] < v:
                f[stack[-1]] = index
                stack.pop()
            
            stack.append(index)
        
        index = 0
        while f[index] != -1 and f[index] - index - 1 < k:
            if index == 0:
                k -= 1
            index = f[index]
        
        return index
''',
    call='Solution().findWinningPlayer([4,2,6,3,9], 2)',
    expect=2,
    views=[
        dict(type='array', var='skills', pointers={'index': 'blue'}, label='skills', h=170),
        dict(type='array', var='f', pointers={}, label='f（下一个更大元素的下标）', h=170,
             color=lambda S, i, v: 'green' if v != -1 else None),
        dict(type='stack', var='stack', fmt=lambda i: f'{i}', label='stack（下标）', h=260),
    ],
    watch=[('index', 'index', 'blue'), ('k', 'k', 'yellow'), ('f', 'f', 'green')],
    captions={
        'f = [-1]': '`f[i]` 先全设为 `-1`：表示 `skills[i]` 后面没有更大的人',
        'while stack and': lambda S, B, r: ('栈顶 `' + str(S.skills[S.stack[-1]]) + '` < 当前 `' + str(S.v) + '` → 栈顶遇到了下一个更大元素') if S.stack and S.skills[S.stack[-1]] < S.v else '栈空或栈顶不比当前小，不再弹栈',
        'f[stack[-1]] = index': '栈顶这个人会输给 `index = {index}` 号：`f[{stack[-1]}] = {index}`',
        'stack.pop()': '弹出已经找到对手的人',
        'stack.append': '当前 `{index}` 号入栈，等着它的下一个更大元素',
        'index = 0': '队首一定是 `index` 号；现在是 0 号，下面沿着 `f` 往后跳',
        'while f[index]': lambda S, B, r: (f'`f[{S.index}] = {S.f[S.index]}`：它会输给更大的人；中间只赢 `{S.f[S.index] - S.index - 1}` 人，`< k = {S.k}` → 继续' if S.f[S.index] != -1 and S.f[S.index] - S.index - 1 < S.k else (f'`f[{S.index}] = -1`：没人能赢他，他就是答案' if S.f[S.index] == -1 else f'他能连赢 `{S.f[S.index] - S.index - 1}` 人 `>= k = {S.k}` → 他就是答案')),
        'if index == 0': '`index = {index}`：{"0 号没有赢过前任，要赢满 k 场" if index == 0 else "后面的人在上台前已赢过队首一场，只需再赢 k-1 场"}',
        'k -= 1': '后续上台的人已赢过一场，所以要求少一场：`k` → =={k}==',
        'index = f[index]': '`index` 输给 `f[index]`，新队首是 =={index}== 号',
        'return index': '赢家是 `{index}` 号',
    },
    cards=dict(
        one_liner='答案一定当过队首：用单调栈预处理每人输给谁',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['玩家按 `0..n-1` 排队，队首两人比技能，胜者留队首，败者去队尾',
                 '问谁最先连续赢下 `k` 场',
                 '示例：`skills = [4,2,6,3,9], k = 2` → `2`'],
        quote='由于最终答案必然处于队列的首位，不妨设当前队首玩家的编号为index，而index在碰到index后方且比skills[index]大的玩家时将会落败。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[index]` = `skills[index]` 的下一个更大元素下标，用单调栈求（496 题思路）',
              '`index` 当队首时能赢 `f[index] - index - 1` 人，够 `k` 场就是答案',
              '不是 0 号时，上台前已赢过一场，只需赢 `k - 1` 人（代码里用 `k -= 1` 一次处理）'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`f[index] == -1`：它是最大值，必然赢到底',
                 '==非 0 号只需赢 k-1 场==：上台时已经赢过前任一次',
                 '原文是 Python 2 风格（`class Solution(object)`），Python 3 直接可跑，代码未改',
                 '对比灵神：灵神 `O(1)` 空间边扫边打擂台，yiduobo 先建 `f` 表再跳'],
    ),
)
