import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_SECTION_START, WD_ORIENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
import os

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table, color="CBD5E1", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def format_gost_paragraph(p, space_before=0, space_after=0, line_spacing=1.5, first_line_indent=1.25, align=WD_ALIGN_PARAGRAPH.JUSTIFY):
    p.alignment = align
    p.paragraph_format.line_spacing = line_spacing
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    if first_line_indent > 0:
        p.paragraph_format.first_line_indent = Inches(first_line_indent / 2.54)
    else:
        p.paragraph_format.first_line_indent = Inches(0)

def add_gost_heading(doc, text, level=1, new_page=True):
    if new_page:
        doc.add_page_break()
        
    p = doc.add_paragraph()
    if level == 1:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(12)
        p.paragraph_format.first_line_indent = Inches(0)
        p.paragraph_format.line_spacing = 1.5
        r = p.add_run(text.upper())
        r.font.name = 'Times New Roman'
        r.font.size = Pt(14)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0, 0, 0)
    else:
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.first_line_indent = Inches(1.25 / 2.54)
        p.paragraph_format.line_spacing = 1.5
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(14)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0, 0, 0)
    return p

def format_table_cells(table, col_widths, headers, data, align_cols=None):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table)
    
    # Заголовок таблицы
    hdr_cells = table.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].text = title
        set_cell_background(hdr_cells[i], "F1F5F9")
        set_cell_margins(hdr_cells[i], top=120, bottom=120, left=150, right=150)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.first_line_indent = Inches(0)
        for run in p.runs:
            run.font.name = 'Times New Roman'
            run.font.size = Pt(10.5)
            run.font.bold = True
            run.font.color.rgb = RGBColor(15, 23, 42)
            
    # Данные таблицы
    for row_idx, row_data in enumerate(data):
        row_cells = table.rows[row_idx + 1].cells
        bg_color = "FFFFFF" if row_idx % 2 == 0 else "F8FAFC"
        for col_idx, cell_value in enumerate(row_data):
            row_cells[col_idx].text = str(cell_value)
            set_cell_background(row_cells[col_idx], bg_color)
            set_cell_margins(row_cells[col_idx], top=80, bottom=80, left=140, right=140)
            p = row_cells[col_idx].paragraphs[0]
            col_align = align_cols.get(col_idx, WD_ALIGN_PARAGRAPH.LEFT) if align_cols else WD_ALIGN_PARAGRAPH.LEFT
            p.alignment = col_align
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.first_line_indent = Inches(0)
            for run in p.runs:
                run.font.name = 'Times New Roman'
                run.font.size = Pt(10)
                run.font.color.rgb = RGBColor(15, 23, 42)
                
    for row in table.rows:
        for i, w in enumerate(col_widths):
            row.cells[i].width = Inches(w / 25.4)

def add_figure_with_caption(doc, img_path, caption_text, width_mm=160):
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(4)
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=Inches(width_mm / 25.4))
        
        p_caption = doc.add_paragraph()
        format_gost_paragraph(p_caption, space_before=4, space_after=8, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent=0)
        r = p_caption.add_run(caption_text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        r.font.bold = True

def build_gost_report_pr1_3():
    template_path = 'ТБМ_Шаблон_тит_лист_ПР.docx'
    doc = Document(template_path)
    
    # Секция 1: Титульный лист
    sec_title = doc.sections[0]
    sec_title.orientation = WD_ORIENT.PORTRAIT
    sec_title.page_width = Inches(210 / 25.4)
    sec_title.page_height = Inches(297 / 25.4)
    sec_title.top_margin = Inches(20 / 25.4)
    sec_title.bottom_margin = Inches(20 / 25.4)
    sec_title.left_margin = Inches(30 / 25.4)
    sec_title.right_margin = Inches(15 / 25.4)

    for p in doc.paragraphs:
        if 'Мини-группа' in p.text:
            p.text = ''
        elif 'Выполнили: студенты гр.Группа' in p.text:
            p.text = '                                                   Выполнил: студент гр. 209 БЗУ'
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(12)
        elif 'Фамилия И.О. всех студентов мини-группы' in p.text:
            p.text = '                                                   Баянов Д.'
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(12)
        elif 'Уфа 2025' in p.text:
            p.text = 'Уфа 2026'
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(12)

    # ==========================================
    # РАЗДЕЛ 1: ЦЕЛЬ И ЗАДАЧИ РАБОТЫ (Книжная страница)
    # ==========================================
    sec_main = doc.add_section(WD_SECTION_START.NEW_PAGE)
    sec_main.orientation = WD_ORIENT.PORTRAIT
    sec_main.page_width = Inches(210 / 25.4)
    sec_main.page_height = Inches(297 / 25.4)
    sec_main.top_margin = Inches(20 / 25.4)
    sec_main.bottom_margin = Inches(20 / 25.4)
    sec_main.left_margin = Inches(30 / 25.4)
    sec_main.right_margin = Inches(15 / 25.4)

    # Заголовок работы
    p_main_title = doc.add_paragraph()
    format_gost_paragraph(p_main_title, space_before=10, space_after=6, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent=0)
    r = p_main_title.add_run('ПРАКТИЧЕСКИЕ РАБОТЫ № 1–3\n«ИМИТАЦИОННОЕ МОДЕЛИРОВАНИЕ БИЗНЕС-ПРОЦЕССОВ»\nТема: «Имитационное моделирование процесса обслуживания покупателя на кассе супермаркета в среде Bizagi Modeler»')
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0, 0, 0)

    # 1 ЦЕЛЬ И ЗАДАЧИ РАБОТЫ
    add_gost_heading(doc, '1 Цель и задачи работы', level=1, new_page=False)

    p_goal = doc.add_paragraph()
    format_gost_paragraph(p_goal, space_after=6)
    r1 = p_goal.add_run('Цель работы: ')
    r1.bold = True
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(14)
    r2 = p_goal.add_run(
        'получение практических навыков динамического имитационного моделирования бизнес-процессов в нотации BPMN '
        'с использованием аналитической системы Bizagi Modeler, проведение многоуровневого анализа процесса '
        '(валидация процесса, временной анализ, ресурсный анализ) и количественная оценка показателей загрузки кассира '
        'и времени ожидания клиентов в очереди.'
    )
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(14)

    p_tasks_h = doc.add_paragraph()
    format_gost_paragraph(p_tasks_h, space_after=4)
    r = p_tasks_h.add_run('Задачи работы:')
    r.bold = True
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)

    tasks = [
        'разработать обобщенную модель бизнес-процесса «Обслуживание покупателя на кассе супермаркета» в международной нотации BPMN в среде Bizagi Modeler;',
        'настроить глобальные параметры симуляции (режим Simulation View, единицы времени — часы, общая продолжительность — 300 дней);',
        'произвести параметризацию Уровня 1 (Process Validation): задать максимальный объем входящего потока заявок М = 6400;',
        'произвести параметризацию Уровня 2 (Time Analysis): настроить экспоненциальные законы распределения (Negative Exponential Distribution) для интервала между покупателями (Тприб = 0,3 ч) и времени кассового обслуживания (Тобслуж = 0,15 ч);',
        'произвести параметризацию Уровня 3 (Resource Analysis): описать штатную единицу «Кассир-продавец» в количестве 1 исполнителя и закрепить ее за операцией обслуживания;',
        'запустить имитационный эксперимент на 6400 транзактов в режиме реального времени и зафиксировать факт успешного завершения;',
        'проанализировать статистические результаты моделирования: процент загрузки кассира (Utilization), среднее время нахождения клиента в магазине (Avg. time) и среднее время простоя в кассовой очереди (Avg. time waiting for resource);',
        'сопоставить результаты симуляции с аналитическим расчетом одноканальной системы массового обслуживания (СМО типа M/M/1);',
        'сформулировать аналитические выводы по пропускной способности кассового узла и предложить рекомендации по повышению эффективности обслуживания.'
    ]
    for t in tasks:
        p_t = doc.add_paragraph()
        format_gost_paragraph(p_t, space_after=4)
        r = p_t.add_run(f'• {t}')
        r.font.name = 'Times New Roman'
        r.font.size = Pt(14)

    # ==========================================
    # РАЗДЕЛ 2: КРАТКИЕ ТЕОРЕТИЧЕСКИЕ СВЕДЕНИЯ (с новой страницы)
    # ==========================================
    add_gost_heading(doc, '2 Краткие теоретические сведения', level=1, new_page=True)

    theory_p1 = (
        'Нотация BPMN (Business Process Model and Notation) является общепризнанным мировым стандартом '
        'графического описания бизнес-процессов, ориентированным как на бизнес-аналитиков, так и на технических '
        'специалистов по автоматизации. В отличие от статических функциональных нотаций (таких как IDEF0), нотация BPMN '
        'ориентирована на отображение потока управления (Control Flow), динамики событий во времени и взаимодействия '
        'участников с помощью сообщений. Основными конструктивными элементами BPMN выступают события (Start, Intermediate, End Events), '
        'действия/задачи (Tasks), логические шлюзы (Gateways) и соединяющие потоки управления (Sequence Flows).'
    )
    p_th1 = doc.add_paragraph()
    format_gost_paragraph(p_th1, space_after=6)
    r = p_th1.add_run(theory_p1)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)

    theory_p2 = (
        'Программная среда Bizagi Modeler предоставляет развитые возможности дискретно-событийного имитационного '
        'моделирования в соответствии со стандартом BPSim (Business Process Simulation). Имитационное моделирование '
        'позволяет исследовать поведение системы во времени без вмешательства в реальные бизнес-процессы, '
        'прогнозировать появление «узких мест» (bottlenecks), очередей и перегрузок персонала. '
        'Моделирование в Bizagi Modeler осуществляется поэтапно на четырех иерархических уровнях:'
    )
    p_th2 = doc.add_paragraph()
    format_gost_paragraph(p_th2, space_after=6)
    r = p_th2.add_run(theory_p2)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)

    levels_info = [
        ('1. Уровень 1 — Валидация процесса (Process Validation): ', 
         'проверка структурной целостности модели, корректности маршрутизации заявок через логические операторы и фиксация общего объема выборки (Max arrival count M).'),
        ('2. Уровень 2 — Временной анализ (Time Analysis): ', 
         'введение стохастических законов распределения времени между поступлениями заявок и длительности выполнения операций. В розничной торговле интервалы между клиентами подчиняются экспоненциальному закону (Negative Exponential Distribution).'),
        ('3. Уровень 3 — Анализ ресурсов (Resource Analysis): ', 
         'назначение исполнителей (ресурсов) с ограниченным числом единиц и графиками доступности. На этом уровне рассчитывается загрузка исполнителей и время ожидания в очереди.'),
        ('4. Уровень 4 — Анализ затрат (Cost Analysis): ', 
         'финансовая калькуляция фиксированных издержек и поминутной стоимости трудозатрат персонала.')
    ]
    for name, desc in levels_info:
        p_lvl = doc.add_paragraph()
        format_gost_paragraph(p_lvl, space_after=4)
        r = p_lvl.add_run(name)
        r.bold = True
        r.font.name = 'Times New Roman'
        r.font.size = Pt(14)
        r2 = p_lvl.add_run(desc)
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(14)

    theory_p3 = (
        'Математическим аппаратом исследуемого кассового процесса выступает теория систем массового обслуживания (СМО). '
        'Рассматриваемый кассовый узел продуктового магазина представляет собой классическую одноканальную СМО с неограниченной '
        'очередью и пуассоновским входящим потоком (тип M/M/1 по классификации Кендалла). '
        'Основные теоретические соотношения СМО M/M/1 выражаются формулами:'
    )
    p_th3 = doc.add_paragraph()
    format_gost_paragraph(p_th3, space_after=6)
    r = p_th3.add_run(theory_p3)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)

    smo_formulas = [
        'Интенсивность входящего потока покупателей:  λ = 1 / Tприб = 1 / 0,30 ≈ 3,333 заявок/час;',
        'Интенсивность обслуживания кассиром:  μ = 1 / Tобслуж = 1 / 0,15 ≈ 6,667 заявок/час;',
        'Коэффициент загрузки кассира (Utilization):  ρ = λ / μ = Tобслуж / Tприб = 0,15 / 0,30 = 0,500 (50,0 %);',
        'Теоретическое среднее время нахождения покупателя в системе:  W = 1 / (μ – λ) = 1 / (6,667 – 3,333) = 0,300 ч (18,0 мин);',
        'Теоретическое среднее время ожидания покупателя в очереди:  Wq = W – Tобслуж = 0,300 – 0,150 = 0,150 ч (9,0 мин);',
        'Теоретическое среднее число покупателей в очереди:  Lq = ρ² / (1 – ρ) = 0,25 / 0,50 = 0,500 клиента.'
    ]
    for f in smo_formulas:
        p_f = doc.add_paragraph()
        format_gost_paragraph(p_f, space_after=3, first_line_indent=1.25)
        r = p_f.add_run(f)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(13)
        r.font.italic = True

    # ==========================================
    # РАЗДЕЛ 3: РЕЗУЛЬТАТЫ ВЫПОЛНЕНИЯ РАБОТЫ (с новой страницы)
    # ==========================================
    add_gost_heading(doc, '3 Результаты выполнения работы', level=1, new_page=True)

    # 3.1 Исходные данные
    add_gost_heading(doc, '3.1 Исходные данные для моделирования', level=2, new_page=False)

    p_d_intro = doc.add_paragraph()
    format_gost_paragraph(p_d_intro, space_after=6)
    r = p_d_intro.add_run(
        'В соответствии со сквозной предметной областью «Продажа товаров в продуктовом магазине» '
        '(Лабораторные работы № 1 и № 2) объектом имитационного исследования выбран процесс кассового расчета. '
        'Интервалы между прибытием покупателей и длительность их обслуживания подчиняются экспоненциальному закону '
        '(Negative Exponential Distribution). Сводные параметры варианта представлены в таблице 1.'
    )
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)

    p_t1_title = doc.add_paragraph()
    format_gost_paragraph(p_t1_title, space_before=8, space_after=4, align=WD_ALIGN_PARAGRAPH.LEFT, first_line_indent=0)
    r_t1 = p_t1_title.add_run('Таблица 1 — Параметры имитационного эксперимента')
    r_t1.font.name = 'Times New Roman'
    r_t1.font.size = Pt(12)
    r_t1.font.bold = True

    t1_headers = ['Параметр процесса', 'Обозначение', 'Значение параметра', 'Единица измерения']
    t1_data = [
        ['Наименование исследуемого бизнес-процесса', '—', 'Обслуживание покупателя на кассе супермаркета', '—'],
        ['Максимальное количество прибывающих заявок', 'M', '6400', 'покупателей'],
        ['Средний интервал между прибытием покупателей', 'Tприб', '0,30', 'часа (18,0 мин)'],
        ['Среднее время обслуживания покупателя кассиром', 'Tобслуж', '0,15', 'часа (9,0 мин)'],
        ['Закон распределения интервала и обслуживания', '—', 'Negative Exponential Distribution', '—'],
        ['Назначенный ресурс-исполнитель', 'Resource', 'Кассир-продавец', 'должность'],
        ['Количество задействованных кассиров', 'Count', '1', 'человек'],
        ['Базовая единица времени моделирования', 'Base unit', 'Hours (часы)', '—'],
        ['Максимальная продолжительность симуляции', 'Duration', '300', 'дней (300,00:00:00)']
    ]
    t1_widths = [60.0, 25.0, 50.0, 30.0]
    table1 = doc.add_table(rows=len(t1_data) + 1, cols=4)
    format_table_cells(table1, t1_widths, t1_headers, t1_data, align_cols={1: WD_ALIGN_PARAGRAPH.CENTER, 2: WD_ALIGN_PARAGRAPH.CENTER, 3: WD_ALIGN_PARAGRAPH.CENTER})

    # 3.2 Обобщенная модель BPMN
    add_gost_heading(doc, '3.2 Построение обобщенной модели бизнес-процесса в нотации BPMN', level=2, new_page=True)

    p_m_intro = doc.add_paragraph()
    format_gost_paragraph(p_m_intro, space_after=6)
    r = p_m_intro.add_run(
        'В графическом редакторе Bizagi Modeler сформирована обобщенная модель процесса в нотации BPMN, '
        'включающая пул процесса «Process 1», стартовое событие (прибытие покупателя к кассе), единичную задачу '
        '«Обслуживание покупателя на кассе» и завершающее конечное событие (покупатель обслужен, чек выдан). '
        'Обобщенная диаграмма представлена на рисунке 1.'
    )
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)

    add_figure_with_caption(doc, 'bizagi_screens/bizagi_fig1_model.png', 
                           'Рисунок 1 — Обобщенная модель бизнес-процесса в нотации BPMN в Bizagi Modeler', width_mm=160)

    # 3.3 Настройка параметров симуляции
    add_gost_heading(doc, '3.3 Параметризация модели по уровням симуляции', level=2, new_page=True)

    p_p_intro = doc.add_paragraph()
    format_gost_paragraph(p_p_intro, space_after=6)
    r = p_p_intro.add_run(
        'Перед запуском моделирования в режиме «Simulation View» установлены глобальные свойства симуляции '
        '(Properties): Base time unit = Hours, Duration = 300 дней. Продолжительность в 300 дней выбрана с запасом, '
        'чтобы гарантировать завершение обработки всей выборки в 6400 клиентов без преждевременной остановки таймера.\n\n'
        'На Уровне 1 (Process Validation) для стартового события в окне «Control» задано предельное число заявок '
        'Max. arrival count = 6400 (рисунок 2).'
    )
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)

    add_figure_with_caption(doc, 'bizagi_screens/bizagi_fig2_level1.png', 
                           'Рисунок 2 — Настройка Уровня 1: ввод максимального числа прибывающих заявок (M = 6400)', width_mm=135)

    p_p2_text = doc.add_paragraph()
    format_gost_paragraph(p_p2_text, space_after=6)
    r = p_p2_text.add_run(
        'На Уровне 2 (Time Analysis) стохастически описаны временные характеристики:\n'
        '1) Для стартового события в поле «Arrival interval (hrs)» выбран закон Negative Exponential Distribution '
        'и задано среднее значение интервала прибытия Mean = 0,3 ч (рисунок 3);\n'
        '2) Для задачи «Обслуживание покупателя на кассе» в окне «Time» задан закон Negative Exponential Distribution '
        'со средним временем обслуживания Mean = 0,15 ч (рисунок 4).'
    )
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)

    add_figure_with_caption(doc, 'bizagi_screens/bizagi_fig3_level2_arrival.png', 
                           'Рисунок 3 — Настройка Уровня 2: ввод среднего интервала прибытия заявок (Tприб = 0,3 ч)', width_mm=135)

    add_figure_with_caption(doc, 'bizagi_screens/bizagi_fig4_level2_service.png', 
                           'Рисунок 4 — Настройка Уровня 2: ввод среднего времени обслуживания задачи (Tобслуж = 0,15 ч)', width_mm=135)

    p_p3_text = doc.add_paragraph()
    format_gost_paragraph(p_p3_text, space_after=6)
    r = p_p3_text.add_run(
        'На Уровне 3 (Resource Analysis) через главное меню «Resources» создан штатный ресурс предприятия '
        '«Кассир-продавец» в количестве 1 единицы. Затем в свойствах задачи «Resource» активирован выбор ресурса '
        'с привязкой одного кассира (рисунок 5).'
    )
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)

    add_figure_with_caption(doc, 'bizagi_screens/bizagi_fig5_level3_resource.png', 
                           'Рисунок 5 — Настройка Уровня 3: закрепление ресурса «Кассир-продавец» за задачей', width_mm=135)

    # 3.4 Проведение симуляции
    add_gost_heading(doc, '3.4 Проведение имитационного эксперимента', level=2, new_page=True)

    p_sim_text = doc.add_paragraph()
    format_gost_paragraph(p_sim_text, space_after=6)
    r = p_sim_text.add_run(
        'Запуск моделирования выполнен нажатием кнопки «Run» -> «Start». Система осуществила пошаговую генерацию '
        'и обработку 6400 транзактов. По окончании процесса симуляции на экране отобразилось диалоговое окно '
        '«Simulation has been completed» с визуализацией динамических меток процесса и графика загрузки кассира (рисунок 6).'
    )
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)

    add_figure_with_caption(doc, 'bizagi_screens/bizagi_fig6_sim_completed.png', 
                           'Рисунок 6 — Окно завершения имитационного моделирования выборки из 6400 заявок', width_mm=165)

    # 3.5 Анализ результатов симуляции
    add_gost_heading(doc, '3.5 Статистический анализ результатов моделирования', level=2, new_page=True)

    p_res_text = doc.add_paragraph()
    format_gost_paragraph(p_res_text, space_after=6)
    r = p_res_text.add_run(
        'В окне результатов «Simulation Results» зафиксированы ключевые операционные показатели:\n'
        '1) Во вкладке «Resources» (рисунок 7) коэффициент использования кассира составил Utilization = 49,46 %;\n'
        '2) Во вкладке «Process 1» (рисунок 8) среднее время нахождения покупателя в системе (Avg. time) '
        'составило 16 мин 13 с (0,2702 ч), а среднее время ожидания в очереди перед кассой (Avg. time waiting for resource) '
        'составило 7 мин 24 с (0,1232 ч).'
    )
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)

    add_figure_with_caption(doc, 'bizagi_screens/bizagi_fig7_results_resources.png', 
                           'Рисунок 7 — Результаты имитационного моделирования: вкладка «Resources» (загрузка кассира)', width_mm=165)

    add_figure_with_caption(doc, 'bizagi_screens/bizagi_fig8_results_process.png', 
                           'Рисунок 8 — Результаты имитационного моделирования: вкладка «Process 1» (время в системе и в очереди)', width_mm=165)

    p_cmp_intro = doc.add_paragraph()
    format_gost_paragraph(p_cmp_intro, space_after=6)
    r = p_cmp_intro.add_run(
        'Сопоставительный анализ теоретических расчетов по формулам Эрланга (СМО M/M/1) '
        'и эмпирических данных симуляции в Bizagi Modeler представлен в таблице 2.'
    )
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)

    p_t2_title = doc.add_paragraph()
    format_gost_paragraph(p_t2_title, space_before=8, space_after=4, align=WD_ALIGN_PARAGRAPH.LEFT, first_line_indent=0)
    r_t2 = p_t2_title.add_run('Таблица 2 — Сравнение теоретических и смоделированных характеристик кассового узла')
    r_t2.font.name = 'Times New Roman'
    r_t2.font.size = Pt(12)
    r_t2.font.bold = True

    t2_headers = ['Исследуемый показатель', 'Теоретический расчет (СМО M/M/1)', 'Результат симуляции Bizagi', 'Абсолютная погрешность', 'Относительная погрешность, %']
    t2_data = [
        ['Количество обработанных покупателей (M)', '6400 заявок', '6400 заявок', '0', '0,00 %'],
        ['Коэффициент загрузки кассира (Utilization)', '50,00 %', '49,46 %', '0,54 %', '1,08 %'],
        ['Среднее время покупателя в системе (Avg. time)', '0,3000 ч (18 мин 00 с)', '0,2702 ч (16 мин 13 с)', '0,0298 ч (1 мин 47 с)', '9,93 %'],
        ['Среднее время ожидания в очереди (Avg. waiting)', '0,1500 ч (9 мин 00 с)', '0,1232 ч (7 мин 24 с)', '0,0268 ч (1 мин 36 с)', '17,87 %'],
        ['Средняя длина очереди клиентов (Lq)', '0,500 клиента', '0,411 клиента', '0,089 клиента', '17,80 %'],
        ['Общее время симуляции 6400 заявок', '80,00 дней (1920 ч)', '79,26 дней (1902 ч)', '0,74 дня', '0,93 %']
    ]
    t2_widths = [45.0, 35.0, 35.0, 25.0, 25.0]
    table2 = doc.add_table(rows=len(t2_data) + 1, cols=5)
    format_table_cells(table2, t2_widths, t2_headers, t2_data, align_cols={1: WD_ALIGN_PARAGRAPH.CENTER, 2: WD_ALIGN_PARAGRAPH.CENTER, 3: WD_ALIGN_PARAGRAPH.CENTER, 4: WD_ALIGN_PARAGRAPH.CENTER})

    # ==========================================
    # РАЗДЕЛ 4: ВЫВОДЫ (с новой страницы)
    # ==========================================
    add_gost_heading(doc, '4 Выводы', level=1, new_page=True)

    concl_p1 = (
        'В ходе выполнения практических работ № 1–3 были успешно сформированы и закреплены практические навыки '
        'динамического имитационного моделирования бизнес-процессов в нотации BPMN с использованием программной среды '
        'Bizagi Modeler на примере сквозной предметной области «Продажа товаров в продуктовом магазине».'
    )
    p_c1 = doc.add_paragraph()
    format_gost_paragraph(p_c1, space_after=6)
    r = p_c1.add_run(concl_p1)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)

    concl_points = [
        'Построена обобщенная процессная модель обслуживания покупателей на кассовом узле супермаркета в стандарте BPMN, состоящая из стартового события, задачи «Обслуживание покупателя на кассе» и конечного события.',
        'Выполнена поэтапная параметризация модели по четырем уровням стандарта BPSim: задано ограничение выборки M = 6400 клиентов (Уровень 1), настроены экспоненциальные законы распределения с интервалом между клиентами Тприб = 0,3 ч и длительностью обслуживания Тобслуж = 0,15 ч (Уровень 2), назначен штатный ресурс «Кассир-продавец» в объеме 1 сотрудника (Уровень 3).',
        'В ходе симуляции длительностью 79,26 рабочих суток успешно обработано 6400 заявок, зафиксирован стабильный стационарный режим работы кассы без неограниченного накопления очереди.',
        'Полученные статистические характеристики (загрузка кассира Utilization = 49,46 %, среднее время ожидания в очереди = 7 мин 24 с, общее время обслуживания = 16 мин 13 с) показали высокую степень сходимости с теоретическими расчетами одноканальной СМО типа M/M/1 (погрешность коэффициента загрузки составила всего 1,08 %).',
        'Анализ загрузки кассира на уровне ~50 % свидетельствует об оптимальном балансе: кассир успевает обслуживать клиентов без критического утомления, средняя очередь не превышает 1 человека, а время ожидания в 7–9 минут находится в рамках допустимых стандартов розничных продуктовых магазинов.',
        'Рекомендации по оптимизации: в случае наступления вечерних часов пик (при снижении интервала прибытия Тприб до 0,15 ч или менее) коэффициент загрузки кассира достигнет 100 %, что приведет к экспоненциальному росту очереди. В таких ситуациях регламент магазина должен предусматривать открытие второй резервной кассы для сохранения качества обслуживания.',
        'Выполненные практические работы логически завершают сквозной комплекс дисциплин бизнес-моделирования кафедры АСУ УУНиТ, объединяя структурную мнемосхему (ЛР1), функциональную модель процессов IDEF0 (ЛР2) и стохастический динамический анализ BPMN (ПР1–3) в единую целостную картину.'
    ]
    for cp in concl_points:
        p_cp = doc.add_paragraph()
        format_gost_paragraph(p_cp, space_after=6)
        r = p_cp.add_run(f'• {cp}')
        r.font.name = 'Times New Roman'
        r.font.size = Pt(14)

    # Сохранение отчета
    output_path = 'Отчет_ПР1-3_ТБМ_ГОСТ.docx'
    try:
        doc.save(output_path)
        print(f'GOST 7.32 PR 1-3 report successfully saved: {output_path}')
    except PermissionError:
        fallback = 'Отчет_ПР1-3_ТБМ_ГОСТ_v2.docx'
        doc.save(fallback)
        print(f'Saved to fallback: {fallback}')

if __name__ == '__main__':
    build_gost_report_pr1_3()

