def _fs(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '文件树（蓝 = 文件夹，绿 = 文件，黄 = 当前节点 now）', 24, T['muted'], bold=True)
    root = S.get('self.root')
    if root is None:
        return
    now = S.get('now')
    rows = []

    def walk(n, d):
        rows.append((n, d))
        for k in sorted(n.childs):
            walk(n.childs[k], d + 1)

    walk(root, 0)
    rh = min(56, (y1 - y0 - 70) / max(len(rows), 1))
    for i, (n, d) in enumerate(rows):
        X = x0 + 40 + d * 60
        Y = y0 + 60 + i * rh
        isnow = n is now
        base = T['green'] if n.file_flag else T['blue']
        if d > 0:
            cv.line([(X - 40, Y + rh / 2), (X - 8, Y + rh / 2)], T['border'], 2)
        cv.rect((X, Y + 3, X + 150, Y + rh - 3), fill=T['yellow'] if isnow else T['panel2'], outline=base, width=3, r=8)
        name = '/ (root)' if n is root else n.file_name
        cv.text((X + 75, Y + rh / 2), name, 22, T['bg'] if isnow else T['text'], anchor='mm', bold=True, mono=True)
        if n.file_flag:
            cv.text((X + 164, Y + rh / 2), f'内容 = "{n.file_content}"', 22, T['green'], anchor='lm', mono=True)


def _parts(S):
    p = S.get('parts')
    if p is None:
        return ''
    return '路径拆分：`' + str(p) + '`（下标 0 是空串，从 1 开始）'


CONFIG = dict(
    num=588, title='设计内存文件系统', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='树结构 + 逐级向下迭代',
    code='''
class TreeNode(object):

    def __init__(self, file_name, file_flag, file_content = ""):
        self.file_name = file_name
        self.file_flag = file_flag
        self.file_content = file_content
        self.childs = {}

class FileSystem(object):

    def __init__(self):
        self.root = TreeNode('', False)

    def ls(self, path):

        now = self.root
        if len(path) > 1:
            parts = path.split('/')
            for name in parts[1:]:
                now = now.childs[name]
            
        if now.file_flag:
            return [now.file_name]
        else:
            return sorted(now.childs.keys())

    def mkdir(self, path):

        now = self.root
        parts = path.split('/')
        for name in parts[1:]:
            if name not in now.childs:
                tmp = TreeNode(name, False)
                now.childs[name] = tmp
            
            now = now.childs[name]

    def addContentToFile(self, filePath, content):

        now = self.root
        parts = filePath.split('/')
        for name in parts[1: len(parts) - 1]:
            now = now.childs[name]
        
        if parts[-1] not in now.childs:
            now.childs[parts[-1]] = TreeNode(parts[-1], True, content)
        else:
            now.childs[parts[-1]].file_content += content

    def readContentFromFile(self, filePath):

        now = self.root
        parts = filePath.split('/')
        for name in parts[1:]:
            now = now.childs[name]
        
        return now.file_content
''',
    call='''fs = FileSystem()
out = []
fs.mkdir("/a/b")
fs.addContentToFile("/a/b/c", "hi")
fs.addContentToFile("/a/b/c", "!")
out.append(fs.ls("/a/b"))
out.append(fs.readContentFromFile("/a/b/c"))
out''',
    expect=[['c'], 'hi!'],
    views=[
        dict(type='text', fn=_parts, size=24),
        dict(type='custom', draw=_fs, h=360),
        dict(type='calls', label='正在执行', h=110),
    ],
    watch=['path', 'filePath', 'content', 'name', ('now', "getattr(now, 'file_name', None)", 'yellow')],
    skip=['self.file_name = file_name', 'self.file_flag = file_flag', 'self.file_content = file_content', 'self.childs = {}',
          'tmp = TreeNode(name, False)'],
    max_steps=90,
    captions={
        'self.root = TreeNode': '初始化：只需要一个根节点 `root`，它是==文件夹==',
        'now = self.root': '每个操作都从 `root` 出发，用 `now` 逐级向下',
        'if len(path) > 1': lambda S, B, r: ('`path` 不只是 `/` → 要往下走' if len(S.path) > 1 else '`path` 就是 `/` → 停在根目录'),
        'parts = path.split': '按 `/` 拆分：`{parts}`，下标 0 是空串所以从 1 开始',
        'parts = filePath.split': '按 `/` 拆分：`{parts}`，下标 0 是空串所以从 1 开始',
        'for name in parts[1:]': lambda S, B, r: (f'进入下一级：`name = "{S.name}"`' if S.get('name') != B.get('name') or 'name' not in B else '路径走完了'),
        'for name in parts[1: len': lambda S, B, r: (f'进入下一级目录：`name = "{S.name}"`' if S.get('name') != B.get('name') or 'name' not in B else '==只走到最后一级之前==（父目录），文件名留给下面处理'),
        'now = now.childs[name]': lambda S, B, r: f'`now` 走进 `{S.name}`',
        'if now.file_flag': lambda S, B, r: ('目标是==文件==：`ls` 返回只含它自己名字的列表' if S.now.file_flag else '目标是==文件夹==：返回孩子名字'),
        'return [now.file_name]': '返回 `{ret}`',
        'return sorted': '子目录内容==排序==后返回：`{ret}`',
        'if name not in now.childs': lambda S, B, r: (f'`"{S.name}"` 还不存在 → 新建文件夹' if S.name not in S.now.childs else f'`"{S.name}"` 已存在，直接进入'),
        'now.childs[name] = tmp': '在 `now` 下挂上新文件夹 `{name}`',
        'if parts[-1] not in now.childs': lambda S, B, r: (f'文件 `{S.parts[-1]}` 不存在 → 新建一个内容为 `"{S.content}"` 的文件' if S.parts[-1] not in S.now.childs
                                                           else f'文件 `{S.parts[-1]}` 已存在 → 在末尾追加内容'),
        'now.childs[parts[-1]] = TreeNode': '新建文件：`file_flag = True`，内容 `"{content}"`',
        '.file_content += content': '追加 `"{content}"`，内容变成 `"{now.childs[parts[-1]].file_content}"`',
        'return now.file_content': '读到的内容 `"{ret}"`',
    },
    cards=dict(
        one_liner='一切都是树节点：文件夹和文件只差一个标记',
        complexity='每个操作 `O(路径长度)`（`ls` 目录另加排序）',
        problem=['设计内存文件系统：`ls`、`mkdir`、`addContentToFile`、`readContentFromFile`',
                 '`ls` 目录返回其下名字（字典序）；`ls` 文件返回只含文件名的列表',
                 '`mkdir` 逐级创建；`addContentToFile` 文件不存在就新建，存在则追加'],
        quote='文件系统应该是某种树结构，其中所有的东西都可以认为是文件，因此可以使用树节点来表示单个的文件或者文件夹。',
        quote_src='—— yiduobo 题解原文',
        idea=['节点四个属性：名称、是否文件、文件内容、子目录 `childs`（哈希表）',
              '所有操作同一个套路：`path.split("/")`，`now` 从 `root` 逐级向下',
              '`addContentToFile` 只走到父目录，最后一级再判断新建或追加'],
        summary=['`ls`、`mkdir` 等都是 `O(L)`，`L` 为路径长度（`ls` 目录加排序）',
                 '易错：`split("/")` 的第 0 项是空串，要从 `parts[1:]` 开始',
                 '易错：`ls("/")` 不能 split（会得到两个空串），所以先判断 `len(path) > 1`',
                 '`ls` 路径是文件时返回 `[文件名]`，是目录时返回排序后的孩子名',
                 '原文本就能在 Python 3 运行，代码无改动（类名 `TreeNode` 为作者原名）'],
    ),
)
