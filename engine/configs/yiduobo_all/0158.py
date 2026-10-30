CONFIG = dict(
    num=158, title='用 Read4 读取 N 个字符 II', difficulty='Hard', category='设计',
    author='yiduobo', technique='类内保留 buf4 + 指针 p',
    code='''
class Solution(object):

    def __init__(self):
        self.p = 0
        self.read_len = 0
        self.buf4 = [' '] * 4

    def read(self, buf, n):

        cnt = 0
        while cnt < n:
            if self.p == self.read_len:
                self.buf4 = [' '] * 4
                self.read_len = read4(self.buf4)
                self.p = 0
                if self.read_len == 0:
                    break
            
            buf[cnt] = self.buf4[self.p]
            self.p += 1
            cnt += 1
        
        return cnt
''',
    setup='''
_file = list("abcdefg")
_fp = [0]
def read4(buf4):
    k = 0
    while k < 4 and _fp[0] < len(_file):
        buf4[k] = _file[_fp[0]]
        k += 1
        _fp[0] += 1
    return k
''',
    call='''sol = Solution()
out = []
for _n in (3, 2, 4):
    b = [''] * 4
    k = sol.read(b, _n)
    out.append(''.join(b[:k]))
out''',
    expect=['abc', 'de', 'fg'],
    max_steps=90,
    views=[
        dict(type='array', var='self.buf4',
             label='self.buf4（上一次 read4 读来的 4 个）', cell=80, h=190,
             pointers={'self.p': 'blue'}, pointer_labels={'self.p': 'p'},
             color=lambda S, i, v: 'green' if v != ' ' else None),
        dict(type='array', var='buf', label='buf（本次调用的目标缓冲区）', cell=70, h=190,
             pointers={'cnt': 'pink'}, color=lambda S, i, v: 'green' if v != '' else None),
    ],
    watch=['n', 'cnt', ('p', 'self.p', 'blue'), ('read_len', 'self.read_len', 'orange')],
    captions={
        'self.p = 0': '`p`：`buf4` 里已经被消耗掉的字符数（下一个要取的位置）',
        'self.read_len = 0': '`read_len`：`buf4` 里一共有多少个有效字符',
        13: '`buf4` 放到成员变量上：==下一次 read 还能接着用==',
        'cnt = 0': '本次调用已经写入 `buf` 的个数，要凑够 `n = {n}`',
        'while cnt < n': '`cnt = {cnt}`，`n = {n}`：{"还没凑够，继续" if cnt < n else "凑够了，结束"}',
        'if self.p == self.read_len': lambda S, B, ret: (f'`p = {S.self.p} == read_len = {S.self.read_len}`：缓存用完了 → 要调用 `read4` 重新装载' if S.self.p == S.self.read_len else f'`p = {S.self.p}` < `read_len = {S.self.read_len}`：缓存里还有字符，==直接用=='),
        'self.read_len = read4': '`read4` 读到 `{self.read_len}` 个，更新 `read_len`',
        'self.p = 0': '新装载了一批，`p` 重置为 0',
        'if self.read_len == 0': lambda S, B, ret: ('读到 0 个：文件结束，==break==' if S.self.read_len == 0 else '读到了新字符，继续'),
        'buf[cnt] = self.buf4[self.p]': '`buf[{cnt}] = buf4[{self.p}] = {buf[cnt]!r}`',
        'self.p += 1': '这个字符被消耗了，`p` → {self.p}（剩下的留给==下一次调用==）',
        'cnt += 1': '`cnt` → {cnt}',
        'return cnt': '本次调用返回 `{ret}` 个字符',
    },
    cards=dict(
        one_liner='read4 读多了的字符，要存在成员变量里留给下次调用',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['同样给 `read4`，但 `read(buf, n)` 会被==多次调用==',
                 '一次 `read4` 读来的 4 个字符，这次可能只用掉一部分，剩下的下次调用要接着用',
                 '文件 `"abcdefg"`，依次 `read(3)`、`read(2)`、`read(4)` → `abc`、`de`、`fg`'],
        quote='需要设置一个全局的buf4，同时设置配套的read_len和p，表示这个全局buf4的长度以及已经消耗掉的字符数。',
        quote_src='—— yiduobo 题解原文',
        idea=['`buf4`、`read_len`、`p` 都放在 `self` 上，跨调用保留',
              '`p == read_len` 说明缓存耗尽，才调用 `read4` 重新装载，`p` 归 0',
              '直到写满 `n` 个，或者 `read4` 读到 0 个（文件结束）为止'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：`buf4` 必须是成员变量，局部变量会把没用完的字符丢掉',
                 '易错点：重新装载后若 `read_len == 0` 要 `break`，否则会读到空字符',
                 '演示用 `setup` 里实现了读 `"abcdefg"` 的 `read4`，作者代码未改，最后一行 `out` 收集每次返回的内容'],
    ),
)
