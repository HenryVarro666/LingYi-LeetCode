def _top(S):
    if 'z' not in S or 'index' not in S:
        return '`z[index]`：从 index 开始的后缀与 `word` 前缀能匹配的最大长度'
    w, k, idx, z = S['word'], S['k'], S['index'], S['z']
    if S['_line'] >= 17 and idx < len(z):
        need = len(w) - idx
        return f"第二趟：`index = {idx}`，后缀 `{w[idx:]}` 长 {need}，`z[{idx}] = {z[idx]}` → {'==整个后缀都匹配前缀==' if z[idx] >= need else '没匹配完'}"
    if idx < len(z):
        return f"算 `z[{idx}]`：后缀 `{w[idx:]}` 对比前缀 `{w}`，目前匹配 {z[idx]} 位"
    return f'准备算 `z[{idx}]`：后缀 `{w[idx:]}`'


def _cond(S, B, ret):
    i, l, r, z = S.index, S.left, S.right, S.z
    if i > r:
        return f'`index = {i} > right = {r}`：不在已知区间里，要从头匹配（走 else）'
    a, b = B.z[i - l] if i - l < len(B.z) else None, r - i + 1
    if a is not None and a < b:
        return f'`index <= right`，且 `z[{i}-{l}] = {a} < right-index+1 = {b}` → ==直接抄== `z[{i - l}] = {a}`'
    return f'`index <= right`，但 `z[{i}-{l}] = {a} >= right-index+1 = {b}` → 抄不全，要先取 {b} 再往后比（走 else）'


def _while(S, B, ret):
    w, i, zl = S.word, S.index, S.z[-1]
    if i + zl >= len(w):
        return f'`z[-1] + index = {i + zl}` 已到末尾，停止；`z[{i}] = {zl}`'
    a, b = w[zl], w[i + zl]
    if a == b:
        return f"比 `word[{zl}] = '{a}'` 和 `word[{i + zl}] = '{b}'` → ==相同==，匹配长度加 1 → `z[{i}] = {zl + 1}`"
    return f"比 `word[{zl}] = '{a}'` 和 `word[{i + zl}] = '{b}'` → ==不同==，停止，`z[{i}] = {zl}`"


CONFIG = dict(
    num=3031, title='将单词恢复初始状态所需的最短时间 II', difficulty='Hard', category='字符串',
    author='yiduobo', technique='Z 数组 · 先求 z 再按 k 步长检查',
    tags=['灵神题单', '字符串', '难度分 2278'],
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
    call='Solution().minimumTimeToInitialState("abababab", 3)',
    expect=2,
    skip=['else:', 'z[-1] += 1'],
    views=[
        dict(type='text', fn=_top, size=26, h=70),
        dict(type='string', var='word', label='word（蓝框 = [left, right] 已知匹配区间，指针 = index）', pointers={'index': 'blue'},
             window=('left', 'right'), h=210,
             color=lambda S, i, v: 'green' if ('index' in S and 'z' in S and S['index'] < len(S['z']) and S['index'] <= i < S['index'] + S['z'][S['index']]) else None),
        dict(type='array', var='z', label='z 数组（边算边追加）', pointers={'index': 'blue'}, h=200,
             color=lambda S, i, v: 'green' if S.get('index') == i else None),
    ],
    watch=[('index', 'index', 'blue'), ('left', 'left', 'cyan'), ('right', 'right', 'cyan'), ('k', 'k'),
           ('len(word) - index', 'len(word) - index', 'orange')],
    captions={
        'z = [0]': '`z[0]` 记为 0（按定义该是 n，但会妨碍后面的计算），后面的 z 一个个 append 进来',
        'left, right = 0, 0': '`left`、`right`：当前已知==最靠后==的匹配区间，`word[left..right]` 等于前缀',
        'for index in range(1': lambda S, B, ret: (f'求 `z[{S.index}]`：从 `{S.index}` 开始的后缀能和前缀匹配多长' if len(S.z) < len(S.word) else '第一趟结束：z 数组全部算完'),
        'if index <= right and': _cond,
        'z.append(z[index - left])': '两段去掉前 `index - left` 个字符仍然相同，且没超出 right → `z[{index}] = {z[-1]}`，不用再比',
        'z.append(max(0': '起点先取 `max(0, right - index + 1)` = =={z[-1]}==（区间内已确认匹配的部分），再往后暴力匹配',
        'while z[-1] + index': _while,
        'if index + z[-1] - 1 > right': lambda S, B, ret: (f'这一段延伸到 `{S.index + S.z[-1] - 1}`，比 `right = {S.right}` ==更靠后== → 要更新区间'
                                                           if S.index + S.z[-1] - 1 > S.right else
                                                           f'延伸到 `{S.index + S.z[-1] - 1}`，没超过 `right = {S.right}` → 区间不变'),
        'left, right = index': '更新区间：`left = {left}`，`right = {right}`',
        'for index in range(k': lambda S, B, ret: f'第二趟：只看 `k` 的倍数，现在 `index = {S.index}`，即操作 `{S.index // S.k}` 次后',
        'if z[index] >= len(word) - index': lambda S, B, ret: (f'`z[{S.index}] = {S.z[S.index]}` ≥ 后缀长度 `{len(S.word) - S.index}`：后缀整个是前缀 → ==成立=='
                                                               if S.z[S.index] >= len(S.word) - S.index else
                                                               f'`z[{S.index}] = {S.z[S.index]}` < 后缀长度 `{len(S.word) - S.index}` → 不成立，看下一个倍数'),
        'return index // k': '后缀补成前缀就复原了 → 操作 `index // k` = =={ret}== 次',
        'return (len(word) - 1) // k + 1': '没有任何后缀能匹配 → 原字符全删光，`ceil(n/k)` = =={ret}== 次',
    },
    cards=dict(
        one_liner='先求 z 数组，再按步长 k 找第一个整个后缀都匹配前缀的位置',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['每秒删掉 `word` 前 `k` 个字符，末尾补任意 `k` 个字符',
                 '求最少几秒能让 `word` 复原',
                 '示例：`abacaba`，`k = 3` → `2`；本视频：`abababab`，`k = 3` → `2`'],
        quote='如果字符串中剩下的 n - t * k 个字符，也就是 word[t * k : n] 与字符串的前缀 word[:n - t * k] 相同，那么就可以让补充进来的 t * k 个字符与 word 的后缀相同，从而使得字符串复原。',
        quote_src='—— yiduobo 题解原文',
        idea=['先给上界：操作 `ceil(n/k)` 次，原字符全被替换，补回原样即可',
              '更早复原的条件：`word[t*k:]` 等于 `word` 的前缀 → 需要每个位置的 z 值',
              '求 z 时用 `left/right` 记最靠后的匹配区间：区间内的位置直接抄 `z[index-left]`，抄不全才往后比'],
        result='`index = 6`：`z[6] = 2` 等于后缀长度 2 → 6 // 3 = 2 次 ✓',
        summary=['时间 `O(n)`（`right` 只增不减），空间 `O(n)`',
                 '第二趟从 `k` 开始、步长 `k`；`z[0]` 记为 0，所以不会从 0 查起',
                 '原文为 Python 2 写法，`index / k` 与 `(len(word) - 1) / k + 1` 已改为整数除法 `//`',
                 '对比灵神：灵神边算 z 边判断，yiduobo 先算完整个 z 再单独扫一趟'],
    ),
)
