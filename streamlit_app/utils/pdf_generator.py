from xhtml2pdf import pisa

def generate_pdf(report_html: str, output_path: str = "fin_report.pdf") -> str:
    with open(output_path, "w+b") as result_file:
        pisa.CreatePDF(report_html, dest=result_file)
    return output_path