CONFIG = dict(
    num=734, title='句子相似性', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='哈希表存相似词对',
    code='''
class Solution(object):
    def areSentencesSimilar(self, sentence1, sentence2, similarPairs):

        if len(sentence1) != len(sentence2):
            return False

        words_mapping = {}
        similar_set = set()
        id = 0
        for x, y in similarPairs:
            if x not in words_mapping:
                words_mapping[x] = id
                id += 1
            if y not in words_mapping:
                words_mapping[y] = id
                id += 1

            x_id, y_id = words_mapping[x], words_mapping[y]
            if x_id > y_id:
                x_id, y_id = y_id, x_id
            similar_set.add((x_id, y_id))

        for x, y in zip(sentence1, sentence2):
            if x == y:
                continue
            
            x_id, y_id = words_mapping.get(x, -1), words_mapping.get(y, -1)
            if x_id > y_id:
                x_id, y_id = y_id, x_id
            if (x_id, y_id) not in similar_set:
                return False
        
        return True
''',
    call='Solution().areSentencesSimilar(["great","acting","skills"], ["fine","drama","talent"], [["great","fine"],["drama","acting"],["skills","talent"]])',
    expect=True,
    views=[
        dict(type='array', var='sentence1', label='sentence1', cell=130, h=140,
             color=lambda S, i, v: 'blue' if S['_line'] >= 23 and v == S.get('x') else None),
        dict(type='array', var='sentence2', label='sentence2', cell=130, h=140,
             color=lambda S, i, v: 'pink' if S['_line'] >= 23 and v == S.get('y') else None),
        dict(type='map', var='words_mapping', label='words_mapping（单词 → id）', fmt=lambda k, v: f"'{k}': {v}", h=150, font=26),
        dict(type='set', var='similar_set', label='similar_set（id 对，小的在前）', fmt=lambda x: f'{x[0]}-{x[1]}', h=110),
    ],
    watch=['x', 'y', 'x_id', 'y_id', 'id'],
    captions={
        'len(sentence1) != len(sentence2)': '两句话长度 `{len(sentence1)}` 和 `{len(sentence2)}`：{"不同 → 不可能相似" if len(sentence1) != len(sentence2) else "相同，才有必要逐词比较"}',
        'words_mapping = {}': '`words_mapping`：给每个单词编一个数字 id，后面比较数字比比较字符串快',
        'similar_set = set()': '`similar_set` 存相似词对的 id；一对只存一次，所以要保证有序',
        'id = 0': '`id` 是下一个要分配的编号，从 0 开始',
        'for x, y in similarPairs': '取出一对相似词 `{x}` 和 `{y}`',
        'if x not in words_mapping': '`{x}` 还没有编号？{"是，分配新 id" if x not in B.words_mapping else "已经有了"}',
        'if y not in words_mapping': '`{y}` 还没有编号？{"是，分配新 id" if y not in B.words_mapping else "已经有了"}',
        'words_mapping[x] = id': '`{x}` 的编号是 `{id}`，记入 `words_mapping`',
        'id += 1': '下一个编号 `id` = {id}',
        'words_mapping[y] = id': '`{y}` 的编号是 `{id}`，记入 `words_mapping`',
        'x_id, y_id = words_mapping[x], words_mapping[y]': '查出两个 id：`{x_id}` 和 `{y_id}`',
        'if x_id > y_id': '`{x_id} > {y_id}`？{"成立，交换让小的在前（相似是对称的，只存一份）" if x_id > y_id else "已经是小的在前，不用换"}',
        'x_id, y_id = y_id, x_id': '交换后 `({x_id}, {y_id})`',
        'similar_set.add': '把 `({x_id}, {y_id})` 加入 `similar_set`',
        'for x, y in zip(sentence1, sentence2)': '比较对应位置的两个词：`{x}` 和 `{y}`',
        'if x == y': '`{x}` 和 `{y}` {"相同 → 天然相似，跳过" if x == y else "不同 → 要查它们是不是相似词对"}',
        'continue': '相同的词直接通过，看下一对',
        'words_mapping.get(x, -1)': '查 id：`{x}` → `{x_id}`，`{y}` → `{y_id}`（没出现过的记 -1）',
        'if (x_id, y_id) not in similar_set': '`({x_id}, {y_id})` {"不在" if (x_id, y_id) not in similar_set else "在"} `similar_set` 里 → {"这一对不相似" if (x_id, y_id) not in similar_set else "相似，继续"}',
        'return False': '有一对既不相同也不相似 → 返回 `False`',
        'return True': '所有对应词都相同或相似 → 返回 `True`',
    },
    cards=dict(
        one_liner='相似词对存进哈希表，逐位置查表判断',
        complexity='时间 `O(n + p)`（n 为句长，p 为词对数），空间 `O(p)`',
        problem=['两个句子 `sentence1`、`sentence2` 和一组相似词对 `similarPairs`',
                 '每个位置的两个词要么相同，要么是相似词对，且长度必须一致，则两句话相似',
                 '示例：`great acting skills` 与 `fine drama talent` → `True`',
                 '相似关系不传递，但是对称的'],
        quote='若x和y相似，那么y也和x相似，需要分别储存。如果想只储存一组，那么就需要保证x和y的有序性。',
        quote_src='—— yiduobo 题解原文',
        idea=['先把词对存进哈希表，之后就能 `O(1)` 判断两个词相不相似',
              '对称关系只存一份：用 id 把小的放前面',
              '先给单词编 id，用数字而不是字符串做比较，效率更高',
              '遍历两句话：相同的跳过，不同的就查表'],
        summary=['时间 `O(n + p)`，空间 `O(p)`',
                 '易错点：先判长度；相似关系==不传递==，只看直接给出的词对',
                 '没出现过的词 id 记 `-1`，`(-1, id)` 不会在集合里，所以自然返回 False',
                 '原文为 Python 2 风格，在 Python 3 下无需修改即可运行'],
    ),
)
