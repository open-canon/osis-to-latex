import pathlib

from osis_to_latex import serializer
import pyosis.serialization
import fire
import jinja2
import subprocess

CLS_FILE = pathlib.Path(__file__).parent / 'latex_templates' / 'scriptureclass.cls'

def main(input_path: str | pathlib.Path, output_path: str | pathlib.Path) -> None:
    """
    Main function to convert OSIS files to LaTeX format.
    
    Args:
        path (str | pathlib.Path): Path to the OSIS file or directory containing OSIS files.
    """
    input_path = pathlib.Path(input_path)
    output_path = pathlib.Path(output_path)
    if not output_path.exists():
        output_path.mkdir(parents=True, exist_ok=True)
    if output_path.is_file():
        raise ValueError("Output path must be a directory.")

    
    osis_obj = pyosis.serialization.OsisXML.from_xml(input_path.read_text('utf-8'))
    tex = serializer.pyosis_to_latex(osis_obj.osis)

    jinja2_env = jinja2.Environment(
        loader=jinja2.PackageLoader('osis_to_latex', 'latex_templates'),
        autoescape=jinja2.select_autoescape(['html', 'xml'])
    )
    template = jinja2_env.get_template('main.tex.jinja2')
    tex = template.render(document=tex)

    # Copy the cls file to the output directory
    (output_path / 'scriptureclass.cls').write_text(CLS_FILE.read_text())
    scripture_tex_name = "scripture.tex"
    output_file = output_path / scripture_tex_name
    output_file.write_text(tex)
    
    subprocess.run(['latexmk', '-pdf', "-e", "\"$pdflatex='xelatex %O -interaction=nonstopmode %S'\"", scripture_tex_name, "-f"], check=True, cwd=output_path)
    


if __name__ == "__main__":
    fire.Fire(main)