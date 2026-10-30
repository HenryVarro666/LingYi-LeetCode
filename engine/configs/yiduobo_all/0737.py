CONFIG = dict(
    num=737, title='句子相似性 II', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='并查集 · 单词转 id',
    tags=[],
    code='''
class Solution(object):
    def areSentencesSimilarTwo(self, sentence1, sentence2, similarPairs):

        if len(sentence1) != len(sentence2):
            return False

        words_mapping = {}
        fa = {}
        id = 0

        def find(now):
            if fa[now] != now:
                fa[now] = find(fa[now])
            return fa[now]

        for x, y in similarPairs:
            if x not in words_mapping:
                words_mapping[x] = id
                fa[id] = id
                id += 1
            if y not in words_mapping:
                words_mapping[y] = id
                fa[id] = id
                id += 1

            x_id, y_id = words_mapping[x], words_mapping[y]

            x_fa = find(x_id)
            y_fa = find(y_id)
            if x_fa != y_fa:
                fa[x_fa] = y_fa

        for x, y in zip(sentence1, sentence2):
            if x == y:
                continue

            x_id, y_id = words_mapping.get(x, -1), words_mapping.get(y, -1)
            if x_id == -1 or y_id == -1:
                return False

            x_fa = find(x_id)
            y_fa = find(y_id)
            if x_fa != y_fa:
                return False

        return True
''',
    call="Solution().areSentencesSimilarTwo(['great','acting'], ['fine','drama'], [['great','good'],['fine','good'],['drama','acting']])",
    expect=True,
    views=[
        dict(type='array', var='sentence1', label='sentence1', cell=140, h=175),
        dict(type='array', var='sentence2', label='sentence2', cell=140, h=175),
        dict(type='map', var='words_mapping', label='words_mapping（单词 → id）', fmt=lambda k, v: f"'{k}': {v}", h=140, font=26),
        dict(type='map', var='fa', label='fa（id → 父节点；根指向自己）', fmt=lambda k, v: f'{k}: {v}', h=140, font=28),
        dict(type='text', h=70, size=28, fn=lambda S: (f"当前一对：`{S['x']}` ↔ `{S['y']}`" if 'y' in S else '')),
    ],
    watch=['id', 'x', 'y', 'x_id', 'y_id', 'x_fa', 'y_fa'],
    captions={
        'if len(sentence1)': '句子长度不同，一定不相似；这里都是 `{len(sentence1)}`，继续',
        'words_mapping = {}': '`words_mapping`：把单词编号成整数 id，并查集就能用 id 当下标',
        'fa = {}': '`fa[id]`：id 的父节点，根节点的父节点是自己',
        'if x not in words_mapping': '`{x}` 还没编号吗？{"没有，要新建" if x not in words_mapping else "已有编号，不用新建"}',
        'if y not in words_mapping': '`{y}` 还没编号吗？{"没有，要新建" if y not in words_mapping else "已有编号，不用新建"}',
        'words_mapping[x] = id': '给 `{x}` 编号 `{id}`',
        'words_mapping[y] = id': '给 `{y}` 编号 `{id}`',
        'fa[id] = id': '新节点自成一个集合：`fa[{id}] = {id}`',
        'x_id, y_id = words_mapping[x], words_mapping[y]': '取出这对近义词的 id：`{x_id}` 和 `{y_id}`',
        'x_fa = find(x_id)': '`find({x_id})`：顺着 `fa` 往上找 x 的根，并做路径压缩',
        'y_fa = find(y_id)': '`find({y_id})`：找 y 的根',
        'if x_fa != y_fa:': '两个根 `{x_fa}` 和 `{y_fa}`：{"不同 → 不是同一集合" if x_fa != y_fa else "相同 → 已在同一集合"}',
        'fa[x_fa] = y_fa': '把 x 的根挂到 y 的根下：`fa[{x_fa}] = {y_fa}`，两个集合合成一个',
        'for x, y in zip(sentence1, sentence2)': '逐位比较两个句子：`{x}` 对 `{y}`',
        'if x == y:': '`{x} == {y}`？{"相同，天然相似" if x == y else "不同，要查它们是否在同一集合"}',
        'continue': '这一位相同，跳过',
        'x_id, y_id = words_mapping.get': '查 id：`{x}` → `{x_id}`，`{y}` → `{y_id}`（`-1` 表示不在任何相似对里）',
        'if x_id == -1': '{"有单词不在任何相似对里，又不相等 → 不可能相似" if x_id == -1 or y_id == -1 else "两个单词都在相似对里，继续比根"}',
        'return False': '返回 `False`',
        'return True': '每一位都相等或在同一集合 → ==相似==，返回 `True`',
    },
    skip=['id += 1', 'return fa[now]', 'x_id, y_id = words_mapping'],
    max_steps=95,
    cards=dict(
        one_liner='相似可传递 → 单词是点，相似对是边，同一连通块都相似',
        complexity='时间 `O((n+m)·α)`，空间 `O(m)`',
        problem=['给两个句子 `sentence1`、`sentence2` 和相似单词对 `similarPairs`',
                 '相似关系可以传递，一个单词和自己也相似',
                 '两句长度相同且逐位相似才返回 `True`',
                 '本视频：great/fine（经 good 相连）、acting/drama → `True`'],
        quote='如果将单词视为无向图中的点，相似关系视为无向图中的边，那么同一个连通块中的单词都是相似的。',
        quote_src='—— yiduobo 题解原文',
        idea=['上一题用哈希表判相似，这题相似会传递，改用==并查集==',
              '单词先转成 id 存进 `words_mapping`，`fa` 用 id 做键',
              '先把所有相似对合并，再逐位比较：相等直接过，否则看根是否相同'],
        summary=['时间近似 `O(n+m)`（路径压缩），空间 `O(m)`',
                 '易错点：先判长度；不在任何相似对里的单词只和自己相似',
                 '合并必须对==根==操作：`fa[x_fa] = y_fa`，不能改 `fa[x_id]`',
                 '`find` 做了路径压缩，把链上的节点直接挂到根上',
                 '原文本身可在 Python 3 运行，未做修改'],
    ),
)
