# CuraData — Functional Blood Work Decoder

**Built by Nasly Duarte · nasly.ai · Think Like a Healer Initiative**  
*NLP + Computer Vision · Miami Dade College CAI2840C*

---

## The Origin Story

I didn't come to this work through a lab or a university research grant.

I came to it through survival.

I am a first-generation Latina, a single mother, an operations accountant, an AI student, and what I've started calling an **indigenous biohacker** — someone who looks at the data the healthcare system already collected on my body, and refuses to accept "your labs are normal" as a final answer.

For years I lived inside what I now recognize as a full adrenal crash. The stressors stacked quietly and relentlessly — a chaotic, high-pressure work environment, financial pressure, the invisible labor of managing a household alone, the weight of showing up for everyone while running on empty. I was doing everything "right" by the world's standards and falling apart by every biological one.

The fatigue wasn't laziness. The brain fog wasn't distraction. The inability to lose weight wasn't a lack of willpower. My body was screaming in a language the system didn't speak — and every doctor visit ended the same way: *your labs look normal, you should be fine.*

I was not fine.

---

## What Changed Everything

Books. Research. Stubbornness.

I started reading — really reading. Jeff Bowles on high-dose Vitamin D3. Functional medicine frameworks. Papers on iron transport and thyroid conversion. The relationship between cortisol and sleep and blood sugar and adrenal function. The more I read, the more I understood that the gap between *standard lab ranges* and *optimal ranges* was not a small clinical footnote — it was the difference between being told you're fine and actually feeling like yourself again.

I began tracking. Adjusting. Testing. Rebuilding — supplement by supplement, lab draw by lab draw, degree by degree on a thermometer before getting out of bed in the morning.

And slowly, undeniably, I started feeling better.

Not because I had access to a functional medicine doctor. I didn't. Not because I had unlimited time or resources. I had neither. But because I refused to stop asking questions, and because I was willing to become my own first patient.

---

## Why I Built This

The American healthcare system was not designed with my community in mind.

Underserved communities — Latinx families, Black families, immigrant families, working-class families — have been navigating a system built on data that largely excluded them. The "normal" lab ranges were established on populations that didn't look like us, live like us, eat like us, or carry the same generational stress loads we carry. And when AI arrived, it didn't fix this gap. It scaled it.

**AI trained on exclusionary data will scale exclusionary outcomes — unless communities build their own biological intelligence.**

That is the mission of CuraData. That is the mission of Sanar AI. That is what Think Like a Healer is about.

This tool exists because I believe that every person — regardless of income, zip code, insurance status, or whether they can afford a functional medicine practitioner — deserves to understand what their own blood is telling them. The labs have already been drawn. The blood has already been given. The answers are already there.

We just need the tools to read them.

---

## What This Tool Does

The **CuraData Functional Blood Work Decoder** is a standalone HTML tool that layers functional medicine interpretation on top of standard lab results. It was built as part of an NLP and Computer Vision course at Miami Dade College and is intended for **educational purposes only**.

It does not diagnose. It does not prescribe. It does not replace a qualified healthcare provider.

What it does is give you a framework — rooted in functional medicine principles — for understanding what your markers mean beyond the standard reference range, and what questions to ask next.

---

## How to Use This Tool

### Getting Started

1. Open `bloodwork_decoder.html` in any modern web browser — no installation, no login, no internet connection required after opening
2. Enter your draw date, lab name, and name or ID at the top
3. Navigate between lab panels using the tabs at the top of the decoder

### The Six Lab Panels

| Tab | What it covers |
|---|---|
| **CMP** | Kidney, adrenal/electrolytes, liver, leaky gut indicators, blood sugar |
| **CBC w/ Differential** | Anemia pattern (RBC markers), immune pattern (differential) |
| **Thyroid** | Full thyroid panel — TSH, Free T4, Free T3, Reverse T3, antibodies |
| **Iron + Temp** | Iron panel with body temperature tracker (thyroid-iron transport connection) |
| **Lipid** | Full lipid panel with insulin resistance pattern decoder |
| **Vitamin D & Minerals** | D3, calcium, magnesium, zinc, selenium, B12, folate |

### Reading Each Row

Every marker shows you five things side by side:

1. **Standard range** — what a conventional lab flags as abnormal
2. **Functional/optimal range** — the narrower range associated with optimal health, not just absence of disease
3. **If LOW** — what that pattern likely signals + what I've researched
4. **If HIGH** — what that pattern likely signals + what I've researched
5. **Your value + status** — enter your number, select optimal/low/high, watch the summary counters update

### Color-Coded Badge System

- **Blue badges** — what a low result likely means
- **Red/orange badges** — what a high result likely means
- **Green badges** — supplements or protocols researched for low values
- **Amber badges** — supplements or protocols researched for high values
- **Purple badges** — tap to expand inline research panels (methylation, B vitamins)

### The Research Panels

Two expandable research panels are embedded directly in the CBC tab:

- **Research methylation** — what methylation is, why MTHFR matters, signs of poor methylation, what supports it
- **Research B vitamins** — all 8 recognized B vitamins, what each does, why the retired numbers (B4, B8, B10–B17) were removed

Tap the purple badge to expand. Tap again to collapse.

### Iron + Temperature Tracker

The Iron tab includes a **daily waking temperature log**. This matters because low body temperature — a common hypothyroid symptom — physically impairs transferrin's ability to transport iron. You can supplement iron aggressively and still not move the needle if your body temperature is chronically below 97.8°F.

Track your temperature before getting out of bed. The tool color-codes each reading:

- **98.6°F+** → Optimal — iron transport working
- **97.8–98.5°F** → Monitor thyroid panel
- **Below 97.8°F** → 🚩 Iron transport likely impaired — address thyroid first
- **Below 97.0°F** → 🚩🚩 Significant suppression — iron supplementation alone will not work

### My Daily Stack Tab

This tab documents my personal supplement protocol — what I take, when I take it, and why. It is organized around my two-meal daily schedule:

- **Morning with first meal** — D3 (Bowles protocol), MK-4 K2, magnesium, selenium, thyroid blend, DHEA 50mg, Pregnenolone 80mg
- **Mid-morning spaced** — Ferrex 150 + Vitamin C (iron protocol, spaced from thyroid meds)
- **Evening with second meal** — MK-7 K2, magnesium second dose, GA + Cinulin + Calm (sleep protocol)

The tab includes checkboxes for daily tracking, a journal with waking temp and energy level, and four color-coded spacing rule cards covering iron timing, D3/K2 pairing, sleep protocol, and hormone precursor guidance.

**Important:** DHEA and Pregnenolone are hormonal precursors. What I take reflects my own personal health journey and research. This should not be replicated without guidance from a qualified healthcare provider.

### My Protocol Tab

Documents the full rationale behind my high-dose approaches:

- **D3 rebuild protocol** — why standard dosing fails long-term deficiency, the full taper schedule, MK-4/MK-7 cofactor logic
- **Magnesium types** — all 8 forms explained, why Life Extension ZümXR bisglycinate extended release is what I personally take
- **Iron rebuild** — why long-term deficiency takes 6–12 months to reverse, the Ferrex 150 + Vitamin C protocol, %Tsat monitoring

---

## Important Disclaimer

This tool documents personal research, personal experience, and educational content rooted in functional medicine frameworks. It does not constitute medical advice. It is not a diagnostic tool. It does not replace the guidance of a qualified healthcare provider.

The supplement protocols described reflect what I personally take as part of my own health journey. Individual needs vary significantly. Always consult a qualified healthcare professional before making changes to your health regimen, especially regarding hormonal supplements like DHEA and Pregnenolone.

---

## Project Context

This tool is part of **CuraData** — an open-source health tech project that uses AI to help people decode their lab results from blood, urine, stool, and saliva. By combining NLP and computer vision, CuraData delivers culturally relevant health insights rooted in both science and ancestral wisdom.

**CuraData lives at the intersection of:**
- Functional medicine interpretation
- AI-powered health literacy
- Health equity for underserved and Latinx communities
- Ancestral healing knowledge validated through modern biomarker science

It was built as an academic project at Miami Dade College (CAI2840C — NLP and Computer Vision) and continues to grow as part of the broader **Sanar AI** ecosystem.

---

## Connect

- **nasly.ai** — AI + health equity speaker identity
- **Think Like a Healer** — newsletter, research blog, community content
- **GitHub** — github.com/nasly-ai
- **Instagram** — @girlgoneverde

---

*"The data already exists. The blood has already been given. We just need the tools — and the courage — to read it."*

**— Nasly Duarte**

