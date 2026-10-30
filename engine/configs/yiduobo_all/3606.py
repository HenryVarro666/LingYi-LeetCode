def _idx(S):
    a = S.get('active_index')
    if a is None:
        return ''
    return f"可用优惠券下标 `active_index` = {a}" + (f"  →  code = {[S['code'][i] for i in a]}" if a else '')


CONFIG = dict(
    num=3606, title='优惠券校验器', difficulty='Easy', category='模拟',
    author='yiduobo', technique='先筛选下标，再按 (类别, code) 排序',
    tags=[],
    code='''
class Solution(object):
    def validateCoupons(self, code, businessLine, isActive):
        
        def check_code(code):
            if not code:
                return False

            for c in code:
                if not (c == '_' or 'a' <= c <= 'z' or 'A' <= c <= 'Z' or '0' <= c <= '9'):
                    return False
            
            return True
        
        business_set = set(['electronics', 'grocery', 'pharmacy', 'restaurant'])
        def check_business(business):
            return business in business_set

        def check_active(is_active):
            return is_active

        active_index = []
        for index in range(len(code)):
            if check_code(code[index]) and check_business(businessLine[index]) and check_active(isActive[index]):
                active_index.append(index)

        active_index.sort(key=lambda d:(businessLine[d], code[d]))
        return [code[index] for index in active_index]
''',
    call='Solution().validateCoupons(["SAVE20","","PHARMA5","SAVE@20","Z9","A_1"], ["restaurant","grocery","pharmacy","restaurant","grocery","grocery"], [True]*6)',
    expect=['A_1', 'Z9', 'PHARMA5', 'SAVE20'],
    skip=['for c in code', 'if not (c ==', 'return business in', 'return is_active'],
    views=[
        dict(type='array', var='code', label='code（蓝 = 当前检查的优惠券）', cell=130, h=190,
             pointers={'index': 'blue'}),
        dict(type='array', var='businessLine', label='businessLine', cell=130, h=190, pointers={'index': 'blue'}),
        dict(type='text', fn=_idx, size=24),
    ],
    watch=['index', ('active_index', 'active_index', 'green')],
    captions={
        'business_set = ': '合法类别放进集合，判断类别是否合法只需 `in`',
        'for index in range': '检查第 `{index}` 张：`code = {code[index]!r}`，`businessLine = {businessLine[index]!r}`',
        'if check_code(code[index])': '依次检查三条规则：code 合法、类别合法、已激活，==三条都过==才算可用',
        'active_index.append': '可用，只记下标：`active_index = {active_index}`',
        'return False': '含非法字符（或为空）→ code 不合法，返回 `False`',
        'return True': 'code 每个字符都是字母、数字或 `_` → 合法，返回 `True`',
        'active_index.sort': '==一次排序==：关键字 `(businessLine, code)`，类别名本身的字典序刚好就是题目要求的类别顺序 → `{active_index}`',
        'return [code': '按排好的下标取出 code → `{ret}`',
    },
    cards=dict(
        one_liner='先一趟筛出可用下标，再按 (类别, code) 一次排序',
        complexity='时间 `O(L log n)`，空间 `O(n)`',
        problem=['给出三个数组 `code`、`businessLine`、`isActive`，筛出==可用优惠券==',
                 '可用：code 非空且只含字母数字下划线；类别是 4 个之一；已激活',
                 '先按类别顺序、再按 code 字典序，返回 code 列表'],
        quote='注意到题目中businessLine的顺序刚好是按照字典序排好的，因此可以直接以businessLine为第一关键字，code为第二关键字，对可用优惠券的下标进行排序。',
        quote_src='—— yiduobo 题解',
        idea=['先一趟遍历，三条规则分别写成 `check_code / check_business / check_active`',
              '可用的优惠券只保存==下标==',
              '`electronics < grocery < pharmacy < restaurant` 正好是字典序，所以直接用 `(businessLine[d], code[d])` 做排序键'],
        summary=['时间 `O(L log n)`，空间 `O(n)`',
                 '易错：空串 code 要单独判 `not code`，否则会被误判为合法',
                 '字典序是按 ASCII 比较：大写字母排在小写之前，数字在字母之前',
                 '关键观察：类别顺序恰好等于字典序，省去了自定义映射'],
    ),
)
