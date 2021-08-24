# native packs
from typing import List
import random
# installed packs
from IPython.core.display import HTML
# my packs
from skillNer.visualizer.phrase_class import Phrase
from skillNer.general_params import SKILL_TO_COLOR_TAILWIND


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
        return "&nbsp" + phrase.raw_text + "&nbsp"

    # case of skill
    # give an id to identiify element
    id_element = f"{phrase.skill_id}_{random.randint(0, 1000)}"

    # script to show hide meta data
    src = """
        function mouseEnterHandler_%s() {
            document.getElementById("%s").style.display = "";
        }

        function mouseLeaveHandler_%s() {
            document.getElementById("%s").style.display = "none";
        }
    """ % (id_element, id_element, id_element, id_element)

    # props of the div
    on_mouse_enter = f"mouseEnterHandler_{id_element}()"
    on_mouse_leave = f"mouseLeaveHandler_{id_element}()"

    # component for meta data
    def meta_data_component(key, value): return element(ele_type="div", className="flex grid-cols-2 gap-2 mb-4", children=[
        element(ele_type="span",
                className="font-bold col-1", children=[key]),
        element(ele_type="span", className="col-1", children=[str(value)])
    ])

    # color of element
    color = SKILL_TO_COLOR_TAILWIND[phrase.skill_type]

    return element(ele_type="span", onmouseleave=on_mouse_leave, onmouseenter=on_mouse_enter, className=f"relative p-1 text-white rounded-md border bg-{color}", children=[
        # phrase
        phrase.raw_text,

        # type skill
        element(ele_type="span", className='text-xs text-white font-bold', children=[
            " (", phrase.skill_type, ")"
        ]),

        # meta data
        element(ele_type="div", id=id_element,
                style="display: none;",
                className='absolute shadow-lg z-40 bg-white flex-col text-sm text-black p-2 border left-0 -bottom-15',
                children=[
                    meta_data_component(key, val)
                          for key, val in phrase.get_meta_data().items()
                ]),

        element(ele_type="script", children=[src])
    ])


def DOM(children: List[str] = []):

    content = f"""
        <head>
            <link
                id="external-css"
                rel="stylesheet"
                type="text/css"
                href="https://unpkg.com/tailwindcss@^2/dist/tailwind.min.css"
                media="all"
            />
        </head>

        <body>
            <div id="root" class="px-4 leading-10 mb-24">
                {" ".join(children)}
            </div>
        </body>
    """
    return HTML(content)
