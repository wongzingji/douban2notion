from typing import Callable

def upload_elem(
    notion: Callable, 
    elem, 
    paragraph: str, 
    page_id: str
):
    """
    Upload element from the source website to Norion according to its category

    Args:
        n: the Notion object
        elem: the HTML element from the source page
        paragraph: the previously concatenated string
        page_id: the page ID in Notion
    """
    try:
        class_ = elem['class'][0]
    except:
        class_ = None

    try:
        style = elem['style']
    except Exception:
        style = None

    if isinstance(elem, str):
        # concat the text
        if paragraph:
            paragraph += '\n' + elem.strip()
        else:
            paragraph += elem.strip()
        return paragraph
    else:
        # if the next element is not string, upload the previously concatenated text first
        if paragraph:
            notion.add_paragraph(page_id, paragraph)

        # CASE WHEN
        # heading
        if elem.name != 'hr' and elem.name[0] == 'h':
            type = 'heading_'+'3' if int(elem.name[1:]) > 3 else 'heading_'+elem.name[1:]  
                                                            # only h1, h2, h3 are available in Notion
            notion.add_text(page_id, type, elem.text)

        # divider
        elif elem.name == 'hr':
            type = 'divider'
            notion.add_simple_block(page_id, type)

        # image
        elif class_ and class_ == 'image-wrapper':
            img_url = elem.img['src']
            notion.add_image(page_id, img_url)

        # image_caption
        elif class_ and class_ == 'image-caption-wrapper':
            type = 'paragraph'
            notion.add_text(page_id, type, elem.text)

        # link
        elif elem.name == 'a':
            notion.add_link(page_id, elem.text, elem['href'])

        # bulleted list
        elif elem.name == 'li':
            type = 'bulleted_list_item'
            notion.add_text(page_id, type, elem.text)

        elif elem.name == 'blockquote':
            type = 'quote'
            notion.add_text(page_id, type, elem.text)

        # mark -- background color
        elif elem.name == 'mark':
            annotations = {'color': 'orange_background'}
            notion.add_text(page_id, 'paragraph', elem.text, annotations)

        # span -- bold
        elif elem.name == 'span':
            if elem.contents[0].name == 'mark':
                annotations = {'color': 'orange_background'}
                notion.add_text(page_id, 'paragraph', elem.text, annotations)
            elif style == 'font-weight: bold;':
                annotations = {'bold': True}
                notion.add_text(page_id, 'paragraph', elem.text, annotations)
            else:
                notion.add_text(page_id, 'paragraph', elem.text)

        return ''


def upload_block(
    notion: Callable,
    block_elem, 
    paragraph: str, 
    page_id: str):
    """
    Upload all elements in a block from the source website to Norion
    """
    elems = block_elem.contents
    if len(elems) != 0:
        for elem in elems:
            paragraph = upload_elem(notion, elem, paragraph, page_id)
    return paragraph