PATH = '/.../a/../b/c/../d/./'
PARTS = PATH.split('/')

# 代码里是 `for s in path.split('/')`，没有下标变量；字幕按顺序生成时记下“当前是第几段”，供视图画指针
_cnt = [-1]
_POS = {}


def _rec(fn):
    def g(S, B, ret):
        if S._line == 4:
            _cnt[0] += 1
        _POS[id(S.stk)] = _cnt[0]
        return fn(S, B, ret)
    return g


def _idx(S):
    k = _POS.get(id(S.get('stk')))
    return k if k is not None and k < len(PARTS) else None


def _pcolor(S, i, v):
    k = _idx(S)
    if k is None:
        return None
    if i == k:
        return 'yellow'
    return None


def _pdim(S, i, v):
    k = _idx(S)
    done = k is None and S.get('_line') == 11
    return done or (k is not None and i < k)


def _cap_for(S, B, ret):
    k = _cnt[0]
    if k == 0:
        return f'`path.split("/")` 切成 {len(PARTS)} 段，从左到右处理。第 0 段：`"{S.s}"`'
    if k >= len(PARTS):
        return '所有段都处理完了'
    return f'第 {k} 段：`"{S.s}"`'


def _cap_skip(S, B, ret):
    if S.s == '':
        return '==空串==（开头、结尾或连续的 `/` 切出来的）→ 跳过'
    if S.s == '.':
        return '`"."` 表示==当前目录== → 跳过'
    return f'`"{S.s}"` 不是空串也不是 `"."` → 往下看'


def _cap_ne(S, B, ret):
    if S.s != '..':
        extra = '（三个点不是 `..`，是合法名字）' if S.s == '...' else ''
        return f'`"{S.s}"` 是普通目录名{extra} → 入栈'
    return '`".."`：要==返回上一级==目录'


def _cap_elif(S, B, ret):
    if S.stk:
        return f'栈非空 → 删掉 `..` 左侧的 `"{S.stk[-1]}"`'
    return '栈空：已经在根目录，`..` 无效'


CONFIG = dict(
    num=71, title='简化路径', difficulty='Medium', category='栈',
    author='灵茶山艾府', technique='栈模拟',
    tags=['字节30天', '面试经典150'],
    code='''
class Solution:
    def simplifyPath(self, path: str) -> str:
        stk = []
        for s in path.split('/'):
            if s == "" or s == ".":
                continue
            if s != "..":
                stk.append(s)
            elif stk:
                stk.pop()
        return '/' + '/'.join(stk)
''',
    call=f'Solution().simplifyPath({PATH!r})',
    expect='/.../b/d',
    views=[
        dict(type='text', text=f'`path = "{PATH}"`', h=60),
        dict(type='array', var=lambda S: [x if x else '""' for x in PARTS] if 'stk' in S else None,
             label="path.split('/')（黄 = 当前段，灰 = 已处理）", cell=96, color=_pcolor, dim=_pdim,
             pointers={_idx: 'yellow'}, pointer_labels={_idx: 's'}),
        dict(type='stack', var='stk', label='stk（目录栈）', h=130, font=30),
        dict(type='text', fn=lambda S: f"当前所在目录：`{'/' + '/'.join(S['stk'])}`" if 'stk' in S else '', h=70, size=32),
    ],
    watch=[('s', 's', 'yellow'), ('stk', 'stk', 'purple')],
    skip=['continue'],
    captions={
        'stk = []': _rec(lambda S, B, ret: '栈 `stk` 记录==从根目录走到当前目录==经过的目录名'),
        'for s in': _rec(_cap_for),
        'if s == ""': _rec(_cap_skip),
        'continue': _rec(lambda S, B, ret: '`continue`：什么也不做'),
        'if s != ".."': _rec(_cap_ne),
        'stk.append': _rec(lambda S, B, ret: f'`"{S.s}"` 入栈：走进这个目录'),
        'elif stk': _rec(_cap_elif),
        'stk.pop()': _rec(lambda S, B, ret: f'弹出 `"{B.stk[-1]}"`：退回上一级'),
        'return': _rec(lambda S, B, ret: f'栈里的目录名用 `/` 拼起来，最前面补 `/` → =={ret}=='),
    },
    cards=dict(
        one_liner='按 / 切开：普通目录入栈，遇到 .. 弹栈',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['把 Unix 风格的绝对路径化简成==规范路径==',
                 '`.` 是当前目录，`..` 是上一级，连续多个 `/` 算一个，`...` 是合法名字',
                 '示例：`"/home//foo/"` → `"/home/foo"`；`"/../"` → `"/"`',
                 '演示（示例 5）：`"/.../a/../b/c/../d/./"` → `"/.../b/d"`'],
        quote='给你一组由 / 隔开的字符串（忽略空串和 .），请你从左到右遍历这些字符串，==依次删除每个 .. 及其左侧的字符串==（模拟返回上一级目录）。',
        quote_src='—— 灵茶山艾府题解（题意转述）',
        idea=['把 `path` 用 `/` 分割，遍历的同时==用栈维护==遍历过的字符串',
              '空串或 `.`：跳过；不是 `..`：入栈；是 `..`：栈非空就弹栈',
              '最后用 `/` 拼接，最前面也要有个 `/`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：根目录再 `..` 还是根目录 → 弹栈前先判断栈非空',
                 '易错：`...` 是普通目录名，只有恰好两个点才是上一级',
                 '栈空时 `"/" + ""` 正好是 `"/"`，不用特判'],
    ),
)
