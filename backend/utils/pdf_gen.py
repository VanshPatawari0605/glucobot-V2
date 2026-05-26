import io
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch


def generate_report_pdf(inputs: dict, prob: float, label: str) -> io.BytesIO:
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                            rightMargin=50, leftMargin=50,
                            topMargin=60, bottomMargin=50)

    rc = {
        "LOW RISK":      ("#166534", "#f0fdf4", "#4ade80"),
        "MODERATE RISK": ("#854d0e", "#fefce8", "#facc15"),
        "HIGH RISK":     ("#991b1b", "#fef2f2", "#f87171"),
    }
    dark, light, accent = rc[label]

    def ps(name, **kw): return ParagraphStyle(name, **kw)
    story = []

    # ── Title ────────────────────────────────────────────────────────────────
    story.append(Paragraph("GlucoBot Health Report",
        ps("t", fontSize=26, fontName="Helvetica-Bold",
           textColor=colors.HexColor("#1d4ed8"))))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        f"Generated: {datetime.now().strftime('%B %d, %Y  —  %I:%M %p')}",
        ps("d", fontSize=10, textColor=colors.HexColor("#94a3b8"))))
    story.append(Spacer(1, 12))
    story.append(Table([[""]], colWidths=[495], rowHeights=[2],
        style=TableStyle([("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#1d4ed8"))])))
    story.append(Spacer(1, 16))

    # ── Risk Banner ──────────────────────────────────────────────────────────
    story.append(Table(
        [[Paragraph(f"Diabetes Risk: {label}",
            ps("rl", fontSize=15, fontName="Helvetica-Bold",
               textColor=colors.HexColor(dark))),
          Paragraph(f"{prob*100:.1f}%",
            ps("rp", fontSize=30, fontName="Helvetica-Bold",
               textColor=colors.HexColor(dark), alignment=2))]],
        colWidths=[350, 145],
        style=TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), colors.HexColor(light)),
            ("PADDING",    (0,0), (-1,-1), 14),
            ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
        ])))
    story.append(Spacer(1, 20))

    # ── Donut Chart ──────────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(4, 4), facecolor="white")
    ax.pie([prob, 1-prob], colors=[accent, "#e5e7eb"], startangle=90,
           wedgeprops=dict(width=0.28, edgecolor="white", linewidth=2))
    ax.text(0,  0.08, f"{prob*100:.1f}%", ha="center", va="center",
            fontsize=28, fontweight="bold", color=accent)
    ax.text(0, -0.22, label, ha="center", va="center", fontsize=9, color=dark)
    ax.axis("off")
    plt.tight_layout(pad=0.3)
    cb = io.BytesIO()
    fig.savefig(cb, format="png", dpi=150, bbox_inches="tight", facecolor="white")
    cb.seek(0)
    plt.close(fig)
    story.append(Table([[RLImage(cb, width=2.8*inch, height=2.8*inch)]],
        colWidths=[495],
        style=TableStyle([("ALIGN", (0,0), (-1,-1), "CENTER")])))
    story.append(Spacer(1, 20))

    # ── Input Table ──────────────────────────────────────────────────────────
    story.append(Paragraph("Patient Input Summary",
        ps("h", fontSize=13, fontName="Helvetica-Bold",
           textColor=colors.HexColor("#1e293b"))))
    story.append(Spacer(1, 10))
    rows = [
        ["Parameter",               "Your Value",                              "Normal Range"],
        ["Glucose (mg/dL)",         str(inputs.get("glucose",         "—")),   "70 – 99"],
        ["Blood Pressure (mm Hg)",  str(inputs.get("blood_pressure",  "—")),   "60 – 80"],
        ["BMI (kg/m2)",             str(inputs.get("bmi",             "—")),   "18.5 – 24.9"],
        ["Insulin (uU/mL)",         str(inputs.get("insulin",         "—")),   "16 – 166"],
        ["Age (years)",             str(inputs.get("age",             "—")),   "—"],
        ["Pregnancies",             str(inputs.get("pregnancies",     "—")),   "—"],
        ["Skin Thickness (mm)",     str(inputs.get("skin_thickness",  "—")),   "—"],
        ["Diabetes Pedigree",       str(inputs.get("dpf",             "—")),   "—"],
    ]
    t = Table(rows, colWidths=[210, 145, 140])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0), colors.HexColor("#1d4ed8")),
        ("TEXTCOLOR",     (0,0), (-1,0), colors.white),
        ("FONTNAME",      (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,-1), 10),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [colors.HexColor("#f8fafc"), colors.white]),
        ("GRID",          (0,0), (-1,-1), 0.4, colors.HexColor("#e2e8f0")),
        ("PADDING",       (0,0), (-1,-1), 9),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ]))
    story.append(t)
    story.append(Spacer(1, 20))

    # ── Recommendations ──────────────────────────────────────────────────────
    story.append(Paragraph("Personalised Recommendations",
        ps("h2", fontSize=13, fontName="Helvetica-Bold",
           textColor=colors.HexColor("#1e293b"))))
    story.append(Spacer(1, 10))
    recs = {
        "LOW RISK": [
            "Maintain your current healthy lifestyle — you're doing great!",
            "Continue a balanced diet with vegetables, whole grains, and lean protein.",
            "Keep regular physical activity — aim for 150 minutes per week.",
            "Schedule yearly screening to stay on track.",
            "Stay well hydrated and limit sugary beverages.",
        ],
        "MODERATE RISK": [
            "Moderate risk detected — lifestyle changes can make a big difference.",
            "Reduce refined carbohydrates and sugar intake significantly.",
            "Increase physical activity — aim for 30 minutes of exercise daily.",
            "Losing 5–7% body weight can reduce diabetes risk by up to 58%.",
            "Get a fasting glucose test every 6 months.",
            "Prioritise 7–8 hours of quality sleep each night.",
        ],
        "HIGH RISK": [
            "High risk detected — please consult a doctor as soon as possible.",
            "A doctor should review your glucose and insulin levels in person.",
            "Follow a strict low-glycaemic diet — avoid all processed sugars.",
            "Begin a supervised exercise program with your doctor's guidance.",
            "Ask your doctor about preventive medications like Metformin.",
            "Monitor your blood glucose daily if possible.",
            "Manage stress — chronic stress raises blood sugar levels.",
        ],
    }[label]

    for r in recs:
        story.append(Paragraph(r,
            ps("b", fontSize=10, textColor=colors.HexColor("#374151"), leading=16)))
        story.append(Spacer(1, 5))

    story.append(Spacer(1, 20))

    # ── Disclaimer ───────────────────────────────────────────────────────────
    story.append(Table([[Paragraph(
        "Disclaimer: This report is generated by an AI system for informational purposes only. "
        "It is not a substitute for professional medical advice. Always consult a qualified healthcare provider.",
        ps("dis", fontSize=8, textColor=colors.HexColor("#94a3b8"), leading=12))]],
        colWidths=[495],
        style=TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#f8fafc")),
            ("PADDING",    (0,0), (-1,-1), 12),
            ("GRID",       (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ])))

    doc.build(story)
    buf.seek(0)
    return buf