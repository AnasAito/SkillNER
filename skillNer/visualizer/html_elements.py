# native packs
from typing import List
import random
# installed packs
from IPython.core.display import HTML
# my packs
from skillNer.visualizer.phrase_class import Phrase


def element(
    ele_type: str = "div",
    className: str = "",
    children: List = [],
    **kwargs
) -> str:

    # addition props
    other_props = ""
    for key, val in kwargs.items():
        other_props += f"{key}='{val}'"

    # content of the element
    content = f"""
        <{ele_type} class='{className}' {other_props}>
            {" ".join(children)}
        </{ele_type}>
    """

    return content


def render_phrase(phrase: Phrase) -> str:
    # case of non skill phrase
    if not phrase.is_skill:
        return element(ele_type='div', className="relative", children=[
            element(ele_type='span', className="flex items p-2 rounded-lg mx-2", children=[
                phrase.raw_text
            ])
        ])

    # case of skill
    # give an id to identiify element
    id_element = f"{phrase.skill_id}_{random.randint(0, 1000)}"

    # script to show hide meta data
    src = """
        function mouseEnterHandler_%s() {
            document.getElementById("%s").style.visibility = "visible";
        }

        function mouseLeaveHandler_%s() {
            document.getElementById("%s").style.visibility = "hidden";
        }
    """ % (id_element, id_element, id_element, id_element)

    # props of the div
    on_mouse_enter = f"mouseEnterHandler_{id_element}()"
    on_mouse_leave = f"mouseLeaveHandler_{id_element}()"

    # component for meta data
    def meta_data_component(key, value): return element(ele_type="div", className="flex grid grid-cols-2 gap-4 my-1", children=[
        element(ele_type="span",
                className="text-sm font-semibold", children=[key]),
        element(ele_type="span", className="text-sm", children=[str(value)])
    ])

    return element(ele_type="span", className="relative", children=[
        # phrase
        element(ele_type="div", className='flex items border p-2 px-6 pb-6 rounded-lg mx-2 cursor-pointer', onmouseleave=on_mouse_leave, onmouseenter=on_mouse_enter, children=[
            phrase.raw_text
        ]),

        # type skill
        element(ele_type="div", className='absolute right-4 bottom-1 text-xs font-bold', children=[
            phrase.skill_type
        ]),

        # meta data
        element(ele_type="div", id=id_element,
                className='flex flex-col w-64 left-2 -bottom-17 invisible absolute bg-white opacity-90 text-black border p-2 rounded-lg z-40',
                children=[
                    meta_data_component(key, val)
                          for key, val in phrase.get_meta_data().items()
                ]),

        element(ele_type="script", children=[src])
    ])
