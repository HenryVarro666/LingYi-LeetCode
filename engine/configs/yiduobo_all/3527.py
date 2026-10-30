R = [["good", "ok", "good", "ok"], ["ok", "bad", "good", "ok", "ok"], ["good"], ["bad"]]
CONFIG = dict(
    num=3527, title='找到最常见的回答', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='集合去重 + 字典统计 + 择优遍历',
    tags=[],
    code='''
class Solution(object):
    def findCommonResponse(self, responses):
        
        cnt = {}
        for resp in responses:
            resp_set = set(resp)
            for s in resp_set:
                cnt[s] = cnt.get(s, 0) + 1
        
        res = None
        for s in cnt:
            if res is None or cnt[s] > cnt[res] or (cnt[s] == cnt[res] and s < res):
                res = s
        return res
''',
    call='Solution().findCommonResponse(%r)' % (R,),
    expect='good',
    views=[
        dict(type='array', var='resp', h=190, label='当天的 resp', cell=110),
        dict(type='set', var='resp_set', h=150, fmt=lambda x: str(x)),
        dict(type='map', var='cnt', h=300, fmt=lambda k, v: f'{k}: {v}'),
        dict(type='text', size=30, fn=lambda S: f"当前最优 `res` = =={S['res']}=={'，正在看 `' + str(S['s']) + '`' if 's' in S and S.get('res', 0) != 0 and S['s'] in S['cnt'] else ''}" if 'res' in S and S['res'] is not None else ''),
    ],
    watch=['res', 's'],
    captions={
        'cnt = {}': '`cnt` 统计每个回答出现在多少天里',
        'resp_set = set': '这一天的回答去重：`{sorted(resp_set)}`',
        'cnt[s] = cnt.get': '`cnt[{s}]` 加 1 → =={cnt[s]}==（当天只算一次）',
        'res = None': '`res` 保存当前最常见的回答，先为 `None`',
        'if res is None': lambda S, B, r: (f'`res` 为空，`{S.s}` 先当候选' if S.res is None or B.get('res', 0) is None else
                                           f'`{S.s}`：{S.cnt[S.s]} 次，对比 `res={S.res}` 的 {S.cnt[S.res]} 次；次数更多，或次数相同且字典序更小才替换'),
        'res = s': '更新 `res` = =={res}==（{cnt[res]} 次）',
        'return res': '次数最多、同次数里字典序最小的是 =={ret}==',
    },
    cards=dict(
        one_liner='先去重统计出现天数，再挑次数最多、字典序最小的',
        complexity='时间 `O(L)`，空间 `O(L)`',
        problem=['每天的回答先去重，再统计所有天里谁出现得最多',
                 '次数相同，取字典序最小的',
                 '本视频：`[[good,ok,good,ok],[ok,bad,good,ok,ok],[good],[bad]]` → `good`'],
        quote='先使用集合去重，然后使用哈希表统计每天去重后的回答出现的次数。遍历完成后，再遍历哈希表中的所有回答，取其中出现次数最多且字典序最小的那个即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['第一遍：每天 `set(resp)` 去重，把回答的次数累加进 `cnt`',
              '第二遍：遍历 `cnt`，`res` 保存当前最优',
              '次数更多就换；次数相同且 `s < res` 也换'],
        summary=['时间 `O(L)`，空间 `O(L)`',
                 '易错：忘记先去重，同一天重复回答会被多数',
                 '判断顺序：`res is None` 要放最前，否则 `cnt[res]` 会报错',
                 '原文为 Python 2 风格，仅有类型说明注释，代码无需修改'],
    ),
)
