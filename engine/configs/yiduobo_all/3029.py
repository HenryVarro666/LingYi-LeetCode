CONFIG = dict(
    num=3029, title='将单词恢复初始状态所需的最短时间 I', difficulty='Medium', category='字符串',
    author='yiduobo', technique='Z 数组（扩展 KMP）',
    tags=[],
    code='''
class Solution(object):
    def minimumTimeToInitialState(self, word, k):

        z = [0]
        left, right = 0, 0
        for index in range(1, len(word)):
            if index <= right and z[index - left] < right - index + 1:
                z.append(z[index - left])
            else:
                z.append(max(0, right - index + 1))
                while z[-1] + index < len(word) and word[z[-1] + index] == word[z[-1]]:
                    z[-1] += 1
                
            if index + z[-1] - 1 > right:
                left, right = index, index + z[-1] - 1

        for index in range(k, len(word), k):
            if z[index] >= len(word) - index:
                return index // k
        
        return (len(word) - 1) // k + 1
''',
    call="Solution().minimumTimeToInitialState('abacaba', 3)",
    expect=2,
    skip=['z = [0]', 'left, right = 0, 0'],
    views=[
        dict(type='text', fn=lambda S: (
            f"Z 盒子 `word[{S['left']}..{S['right']}]` 与前缀相同" if S.get('right', 0) > S.get('left', 0) else '暂无可复用的 Z 盒子') if 'right' in S else ''),
        dict(type='string', var='word', label='word（蓝 = index，框 = Z 盒子 [left, right]）', h=250,
             pointers={'index': 'blue'},
             window=('left', 'right')),
        dict(type='array', var='z', label='z[i]：从 i 开始的后缀与前缀的最长公共长度', h=220, pointers={'index': 'blue'}),
    ],
    watch=[('index', 'index', 'blue'), ('left', 'left', 'cyan'), ('right', 'right', 'cyan'), 'k'],
    captions={
        'if index <= right and z[index - left] < right - index + 1': lambda S, B, r: (
            f'`index={B.index} <= right={B.right}`，且 `z[{B.index - B.left}]={B.z[B.index - B.left]} < {B.right - B.index + 1}`：==复用 Z 盒子==，不用暴力比'
            if B.index <= B.right and B.z[B.index - B.left] < B.right - B.index + 1
            else f'`index={B.index}` 不在盒子里，或复用的值碰到 right 边界 → 要从边界起暴力匹配'),
        'z.append(z[index - left])': '直接 `z[{index}] = z[{index - left}] = {z[-1]}`，盒子内字符和前缀一样，结果可以照抄',
        'z.append(max(0': '起点：盒子内已知能匹配 `{z[-1]}` 个字符，从这之后再往后比',
        'while z[-1] + index': lambda S, B, r: (
            f'比较 `word[{B.z[-1] + B.index}]={B.word[B.z[-1] + B.index]}` 与 `word[{B.z[-1]}]={B.word[B.z[-1]]}` → 相等，匹配长度 +1'
            if B.z[-1] + B.index < len(B.word) and B.word[B.z[-1] + B.index] == B.word[B.z[-1]]
            else f'不再相等（或到末尾），`z[{B.index}] = {B.z[-1]}` 定下来'),
        'z[-1] += 1': '匹配长度 +1：`z[{index}] = {z[-1]}`',
        'if index + z[-1] - 1 > right': lambda S, B, r: (
            f'这个匹配区间右端 `{B.index + B.z[-1] - 1}` 超过 right={B.right} → 更新 Z 盒子'
            if B.index + B.z[-1] - 1 > B.right else f'右端 `{B.index + B.z[-1] - 1}` 没超过 right={B.right}，盒子不变'),
        'left, right = index': 'Z 盒子更新为 `[{left}, {right}]`',
        'for index in range(k, len(word), k)': lambda S, B, r: (
            f'每 k={B.k} 个字符删一次：删 `t` 次后剩下后缀从 `index={S.index}` 开始' if 'index' in S else ''),
        'if z[index] >= len(word) - index': lambda S, B, r: (
            f'`z[{S.index}]={S.z[S.index]} >= {len(S.word) - S.index}`：剩下的后缀正好是前缀 → ==补回被删部分就能复原==，答案 `{S.index}//{S.k}`'
            if S.z[S.index] >= len(S.word) - S.index
            else f'`z[{S.index}]={S.z[S.index]} < {len(S.word) - S.index}`：剩下的后缀对不上前缀，再多删一次'),
        'return index // k': '返回 `{index} // {k} = {ret}` 秒',
        'return (len(word) - 1) // k + 1': '都对不上：删光原字符（`ceil(n/k)` 次）后全部补成原字符，一定能复原',
    },
    cards=dict(
        one_liner='删 t 次后，剩余后缀等于前缀就能复原：Z 数组一次算出',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['每秒删掉 `word` 前 `k` 个字符，再在末尾补任意 `k` 个字符',
                 '求最少几秒（> 0）能让 `word` 回到初始状态',
                 '示例：`word = "abacaba"`，`k = 3` → `2`'],
        quote='如果字符串中剩下的n - t * k个字符，也就是word[t * k : n]与字符串的前缀word[:n - t * k]相同，那么就可以让补充进来的t * k个字符与word的后缀相同，从而使得字符串复原。',
        quote_src='—— yiduobo 题解原文',
        idea=['上界：`ceil(n/k)` 次后原字符全删光，补回原字符即可',
              '更早复原的条件：`word[t*k:]` 等于 `word[:n-t*k]`',
              '这正是 Z 数组的定义，只需看 `index = k, 2k, ...` 的 `z[index]`'],
        summary=['时间 `O(n)`：Z 数组靠 left/right 盒子复用，指针不回退',
                 '易错：`z[0]` 设为 0，不能当作 n；答案必须大于 0，所以从 `index = k` 起查',
                 '找不到时答案是 `(n-1)//k + 1`',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`'],
    ),
)
