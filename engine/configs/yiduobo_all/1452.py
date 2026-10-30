CONFIG = dict(
    num=1452, title='收藏清单', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='公司映射成数字 · 从长到短判子集', tags=[],
    code='''
class Solution(object):
    def peopleIndexes(self, favoriteCompanies):

        mapping_dict = {}
        fav_list = []
        company_cnt = 0
        for fav in favoriteCompanies:
            fav_list.append([])
            for company in fav:
                if company not in mapping_dict:
                    mapping_dict[company] = company_cnt
                    company_cnt += 1
                fav_list[-1].append(mapping_dict[company])
        
            fav_list[-1] = sorted(fav_list[-1])

        res = []
        n = len(fav_list)
        for index in sorted(range(n), key=lambda d:len(fav_list[d]), reverse = True):
            flag = True
            for c in res:
                if self.check(fav_list[index], fav_list[c]):
                    flag = False
                    break
            if flag:
                res.append(index)
        
        return sorted(res)

    def check(self, list1, list2):
        p = 0
        for num in list1:
            while p < len(list2) and list2[p] != num:
                p += 1
            if p == len(list2):
                return False
        
        return True
''',
    call='Solution().peopleIndexes([["a","b"],["b"],["b","c"]])',
    expect=[0, 2],
    max_steps=90,
    skip=["fav_list.append([])", "fav_list[-1].append", "company_cnt += 1", "if company not in", "for company in fav"],
    views=[
        dict(type='map', var='mapping_dict', h=170, fmt=lambda k, v: f'{k} → {v}'),
        dict(type='array', var='fav_list', label='fav_list（每人的公司编号，已排序）', h=190, cell=170),
        dict(type='array', var='res', label='res（已确定不是别人子集的人）', h=170),
        dict(type='text', fn=lambda S: (f"正在判断第 `{S['index']}` 个人 `{S['fav_list'][S['index']]}` 是不是 res 中某人的子集" if 'index' in S and 'fav_list' in S else ''), size=28),
    ],
    watch=[('index', 'index', 'blue'), 'c', 'flag', 'p', 'num'],
    captions={
        'mapping_dict[company] = company_cnt': '新公司 `{company}` 分配编号 `{mapping_dict[company]}`：以后比较的是整数，不用比字符串',
        'fav_list[-1] = sorted': '这个人的编号排好序：`{fav_list[-1]}`，后面可以用双指针判子集',
        'for index in sorted': lambda S, B, r: ('每个人都处理完了，循环结束' if B.get('index') == S.index and 'flag' in B else f'==按清单长度从长到短==处理：长的不可能是短的子集，所以只需和 `res` 里已选的比 → 第 `{S.index}` 个人'),
        'flag = True': '先假设这个人不是任何人的子集',
        'for c in res': '逐个和已入选的 `res = {res}` 比较（`res` 为空就直接入选）',
        'if self.check(': '调用 `check`：`{fav_list[index]}` 是不是 `{fav_list[c]}` 的子集？',
        'flag = False': '是别人的子集，标记 `flag = False`',
        'res.append(index)': '没有被任何人包含 → 加入答案：`res = {res}`',
        'return sorted(res)': '题目要求下标升序：`{ret}`',
        'p = 0': '`p` 是在 `list2` 里的扫描位置',
        'while p < len': lambda S, B, r: (f'`list2[{S.p}] = {S.list2[S.p]}`，和要找的 `{S.num}` 不等 → 往后挪' if S.p < len(S.list2) and S.list2[S.p] != S.num else (f'`list2[{S.p}] = {S.num}`，找到了' if S.p < len(S.list2) else 'p 走到末尾，没找到')),
        'p += 1': '`p` → {p}',
        'if p == len(list2)': lambda S, B, r: ('`p` 走到了末尾：`{}` 不在 list2 里 → ==不是子集=='.format(S.num) if S.p == len(S.list2) else '`{}` 找到了，继续找下一个'.format(S.num)),
        'return False': '有元素找不到 → `False`',
        'return True': '每个元素都按顺序找到了 → list1 是子集，`True`',
    },
    cards=dict(
        one_liner='把公司映射成数字，从长到短，只和已入选的清单比子集',
        complexity='时间约 `O(n²·m)`，空间 `O(nm)`',
        problem=['LeetCode 1452：`favoriteCompanies[i]` 是第 `i` 个人收藏的公司清单',
                 '返回清单==不是任何其他人清单的子集==的人的下标，升序',
                 '本视频：`[[a,b],[b],[b,c]]` → `[0, 2]`'],
        quote='可以首先将清单中的所有字符串都收集起来，并建立起字符串到自然数的映射，然后判断自然数相等即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['公司名映射成整数，每人的清单排序后变成有序整数列表',
              '按清单长度从长到短处理：能包含你的人一定不比你短',
              '`check` 用双指针在长清单里顺序找每个元素，判断子集'],
        summary=['时间约 `O(n²·m)`，`n` 人、清单长 `m`',
                 '先排序再判子集，`check` 才能用单个指针一趟扫完',
                 '只和 `res` 比：被淘汰者的超集也在 `res` 里，不会漏判',
                 '原文称用 KMP；代码里的 `check` 实际是子序列双指针，因为清单已排序，二者等价',
                 '原文已是 Python 3 可运行写法，无需改动'],
    ),
)
