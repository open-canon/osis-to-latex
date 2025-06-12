import pyosis.generated
import pydantic
from typing import Sequence, TypeVar, Type
T = TypeVar("T")


# Cover page needs its own page
# Title page needs its own page
# Testimonies should share



# Both of these below are caused by https://github.com/tefra/xsdata-pydantic/issues/38
# The small caps are all over the place in the Brief explanation about the Book of Mormon
# footnote text is ending up in the footnotes???


def escape_latex(text: str) -> str:
        """Very minimal LaTeX escaping."""
        return (
            text.replace("\\", r"\textbackslash{}")
                .replace("&", r"\&")
                .replace("%", r"\%")
                .replace("$", r"\$")
                .replace("#", r"\#")
                .replace("_", r"\_")
                .replace("{", r"\{")
                .replace("}", r"\}")
                .replace("~", r"\textasciitilde{}")
                .replace("^", r"\^{}")
        )
def find(contents: Sequence[object | T], type_: Type[T]) -> T | None:
    for content in contents:
        if isinstance(content, type_):
            return content
    return None

def children_content(contents: Sequence[object | pydantic.BaseModel | str]) -> str:
        return "".join(pyosis_to_latex(content) for content in contents)

def pyosis_to_latex(osis_model: object | pydantic.BaseModel | str | None) -> str:
    if osis_model is None:
        return ""
    if isinstance(osis_model, str):
        return escape_latex(osis_model)
    if isinstance(osis_model, pyosis.generated.LbCt):
        return r"\hfill\break "
    if isinstance(osis_model, pyosis.generated.VerseCt):
        return r"\bibleverse{" + children_content(osis_model.content).strip() + "}\n"
    if isinstance(osis_model, pyosis.generated.NoteCt):
        return r"\vfn{" + children_content(osis_model.content).strip() + "} "
    if isinstance(osis_model, pyosis.generated.ReferenceCt):
        # TODO: Properly support cross references if the work is in the same LaTeX document or can be easily linked to.
        return children_content(osis_model.content)
    if isinstance(osis_model, pyosis.generated.HiCt):
        if osis_model.type_value == pyosis.generated.OsisHi.ACROSTIC:
            raise NotImplementedError("Acrostics not currently supported for LaTeX.")
        elif osis_model.type_value == pyosis.generated.OsisHi.BOLD:
            return r"\textbf{" + children_content(osis_model.content) + "}"
        elif osis_model.type_value == pyosis.generated.OsisHi.EMPHASIS:
            return r"\emph{" + children_content(osis_model.content) + "}"
        elif osis_model.type_value == pyosis.generated.OsisHi.ILLUMINATED:
            raise NotImplementedError("Illuminated not supported.")
        elif osis_model.type_value == pyosis.generated.OsisHi.ITALIC:
            return r"\textit{" + children_content(osis_model.content) + "}"
        elif osis_model.type_value == pyosis.generated.OsisHi.LINE_THROUGH:
            raise NotImplementedError("Strike-through is not supported.")
        elif osis_model.type_value == pyosis.generated.OsisHi.NORMAL:
            return r"\textnormal{" + children_content(osis_model.content) + "}"
        elif osis_model.type_value == pyosis.generated.OsisHi.SMALL_CAPS:
            return r"\textsc{" + children_content(osis_model.content).strip() + "}"
        elif osis_model.type_value == pyosis.generated.OsisHi.SUB:
            return r"\textsubscript{" + children_content(osis_model.content) + "}"
        elif osis_model.type_value == pyosis.generated.OsisHi.SUPER:
            return r"\textsuperscript{" + children_content(osis_model.content) + "}"
        elif osis_model.type_value == pyosis.generated.OsisHi.UNDERLINE:
            return r"\underline{" + children_content(osis_model.content) + "}"
        raise NotImplementedError("Non-standard Highlights not supported.")
    if isinstance(osis_model, pyosis.generated.ChapterCt) or isinstance(osis_model, pyosis.generated.DivCt) and osis_model.type_value == pyosis.generated.OsisDivs.CHAPTER:
        return r"\chapter{}" +"\n\n"+ children_content(osis_model.content).strip() + "\n\n"
    if isinstance(osis_model, pyosis.generated.PCt):
        return "\n\n" + children_content(osis_model.content) + "\n\n"
    if isinstance(osis_model, pyosis.generated.DivCt):
        if osis_model.type_value == pyosis.generated.OsisDivs.ACKNOWLEDGEMENT:
            return children_content(osis_model.content) + "\n"
        if osis_model.type_value == pyosis.generated.OsisDivs.AFTERWORD:
            raise NotImplementedError(f"Unsupported div type: {osis_model}")
        if osis_model.type_value == pyosis.generated.OsisDivs.ANNOTANT:
            raise NotImplementedError(f"Unsupported div type: {osis_model}")
        if osis_model.type_value == pyosis.generated.OsisDivs.APPENDIX:
            head = find(osis_model.content, pyosis.generated.HeadCt)
            title = find(osis_model.content, pyosis.generated.TitleCt)
            book_contents = [x for x in osis_model.content if x not in (head, title)]
            if head:
                head_contents = children_content(head.content)
            else:
                raise NotImplementedError("Div Book without Head child is not supported.")
            title_contents = children_content(title.content) if title is not None else ""
            return "\n\n" + r"\section*{" + head_contents + "}" + "\n\n" + title_contents + "\n\n" + children_content(book_contents) + "\n\n"
        
        if osis_model.type_value == pyosis.generated.OsisDivs.ARTICLE:
            raise NotImplementedError(f"Unsupported div type: {osis_model}")
        if osis_model.type_value == pyosis.generated.OsisDivs.BACK:
            return "\n\n" + r"\appendix" + "\n\n" + children_content(osis_model.content) + "\n\n"
        if osis_model.type_value == pyosis.generated.OsisDivs.BIBLIOGRAPHY:
            raise NotImplementedError(f"Unsupported div type: {osis_model}")
        if osis_model.type_value == pyosis.generated.OsisDivs.BODY:
            raise NotImplementedError(f"Unsupported div type: {osis_model}")
        if osis_model.type_value == pyosis.generated.OsisDivs.BOOK:
            head = find(osis_model.content, pyosis.generated.HeadCt)
            title = find(osis_model.content, pyosis.generated.TitleCt)
            book_contents = [x for x in osis_model.content if x not in (head, title)]
            if head:
                head_contents = children_content(head.content).strip()
            else:
                raise NotImplementedError("Div Book without Head child is not supported.")
            first_chapter = find(book_contents, pyosis.generated.ChapterCt)
            if first_chapter is None:
                raise NotImplementedError("Div Book without Verse child is not supported.")

            first_chapter_index = book_contents.index(first_chapter)
            before_chapters = book_contents[:first_chapter_index]
            after_chapters = book_contents[first_chapter_index:]
            
            title_contents = children_content(title.content).strip() if title is not None else None
            header = r"\book{" + head_contents +"}"+"{"+ " ".join(osis_model.osis_id) + "}\n" 
            if title_contents:
                header += r"\booksectiontitle{" + title_contents + "}"
            return (
                header + "\n"
                + children_content(before_chapters) 
                +r"\begin{multicols}{2}" 
                +"\n"
                +children_content(after_chapters)
                + "\n\n" 
                + r"\end{multicols}" 
                + "\n\n")
        if osis_model.type_value == pyosis.generated.OsisDivs.BOOK_GROUP:
            raise NotImplementedError(f"Unsupported div type: {osis_model}")
        if osis_model.type_value == pyosis.generated.OsisDivs.BRIDGE:
            raise NotImplementedError(f"Unsupported div type: {osis_model}")
        if osis_model.type_value == pyosis.generated.OsisDivs.CHAPTER:
            raise NotImplementedError(f"Unsupported div type: {osis_model}")
        if osis_model.type_value == pyosis.generated.OsisDivs.COLOPHON:
            raise NotImplementedError(f"Unsupported div type: {osis_model}")
        if osis_model.type_value == pyosis.generated.OsisDivs.COMMENTARY:
            raise NotImplementedError(f"Unsupported div type: {osis_model}")
        if osis_model.type_value == pyosis.generated.OsisDivs.CONCORDANCE:
            raise NotImplementedError(f"Unsupported div type: {osis_model}")
        if osis_model.type_value == pyosis.generated.OsisDivs.COVER_PAGE:
            head = find(osis_model.content, pyosis.generated.HeadCt)
            title = find(osis_model.content, pyosis.generated.TitleCt)
            head_str = (r"\textbf{" + children_content(head.content).strip() + "}" + "\n") if head else ""
            title_str = (r"\textbf{" + children_content(title.content).strip() + "}" + "\n") if title else ""
            book_contents = [x for x in osis_model.content if x not in (head, title)]
            if head_str != "" or title_str != "":
                header_text = r"\begin{center}" + "\n" + head_str +"\n\n"+ title_str  + "\n" + r"\vspace{1cm}" + "\n" + r"\noindent" + "\n"
            else:
                header_text = ""
            return f"{header_text}\n\n{children_content(book_contents)}" + r"\end{center}"+"\n\n"
        if osis_model.type_value == pyosis.generated.OsisDivs.DEDICATION:
            raise NotImplementedError(f"Unsupported div type: {osis_model}")
        if osis_model.type_value == pyosis.generated.OsisDivs.DEVOTIONAL:
            raise NotImplementedError(f"Unsupported div type: {osis_model}")
        if osis_model.type_value == pyosis.generated.OsisDivs.ENTRY:
            raise NotImplementedError(f"Unsupported div type: {osis_model}")
        if osis_model.type_value == pyosis.generated.OsisDivs.FRONT:
            return  "\n\n" + children_content(osis_model.content) + "\n\n"
        if osis_model.type_value == pyosis.generated.OsisDivs.GAZETTEER:
            raise NotImplementedError(f"Unsupported div type: {osis_model}")
        if osis_model.type_value == pyosis.generated.OsisDivs.GLOSSARY:
            raise NotImplementedError(f"Unsupported div type: {osis_model}")
        if osis_model.type_value == pyosis.generated.OsisDivs.IMPRIMATUR:
            raise NotImplementedError(f"Unsupported div type: {osis_model}")
        if osis_model.type_value == pyosis.generated.OsisDivs.INDEX:
            raise NotImplementedError(f"Unsupported div type: {osis_model}")
        if osis_model.type_value == pyosis.generated.OsisDivs.INTRODUCTION:
            return r"\booksectionsummary{" + children_content(osis_model.content).strip() + "}\n"
        if osis_model.type_value == pyosis.generated.OsisDivs.MAJOR_SECTION:
            raise NotImplementedError(f"Unsupported div type: {osis_model}")
        if osis_model.type_value == pyosis.generated.OsisDivs.MAP:
            raise NotImplementedError(f"Unsupported div type: {osis_model}")
        if osis_model.type_value == pyosis.generated.OsisDivs.OUTLINE:
            raise NotImplementedError(f"Unsupported div type: {osis_model}")
        if osis_model.type_value == pyosis.generated.OsisDivs.PARAGRAPH:
            raise NotImplementedError(f"Unsupported div type: {osis_model}")
        if osis_model.type_value == pyosis.generated.OsisDivs.PART:
            raise NotImplementedError(f"Unsupported div type: {osis_model}")
        if osis_model.type_value == pyosis.generated.OsisDivs.PREFACE:
            head = find(osis_model.content, pyosis.generated.HeadCt)
            title = find(osis_model.content, pyosis.generated.TitleCt)
            book_contents = [x for x in osis_model.content if x not in (head, title)]
            title_str = (r"\begin{center}" + "\n" +
                r"\textbf{" + children_content(title.content).strip() + "}" + "\n" +
                r"\end{center}" + "\n" +
                r"\vspace{1cm}" + "\n" +
                r"\noindent" + "\n" ) if title else ""
            return (
                r"\section*{" + (children_content(head.content).strip() if head else "") + "}" + "\n" +
                title_str +
                children_content(book_contents) + "\n\n"
                
            )
        if osis_model.type_value == pyosis.generated.OsisDivs.PUBLICATION_DATA:
            raise NotImplementedError(f"Unsupported div type: {osis_model}")
        if osis_model.type_value == pyosis.generated.OsisDivs.SECTION:
            raise NotImplementedError(f"Unsupported div type: {osis_model}")
        if osis_model.type_value == pyosis.generated.OsisDivs.SUB_SECTION:
            raise NotImplementedError(f"Unsupported div type: {osis_model}")
        if osis_model.type_value == pyosis.generated.OsisDivs.SUMMARY:
            return r"\chapterheader{" + children_content(osis_model.content).strip() + "}\n"
        if osis_model.type_value == pyosis.generated.OsisDivs.TABLEOF_CONTENTS:
            raise NotImplementedError(f"Unsupported div type: {osis_model}")
        if osis_model.type_value == pyosis.generated.OsisDivs.TITLE_PAGE:
            head = find(osis_model.content, pyosis.generated.HeadCt)
            title = find(osis_model.content, pyosis.generated.TitleCt)
            book_contents = [x for x in osis_model.content if x not in (head, title)]
            head_str = (children_content([x for x in head.content if not isinstance(x, pyosis.generated.LbCt)]).strip()) if head else ""
            title_str = (r"\begin{center}" + "\n" +
                r"\textbf{" + children_content(title.content) + "}" + "\n" +
                r"\end{center}" + "\n" +
                r"\vspace{1cm}" + "\n" +
                r"\noindent" + "\n" ) if title else ""
            return (
                r"\section*{" + head_str + "}" + "\n" +
                title_str +
                children_content(book_contents) + "\n\n"
                
            )

        # CUSTOM DIVS DEFINED IN CHURCH_STUDY_TO_OSIS PACKAGE
        if osis_model.type_value == "x-figure":
            return (
                r"\begin{figure}[ht]"+"\n" + r"\centering" + "\n" 
                + children_content(osis_model.content) 
                + r"\end{figure}"+"\n")
        if osis_model.type_value == "x-publish-info":
            return f"\n\n{children_content(osis_model.content)}\n\n"
        if osis_model.type_value == "x-copyright-info":
            return f"\n\n{children_content(osis_model.content)}\n\n"
        if osis_model.type_value == "x-figcaption":
            return f"\n\n{children_content(osis_model.content)}\n\n"
        raise NotImplementedError(f"Unsupported div: {osis_model}")

    if isinstance(osis_model, pyosis.generated.HeadCt):
        raise NotImplementedError(f"Head outside of div not supported: {osis_model}")

    if isinstance(osis_model, pyosis.generated.SignedCt):
        return r"\medskip" + "\n" + r"\noindent" + "\n\n" + "\n\n".join(pyosis_to_latex(x) for x in osis_model.content)

    if isinstance(osis_model, pyosis.generated.NameCt):
        return children_content(osis_model.content)

    if isinstance(osis_model, pyosis.generated.ListCt):
        return r"\begin{osislist}"+"\n" + children_content(osis_model.content).strip() + "\n" + r"\end{osislist}"+"\n"

    if isinstance(osis_model, pyosis.generated.ItemCt):
        return r"\item {" + children_content(osis_model.content).strip() + "}\n"


    if isinstance(osis_model, pyosis.generated.FigureCt):
        src = osis_model.src
        captions = osis_model.caption
        caption_str = ""
        for caption in captions:
            caption_str += r"\caption{" + children_content(caption.content) + "}\n"
        

        settings = "["
        if osis_model.alt:
            settings += "alt={" + escape_latex(osis_model.alt) + "}"

        settings += "]"
        if settings == "[]":
            settings = ""

        # TODO: Fix graphics from remote sources. Will likely require something custom in the class
        graphics = ""
        # graphics = r"\includegraphics" + settings + "{" + (src or "") + "}\n"

        return (caption_str + graphics)

    if isinstance(osis_model, pyosis.generated.TableCt):
        head = children_content(osis_model.head.content) if osis_model.head else ""
        num_cols = osis_model.cols or len(osis_model.row[0].cell)

        col_headers = "|" + "|".join(["c"] * num_cols) + "|"

        table_str = r"\begin{center}" + "\n" +r"\begin{tabular}{ " + col_headers + " } " + "\n" + r"\hline" + "\n"
        if head:
            table_str += r"\multicolumn{" + str(num_cols) + r"}{c}{" + head + r"} \\" + "\n" + r"\hline" + "\n"

        for i, row in enumerate(osis_model.row):
            cells = [children_content(cell.content).strip() for cell in row.cell]
            table_str += " & ".join(cells) 
            if i != len(osis_model.row)-1:
                table_str+= r" \\" 
            table_str += "\n"
        # table_str += r"\hline" + "\n"

        table_str += r"\end{tabular}" + "\n"
        table_str += r"\end{center}" + "\n"
        return table_str

    if isinstance(osis_model, pyosis.generated.ForeignCt):
        return children_content(osis_model.content)

    if isinstance(osis_model, pyosis.generated.DivineNameCt):
        # TODO: Properly format
        return children_content(osis_model.content)
        
    if isinstance(osis_model, pyosis.generated.OsisTextCt):
        title = osis_model.osis_ref_work
        title_tex = r"\title{" + escape_latex(title) + "}\n"  + "\n\n"
        document_begin = r"\begin{document}" + r"\maketitle"
        document_end = r"\end{document}"


        # Find the first book div to split front and main matters
        i = 0
        for i, content in enumerate(osis_model.div):
            if content.type_value == pyosis.generated.OsisDivs.BOOK:
                break

        front_matters = r"\frontmatter" + "\n\n" + children_content(osis_model.div[:i])
        main_matters = r"\mainmatter" + "\n\n" + children_content(osis_model.div[i:])
        
        return title_tex+document_begin+ front_matters + main_matters + document_end
    if isinstance(osis_model, pyosis.generated.OsisCt):
        return pyosis_to_latex(osis_model.osis_text)
        
        

    raise NotImplementedError(f"Encountered unknown OSIS object that cannot be serialized to LaTeX: {osis_model}")
