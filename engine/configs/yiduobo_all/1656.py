CALL = """os = OrderedStream(5)
out = []
out.append(os.insert(3, "ccccc"))
out.append(os.insert(1, "aaaaa"))
out.append(os.insert(2, "bbbbb"))
out.append(os.insert(5, "eeeee"))
out.append(os.insert(4, "ddddd"))
out"""

CONFIG = dict(
    num=1656, title='设计有序流', difficulty='Easy', category='设计',
    author='yiduobo', technique='字典记录已到的位置 + pos 指针',
    code='''
class OrderedStream(object):

    def __init__(self, n):
        self.char_dict = {}
        self.pos = 1

    def insert(self, idKey, value):
        self.char_dict[idKey] = value
        res = []
        while self.pos in self.char_dict:
            res.append(self.char_dict[self.pos])
            self.pos += 1
        
        return res
''',
    call=CALL,
    expect=[[], ['aaaaa'], ['bbbbb', 'ccccc'], [], ['ddddd', 'eeeee']],
    views=[
        dict(type='text', fn=lambda S: (f"等待的位置 `pos = {S['self.pos']}`，字典里{'有' if S['self.pos'] in S['self.char_dict'] else '还没有'}它" if 'self.pos' in S and 'self.char_dict' in S else '')),
        dict(type='map', var='self.char_dict', fmt=lambda k, v: f'{k} → {v}', label='char_dict：已经到达的 id → value', h=260),
        dict(type='array', var='res', label='res（这次 insert 要返回的列表）', h=200, cell=110),
    ],
    watch=[('pos', 'self.pos', 'blue'), ('idKey', 'idKey', 'yellow'), ('value', 'value', 'green'), ('res', 'res', 'orange')],
    captions={
        'self.char_dict = {}': '用字典记下「哪些 id 已经到了」，没到的位置字典里就没有',
        'self.pos = 1': '`pos = 1`：下一个该输出的 id',
        'self.char_dict[idKey] = value': '`id = {idKey}` 到了：存入 `char_dict[{idKey}] = {value}`',
        'res = []': '这次要返回的列表 `res` 先清空',
        'while self.pos in': lambda S, B, r: (f"`pos = {S['self.pos']}` 在字典里 → 它可以输出" if S['self.pos'] in S['self.char_dict'] else f"`pos = {S['self.pos']}` 还没到 → 停止，后面的先等着"),
        'res.append': '把 `char_dict[{self.pos}]` = `{res[-1]}` 加入答案',
        'self.pos += 1': '`pos` 后移到 {self.pos}，看下一个位置到了没有',
        'return res': lambda S, B, r: ('`pos` 处没值 → 返回空列表' if not r else f'返回 {r}，`pos` 停在 {S["self.pos"]}'),
    },
    cards=dict(
        one_liner='字典记着谁到了，pos 往后数到第一个没到的',
        complexity='insert 均摊 `O(1)`，空间 `O(n)`',
        problem=['`n` 个 `(id, value)` 以任意顺序到来',
                 '每次 `insert` 后，从 `ptr` 起返回最长的 id 连续的一段，`ptr` 随之移动；否则返回空列表',
                 '示例：依次插入 id 3, 1, 2, 5, 4 → `[]`, `[aaaaa]`, `[bbbbb, ccccc]`, `[]`, `[ddddd, eeeee]`'],
        quote='只需要通过dict记录下当前有值的位置，然后对于每次insert操作而言，若当前ptr对应的位置有值，那么将这个值加入到答案中，并将ptr向后移动，直到ptr对应的位置没有值为止。',
        quote_src='—— yiduobo 题解原文',
        idea=['`char_dict` 存已到的 `id → value`',
              '每次 insert 先存值，再从 `pos` 起：字典里有就加入 `res`、`pos` 后移',
              '遇到没到的位置就停，`pos` 保留给下一次调用'],
        summary=['时间：`pos` 总共只右移 `n` 次，insert 均摊 `O(1)`；空间 `O(n)`',
                 '易错：`pos` 是对象属性，要跨调用保留，不能每次重置',
                 '和数组版的区别：用「key 是否在字典里」判断有没有到，不需要预分配',
                 '原文为 Python 2 风格，在本视频里原样运行，无需修改'],
    ),
)
