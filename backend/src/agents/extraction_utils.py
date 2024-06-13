from setup import project_root
import os
import io

from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph
from docx.document import Document as _Document

from .openai_utils import openai_prompt

def _iter_block_items(parent):
    """
    Yield each paragraph and table child within *parent*, in document order.
    Each returned value is an instance of either Table or Paragraph.
    """
    if isinstance(parent, _Document):
        parent_elm = parent.element.body
    else:
        parent_elm = parent._element
    for child in parent_elm.iterchildren():
        if child.tag.endswith('p'):
            yield Paragraph(child, parent)
        elif child.tag.endswith('tbl'):
            yield Table(child, parent)


def _extract_and_clean_text(docx_bytes):
    # Load the DOCX document from bytes
    doc = Document(io.BytesIO(docx_bytes))


    def iter_unique_cells(row):
        """Generate cells in `row` skipping empty grid cells."""
        prior_tc = None
        for cell in row.cells:
            this_tc = cell._tc
            if this_tc is prior_tc:
                continue
            prior_tc = this_tc
            yield cell


    # Function to extract text from tables
    def extract_text_from_table(table):
        table_text = []
        for row in table.rows:
            for cell in iter_unique_cells(row):
                cell_text = cell.text
                table_text.append(cell_text)
        return ' '.join(table_text)

    # Extract all text from the document
    full_text = []

    for block in _iter_block_items(doc):
        if isinstance(block, Paragraph):
            full_text.append(block.text)
        elif isinstance(block, Table):
            full_text.append(extract_text_from_table(block))

    full_text = ' '.join(full_text)
    # Remove extraneous white spaces
    cleaned_text = ' '.join(full_text.split())

    return cleaned_text

docx_path = os.path.join(project_root, './assets/prt.docx')
extracted_text_cache_path = os.path.join(project_root, './assets/prt_clean.txt')

def extract_prt_summary():
    """
    Extracts the key information from a Pension Risk Transfer Document (PRT)
    or specifically the pension benefits scheme component of a PRT. 
    """
    # TEMP: first check if cached result exists
    if os.path.exists(extracted_text_cache_path):
        with open(extracted_text_cache_path, 'r') as file:
            return file.read()

    with open(docx_path, 'rb') as file:
        docx_bytes = file.read()
    cleaned_text = _extract_and_clean_text(docx_bytes)

    prompt_path = os.path.join(project_root, './src/prompts/extraction.txt')
    with open(prompt_path, 'r') as file:
        prompt = file.read()

    extracted_text = openai_prompt(prompt + cleaned_text)

    # TEMP: cache contents to file
    with open(extracted_text_cache_path, 'w') as file:
        file.write(extracted_text)
    return extracted_text
