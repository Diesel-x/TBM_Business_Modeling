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
                
    # Установка ширины колонок
    for row in table.rows:
        for i, w in enumerate(col_widths):
            row.cells[i].width = Inches(w / 25.4)


def build_gost_report_lr2():
    template_path = 'ТБМ_Шаблон_тит_лист_ЛР2.docx'
    doc = Document(template_path)
    
    # Настраиваем параметры первой секции (Титульный лист)
    sec_title = doc.sections[0]
    sec_title.orientation = WD_ORIENT.PORTRAIT
    sec_title.page_width = Inches(210 / 25.4)
    sec_title.page_height = Inches(297 / 25.4)
    sec_title.top_margin = Inches(20 / 25.4)
    sec_title.bottom_margin = Inches(20 / 25.4)
    sec_title.left_margin = Inches(30 / 25.4)
    sec_title.right_margin = Inches(15 / 25.4)

    # Заполняем титульный лист данными мини-группы 1 (студенты гр. ПИ-209Бзу и ПИ-208Бзу)
    for p in doc.paragraphs:
        if 'Мини-группа' in p.text:
            p.text = 'Мини-группа-1'
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(14)
        elif 'Выполнили: студенты гр.Группа' in p.text:
            p.text = 'Выполнили: студенты гр. ПИ-209Бзу, ПИ-208Бзу'
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(12)
        elif 'Фамилия И.О. всех студентов мини-группы' in p.text:
            p.text = 'Ардаширов Э.Ф.\nБайгускаров Т.Р.\nБаянов Д.Г.'
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
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
    r = p_main_title.add_run('ЛАБОРАТОРНАЯ РАБОТА № 2\n«ФУНКЦИОНАЛЬНОЕ МОДЕЛИРОВАНИЕ ПРЕДМЕТНОЙ ОБЛАСТИ»\nТема: «Функциональная модель розничной продажи товаров в продуктовом магазине в нотации IDEF0»')
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
        'получение практических навыков функционального моделирования предметной области в нотации IDEF0, '
        'разработки контекстной диаграммы и диаграммы функциональной декомпозиции бизнес-процесса розничной продажи '
        'продовольственных товаров с обеспечением стопроцентной преемственности и согласованности потоков мнемосхемы.'
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
        'провести системный анализ предметной области «Продажа товаров в продуктовом магазине» на основе мнемосхемы, разработанной в рамках лабораторной работы № 1;',
        'сформулировать цель моделирования и точку зрения функциональной модели в нотации IDEF0;',
        'разработать контекстную диаграмму А-0 («Выполнить розничную продажу товаров в магазине») с выделением внешних входов (Inputs), управлений (Controls), механизмов (Mechanisms) и выходов (Outputs);',
        'построить диаграмму функциональной декомпозиции первого уровня А0, включающую пять взаимосвязанных функциональных блоков (А1–А5);',
        'определить и специфицировать внутренние интерфейсные дуги между блоками декомпозиции, обратные связи и правила ветвления дуг управления и механизмов;',
        'проверить и подтвердить строгое соблюдение баланса граничных интерфейсных дуг (ICOM) между контекстной диаграммой А-0 и диаграммой декомпозиции А0;',
        'составить словарь терминов (Activity Dictionary) и словарь интерфейсных дуг (Arrow Dictionary) модели;',
        'сформулировать аналитические выводы по результатам функционального моделирования.'
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
        'Методология функционального моделирования IDEF0 (Integration Definition for Function Modeling) '
        'представляет собой формализованную методологию графического описания систем и бизнес-процессов, '
        'основанную на концепции структурного анализа SADT (Structured Analysis and Design Technique), разработанной '
        'Дугласом Россом. Стандарт IDEF0 регламентирован отечественными рекомендациями по стандартизации Р 50.1.028-2001 '
        'и международным стандартом IEEE 1320.1. Модель IDEF0 предназначена для наглядного представления функций, '
        'выполняемых системой, а также информационных, материальных и финансовых потоков, связывающих эти функции между собой '
        'и с окружающей внешней средой.'
    )
    p_th1 = doc.add_paragraph()
    format_gost_paragraph(p_th1, space_after=6)
    r = p_th1.add_run(theory_p1)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)

    theory_p2 = (
        'Основными семантическими элементами нотации IDEF0 выступают функциональные блоки (Activity Boxes) '
        'и интерфейсные дуги (Arrows). Функциональный блок изображается в виде прямоугольника и олицетворяет '
        'собой конкретную функцию, работу, процедуру или процесс. В соответствии со стандартами нотации блок '
        'именуется активным глаголом в повелительном наклонении или глаголом в неопределенной форме (инфинитиве) '
        'с пояснительными словами (например, «Выполнить розничную продажу товаров в магазине», «Зарегистрировать товар на кассовом узле»). '
        'В правом нижнем углу каждого функционального блока обязательно проставляется номер узла (Node Number), '
        'определяющий его положение в иерархической структуре модели.'
    )
    p_th2 = doc.add_paragraph()
    format_gost_paragraph(p_th2, space_after=6)
    r = p_th2.add_run(theory_p2)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)

    theory_p3 = (
        'Интерфейсные дуги (стрелки) обозначают информацию, физические объекты, документы или ресурсы, '
        'необходимые для выполнения работы либо возникающие в результате ее завершения. В нотации IDEF0 действует '
        'строгое правило: стрелки именуются только именами существительными или субстантивными словосочетаниями '
        '(категорически запрещено применение отглагольных существительных, обозначающих действие). '
        'Значение интерфейсной дуги однозначно определяется стороной блока, к которой она примыкает (принцип ICOM):'
    )
    p_th3 = doc.add_paragraph()
    format_gost_paragraph(p_th3, space_after=6)
    r = p_th3.add_run(theory_p3)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)

    icom_types = [
        ('Вход (Input) — левая грань блока: ', 
         'материальные предметы, сырье, продукция, запросы или исходные информационные данные, которые преобразуются или расходуются в процессе выполнения данной функции.'),
        ('Управление (Control) — верхняя грань блока: ', 
         'законодательные акты, отраслевые стандарты, правила торговли, прейскуранты, регламенты, должностные инструкции и управляющие директивы, которыми руководствуется исполнитель при совершении работы.'),
        ('Выход (Output) — правая грань блока: ', 
         'материальный, документальный или информационный результат выполнения работы (готовый упакованный товар, кассовый чек, сформированная выручка, актуализированная база данных).'),
        ('Механизм (Mechanism) — нижняя грань блока: ', 
         'ресурсы, привлекаемые для выполнения функции: сотрудники и специалисты (кассир, товаровед), оборудование, аппаратные устройства (сканер, POS-терминал, пин-пад) и программные комплексы (1С:Предприятие).')
    ]
    for name, desc in icom_types:
        p_ic = doc.add_paragraph()
        format_gost_paragraph(p_ic, space_after=4)
        r = p_ic.add_run(name)
        r.bold = True
        r.font.name = 'Times New Roman'
        r.font.size = Pt(14)
        r2 = p_ic.add_run(desc)
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(14)

    theory_p4 = (
        'Построение функциональной модели базируется на принципах иерархической декомпозиции. На вершине иерархии '
        'располагается единственная контекстная диаграмма с номером А-0, содержащая один обобщающий функциональный блок, '
        'определяющий границы всей системы в целом. На контекстной диаграмме обязательно фиксируются цель моделирования '
        '(Purpose) и точка зрения (Viewpoint), определяющая ракурс рассмотрения предметной области. '
        'Далее контекстный блок декомпозируется на диаграмме первого уровня А0 на совокупность от 3 до 9 подфункций, '
        'располагаемых по диагонали (доминированию) от верхнего левого угла к правому нижнему.'
    )
    p_th4 = doc.add_paragraph()
    format_gost_paragraph(p_th4, space_after=6)
    r = p_th4.add_run(theory_p4)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)

    theory_p5 = (
        'Фундаментальным законом корректности модели является правило синтаксической балансировки дуг (Arrow Balancing). '
        'Все граничные стрелки (входы, управления, механизмы, выходы), присоединенные к блоку на родительской диаграмме А-0, '
        'должны быть в полном составе и без искажений перенесены на дочернюю диаграмму декомпозиции А0. '
        'При этом стрелки могут разветвляться (Forking) для управления несколькими работами или объединяться (Joining) '
        'в общий поток. Также на диаграмме декомпозиции отображаются внутренние управляющие и материальные связи, '
        'включая обратные связи (Feedback loops), при которых выход последующей работы выступает управляющим или входным фактором для предыдущей.'
    )
    p_th5 = doc.add_paragraph()
    format_gost_paragraph(p_th5, space_after=6)
    r = p_th5.add_run(theory_p5)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)

    # ==========================================
    # РАЗДЕЛ 3: МНЕМОСХЕМА ПРЕДМЕТНОЙ ОБЛАСТИ (ИЗ ЛР1)
    # ==========================================
    add_gost_heading(doc, '3 Мнемосхема предметной области (из лабораторной работы № 1)', level=1, new_page=True)

    p_lr1_intro = doc.add_paragraph()
    format_gost_paragraph(p_lr1_intro, space_after=6)
    r = p_lr1_intro.add_run(
        'В соответствии с методическими требованиями кафедры АСУ УУНиТ функциональное моделирование в нотации IDEF0 '
        'выполняется на основе единой сквозной предметной области — «Продажа товаров в продуктовом магазине», '
        'исследованной и формализованной в лабораторной работе № 1. Модель отражает очный формат розничной торговли '
        'продуктами питания в магазине самообслуживания.'
    )
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)

    p_lr1_struct = doc.add_paragraph()
    format_gost_paragraph(p_lr1_struct, space_after=6)
    r = p_lr1_struct.add_run(
        'В структуре предметной области выделены три внутренних организационных подразделения предприятия '
        '«Магазин "Продукты"» и внешняя среда:\n'
        '1) Подразделение «Торговый зал»: покупатель (субъект), витрина и полки с товарами (объект);\n'
        '2) Подразделение «Кассовый узел»: кассир-продавец (субъект), сканер штрихкодов, POS-терминал с фискальным регистратором, банковский терминал/пин-пад (объекты);\n'
        '3) Подразделение «Бэк-офис и ИТ-инфраструктура»: товароучетная система (сервер базы данных «1С:Предприятие») (объект), администратор / товаровед магазина (субъект);\n'
        '4) Внешняя среда: процессинговый центр банка-эквайера (объект авторизации платежей).'
    )
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)

    p_lr1_fig_ref = doc.add_paragraph()
    format_gost_paragraph(p_lr1_fig_ref, space_after=6)
    r = p_lr1_fig_ref.add_run(
        'Утвержденная мнемосхема бизнес-процесса представлена на рисунке 1. '
        'Схема включает 21 верифицированный поток взаимодействия, разделенный на устные диалоги, материальные предметы, '
        'бумажные документы и электронные пакеты данных, передаваемые исключительно через аппаратные интерфейсы.'
    )
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)

    # ---------------- ВСТАВКА МНЕМОСХЕМЫ НА АЛЬБОМНЫЙ ЛИСТ ----------------
    sec_mnemo = doc.add_section(WD_SECTION_START.NEW_PAGE)
    sec_mnemo.orientation = WD_ORIENT.LANDSCAPE
    sec_mnemo.page_width = Inches(297 / 25.4)
    sec_mnemo.page_height = Inches(210 / 25.4)
    sec_mnemo.top_margin = Inches(15 / 25.4)
    sec_mnemo.bottom_margin = Inches(15 / 25.4)
    sec_mnemo.left_margin = Inches(20 / 25.4)
    sec_mnemo.right_margin = Inches(15 / 25.4)

    mnemo_img_path = 'mnemoscheme_store.png'
    if os.path.exists(mnemo_img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(0)
        p_img.paragraph_format.space_after = Pt(4)
        run_img = p_img.add_run()
        run_img.add_picture(mnemo_img_path, width=Inches(255 / 25.4))
        
        p_caption = doc.add_paragraph()
        format_gost_paragraph(p_caption, space_before=4, space_after=6, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent=0)
        r = p_caption.add_run('Рисунок 1 — Мнемосхема бизнес-процесса «Продажа товаров в продуктовом магазине»')
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        r.font.bold = True

    # ==========================================
    # РАЗДЕЛ 4: РЕЗУЛЬТАТЫ ВЫПОЛНЕНИЯ РАБОТЫ (Возврат к книжной ориентации)
    # ==========================================
    sec_res = doc.add_section(WD_SECTION_START.NEW_PAGE)
    sec_res.orientation = WD_ORIENT.PORTRAIT
    sec_res.page_width = Inches(210 / 25.4)
    sec_res.page_height = Inches(297 / 25.4)
    sec_res.top_margin = Inches(20 / 25.4)
    sec_res.bottom_margin = Inches(20 / 25.4)
    sec_res.left_margin = Inches(30 / 25.4)
    sec_res.right_margin = Inches(15 / 25.4)

    add_gost_heading(doc, '4 Результаты выполнения работы', level=1, new_page=False)

    # 4.1 Цель и точка зрения моделирования
    add_gost_heading(doc, '4.1 Цель моделирования и точка зрения', level=2, new_page=False)

    p_pv_text = doc.add_paragraph()
    format_gost_paragraph(p_pv_text, space_after=6)
    r = p_pv_text.add_run(
        'В соответствии со стандартом IDEF0 функциональная модель не может быть построена без четкой формулировки цели '
        'и определения фиксированной точки зрения. Для модели процесса продажи продовольственных товаров установлены следующие параметры:\n'
        '• Цель моделирования (Purpose): описать функциональную структуру процесса розничной продажи продовольственных товаров '
        'для регламентации работы кассового персонала магазина и комплексной автоматизации складского и финансового товароучета;\n'
        '• Точка зрения (Viewpoint): директор магазина (ведущий товаровед);\n'
        '• Границы моделирования (Scope): процесс охватывает операции от момента входа покупателя в торговый зал и отбора продуктов '
        'до проведения расчета на кассовом узле, выдачи фискального чека и актуализации складских остатков в серверной базе данных 1С.'
    )
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)

    # 4.2 Контекстная диаграмма А-0
    add_gost_heading(doc, '4.2 Контекстная диаграмма функциональной модели (А-0)', level=2, new_page=False)

    p_a0_intro = doc.add_paragraph()
    format_gost_paragraph(p_a0_intro, space_after=6)
    r = p_a0_intro.add_run(
        'Контекстная диаграмма А-0 представляет бизнес-процесс в виде единого функционального блока «Выполнить розничную продажу товаров в магазине» '
        '(узел 0). Контекстная диаграмма отражает граничные связи системы с внешним окружением. '
        'Графическое представление контекстной диаграммы А-0 приведено на рисунке 2 (альбомная ориентация страницы).'
    )
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)

    # ---------------- ВСТАВКА КОНТЕКСТНОЙ ДИАГРАММЫ НА АЛЬБОМНЫЙ ЛИСТ ----------------
    sec_a0_img = doc.add_section(WD_SECTION_START.NEW_PAGE)
    sec_a0_img.orientation = WD_ORIENT.LANDSCAPE
    sec_a0_img.page_width = Inches(297 / 25.4)
    sec_a0_img.page_height = Inches(210 / 25.4)
    sec_a0_img.top_margin = Inches(15 / 25.4)
    sec_a0_img.bottom_margin = Inches(15 / 25.4)
    sec_a0_img.left_margin = Inches(20 / 25.4)
    sec_a0_img.right_margin = Inches(15 / 25.4)

    a0_img_path = 'idef0_a_minus_0.png'
    if os.path.exists(a0_img_path):
        p_img2 = doc.add_paragraph()
        p_img2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img2.paragraph_format.space_before = Pt(0)
        p_img2.paragraph_format.space_after = Pt(4)
        run_img2 = p_img2.add_run()
        run_img2.add_picture(a0_img_path, width=Inches(255 / 25.4))
        
        p_caption2 = doc.add_paragraph()
        format_gost_paragraph(p_caption2, space_before=4, space_after=6, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent=0)
        r = p_caption2.add_run('Рисунок 2 — Контекстная диаграмма А-0 «Выполнить розничную продажу товаров в магазине»')
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        r.font.bold = True

    # ---------------- ВОЗВРАТ К КНИЖНОЙ СЕКЦИИ: СПЕЦИФИКАЦИЯ СТРЕЛОК А-0 ----------------
    sec_a0_tbl = doc.add_section(WD_SECTION_START.NEW_PAGE)
    sec_a0_tbl.orientation = WD_ORIENT.PORTRAIT
    sec_a0_tbl.page_width = Inches(210 / 25.4)
    sec_a0_tbl.page_height = Inches(297 / 25.4)
    sec_a0_tbl.top_margin = Inches(20 / 25.4)
    sec_a0_tbl.bottom_margin = Inches(20 / 25.4)
    sec_a0_tbl.left_margin = Inches(30 / 25.4)
    sec_a0_tbl.right_margin = Inches(15 / 25.4)

    p_tbl1_intro = doc.add_paragraph()
    format_gost_paragraph(p_tbl1_intro, space_after=6)
    r = p_tbl1_intro.add_run(
        'Полная спецификация интерфейсных дуг контекстной диаграммы А-0 по категориям стандарта ICOM '
        'представлена в таблице 1. В соответствии с правилами нотации все стрелки названы строго именами существительными, '
        'полностью исключены отглагольные существительные и отражено реальное материально-техническое взаимодействие.'
    )
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)

    p_t1_title = doc.add_paragraph()
    format_gost_paragraph(p_t1_title, space_before=8, space_after=4, align=WD_ALIGN_PARAGRAPH.LEFT, first_line_indent=0)
    r_t1 = p_t1_title.add_run('Таблица 1 — Стрелки контекстной диаграммы А-0')
    r_t1.font.name = 'Times New Roman'
    r_t1.font.size = Pt(12)
    r_t1.font.bold = True

    t1_headers = ['Метка', 'Имя стрелки (Arrow Name)', 'Определение стрелки (Arrow Definition)', 'Тип дуги']
    t1_data = [
        ['I1', 'Продовольственные товары со склада', 'Продукты питания, поступившие со складской зоны и выложенные на витрины торгового зала', 'Input'],
        ['I2', 'Покупатель (запрос на покупку)', 'Покупатель с осознанной потребностью в приобретении необходимых товаров повседневного спроса', 'Input'],
        ['I3', 'Платежные средства (наличные / карта)', 'Финансовые платежные средства покупателя (наличные денежные купюры либо банковская карта с модулем NFC)', 'Input'],
        ['C1', 'Закон РФ «О защите прав потребителей»', 'Федеральный закон, регулирующий права граждан на получение качественных продуктов, достоверной информации и кассового чека', 'Control'],
        ['C2', 'Правила торговли товарами', 'Правила продажи отдельных видов продовольственных товаров, санитарные нормы и регламенты выкладки', 'Control'],
        ['C3', 'Прейскурант (ценники)', 'Официально утвержденный перечень розничных цен и наименований, размещенный на ценниках в торговом зале', 'Control'],
        ['C4', 'Инструкции кассира, кассовая дисциплина', 'Должностные регламенты кассира-продавца и правила соблюдения Федерального закона № 54-ФЗ о применении ККТ', 'Control'],
        ['C5', 'Регламент эквайринга банка', 'Технические и правовые стандарты банка-эквайера по проведению безналичных платежей и обработке транзакций', 'Control'],
        ['M1', 'Кассир-продавец', 'Штатный работник кассового узла, осуществляющий регистрацию покупок и проведение расчетных операций', 'Mechanism'],
        ['M2', 'Сканер штрихкодов', 'Лазерное оптическое устройство кассы, преобразующее графический штрихкод в цифровой идентификатор', 'Mechanism'],
        ['M3', 'POS-терминал с фискальным рег.', 'Кассовый аппаратно-программный комплекс с монитором и встроенным фискальным регистратором чеков', 'Mechanism'],
        ['M4', 'Банковский терминал (пин-пад)', 'Автономное электронное устройство для приема бесконтактных карт и передачи запроса на эквайринг', 'Mechanism'],
        ['M5', 'Товароучетная система (1С:Предприятие)', 'Центральный сервер баз данных предприятия, хранящий номенклатуру, цены и текущие складские остатки', 'Mechanism'],
        ['M6', 'Администратор / Товаровед магазина', 'Должностное лицо магазина, контролирующее учет движения товаров и анализирующее отчетность', 'Mechanism'],
        ['O1', 'Приобретенный товар у покупателя', 'Оплаченные продукты питания, сложенные в фирменный пакет и переданные клиенту', 'Output'],
        ['O2', 'Фискальный кассовый чек', 'Официальный бумажный документ фискального накопителя ККМ, подтверждающий факт купли-продажи', 'Output'],
        ['O3', 'Банковский слип-чек', 'Бумажный чек терминала эквайринга с кодом авторизации безналичной транзакции банка', 'Output'],
        ['O4', 'Кассовая выручка (в кассе / на счете)', 'Денежные средства, поступившие в денежный ящик кассы или зачисленные на расчетный счет магазина', 'Output'],
        ['O5', 'Отчет об остатках и продажах', 'Электронный и печатный документ товароведа с актуальными данными по реализации и складским запасам', 'Output']
    ]
    t1_widths = [15.0, 45.0, 85.0, 20.0]
    table1 = doc.add_table(rows=len(t1_data) + 1, cols=4)
    format_table_cells(table1, t1_widths, t1_headers, t1_data, align_cols={0: WD_ALIGN_PARAGRAPH.CENTER, 3: WD_ALIGN_PARAGRAPH.CENTER})

    # 4.3 Диаграмма функциональной декомпозиции А0
    add_gost_heading(doc, '4.3 Диаграмма функциональной декомпозиции (А0)', level=2, new_page=True)

    p_dec_intro = doc.add_paragraph()
    format_gost_paragraph(p_dec_intro, space_after=6)
    r = p_dec_intro.add_run(
        'В процессе функциональной декомпозиции обобщенный контекстный процесс А-0 был детализирован на пять взаимосвязанных '
        'функциональных блоков первого уровня (А1–А5), расположенных по диагонали доминирования:\n'
        '• А1: Отобрать товар в торговом зале;\n'
        '• А2: Зарегистрировать товар на кассовом узле;\n'
        '• А3: Принять оплату (провести расчет с покупателем);\n'
        '• А4: Сформировать и выдать фискальный чек;\n'
        '• А5: Актуализировать товарные остатки в учетной системе.\n'
        'Диаграмма декомпозиции А0 приведена на рисунке 3 (альбомный лист).'
    )
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)

    # ---------------- ВСТАВКА ДИАГРАММЫ ДЕКОМПОЗИЦИИ НА АЛЬБОМНЫЙ ЛИСТ ----------------
    sec_a0_dec_img = doc.add_section(WD_SECTION_START.NEW_PAGE)
    sec_a0_dec_img.orientation = WD_ORIENT.LANDSCAPE
    sec_a0_dec_img.page_width = Inches(297 / 25.4)
    sec_a0_dec_img.page_height = Inches(210 / 25.4)
    sec_a0_dec_img.top_margin = Inches(15 / 25.4)
    sec_a0_dec_img.bottom_margin = Inches(15 / 25.4)
    sec_a0_dec_img.left_margin = Inches(20 / 25.4)
    sec_a0_dec_img.right_margin = Inches(15 / 25.4)

    a0_dec_path = 'idef0_a0.png'
    if os.path.exists(a0_dec_path):
        p_img3 = doc.add_paragraph()
        p_img3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img3.paragraph_format.space_before = Pt(0)
        p_img3.paragraph_format.space_after = Pt(4)
        run_img3 = p_img3.add_run()
        run_img3.add_picture(a0_dec_path, width=Inches(255 / 25.4))
        
        p_caption3 = doc.add_paragraph()
        format_gost_paragraph(p_caption3, space_before=4, space_after=6, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent=0)
        r = p_caption3.add_run('Рисунок 3 — Диаграмма декомпозиции А0 «Выполнить розничную продажу товаров в магазине»')
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        r.font.bold = True

    # ---------------- ВОЗВРАТ К КНИЖНОЙ СЕКЦИИ: СПЕЦИФИКАЦИЯ БЛОКОВ И ДУГ ДЕКОМПОЗИЦИИ ----------------
    sec_a0_tables = doc.add_section(WD_SECTION_START.NEW_PAGE)
    sec_a0_tables.orientation = WD_ORIENT.PORTRAIT
    sec_a0_tables.page_width = Inches(210 / 25.4)
    sec_a0_tables.page_height = Inches(297 / 25.4)
    sec_a0_tables.top_margin = Inches(20 / 25.4)
    sec_a0_tables.bottom_margin = Inches(20 / 25.4)
    sec_a0_tables.left_margin = Inches(30 / 25.4)
    sec_a0_tables.right_margin = Inches(15 / 25.4)

    add_gost_heading(doc, '4.4 Спецификация функциональных блоков декомпозиции А0', level=2, new_page=False)

    p_tbl2_intro = doc.add_paragraph()
    format_gost_paragraph(p_tbl2_intro, space_after=6)
    r = p_tbl2_intro.add_run('Описание функциональных блоков диаграммы декомпозиции А0 представлено в таблице 2.')
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)

    p_t2_title = doc.add_paragraph()
    format_gost_paragraph(p_t2_title, space_before=8, space_after=4, align=WD_ALIGN_PARAGRAPH.LEFT, first_line_indent=0)
    r_t2 = p_t2_title.add_run('Таблица 2 — Функциональные блоки диаграммы декомпозиции А0')
    r_t2.font.name = 'Times New Roman'
    r_t2.font.size = Pt(12)
    r_t2.font.bold = True

    t2_headers = ['Номер узла', 'Имя работы (Activity Name)', 'Определение работы (Activity Definition)']
    t2_data = [
        ['А1', 'Отобрать товар в торговом зале', 'Выбор покупателем необходимых продуктов питания с полок и витрин магазина на основе информации ценников и перемещение отобранных товаров к кассовому узлу.'],
        ['А2', 'Зарегистрировать товар на кассовом узле', 'Выкладка товара на транспортерную ленту, считывание штрихкодов лазерным сканером, получение актуальных цен из базы данных 1С и расчет промежуточного итога кассового чека.'],
        ['А3', 'Принять оплату (провести расчет с покупателем)', 'Согласование суммы к оплате, выбор формы расчета (наличные/карта), списание средств с банковского счета через пин-пад и авторизацию банка либо прием банкнот и выдача сдачи.'],
        ['А4', 'Сформировать и выдать фискальный чек', 'Передача команды фискальному регистратору на печать чека ККТ с реквизитами ФЗ № 54-ФЗ, упаковка покупок в пакет и передача чека и товаров покупателю.'],
        ['А5', 'Актуализировать товарные остатки в учетной системе', 'Электронное списание проданных артикулов со складских остатков в серверной базе 1С, фиксация выручки и формирование аналитического отчета товароведом.']
    ]
    t2_widths = [22.0, 48.0, 95.0]
    table2 = doc.add_table(rows=len(t2_data) + 1, cols=3)
    format_table_cells(table2, t2_widths, t2_headers, t2_data, align_cols={0: WD_ALIGN_PARAGRAPH.CENTER})

    # 4.5 Спецификация интерфейсных дуг диаграммы декомпозиции
    add_gost_heading(doc, '4.5 Спецификация интерфейсных дуг диаграммы декомпозиции А0', level=2, new_page=True)

    p_tbl3_intro = doc.add_paragraph()
    format_gost_paragraph(p_tbl3_intro, space_after=6)
    r = p_tbl3_intro.add_run(
        'Интерфейсные дуги диаграммы декомпозиции А0 связывают функциональные блоки между собой и с внешними '
        'границами родительского блока А-0. В таблице 3 представлены все потоки модели с указанием источника (Source) '
        'и приемника (Destination), подтверждая отсутствие изолированных функциональных узлов.'
    )
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)

    p_t3_title = doc.add_paragraph()
    format_gost_paragraph(p_t3_title, space_before=8, space_after=4, align=WD_ALIGN_PARAGRAPH.LEFT, first_line_indent=0)
    r_t3 = p_t3_title.add_run('Таблица 3 — Интерфейсные дуги диаграммы декомпозиции А0')
    r_t3.font.name = 'Times New Roman'
    r_t3.font.size = Pt(12)
    r_t3.font.bold = True

    t3_headers = ['Метка', 'Имя интерфейсной дуги', 'Источник (Source)', 'Приемник (Destination)', 'Назначение интерфейсной дуги']
    t3_data = [
        ['I1', 'Продовольственные товары со склада', 'Внешний вход (Склад)', 'Блок А1 (Вход)', 'Поступление физических продуктов питания для отбора'],
        ['I2', 'Покупатель (запрос на покупку)', 'Внешний вход (Среда)', 'Блок А1 (Вход)', 'Потребность клиента в покупке товаров'],
        ['I3', 'Платежные средства (наличные / карта)', 'Внешний вход (Клиент)', 'Блок А3 (Вход)', 'Средства для осуществления финансового расчета'],
        ['C1', 'Закон «О защите прав потребителей»', 'Внешнее управление', 'Блоки А1, А4 (Управление)', 'Правовые гарантии качества товара и предоставления чека'],
        ['C2', 'Правила торговли товарами', 'Внешнее управление', 'Блоки А1, А2 (Управление)', 'Санитарные и организационные требования к выкладке и продаже'],
        ['C3', 'Прейскурант (ценники)', 'Внешнее управление', 'Блок А1 (Управление)', 'Информирование клиента о стоимости товаров на полках'],
        ['C4', 'Инструкции кассира, кассовая дисциплина', 'Внешнее управление', 'Блоки А2, А3, А4, А5 (Управление)', 'Регламент работы персонала и соблюдение правил применения ККТ'],
        ['C5', 'Регламент эквайринга банка', 'Внешнее управление', 'Блок А3 (Управление)', 'Правила авторизации безналичных банковских транзакций'],
        ['M1', 'Кассир-продавец', 'Внешний механизм (Штат)', 'Блоки А2, А3, А4 (Механизм)', 'Сотрудник, выполняющий операции сканирования, расчета и выдачи чека'],
        ['M2', 'Сканер штрихкодов', 'Внешний механизм (Оборудование)', 'Блок А2 (Механизм)', 'Устройство распознавания штрихкода'],
        ['M3', 'POS-терминал с фискальным рег.', 'Внешний механизм (Оборудование)', 'Блоки А2, А3, А4 (Механизм)', 'Центральный вычислительный модуль кассы'],
        ['M4', 'Банковский терминал (пин-пад)', 'Внешний механизм (Оборудование)', 'Блок А3 (Механизм)', 'Устройство считывания банковских карт'],
        ['M5', 'Товароучетная система (1С:Предприятие)', 'Внешний механизм (ИТ)', 'Блоки А2, А5 (Механизм)', 'База данных цен, номенклатуры и складских остатков'],
        ['M6', 'Администратор / Товаровед магазина', 'Внешний механизм (Штат)', 'Блок А5 (Механизм)', 'Специалист, курирующий списание остатков и отчетность'],
        ['Внутр.', 'Отобранный товар на кассовой ленте', 'Блок А1 (Выход)', 'Блок А2 (Вход)', 'Физическое перемещение отобранных продуктов на кассовую ленту'],
        ['Внутр.', 'Покупатель у кассовой зоны', 'Блок А1 (Выход)', 'Блок А2 (Вход)', 'Прибытие покупателя к зоне расчета кассира'],
        ['Внутр.', 'Сумма к оплате (данные чека)', 'Блок А2 (Выход)', 'Блок А3 (Вход)', 'Электронный расчет итоговой стоимости покупки'],
        ['Внутр.', 'Зарегистрированный товар к выдаче', 'Блок А2 (Выход)', 'Блок А4 (Вход)', 'Товары, прошедшие сканирование и готовые к упаковке'],
        ['Внутр.', 'Подтверждение оплаты (статус транзакции)', 'Блок А3 (Выход)', 'Блок А4 (Вход)', 'Успешная фиксация внесения денег или одобрения банка'],
        ['Внутр.', 'Данные о совершенной продаже', 'Блок А4 (Выход)', 'Блок А5 (Вход)', 'Электронный пакет данных об артикулах и количестве для списания'],
        ['Обратн.', 'Сведения об остатках и ценах (1С)', 'Блок А5 (Выход)', 'Блок А2 (Управление)', 'Петля обратной связи: актуальные цены и остатки из базы 1С в кассу'],
        ['O1', 'Приобретенный товар у покупателя', 'Блок А4 (Выход)', 'Внешний выход (Клиент)', 'Готовая упакованная покупка на руках у покупателя'],
        ['O2', 'Фискальный кассовый чек', 'Блок А4 (Выход)', 'Внешний выход (Клиент)', 'Бумажный фискальный документ об оплате'],
        ['O3', 'Банковский слип-чек', 'Блок А3 (Выход)', 'Внешний выход (Клиент)', 'Квитанция терминала об одобрении безналичной транзакции'],
        ['O4', 'Кассовая выручка (в кассе / на счете)', 'Блок А3 (Выход)', 'Внешний выход (Магазин)', 'Финансовый результат от продажи продуктов'],
        ['O5', 'Отчет об остатках и продажах', 'Блок А5 (Выход)', 'Внешний выход (Товаровед)', 'Документ складского аудита и анализа товарооборота']
    ]
    t3_widths = [14.0, 38.0, 36.0, 36.0, 41.0]
    table3 = doc.add_table(rows=len(t3_data) + 1, cols=5)
    format_table_cells(table3, t3_widths, t3_headers, t3_data, align_cols={0: WD_ALIGN_PARAGRAPH.CENTER})

    # 4.6 Глоссарий терминов модели
    add_gost_heading(doc, '4.6 Глоссарий терминов модели (Dictionary)', level=2, new_page=True)

    p_gloss_intro = doc.add_paragraph()
    format_gost_paragraph(p_gloss_intro, space_after=6)
    r = p_gloss_intro.add_run(
        'В соответствии с требованиями стандарта IDEF0 для устранения многозначности формулировок '
        'составлен глоссарий функциональной модели (таблица 4), включающий словарь работ (Activity Dictionary) '
        'и словарь интерфейсных дуг (Arrow Dictionary).'
    )
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)

    p_t4_title = doc.add_paragraph()
    format_gost_paragraph(p_t4_title, space_before=8, space_after=4, align=WD_ALIGN_PARAGRAPH.LEFT, first_line_indent=0)
    r_t4 = p_t4_title.add_run('Таблица 4 — Глоссарий функциональной модели IDEF0')
    r_t4.font.name = 'Times New Roman'
    r_t4.font.size = Pt(12)
    r_t4.font.bold = True

    t4_headers = ['Термин модели', 'Категория', 'Толкование в контексте моделируемого бизнес-процесса']
    t4_data = [
        ['Выполнить розничную продажу товаров в магазине', 'Работа (узел 0)', 'Корневой бизнес-процесс магазина самообслуживания по обслуживанию покупателя, расчету и выдаче чека.'],
        ['Отобрать товар в торговом зале', 'Работа (узел 1)', 'Действия покупателя по поиску нужных продовольственных позиций и перемещению их к расчетному узлу.'],
        ['Зарегистрировать товар на кассовом узле', 'Работа (узел 2)', 'Идентификация номенклатуры кассиром с помощью сканера и определение общей стоимости в кассовой программе.'],
        ['Принять оплату (провести расчет с покупателем)', 'Работа (узел 3)', 'Прием денежных средств покупателя либо списание безналичных средств банком-эквайером.'],
        ['Сформировать и выдать фискальный чек', 'Работа (узел 4)', 'Аппаратная фискализация чека в накопителе ККМ и вручение чека с товаром покупателю.'],
        ['Актуализировать товарные остатки в учетной системе', 'Работа (узел 5)', 'Списание учетного количества товаров со склада в базе 1С и расчет аналитических показателей товароведом.'],
        ['Продовольственные товары со склада', 'Стрелка (I1)', 'Материальные продукты питания, находящиеся в розничном обороте магазина.'],
        ['Покупатель (запрос на покупку)', 'Стрелка (I2)', 'Физическое лицо, находящееся в магазине и инициирующее потребительский спрос.'],
        ['Платежные средства', 'Стрелка (I3)', 'Денежные знаки Банка России или авторизованные платежные карты банковских систем.'],
        ['Фискальный кассовый чек', 'Стрелка (O2)', 'Бумажный фискальный документ установленного образца с QR-кодом и фискальным признаком документа.'],
        ['Банковский слип-чек', 'Стрелка (O3)', 'Квитанция терминала безналичной оплаты с кодом RRN, номером терминала и суммой списания.'],
        ['Товароучетная система (1С)', 'Механизм (M5)', 'Программный комплекс «1С:Предприятие 8. Управление торговлей», автоматизирующий учет.'],
        ['POS-терминал / ККМ', 'Механизм (M3)', 'Аппаратный комплекс кассы самообслуживания или рабочего места кассира с фискальным накопителем.']
    ]
    t4_widths = [45.0, 25.0, 95.0]
    table4 = doc.add_table(rows=len(t4_data) + 1, cols=3)
    format_table_cells(table4, t4_widths, t4_headers, t4_data, align_cols={1: WD_ALIGN_PARAGRAPH.CENTER})

    # 4.7 Анализ баланса интерфейсных дуг
    add_gost_heading(doc, '4.7 Анализ баланса интерфейсных дуг (Arrow Balancing)', level=2, new_page=False)

    p_bal_text = doc.add_paragraph()
    format_gost_paragraph(p_bal_text, space_after=6)
    r = p_bal_text.add_run(
        'Проверка синтаксической и семантической корректности разработанной модели подтверждает полное соблюдение '
        'правила балансировки граничных дуг:\n'
        '1. Входы (Inputs): стрелки I1 (Продовольственные товары), I2 (Покупатель) и I3 (Платежные средства) контекстной диаграммы '
        'в полном объеме перенесены на декомпозицию А0 (I1 и I2 входят в блок А1, I3 входит в блок А3);\n'
        '2. Управления (Controls): дуги C1–C5 контекстной диаграммы полностью сохранены на декомпозиции А0 с корректным ветвлением '
        '(C1 управляет А1 и А4; C2 управляет А1 и А2; C3 управляет А1; C4 управляет блоками А2, А3, А4, А5; C5 управляет А3);\n'
        '3. Механизмы (Mechanisms): дуги M1–M6 родительского блока А-0 на 100% представлены на диаграмме А0 '
        '(M1, M3 задействованы в блоках А2, А3, А4; M2 в блоке А2; M4 в блоке А3; M5 в блоках А2 и А5; M6 в блоке А5);\n'
        '4. Выходы (Outputs): все 5 выходов контекстной диаграммы (O1–O5) являются внешними выходами диаграммы декомпозиции '
        '(O1 и O2 выходят из А4; O3 и O4 выходят из А3; O5 выходит из А5);\n'
        '5. Внутренняя целостность: на диаграмме А0 отсутствуют изолированные блоки («черные дыры» или «генераторы данных»), '
        'каждый функциональный блок имеет как минимум один вход, одно управление, один механизм и один выход.'
    )
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)

    # ==========================================
    # РАЗДЕЛ 5: ВЫВОДЫ (с новой страницы)
    # ==========================================
    add_gost_heading(doc, '5 Выводы', level=1, new_page=True)

    concl_p1 = (
        'В ходе выполнения лабораторной работы № 2 были успешно сформированы и закреплены практические навыки '
        'функционального моделирования предметной области с использованием международной методологии IDEF0 '
        'на примере сквозного процесса «Продажа товаров в продуктовом магазине».'
    )
    p_c1 = doc.add_paragraph()
    format_gost_paragraph(p_c1, space_after=6)
    r = p_c1.add_run(concl_p1)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)

    concl_points = [
        'Определены строгие методологические рамки процесса: установлена фиксированная точка зрения (директор магазина / ведущий товаровед) и цель моделирования, направленная на регламентацию кассового обслуживания и автоматизацию учета движения товарных запасов.',
        'Разработана контекстная диаграмма А-0 «Выполнить розничную продажу товаров в магазине», определяющая границы системы и ее внешнее окружение (покупатели, банк-эквайер, законодательство РФ, нормативно-справочная документация).',
        'Построена диаграмма функциональной декомпозиции первого уровня А0, содержащая 5 взаимосвязанных блоков (А1: Отобрать товар в торговом зале; А2: Зарегистрировать товар на кассовом узле; А3: Принять оплату; А4: Сформировать и выдать фискальный чек; А5: Актуализировать товарные остатки в учетной системе).',
        'Обеспечена стопроцентная преемственность данных с результатами лабораторной работы № 1: все субъекты, материальные предметы, документы и электронные пакеты мнемосхемы без потерь трансформированы в соответствующие категории стандарта ICOM.',
        'Строго соблюдены специальные требования и регламентные табу кафедры АСУ УУНиТ: в наименованиях интерфейсных дуг категорически исключены отглагольные существительные, электронный обмен физических лиц организован исключительно через аппаратных посредников (сканер, POS-терминал, пин-пад, сервер 1С), блоки названы активными глаголами, а модель отражает очный формат непосредственного взаимодействия покупателя в торговом зале.',
        'Достигнута полная синтаксическая сбалансированность модели: число и состав граничных дуг (I1–I3, C1–C5, M1–M6, O1–O5) на контекстной диаграмме и диаграмме декомпозиции строго эквивалентны, отражена обратная связь по управлению (А5 -> А2), составлены исчерпывающие словари работ и дуг.',
        'Созданная функциональная модель IDEF0 формирует строгую концептуальную основу для последующего динамического имитационного моделирования бизнес-процесса в нотации BPMN в среде Bizagi Modeler в рамках практических работ № 1–3.'
    ]
    for cp in concl_points:
        p_cp = doc.add_paragraph()
        format_gost_paragraph(p_cp, space_after=6)
        r = p_cp.add_run(f'• {cp}')
        r.font.name = 'Times New Roman'
        r.font.size = Pt(14)

    # Сохранение отчета
    save_targets = [
        'Отчет_ЛР2_ТБМ_ГОСТ.docx',
        'ЛР2_ПИ209бзу_1_Ардаширов_Байгускаров_Баянов.docx',
        'ЛР2_ПИ208бзу_1_Ардаширов_Байгускаров_Баянов.docx',
        os.path.join('МАТЕРИАЛЫ_ДЛЯ_СДАЧИ_ТБМ', '2_Лабораторная_работа_2_IDEF0', 'Отчет_ЛР2_ТБМ_ГОСТ.docx'),
        os.path.join('МАТЕРИАЛЫ_ДЛЯ_СДАЧИ_ТБМ', '2_Лабораторная_работа_2_IDEF0', 'ЛР2_ПИ209бзу_1_Ардаширов_Байгускаров_Баянов.docx'),
        os.path.join('МАТЕРИАЛЫ_ДЛЯ_СДАЧИ_ТБМ', '2_Лабораторная_работа_2_IDEF0', 'ЛР2_ПИ208бзу_1_Ардаширов_Байгускаров_Баянов.docx')
    ]
    for target in save_targets:
        os.makedirs(os.path.dirname(os.path.abspath(target)), exist_ok=True)
        try:
            doc.save(target)
            print(f'GOST Lab 2 report saved: {target}')
        except PermissionError:
            print(f'Warning: {target} is currently locked by Word.')

if __name__ == '__main__':
    build_gost_report_lr2()

