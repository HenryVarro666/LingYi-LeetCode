def _trie_view(root_name, kids, mark, cur_name, title):
    """画 trie：根在上，边标签写在子节点里；绿框 = 某个路径在这里结束（end 标记），蓝 = 当前所在节点。"""
    def draw(cv, S, B, box, T):
        x0, y0, x1, y1 = box
        cv.text((x0 + 18, y0 + 4), title, 24, T['muted'], bold=True)
        root = S.get(root_name)
        if root is None:
            cv.text((x0 + 18, y0 + 56), '（trie 还没建）', 24, T['dim'])
            return
        cur = S.get(cur_name)
        pos, leaves = {}, [0]

        def lay(n, label, d):
            ch = list(kids(n).items())
            if not ch:
                x = leaves[0]
                leaves[0] += 1
            else:
                xs = [lay(c, k, d + 1) for k, c in ch]
                x = sum(xs) / len(xs)
            pos[id(n)] = (x, d, label, n)
            return x

        lay(root, '根', 0)
        maxd = max(d for _, d, _, _ in pos.values())
        nl = max(1, leaves[0])
        W, H = x1 - x0 - 80, y1 - y0 - 110
        gx = min(150, W / max(1, nl))
        gy = min(120, H / max(1, maxd))
        ox = x0 + 40 + (W - gx * (nl - 1)) / 2
        oy = y0 + 70

        def xy(n):
            x, d, _, _ = pos[id(n)]
            return ox + x * gx, oy + d * gy

        for n, (x, d, label, _) in pos.items():
            pass
        for _, (x, d, label, node) in pos.items():
            px, py = ox + x * gx, oy + d * gy
            for k, c in kids(node).items():
                cx, cy = xy(c)
                cv.line([(px, py + 24), (cx, cy - 24)], T['border'], 3)
        for _, (x, d, label, node) in pos.items():
            px, py = ox + x * gx, oy + d * gy
            is_cur = node is cur
            end = bool(mark(node))
            fill = T['blue'] if is_cur else (70, 76, 86)
            cv.rect((px - 30, py - 24, px + 30, py + 24), fill=fill, r=24,
                    outline=(T['green'] if end else None), width=5)
            cv.text((px, py), label, 26, T['bg'] if is_cur else T['text'], anchor='mm', bold=True)
    return draw


def _cur_txt(S):
    fl = S.get('folder_list')
    if fl is None:
        return '把每个路径按 `/` 切成层级列表'
    if 'flag' not in S or S.get('_line') == 8:
        return f'当前路径层级：`{fl}`'
    return f'当前路径 `{fl}`，flag = ==`{S["flag"]}`==（True = 保留）'


CONFIG = dict(
    num=1233, title='删除子文件夹', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='按层级排序 + trie 判断',
    tags=['字典树（trie）'],
    code='''
class Solution(object):
    def removeSubfolders(self, folder):

        splitted_folder = [x[1:].split('/') for index, x in enumerate(folder)]

        res = []
        root = [{}, False]
        for folder_list in sorted(splitted_folder, key=lambda d:len(d)):
            now = root
            flag = True
            for folder in folder_list:
                if now[1]:
                    flag = False
                    break
                if folder not in now[0]:
                    now[0][folder] = [{}, False]
                now = now[0][folder]
            
            if flag:
                now[1] = True
                res.append('/' + '/'.join(folder_list))
        
        return res
''',
    call='Solution().removeSubfolders(["/c/d/e", "/a/b", "/c/f", "/a", "/c/d"])',
    expect=['/a', '/c/f', '/c/d'],
    views=[
        dict(type='custom', h=360, draw=_trie_view('root', lambda n: n[0], lambda n: n[1], 'now',
                                                   'trie（节点 = 目录名；绿框 = 有路径在此结束；蓝 = now）')),
        dict(type='array', var='res', label='res（保留的路径）', cell=130, h=170),
        dict(type='text', h=90, size=28, fn=_cur_txt),
    ],
    watch=[('folder_list', 'folder_list', 'blue'), ('folder', 'folder', 'pink'), ('flag', 'flag', 'yellow')],
    captions={
        'splitted_folder = ': '按 `/` 切开：`/a/b` → `{splitted_folder[1]}`，列表长度就是层级',
        'root = [{}, False]': 'trie 节点 = `[子节点字典, 是否有路径在此结束]`',
        'for folder_list in sorted': lambda S, B, r: ('所有路径都处理完了' if B.get('folder_list') is S.folder_list
                                                      else f'==层级浅的先处理==：`{S.folder_list}`（{len(S.folder_list)} 层），上级一定先入树'),
        'now = root': '每个路径都从根开始往下走',
        'flag = True': '先假定它不是子文件夹',
        'for folder in folder_list': lambda S, B, r: ('这条路径的每一层都走完了' if B.get('folder') == S.folder_list[-1] and B.now is not B.root
                                                      else f'取这一层目录 `{S.folder}`'),
        'if now[1]': lambda S, B, r: (f"`now[1]` 为 True：这条路上已经有路径结束了 → 当前路径在它下面" if S.now[1]
                                      else '`now[1]` 为 False：路上没有更短的路径结束，继续'),
        'flag = False': '路上遇到了结束标记 → ==它是子文件夹==，`flag = False`',
        'break': '不用再往下走了，跳出这一层循环',
        'if folder not in now[0]': lambda S, B, r: (f"`{S.folder}` 还不在 trie 里 → 新建节点" if S.folder not in B.now[0]
                                                    else f"`{S.folder}` 已经在 trie 里 → 直接沿用"),
        'now[0][folder] = ': '新建子节点 `{folder}`',
        'now = now[0][folder]': '走到子节点 `{folder}`',
        'if flag:': lambda S, B, r: ('`flag` 为 True → 不是子文件夹，保留' if S.flag else '`flag` 为 False → 是子文件夹，丢弃'),
        'now[1] = True': '在终点打上结束标记：以后经过这里的更长路径都是它的子文件夹',
        'res.append': '保留路径 `{res[-1]}`',
        'return res': '剩下的文件夹：`{res}`',
    },
    max_steps=90,
    cards=dict(
        one_liner='浅层路径先入 trie，路上撞到结束标记就是子文件夹',
        complexity='时间 `O(n·l)`（排序另算），空间 `O(n·l)`',
        problem=['`folder` 是一组路径，删掉所有位于别的文件夹下面的子文件夹',
                 '`/a/b` 是 `/a` 的子文件夹',
                 '示例：`["/a","/a/b","/c/d","/c/d/e","/c/f"]` → `["/a","/c/d","/c/f"]`'],
        quote='若一个文件夹a是另一个文件夹b的子文件夹，那么二者必然有相同的前缀b，因此一个自然的想法就是利用trie树来进行判断。',
        quote_src='—— yiduobo 题解原文',
        idea=['先按 `/` 切开，==层级数就是列表长度==',
              '按层级从小到大排序，保证上级一定先于下级进入 trie',
              '逐层往下走：路上遇到「有路径结束」的节点，说明它在某个上级之下，丢弃；否则插入并标记终点'],
        summary=['时间：每个路径走 `O(l)` 层，加上排序；空间 `O(n·l)`',
                 '按层级排序是关键：保证插入时上级已在 trie 中',
                 '易错：内层循环变量 `folder` 与参数同名，原文如此，参数在循环前已被用完',
                 '原文为 Python 2 风格写法，没有需要改动的地方',
                 '对比灵神：灵神按字典序排序，只和上一个保留的路径比前缀，不用 trie'],
    ),
)
