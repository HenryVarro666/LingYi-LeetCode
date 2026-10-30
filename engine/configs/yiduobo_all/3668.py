CONFIG = dict(
    num=3668, title='重排完成顺序', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='遍历 order + 集合判断',
    tags=[],
    code='''
class Solution(object):
    def recoverOrder(self, order, friends):
        
        friends_set = set(friends)
        res = []
        for v in order:
            if v in friends_set:
                res.append(v)
        return res
''',
    call='Solution().recoverOrder([1, 4, 5, 3, 2, 7, 6], [2, 5, 6])',
    expect=[5, 2, 6],
    views=[
        dict(type='array', var='order', label='order（黄 = 当前 v，绿 = 已收进 res 的朋友）', cell=90, h=170,
             color=lambda S, i, v: ('yellow' if S.get('v') == v else ('green' if v in S.get('res', []) else None)) if 'friends_set' in S else None),
        dict(type='set', var='friends_set', label='friends_set', fmt=lambda x: str(x), h=140, font=34),
        dict(type='array', var='res', label='res（按完成顺序）', cell=90, h=150),
    ],
    watch=['v', ('res', 'res', 'green')],
    captions={
        'friends_set = set': '把 `friends` 变成集合，查询朋友身份是 `O(1)`',
        'res = []': '`res` 准备按完成顺序收集朋友',
        'for v in order': lambda S, B, r: ('`order` 走完了，没有下一位选手' if 'v' in B and B.v == S.v == S.order[-1]
                                           else f'按完成顺序看下一位选手 `v = {S.v}`'),
        'if v in friends_set': lambda S, B, r: (f'`{S.v}` 在 friends_set 中 → ==是朋友，收进 res==' if S.v in S.friends_set
                                                  else f'`{S.v}` 不在 friends_set 中 → 不是朋友，跳过'),
        'res.append(v)': '朋友 `{v}` 加入答案：`res` = {res}',
        'return res': '`order` 走完，朋友按完成顺序排好：`{ret}`',
    },
    cards=dict(
        one_liner='与其给 friends 排序，不如顺着 order 把朋友挑出来',
        complexity='时间 `O(n)`，空间 `O(m)`',
        problem=['`order` 是 1 到 n 的排列，表示选手完成比赛的先后',
                 '`friends` 是朋友们的 ID，严格递增，且都在 `order` 中',
                 '返回朋友们 ==按完成顺序== 排好的 ID。本视频：`order=[1,4,5,3,2,7,6]`，`friends=[2,5,6]` → `[5,2,6]`'],
        quote='另一种处理方法则是反过来，直接遍历order数组，若当前遍历到的id出现在friends中，则将这个id加入到答案数组中。',
        quote_src='—— yiduobo 题解原文',
        idea=['题目本质：把 `friends` 按它们在 `order` 里的位置排序',
              '正面做：先建 id → 名次的映射，再排序，要 `O(m log m)`',
              '反过来做：遍历 `order`，在集合里的就收下，一趟就是有序的'],
        summary=['时间 `O(n)`，空间 `O(m)`',
                 '先把 `friends` 转成集合，查询才是 `O(1)`',
                 '`friends` 本身的递增顺序对本解法没用',
                 '原文已是 Python 3 可运行的写法，未做修改'],
    ),
)
