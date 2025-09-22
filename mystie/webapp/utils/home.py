from webapp.models import Navigation

def get_navigation():
    all_items = Navigation.objects.all().order_by("order")
    nav_dict = {}

    # 先把所有項目放到字典
    for item in all_items:
        nav_dict[item.id] = {"obj": item, "children": []}

    # 分配 parent / child
    roots = []
    for item in all_items:
        if item.parent_id == 0:
            roots.append(nav_dict[item.id])
        else:
            nav_dict[item.parent_id]["children"].append(nav_dict[item.id])

    return roots