"""Gera um arquivo data.yaml simples para YOLOv5/YOLOv8."""

from pathlib import Path

# Raiz do Capítulo 1 (pasta que contém assets/)
_CAP = Path(__file__).resolve().parent.parent
ROOT = _CAP / "assets" / "dataset_yolo_farmtech"

CLASSES = ["objeto_a", "objeto_b"]

conteudo = f"""train: {ROOT / 'train' / 'images'}
val: {ROOT / 'valid' / 'images'}
test: {ROOT / 'test' / 'images'}

nc: {len(CLASSES)}
names: {CLASSES}
"""

out = Path("data.yaml")
out.write_text(conteudo, encoding="utf-8")
print(f"Arquivo criado: {out.resolve()}")
print("Conteudo do data.yaml:")
print(conteudo)
