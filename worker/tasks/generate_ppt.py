from celery import shared_task
import httpx, os, json
from uuid import UUID
from python_pptx import Presentation
from python_pptx.util import Inches

TEMPLATE_SVC = os.getenv("TEMPLATE_SVC", "<http://template-service:7000>")
EXPORT_SVC = os.getenv("EXPORT_SVC", "<http://export-service:7100/export>")

@shared_task
def generate_ppt(id: str, title: str, outline: str | None = None, template_style: str | None = None):
    """Main orchestration task."""
    # 1) Get outline (call LLM service if not provided)
    if not outline:
        # Fake outline here – integrate OpenAI in real build
        outline = f"1. 封面: {title}\\n2. 内容页: 要点一\\n3. 结束页: 感谢"
    # 2) Fetch template JSON
    tmpl_url = f"{TEMPLATE_SVC}/template/random" if not template_style else f"{TEMPLATE_SVC}/template/{template_style}"
    tmpl_json = httpx.get(tmpl_url, timeout=10).json()
    # 3) Build pptx in‑memory
    prs = Presentation()
    title_slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(title_slide_layout)
    slide.shapes.title.text = title
    slide.placeholders[1].text = "作者: AI"
    # TODO: iterate outline & tmpl_json to add slides...
    # 4) Save and POST to export‑service for storage & URL
    path = f"/tmp/{id}.pptx"
    prs.save(path)
    with open(path, "rb") as f:
        file_url = httpx.post(EXPORT_SVC, files={"file": (f"{id}.pptx", f, "application/vnd.openxmlformats-officedocument.presentationml.presentation")}, timeout=60).json()["url"]
    return {"id": id, "file_url": file_url}
