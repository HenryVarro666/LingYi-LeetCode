CONFIG = dict(
    num=796, title='旋转字符串', difficulty='Easy', category='字符串',
    author='yiduobo', technique='A+A 中用 KMP 找 B',
    tags=['灵神题单', '字符串'],
    code='''
class Solution(object):
    def rotateString(self, A, B):

        if not A and not B:
            return True

        if len(A) != len(B):
            return False

        f = [0]
        pos = 0
        for index in range(1, len(B)):
            while pos > 0 and B[pos] != B[index]:
                pos = f[pos - 1]
            if B[pos] == B[index]:
                pos += 1
            f.append(pos)
        
        pos = 0
        for char in A + A:
            while pos > 0 and B[pos] != char:
                pos = f[pos - 1]
            if B[pos] == char:
                pos += 1
                if pos == len(B):
                    return True

        return False
''',
    call='Solution().rotateString("abaab", "aabab")',
    expect=True,
    views=[
        dict(type='string', var='A + A', label='A + A（复制一遍接在后面，包含 A 的所有旋转）', cell=76, h=170),
        dict(type='text', size=28, h=70, fn=lambda S: f"当前读到的字符 `char = '{S['char']}'`" if 'char' in S else ''),
        dict(type='string', var='B', label='B（绿 = 已匹配的前缀，蓝箭头 = pos）', cell=76, h=230,
             pointers={'pos': 'blue', 'index if _line < 18 else None': 'pink'},
             pointer_labels={'index if _line < 18 else None': 'index'},
             color=lambda S, k, v: 'green' if S.get('pos') and k < S['pos'] and S.get('_line', 0) >= 18 else None),
        dict(type='array', var='f', label='f[i]：B[:i+1] 中最长的「前缀 = 后缀」长度', cell=76, h=170),
    ],
    watch=[('pos', 'pos', 'blue'), ('index', 'index', 'pink'), ('char', 'char'), ('f', 'f', 'green')],
    captions={
        'if not A and not B': '两串都为空 → 直接是 True；这里 A、B 不为空，继续',
        'if len(A) != len(B)': lambda S, B_, r: f'`len(A) = {len(S.A)}`，`len(B) = {len(S.B)}`：长度不同一定 False，相同才往下',
        'f = [0]': '`f[i]` 就是 kmp 的 next 数组：以第 i 位结尾，能和前缀匹配的最长长度；`f[0]` 一定是 0',
        'pos = 0': '`pos` 表示当前已经匹配上的长度',
        'for index in range': '`index = {index}`：拿 `B[{index}]` 去和 `B[pos]` 比',
        'while pos > 0 and B[pos] != B[index]': lambda S, B_, r: (
            f"`B[{S.pos}] = {S.B[S.pos]}` ≠ `B[{S.index}] = {S.B[S.index]}`：失配，`pos` 退到 `f[{S.pos-1}] = {S.f[S.pos-1]}`" if S.pos > 0 and S.B[S.pos] != S.B[S.index]
            else '`pos = 0` 或已经相等，不再回退'),
        'pos = f[pos - 1]': '不从头比，借助 f 回退：`pos` → {pos}',
        'if B[pos] == B[index]': lambda S, B_, r: (
            f"`B[{S.pos}] = {S.B[S.pos]}` == `B[{S.index}]` → ==匹配长度加一==" if S.B[S.pos] == S.B[S.index]
            else f"`B[{S.pos}] = {S.B[S.pos]}` ≠ `B[{S.index}] = {S.B[S.index]}` → 以它结尾的前缀长度为 `{S.pos}`"),
        'pos += 1': '`pos` → {pos}',
        'f.append(pos)': '`f[{index}] = {pos}`：记下来，失配时回退用',
        'for char in A + A': lambda S, B_, r: (f"在 `A + A` 里依次读字符：`char = '{S.char}'`" if 'char' in S else '`A + A` 读完了'),
        'while pos > 0 and B[pos] != char': lambda S, B_, r: (
            f"`B[{S.pos}] = {S.B[S.pos]}` ≠ `char = {S.char}`：失配，`pos` 退到 `f[{S.pos-1}] = {S.f[S.pos-1]}`" if S.pos > 0 and S.B[S.pos] != S.char
            else '`pos = 0` 或已经相等，不再回退'),
        'if B[pos] == char': lambda S, B_, r: (
            f"`B[{S.pos}] = {S.B[S.pos]}` == `char` → ==又多匹配一位==" if S.B[S.pos] == S.char
            else f"`B[{S.pos}] = {S.B[S.pos]}` ≠ `char = {S.char}` → 这位没匹配上"),
        'if pos == len(B)': lambda S, B_, r: (f'`pos = {S.pos} == len(B)`：B 整个出现在 A+A 里 → ==找到了==' if S.pos == len(S.B)
                                              else f'`pos = {S.pos} < len(B) = {len(S.B)}`，继续读'),
        'return True': 'B 是 A+A 的子串，也就是 B 是 A 的某次旋转 → `True`',
        'return False': 'A+A 读完也没匹配完 B → `False`',
    },
    cards=dict(
        one_liner='把 A 复制一遍接在后面，B 只要是它的子串就行',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['每次把 `A` 最左边的字符移到最右边，问能否变成 `B`',
                 '示例：`A = "abcde"`，`B = "cdeab"` → `true`',
                 '本视频：`A = "abaab"`，`B = "aabab"`（旋转 2 次）'],
        quote='可以发现，复制后的串包含了A所有的可能移动，那么此时只需要判断B是否为A + A的子串即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`A[1..n]` 是移 1 位，`A[2..n+1]` 是移 2 位……全在 `A+A` 里',
              '先特判：两串都空是 True，长度不同是 False',
              '判断子串的方法很多，作者用 kmp：先对 B 建 `f`，再扫一遍 `A+A`'],
        summary=['时间 `O(n)`，空间 `O(n)`；数据很小时暴力也行',
                 '易错：长度不同必须先返回 False，否则短串会误判',
                 '这份代码没有 `pos = f[pos - 1]` 之外的特殊处理：匹配满就立刻 `return True`',
                 '对比灵神：灵神先给 `goal in s + s` 的一行写法，再给 KMP 模板'],
    ),
)
