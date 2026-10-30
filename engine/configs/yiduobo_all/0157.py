CONFIG = dict(
    num=157, title='用 Read4 读取 N 个字符', difficulty='Easy', category='字符串',
    author='yiduobo', technique='每次 read4 读 4 个，凑够 n 个',
    code='''
class Solution(object):
    def read(self, buf, n):

        res = 0
        for offset in range(0, n, 4):
            buf4 = [' '] * 4
            for index in range(read4(buf4)):
                buf[offset + index] = buf4[index]
                res += 1
                if res == n:
                    return res
        
        return res
''',
    setup='''
_file = list("abcdefghijk")
_fp = [0]
def read4(buf4):
    k = 0
    while k < 4 and _fp[0] < len(_file):
        buf4[k] = _file[_fp[0]]
        k += 1
        _fp[0] += 1
    return k
''',
    call='buf = [""] * 10\nn = Solution().read(buf, 6)\nbuf[:n]',
    expect=['a', 'b', 'c', 'd', 'e', 'f'],
    max_steps=60,
    views=[
        dict(type='array', var='buf4', label='buf4（read4 每次最多填 4 个）', cell=80, h=190,
             color=lambda S, i, v: 'green' if v != ' ' else None),
        dict(type='array', var='buf', label='buf（要填满的目标缓冲区）', cell=70, h=190,
             pointers={'offset + index': 'blue'}, pointer_labels={'offset + index': 'offset+index'},
             color=lambda S, i, v: 'green' if v != '' else None),
    ],
    watch=['n', 'offset', 'index', ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 记录已经放进 `buf` 的字符数',
        'for offset in range': lambda S, B, ret: (f'每轮最多读 4 个，`offset = {S.offset}`：本轮从 `buf[{S.offset}]` 开始放' if S.get('offset') is not None and S.get('res', 0) < S.n else '读完了'),
        'buf4 = ': '准备一个新的 4 格缓冲区给 `read4` 用',
        7: '`read4` 返回实际读到的个数，==只处理这么多个==字符（`index = {index}`）',
        'buf[offset + index]': '`buf[{offset + index}] = buf4[{index}] = {buf4[index]!r}`',
        'res += 1': '放进去一个，`res` = {res}',
        'if res == n': lambda S, B, ret: (f'`res = {S.res} == n = {S.n}`：够了，==立刻返回==（不能多读）' if S.res == S.n else f'`res = {S.res}` < `n = {S.n}`，还要继续'),
        'return res': '一共读到 `{ret}` 个字符',
    },
    cards=dict(
        one_liner='每轮 read4 最多拿 4 个，凑够 n 个就立刻停',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['已给 API `read4(buf4)`：每次从文件读最多 4 个字符放进 `buf4`，返回实际读到的个数',
                 '用它实现 `read(buf, n)`：从文件读 `n` 个字符到 `buf`，返回实际读到的个数',
                 '文件 `"abcdefghijk"`，`n = 6` → 返回 `6`，`buf = "abcdef"`'],
        quote='由于每次调用最多新增4个字符，那么按照4的步长执行一次for循环，每轮都将读入的字符添加到最终需要返回的buf中就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['`offset` 以 4 为步长，每轮调用一次 `read4`',
              '把 `buf4` 里读到的字符逐个抄进 `buf[offset + index]`',
              'n 不是 4 的倍数，所以抄到第 `n` 个字符就==直接返回=='],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：`read4` 返回值可能小于 4（文件结束），要用返回值而不是固定 4',
                 '易错点：`res == n` 要在每放一个字符后检查，否则会写超出 n',
                 '演示用 `setup` 里实现了一个读 `"abcdefghijk"` 的 `read4`，作者代码未改'],
    ),
)
