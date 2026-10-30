CONFIG = dict(
    num=1772, title='按受欢迎程度排列功能', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='Trie 匹配 + 计数排序',
    tags=[],
    code='''
class TreeNode(object):

    def __init__(self):
        self.childs = {}
        self.end_id = None

class Solution(object):
    def sortFeatures(self, features, responses):

        root = TreeNode()

        for index, s in enumerate(features):
            now = root
            for char in s:
                if char not in now.childs:
                    node = TreeNode()
                    now.childs[char] = node
                
                now = now.childs[char]
            
            now.end_id = index
        
        cnt = [0] * len(features)
        for r in responses:
            hit_set = set()
            for s in r.split(' '):
                now = root
                flag = True
                for char in s:
                    if char not in now.childs:
                        flag = False
                        break
                    now = now.childs[char]
                
                if flag and now.end_id is not None:
                    hit_set.add(now.end_id)
            
            for id in hit_set:
                cnt[id] += 1

        return [features[x] for x in sorted(range(len(features)), key=lambda d:(-cnt[d], d))]
''',
    call='Solution().sortFeatures(["ab","c","de"], ["ab c","abc de","de c"])',
    expect=['c', 'de', 'ab'],
    max_steps=48,
    skip=['self.childs', 'self.end_id = None', 'node = TreeNode()', 'now = root', 'flag = True'],
    views=[
        dict(type='array', var='features', label='features（下标 = 功能编号）', h=150,
             color=lambda S, i, v: 'green' if 'index' in S and i == S['index'] else None),
        dict(type='text', fn=lambda S: ('当前响应 r = `%s`' % S['r']) if 'r' in S else '', size=26, h=60),
        dict(type='text', fn=lambda S: ('当前单词 s = `%s`　flag = ==%s==' % (S['s'], S['flag'])) if 's' in S and 'flag' in S else '', size=26, h=60),
        dict(type='set', var='hit_set', label='hit_set（本条响应命中的功能编号）', h=130),
        dict(type='array', var='cnt', label='cnt（每个功能出现在几条响应中）', h=170,
             pointers={'id': 'pink'}),
    ],
    watch=['index', 'r', 's', 'flag', 'hit_set', 'cnt'],
    captions={
        'now.end_id = index': '单词结尾打上编号：`end_id = {index}`，说明这里正好是一个完整功能名',
        'cnt = [0]': '`cnt[i]` 记录功能 i 出现在多少条响应里',
        'hit_set = set()': '每条响应一个集合：同一功能在一条响应里重复出现只算一次',
        'for s in r.split': '把响应按空格拆成单词，逐个去 trie 里匹配',
        'if char not in now.childs:\n                        flag': '',
        'flag = False': '这个字符 trie 里没有 → 单词不是任何功能的前缀 → `flag = False`',
        'if flag and now.end_id': lambda S, B, r: ('走完了且 `end_id = %s` 不空 → 单词恰好是功能 %s' % (S['now'].end_id, S['now'].end_id)
                                                  if S['flag'] and S['now'].end_id is not None
                                                  else '要么中途断了，要么只是前缀（`end_id` 为空）→ 不算命中'),
        'hit_set.add': '命中功能 `{now.end_id}`，放进 `hit_set`（集合自动去重）',
        'cnt[id] += 1': '功能 `{id}` 又多一条响应：`cnt = {cnt}`',
        'return': lambda S, B, r: '按 `(-cnt, 编号)` 排序：次数多的在前，相同次数编号小的在前 → `%s`' % (r,),
    },
    cards=dict(
        one_liner='用 trie 判断单词是不是功能名，每条响应用集合去重计数',
        complexity='时间 `O(总字符数)`，空间 `O(功能名总长)`',
        problem=['`features` 是功能名列表，`responses` 是用户回答（单词用空格隔开）',
                 '功能的受欢迎程度 = 出现在多少条回答里（一条回答里重复只算一次）',
                 '按受欢迎程度降序排，相同则按原顺序；示例：功能 `[ab,c,de]` → `[c,de,ab]`'],
        quote='这类字符串匹配的问题可以使用trie树来进行求解。',
        quote_src='—— yiduobo 题解原文',
        idea=['先把所有功能名插入 trie，结尾节点记下功能编号',
              '对每条响应：逐词去 trie 里走，走得通且停在结尾节点才算命中',
              '用 `hit_set` 去重，再累加到总计数 `cnt`，最后按次数降序排序'],
        summary=['时间 `O(总字符数)`，空间 `O(功能名总长)`',
                 '易错：`abc` 只是 `ab` 的延伸，必须看 `end_id` 才不会误判',
                 '易错：同一条回答里重复出现只能算一次，所以先放进集合',
                 '排序键 `(-cnt[d], d)` 保证次数相同时保持原顺序',
                 '原文为 Python 2 写法，Python 3 下可直接运行，代码未改'],
    ),
)
