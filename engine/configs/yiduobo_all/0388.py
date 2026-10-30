def _lines(S):
    return [p.lstrip('\t') for p in S['input'].split('\n')]


def _cur(S, i, v):
    parts = S['input'].split('\n')
    if 'part' not in S:
        return None
    return 'blue' if parts[i] == S['part'] else None


def _text(S):
    if 'part' not in S:
        return '每行开头的 tab 个数 = 层数；`prefix[d]` = 前 d 层目录路径的长度（含斜杠）'
    part = S['part']
    d = len(part) - len(part.lstrip('\t'))
    kind = '文件（含 `.`）' if '.' in part else '文件夹'
    return f"当前 ==`{part.lstrip(chr(9))}`==：{d} 个 tab，在第 {d} 层，是{kind}"


CONFIG = dict(
    num=388, title='文件的最长绝对路径', difficulty='Medium', category='字符串',
    author='yiduobo', technique='按层数维护前缀长度数组',
    tags=[],
    code='''
class Solution(object):
    def lengthLongestPath(self, input):

        res = 0

        prefix = [0]
        for part in split(input, '\\n'):
            pos = 0
            while part[pos] == '\\t':
                pos += 1
            l = len(part) - pos + prefix[pos]

            if part.find('.') != -1:
                res = max(res, l)
            else:
                if len(prefix) < pos + 2:
                    prefix.append(l + 1)
                else:
                    prefix[pos + 1] = l + 1

        return res
''',
    setup='''
def split(s, sep):
    return s.split(sep)
''',
    call='Solution().lengthLongestPath("dir\\n\\tsubdir1\\n\\t\\tfile1.ext\\n\\t\\tsubsubdir1\\n\\tsubdir2\\n\\t\\tsubsubdir2\\n\\t\\t\\tfile2.ext")',
    expect=32,
    views=[
        dict(type='text', fn=_text, h=70),
        dict(type='array', var=_lines, label='input 按换行拆开（蓝 = 当前行，名字前的 tab 已省略）', cell=140, color=_cur, h=250),
        dict(type='array', var='prefix', label='prefix[d]：前 d 层目录的路径长度（含斜杠）', cell=96,
             pointers={'pos': 'blue'}, h=200),
        dict(type='text', fn=lambda S: f"res = =={S['res']}==（目前见过的最长文件路径）" if 'res' in S else '', h=60),
    ],
    watch=[('pos', 'pos', 'blue'), 'l', ('res', 'res', 'green')],
    skip=['pos = 0', 'pos += 1'],
    captions={
        'res = 0': '`res` 记录最长的==文件==路径长度',
        'prefix = [0]': '`prefix = [0]`：第 0 层是根目录，前面没有任何路径',
        'for part in': lambda S, B, r: ('所有行都处理完，循环结束' if B.get('part') == S['part'] else f"取下一行 `part`，长度 {len(S['part'])}"),
        'while part[pos]': lambda S, B, r: (f"`part[{S['pos']}]` 是 tab → 数下一个" if S['part'][S['pos']] == '\t'
                                            else f"`part[{S['pos']}]` 不是 tab：tab 数 `pos = {S['pos']}` 就是它所在的层数"),
        'pos += 1': '又一个 tab，`pos` → {pos}',
        'l = len(part)': '去掉 tab 的名字长 `{len(part) - pos}`，加上上面各层的 `prefix[{pos}] = {prefix[pos]}`，路径长 `l` = =={l}==',
        'if part.find': lambda S, B, r: ('名字里有 `.` → 是文件，它下面不会再有内容，只需要比较答案' if '.' in S['part']
                                         else '名字里没有 `.` → 是文件夹，要把它记进 `prefix` 给下一层用'),
        'res = max': '`res = max({B.res}, {l}) = {res}`',
        'if len(prefix) < pos + 2': lambda S, B, r: (f"`prefix` 还没有第 {S['pos'] + 1} 项（长度 {len(S['prefix'])} < {S['pos'] + 2}）→ 追加" if len(S['prefix']) < S['pos'] + 2
                                                     else f"`prefix[{S['pos'] + 1}]` 已有旧值（上一个同层文件夹留下的）→ 直接覆盖"),
        'prefix.append': '第 {pos + 1} 层的前缀长度 = `l + 1` = =={l + 1}==（+1 是路径里的 `/`）',
        'prefix[pos + 1] = l + 1': '同层的上一个文件夹已处理完，==覆盖== `prefix[{pos + 1}]` = {l + 1}',
        'return res': '最长文件路径长度 `{res}`',
    },
    cards=dict(
        one_liner='数 tab 得到层数，用前缀数组记下每层目录的路径长度',
        complexity='时间 `O(n)`，空间 `O(d)`（d 为最大层数）',
        problem=['用 `\\n` 和 `\\t` 表示文件系统：`\\t` 的个数是层数',
                 '名字里有 `.` 的是文件，求==最长文件绝对路径==的长度（无文件返回 0）',
                 '示例：`dir\\n\\tsubdir1\\n\\t\\tfile1.ext\\n\\t\\tsubsubdir1\\n\\tsubdir2\\n\\t\\tsubsubdir2\\n\\t\\t\\tfile2.ext` → `32`'],
        quote='注意到对于文件夹来说，需要关注的是f的前缀和，而对于f本身的值并不关心，于是可以直接维护前缀和数组来提高效率。',
        quote_src='—— yiduobo 题解原文',
        idea=['按换行拆开，每行开头的 tab 数 `pos` 就是它所在的层数',
              '文件夹：把「前面各层长度 + 自己 + 斜杠」记在 `prefix[pos+1]`，同层的新文件夹直接覆盖旧的',
              '文件：路径长 = `prefix[pos]` + 名字长度，只比较答案，不记录'],
        summary=['时间 `O(n)`，空间 `O(d)`',
                 '文件夹长度要 `+1`（斜杠），文件本身不用；所以文件夹存的是 `l + 1`',
                 '用 `.` 判断文件，同层的新文件夹可以直接覆盖旧值',
                 '原文用 Python 2 的 `split(input, \'\\n\')`（string 模块函数），已在 setup 里补成等价的 `str.split`，作者代码未改'],
    ),
)
