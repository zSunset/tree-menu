from django import template

from tree_menu.menu.models import get_all_children

register = template.Library()


def matching_children(menu_items: list, menu_id: int) -> list:
    res = []

    def realign(node: list | dict, parent=None):
        if isinstance(node, dict):
            if node['parent_id'] == menu_id:
                if node not in res:
                    res.append(node)
            else:
                if not parent:
                    for r in res:
                        realign(node, r)
                else:
                    if node['parent_id'] == parent['id']:
                        parent['children'].append(node)
                    else:
                        for child in parent['children']:
                            realign(node, child)

        if isinstance(node, list):
            for item in node:
                realign(item)

    realign(menu_items)

    return res


def get_all_children_data(children):
    return [{'name': child.name, 'url': child.get_url(), 'id': child.id, 'parent_id': child.parent_id, 'children': []}
            for child in children]


def get_activated_menu_ids(menu_items, path):
    res = []
    for i in range(len(menu_items)):
        for item in menu_items:
            if item['url'] == path:
                if not item['parent_id']:
                    return [item['id']]
                elif item['parent_id'] and item['parent_id'] not in res:
                    res.extend([item['id'], item['parent_id']])
            else:
                if item['id'] in res:
                    if item['parent_id'] and item['parent_id'] not in res:
                        res.append(item['parent_id'])

    return res


def extract_menu(items, name):
    for child in items:
        if child['name'] == name:
            items.remove(child)
            return items, child


@register.inclusion_tag('menu/menu.html', takes_context=True)
def draw_menu(context, name: str) -> dict:
    path = context.get('request').path
    menu_children = list(get_all_children(name, include_self=True))
    menu_children_data = get_all_children_data(menu_children)
    activated_menu_ids = get_activated_menu_ids(menu_children_data, path)
    children_data, menu = extract_menu(menu_children_data, name)
    children = matching_children(children_data, menu['id'])
    return {'menu': menu, 'children': children, 'active_menu_ids': activated_menu_ids}
