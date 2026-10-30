PATHS = ['root/a 1.txt(abcd) 2.txt(efgh)', 'root/c 3.txt(abcd)', 'root/c/d 4.txt(efgh)']


def _txt(S):
    if 'file_content' in S and 'file_name' in S and 'file_dir' in S and S['_line'] in (10, 11, 12):
        return f"`{S['file_dir']}` 下的 `{S['file_name']}`，内容 `{S['file_content']}` → 路径 =={S['file_dir']}/{S['file_name']}=="
    if 'file_dir' in S and S['_line'] in (7, 8, 9):
        return f"当前目录 `{S['file_dir']}`，后面每一项形如 `文件名(内容)`"
    return ''


def _tmp_txt(S):
    if 'tmp' not in S:
        return ''
    cur = S.get('index') if S['_line'] >= 8 else None
    parts = []
    for k, t in enumerate(S['tmp']):
        parts.append(f'==`{t}`==' if k == cur else f'`{t}`')
    return 'tmp = ' + '  |  '.join(parts) + ('' if cur is None else f'（下标 {cur}）')


def _done_files(S):
    return 'file_name' in S and 'index' in S and S['tmp'][S['index']].startswith(S['file_name'] + '(')


CONFIG = dict(
    num=609, title='在系统中查找重复文件', difficulty='Medium', category='字符串',
    author='yiduobo', technique='字符串拆分 + 内容为 key 的字典',
    tags=[],
    code='''
class Solution(object):
    def findDuplicate(self, paths):

        file_dict = {}
        for path in paths:
            tmp = path.split(' ')
            file_dir = tmp[0]
            for index in range(1, len(tmp)):
                file_name, file_content = tmp[index][:-1].split('(')
                if file_content not in file_dict:
                    file_dict[file_content] = []
                file_dict[file_content].append(file_dir + '/' + file_name)
        
        res = []
        for file_content in file_dict:
            if len(file_dict[file_content]) > 1:
                res.append(file_dict[file_content])

        return res
''',
    call=f'Solution().findDuplicate({PATHS!r})',
    expect=[['root/a/1.txt', 'root/c/3.txt'], ['root/a/2.txt', 'root/c/d/4.txt']],
    views=[
        dict(type='text', h=170, size=30, fn=_tmp_txt),
        dict(type='map', var='file_dict', label='file_dict（文件内容 → 路径列表）', fmt=lambda k, v: f'{k}: {v}', h=260, font=24),
        dict(type='text', h=100, size=28, fn=_txt),
    ],
    watch=[('file_dir', 'file_dir', 'cyan'), ('file_name', 'file_name', 'blue'), ('file_content', 'file_content', 'orange'), ('res', 'res', 'green')],
    max_steps=90,
    captions={
        'file_dict = {}': '`file_dict`：以==文件内容==为 key，把内容相同的文件路径收在一起',
        'for path in paths': lambda S, B, r: ('所有目录都处理完了' if B.get('path') == S.path else f'处理一个目录串：`{S.path!r}`'),
        'tmp = path.split': '按空格切开：第 0 项是目录，后面是 `文件名(内容)`',
        'file_dir = tmp[0]': '目录 `file_dir = {file_dir!r}`',
        'for index in range': lambda S, B, r: ('这个目录的文件都处理完了' if _done_files(S) else f'取第 `{S.index}` 项 `{S.tmp[S.index]!r}`（下标从 1 开始，跳过目录名）'),
        'file_name, file_content =': '`[:-1]` 去掉结尾的 `)`，再按 `(` 切开：文件名 `{file_name}`，内容 `{file_content}`',
        'if file_content not in file_dict': lambda S, B, r: (f'`{S.file_content}` 第一次出现 → 先建一个空列表' if S.file_content not in B.file_dict
                                                           else f'`{S.file_content}` 已经有了：同内容的文件已经出现过'),
        'file_dict[file_content] = []': '新建 `file_dict[{file_content!r}] = []`',
        'file_dict[file_content].append': '完整路径 `{file_dir}/{file_name}` 加入 `{file_content}` 这一组 → `{file_dict[file_content]}`',
        'res = []': '字典建好了：现在挑出==路径不止一个==的组',
        'for file_content in file_dict': lambda S, B, r: ('每一组都检查过了' if B.get('file_content') == S.file_content else f'检查内容 `{S.file_content}` 这一组'),
        'if len(file_dict[file_content]) > 1': lambda S, B, r: (f'这组有 `{len(S.file_dict[S.file_content])}` 个文件 > 1 → 内容重复，收入答案' if len(S.file_dict[S.file_content]) > 1
                                                              else f'这组只有 1 个文件：没有重复，不要'),
        'res.append(file_dict[file_content])': '把这一组路径整体加入 `res`：`{res}`',
        'return res': '返回所有重复文件组：`{res}`',
    },
    cards=dict(
        one_liner='文件内容当 key，路径当 value：同一个 key 下有多个路径就是重复',
        complexity='时间 `O(总字符数)`，空间 `O(总字符数)`',
        problem=['每个字符串形如 `"目录 文件名(内容) 文件名(内容) …"`',
                 '找出==内容完全相同==的文件，每组返回它们的完整路径，只返回至少两个文件的组',
                 '本视频：3 个目录串共 4 个文件 → `[[root/a/1.txt, root/c/3.txt], [root/a/2.txt, root/c/d/4.txt]]`'],
        quote='遍历每一个目录，然后遍历其中的文件，将文件内容作为key，目录名称加文件名作为value储存到dict当中。处理完毕后，若dict中某个key对应的value中包含多个文件名，说明该文件重复',
        quote_src='—— yiduobo 题解原文',
        idea=['这题其实是==字符串处理==：文件数 ≤ 20000，内容长度 ≤ 50，直接模拟',
              '`split(\' \')` 得到目录和各个 `文件名(内容)`；`[:-1]` 去掉 `)` 后按 `(` 切开',
              '`file_dict[内容]` 收集完整路径 `目录/文件名`；最后只留下长度大于 1 的列表'],
        summary=['时间、空间都与输入总字符数成正比',
                 '易错：`[:-1]` 去掉的是结尾的 `)`，否则内容会带着括号',
                 '完整路径要自己拼：`file_dir + \'/\' + file_name`',
                 '只有一个文件的内容组不能放进答案',
                 '原文为 Python 2 风格，本题代码在 Python 3 下可直接运行，未改动'],
    ),
)
