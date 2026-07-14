# Render QA

Render every DOCX/PDF page and PPTX slide. Run deterministic checks first, then inspect every image at full size.

Reject clipped or overlapping text, missing glyphs, broken tables, weak contrast, unreadable print size, inconsistent headers/footers, answer leakage, sparse orphan pages, and response areas that do not match the item demand. A page under 25% occupied area fails unless its manifest marks an intentional sparse role. Contact sheets help compare rhythm but never replace page-by-page inspection.

After repairs, rerender and reopen the final file. For delivery, extract the exact ZIP and repeat OOXML opening and render checks from the extracted files.
