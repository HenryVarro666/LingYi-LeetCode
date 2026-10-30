def _chk(S, B, r):
    idx, w, c = S.index, S.w, S.c
    k = idx - len(w)
    if idx < len(w):
        return f'`{w}` 比前 `{idx}` 个字符还长 → 放不下，跳过'
    if S.f[k] == -1:
        return f'`f[{k}] = -1`：前 `{k}` 个字符凑不出来 → 跳过 `{w}`'
    seg = S.target[k:idx]
    if seg != w:
        return f'`target[{k}:{idx}] = {seg}` ≠ `{w}` → 对不上，跳过'
    return f'`target[{k}:{idx}] = {seg}` == `{w}`，且 `f[{k}] = {S.f[k]}` 可达 → ==可以接上这个单词=='


def _upd(S, B, r):
    idx, w, c = S.index, S.w, S.c
    k = idx - len(w)
    new = S.f[k] + c
    if S.f[idx] == -1:
        return f'`f[{idx}]` 还拼不出（-1）→ 直接用新方案 `f[{k}] + {c}` = =={new}== 更新'
    if S.f[idx] > new:
        return f'`f[{idx}] = {S.f[idx]}` > 新方案 `f[{k}] + {c}` = =={new}== → 新方案更便宜，更新'
    return f'`f[{idx}] = {S.f[idx]}` ≤ 新方案 `{new}` → 不更新'


CONFIG = dict(
    num=3253, title='最小代价构造字符串（简单）', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='前缀 DP + 枚举单词',
    tags=[],
    code='''
class Solution(object):
    def minimumCost(self, target, words, costs):

        n = len(target)
        f = [-1] * (n + 1)
        f[0] = 0

        for index in range(1, n + 1):
            for w, c in zip(words, costs):
                if index >= len(w) and f[index - len(w)] != -1 and target[index - len(w) : index] == w:
                    if f[index] == -1 or f[index] > f[index - len(w)] + c:
                        f[index] = f[index - len(w)] + c
        
        return f[-1]
''',
    call="Solution().minimumCost('abcd', ['ab', 'abc', 'cd', 'd', 'c'], [2, 4, 3, 1, 1])",
    expect=4,
    views=[
        dict(type='text', h=70, fn=lambda S: (
            f"`f[{S['index']}]` = 拼出 `target` 前 {S['index']} 个字符 `{S['target'][:S['index']]}` 的最小代价" if 'index' in S and 'f' in S
            else '`f[i]` = 拼出 `target` 前 `i` 个字符的最小代价，`-1` = 拼不出')),
        dict(type='string', var='target', label='target（蓝框 = 当前尝试的单词所覆盖的位置）', h=170, cell=80,
             window=('max(index - len(w), 0)', 'index - 1')),
        dict(type='array', var='f', label='f（下标 = 前几个字符）', h=200, cell=80, pointers={'index': 'pink'}),
        dict(type='array', var='words', label='words（对应 costs = [2, 4, 3, 1, 1]）', h=130, cell=90, index=False),
    ],
    watch=[('index', 'index', 'pink'), ('w', 'w', 'cyan'), ('c', 'c', 'yellow')],
    captions={
        'n = len(target)': '`n = {n}`：要拼的字符串长度',
        'f = [-1]': '`f` 长 `n + 1`，先全设 `-1` = ==拼不出==',
        'f[0] = 0': '拼出空串（前 0 个字符）代价 0 → 这是 DP 的起点',
        'for index in range': '现在算 `f[{index}]`：拼出前 `{index}` 个字符，最后一个单词必须以第 `{index}` 个字符结尾',
        'for w, c in zip': '尝试单词 `{w}`（代价 `{c}`）作为==最后一个单词==',
        'if index >= len(w)': _chk,
        'if f[index] == -1 or': _upd,
        'f[index] = f[index - len(w)] + c': '`f[{index}]` 更新为 =={f[index]}==（`f[{index - len(w)}] = {f[index - len(w)]}` 加上 `{c}`）',
        'return f[-1]': lambda S, B, r: (f'`f[n] = {r}`：整个 `target` 的最小代价' if r != -1 else '`f[n] = -1`：拼不出来'),
    },
    max_steps=64,
    cards=dict(
        one_liner='f[i] 表示拼出前 i 个字符的最小代价，枚举最后一个单词',
        complexity='时间 `O(n × m × L)`（m 个单词，每次比较长度 L），空间 `O(n)`',
        problem=['给 `target`、单词数组 `words` 和对应代价 `costs`，每个单词可以反复使用',
                 '用单词首尾相接拼出 `target`，求最小总代价；拼不出返回 `-1`',
                 '本视频：`abcd`，答案 `4`（`ab` + `c` + `d` = 2 + 1 + 1）'],
        quote='令f[index]表示构造target的前index个字符的最小代价，边界情况有f[0] = 0。接下来对于所有的f[index]，枚举所有长度小于等于index的单词w……',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[index]`：前 `index` 个字符的最小代价，`f[0] = 0`，`-1` 表示拼不出',
              '枚举最后一个单词 `w`：必须 `target[index-len(w):index] == w`',
              '并且 `f[index - len(w)]` 要可达，再取 `f[index - len(w)] + c` 的最小值'],
        summary=['时间 `O(n·m·L)`，空间 `O(n)`；题目标「简单」是因为数据规模小',
                 '易错点：`-1` 是「拼不出」不是代价，必须先判断 `f[...] != -1` 再相加；更新时也要处理 `f[index] == -1`',
                 '`target[a:b]` 左闭右开，长度刚好是 `len(w)`',
                 '原文已是 Python 3 可运行写法，代码未改动'],
    ),
)
