def _txt(S):
    if 'f' not in S:
        return '先给 pattern 建 next 数组 `f`，再用它在流里匹配'
    if 'char' in S:
        return f"流已读 `{''.join(map(str, S['stream'].seen))}`，匹配了 pattern 的前 `{S['p']}` 位"
    return f"`f[i]` = pattern[0..i] 的最长相同前后缀长度，当前 `p = {S['p']}`"


def _fmt(S):
    return S.get('f', [])


CONFIG = dict(
    num=3023, title='在无限流中寻找模式I', difficulty='Medium', category='字符串',
    author='yiduobo', technique='KMP · 边读流边匹配',
    code='''
class Solution(object):
    def findPattern(self, stream, pattern):

        f = [0]
        p = 0
        for index in range(1, len(pattern)):
            while p and pattern[index] != pattern[p]:
                p = f[p - 1]
            
            if pattern[index] == pattern[p]:
                p += 1
            
            f.append(p)
        
        index = -1
        p = 0
        while p < len(pattern):
            index += 1
            char = stream.next()
            while p and pattern[p] != char:
                p = f[p - 1]
            
            if char == pattern[p]:
                p += 1
        
        return index - len(pattern) + 1
''',
    setup='''
class InfiniteStream:
    def __init__(self, bits):
        self.bits = bits
        self.k = 0
        self.seen = []
    def next(self):
        b = self.bits[self.k % len(self.bits)]
        self.k += 1
        self.seen.append(b)
        return b
''',
    call='Solution().findPattern(InfiniteStream([0,1,1,0,1,0,1,1]), [1,0,1,0])',
    expect=2,
    views=[
        dict(type='array', var='pattern', label='pattern（蓝框 = 已匹配的前 p 位）', h=170, cell=90,
             pointers={'p': 'blue'},
             color=lambda S, i, v: ('green' if 'f' in S and 'char' in S and i < S['p'] else ('pink' if 'char' not in S and 'index' in S and i == S['index'] else None))),
        dict(type='array', var='f', label='f（next 数组：最长相同前后缀长度）', h=170, cell=90,
             color=lambda S, i, v: 'yellow' if i == len(S['f']) - 1 and S['_line'] in (11, 13) else None),
        dict(type='array', var=lambda S: S['stream'].seen if 'char' in S else [], label='stream（已读出的流，绿 = 与 pattern 前缀对上的部分）', h=250, cell=70, min_slots=8,
             color=lambda S, i, v: ('green' if S['p'] > 0 and len(S['stream'].seen) - S['p'] <= i < len(S['stream'].seen)
                                    else ('yellow' if i == len(S['stream'].seen) - 1 else None)) if 'char' in S else None),
        dict(type='text', fn=_txt, size=28, h=90),
    ],
    watch=[('index', 'index', 'pink'), ('p', 'p', 'blue'), ('char', 'char', 'yellow')],
    captions={
        'f = [0]': '`f[i]`：`pattern[0..i]` 里最长的「相同前缀和后缀」长度；`f[0] = 0`',
        'p = 0': '`p`：当前已匹配的长度',
        'for index in range(1, len(pattern))': lambda S, B, r: ('pattern 每一位都处理完：next 数组 `f` 建好了' if B.get('index') == S.index and 'index' in B and B.get('_line') != 15 and len(S.f) == len(S.pattern) else f'用 pattern 自己匹配自己：看 `pattern[{S.index}] = {S.pattern[S.index]}`'),
        'while p and pattern[index] != pattern[p]': lambda S, B, r: (
            f'`p = {S.p}`，`pattern[{S.index}] = {S.pattern[S.index]}` ≠ `pattern[{S.p}] = {S.pattern[S.p]}` → 退回 `f[{S.p - 1}]`' if (S.p and S.pattern[S.index] != S.pattern[S.p])
            else ('`p = 0`，已经退无可退' if not S.p else f'`pattern[{S.index}] == pattern[{S.p}]`，不用回退')),
        'p = f[p - 1]': '前缀退到 `f[p-1]`，`p` → {p}',
        'if pattern[index] == pattern[p]': lambda S, B, r: (
            f'`pattern[{S.index}] == pattern[{S.p}]` → ==又多匹配一位==' if S.pattern[S.index] == S.pattern[S.p]
            else f'`pattern[{S.index}] ≠ pattern[{S.p}]` → 这一位没有相同前后缀'),
        'p += 1': '`p` → {p}',
        'f.append(p)': '`f[{index}] = {p}`：pattern 前 `{index+1}` 位的最长相同前后缀 = {p}',
        'index = -1': '`index`：当前读到流的第几个字符，从 -1 开始',
        'while p < len(pattern)': lambda S, B, r: (f'`p = {S.p} < {len(S.pattern)}`：还没匹配完，继续读流' if S.p < len(S.pattern)
                                                  else f'`p = {S.p}` = pattern 长度：==完整匹配==，停止'),
        'index += 1': '读第 `{index}` 个字符',
        'char = stream.next()': '`stream.next()` 读到 `{char}`',
        'while p and pattern[p] != char': lambda S, B, r: (
            f'`pattern[{S.p}] = {S.pattern[S.p]}` ≠ `char = {S.char}`：失配 → 用 `f[{S.p - 1}]` 回退（不回头读流）' if (S.p and S.pattern[S.p] != S.char)
            else ('`p = 0`：没有已匹配的前缀，不用回退' if not S.p else f'`pattern[{S.p}] = char = {S.char}`：没失配')),
        'if char == pattern[p]': lambda S, B, r: (
            f'`char = {S.char}` == `pattern[{S.p}]` → ==匹配成功，p 加一==' if S.char == S.pattern[S.p]
            else f'`char = {S.char}` ≠ `pattern[0] = {S.pattern[0]}` → 从头再来'),
        'return index': '匹配结束位置是 `index = {index}`，起点 = `{index} - {len(pattern)} + 1` = =={ret}==',
    },
    cards=dict(
        one_liner='流只能读一次：用 KMP 的 next 数组边读边匹配',
        complexity='时间 `O(n+m)`，空间 `O(m)`',
        problem=['有一个只含 0、1 的无限流，只能用 `stream.next()` 逐个读',
                 '给定二进制数组 `pattern`，返回它在流中第一次出现的起始下标',
                 '示例：流 `0110101…`，`pattern = [1,0,1,0]` → `2`'],
        quote='非常标准的字符串匹配问题，适合使用kmp算法。先基于pattern建立next数组，然后不断向后遍历stream，利用next来进行匹配即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['先对 `pattern` 建 next 数组 `f`：失配时 `p` 退到 `f[p-1]`',
              '流不能回头读，正好是 KMP「文本指针不回退」的特点',
              '`p` 走满 `len(pattern)` 时，结束位置 `index` 减去长度加一就是起点'],
        summary=['时间 `O(n+m)`，`n` 是读到匹配成功为止的流长度，空间 `O(m)`',
                 '起点 = `index - len(pattern) + 1`，别忘了 +1',
                 '循环条件 `p < len(pattern)`：`p` 到达末尾即匹配成功，不需要再回退',
                 '3037 题是同样的题目，数据更大',
                 '原文为 Python 2 风格，在 Python 3 下无需修改，逐字使用；本题 `stream.next()` 由 `setup` 中的流对象提供'],
    ),
)
