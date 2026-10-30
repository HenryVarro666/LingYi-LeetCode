PATH = '/../home//user/./../docs/'
PARTS = PATH.split('/')

# 代码是 `for path_part in path_list`，没有下标；字幕按顺序生成时记下“第几段”，给视图画指针用
_cnt = [-1]
_POS = {}


def _rec(fn):
    def g(S, B, ret):
        if S._line == 5:
            _cnt[0] += 1
        if 'now' in S:
            _POS[id(S.now)] = _cnt[0]
        return fn(S, B, ret)
    return g


def _idx(S):
    k = _POS.get(id(S.get('now')))
    return k if k is not None and 0 <= k < len(PARTS) else None


def _case(x):
    if not x:
        return 1
    if x == '.':
        return 2
    if x == '..':
        return 3
    return 4


def _pcolor(S, i, v):
    return 'yellow' if i == _idx(S) else None


def _pdim(S, i, v):
    k = _idx(S)
    if k is None:
        return S.get('_line', 0) >= 15
    return i < k


def _cap_for(S, B, ret):
    k = _cnt[0]
    if k >= len(PARTS):
        return '所有部分都处理完了'
    x = S.path_part
    return f'第 {k} 段 `"{x}"` → 属于==情况 {_case(x)}=='


def _cap_empty(S, B, ret):
    if not S.path_part:
        return '情况 1：==什么都没有==（连续的 `/` 或首尾的 `/`）→ 无事发生'
    return f'`"{S.path_part}"` 不是空串'


def _cap_dot(S, B, ret):
    if S.path_part == '.':
        return '情况 2：==只有一个点==，留在当前目录 → 无事发生'
    return f'`"{S.path_part}"` 不是 `"."`'


def _cap_dd(S, B, ret):
    if S.path_part == '..':
        return '情况 3：==两个点==，跳到上级目录（如果存在）'
    return f'`"{S.path_part}"` 也不是 `".."` → 情况 4'


def _cap_len(S, B, ret):
    if len(S.now) > 0:
        return f'栈里有 {len(S.now)} 个目录 → 存在上级目录，可以往上跳'
    return '栈是空的：已经在最高级目录 `/`，==没法再往上== → 无事发生'


CONFIG = dict(
    num=71, title='简化路径', difficulty='Medium', category='栈',
    author='yiduobo', technique='split 后分四种情况 + 栈',
    tags=['字节30天', '面试经典150'],
    code='''
class Solution(object):
    def simplifyPath(self, path):
        path_list = path.split('/')
        now = []
        for path_part in path_list:
            if not path_part:
                continue
            elif path_part == '.':
                continue
            elif path_part == '..':
                if len(now) > 0:
                    now.pop()
            else:
                now.append(path_part)

        res = '/' + '/'.join(now)
        return res
''',
    call=f'Solution().simplifyPath({PATH!r})',
    expect='/home/docs',
    views=[
        dict(type='text', text=f'`path = "{PATH}"`', h=60),
        dict(type='array', var=lambda S: [x if x else '""' for x in S['path_list']] if 'path_list' in S else None,
             label="path_list（黄 = 当前段，灰 = 已处理）", cell=100, color=_pcolor, dim=_pdim,
             pointers={_idx: 'yellow'}, pointer_labels={_idx: 'path_part'}, h=215),
        dict(type='text', fn=lambda S: (f"情况 {_case(PARTS[_idx(S)])}：" +
                                        ['', '空串 → 无事发生', '`.` → 无事发生', '`..` → 弹出栈顶', '新子目录 → 压入栈顶'][_case(PARTS[_idx(S)])])
             if _idx(S) is not None else '', h=60),
        dict(type='stack', var='now', label='now（用栈维护整个路径）', h=130, font=30),
        dict(type='text', fn=lambda S: f"当前路径：`{'/' + '/'.join(S['now'])}`" if 'now' in S else '', h=70, size=32),
    ],
    watch=[('path_part', 'path_part', 'yellow'), ('now', 'now', 'purple'), 'res'],
    skip=['continue'],
    captions={
        'path_list = path.split': _rec(lambda S, B, ret: f'先 `split("/")`，得到 {len(S.path_list)} 段'),
        'now = []': _rec(lambda S, B, ret: '`now` 当栈用，从底到顶就是从最高级目录往下的路径'),
        'for path_part in': _rec(_cap_for),
        'if not path_part': _rec(_cap_empty),
        "elif path_part == '.'": _rec(_cap_dot),
        "elif path_part == '..'": _rec(_cap_dd),
        'if len(now) > 0': _rec(_cap_len),
        'now.pop()': _rec(lambda S, B, ret: f'弹出栈顶 `"{B.now[-1]}"`：去掉当前路径的最后一个子目录'),
        'else': _rec(lambda S, B, ret: f'情况 4：来到了一个==新的子目录== `"{S.path_part}"`'),
        'now.append': _rec(lambda S, B, ret: f'把 `"{S.path_part}"` 压入栈顶'),
        'res = ': _rec(lambda S, B, ret: f'栈中的目录名用 `/` join，再加上最高级目录的 `/` → `"{S.res}"`'),
        'return res': _rec(lambda S, B, ret: f'返回 =={ret}=='),
    },
    cards=dict(
        one_liner='split 之后只有四种情况：空、点、两个点、新目录',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['把 Unix 风格的绝对路径化简成==规范路径==',
                 '`.` 是当前目录，`..` 是上一级，连续多个 `/` 算一个',
                 '示例：`"/home//foo/"` → `"/home/foo"`；`"/../"` → `"/"`',
                 '演示：`"/../home//user/./../docs/"` → `"/home/docs"`'],
        quote='由于每次往上跳转时都是==去掉了当前路径中的最后一个子目录==，因此可以用栈来维护整个路径，当出现新的子目录时，将其压入栈顶。',
        quote_src='—— yiduobo 题解原文',
        idea=['`/` 之间的字符串只有四种情况：',
              '1 什么都没有、2 只有一个点 → ==无事发生==',
              '3 两个点 → 弹出栈顶（如果存在）；4 其他 → 新子目录压栈',
              '最后把栈 join 起来，再加上最高级目录的 `/`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：在最高级目录遇到 `..` 要先判断 `len(now) > 0`',
                 '`if not path_part` 同时处理开头、结尾和连续的 `/`',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改',
                 '对比灵神：同样是栈，灵神把空串和 `.` 合成一个条件，写得更紧凑'],
    ),
)
