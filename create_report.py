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

def set_table_borders(table, color="A0AEC0", sz="4", val="single"):
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

def build_gost_report():
    template_path = 'ТБМ_Шаблон_тит_лист_ЛР1.docx'
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
    r = p_main_title.add_run('ЛАБОРАТОРНАЯ РАБОТА № 1\n«РАЗРАБОТКА МНЕМОСХЕМЫ ПРЕДМЕТНОЙ ОБЛАСТИ»\nТема: «Продажа товаров в продуктовом магазине»')
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
    r2 = p_goal.add_run('получение практических навыков разработки мнемосхемы предметной области для сложного бизнес-процесса.')
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(14)

    p_tasks_h = doc.add_paragraph()
    format_gost_paragraph(p_tasks_h, space_after=4)
    r = p_tasks_h.add_run('Задачи работы:')
    r.bold = True
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)

    tasks = [
        'провести системный анализ предметной области «Продажа товаров в продуктовом магазине» и составить подробное словесное описание бизнес-процесса от момента входа покупателя в магазин до завершения покупки;',
        'выделить основных субъектов и объекты, участвующие в процессе, и определить их иерархическую структуру (подразделения предприятия и внешняя среда);',
        'определить и классифицировать все виды информационного и материального взаимодействия (устный, бумажный, электронный, материальный) без использования отглагольных существительных;',
        'разработать графическую мнемосхему бизнес-процесса в соответствии с общепринятыми обозначениями и правилами наглядного представления информационных потоков;',
        'сформулировать аналитические выводы по результатам моделирования.'
    ]
    for idx, t in enumerate(tasks):
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
        'Мнемосхема (мнемоническая схема) представляет собой совокупность условных изображений и символов, '
        'отражающих схематическое устройство контролируемого или моделируемого объекта, производственного '
        'или управленческого процесса. Мнемосхема выступает упрощённой структурно-функциональной моделью, '
        'облегчающей визуальное восприятие и глубокое понимание сущности происходящих операций, функционального '
        'назначения служб, оборудования, а также алгоритмов координации действий участников в штатных режимах.'
    )
    p_th1 = doc.add_paragraph()
    format_gost_paragraph(p_th1, space_after=6)
    r = p_th1.add_run(theory_p1)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)

    theory_p2 = (
        'Мнемосхемы применяются в случаях, когда исследуемый объект имеет территориально или функционально '
        'распределенную структуру, и служат эффективным демонстрационным инструментом. На мнемосхеме наглядно '
        'демонстрируются материальные потоки (движение сырья, готовой продукции, денежных средств), бумажный '
        'документооборот, устные коммуникации и электронные информационные потоки между подразделениями.'
    )
    p_th2 = doc.add_paragraph()
    format_gost_paragraph(p_th2, space_after=6)
    r = p_th2.add_run(theory_p2)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)

    theory_p3 = (
        'При проектировании мнемосхем критически важным является соблюдение принципа опосредованности '
        'электронного взаимодействия: физические лица (покупатели, кассиры, администраторы) не могут обмениваться '
        'электронной информацией напрямую. Передача электронных пакетов данных всегда осуществляется через '
        'специализированные аппаратные и программные средства-посредники (сканеры штрихкодов, POS-терминалы, '
        'банковские пин-пады, серверы баз данных).'
    )
    p_th3 = doc.add_paragraph()
    format_gost_paragraph(p_th3, space_after=6)
    r = p_th3.add_run(theory_p3)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)

    # ==========================================
    # РАЗДЕЛ 3: ПОДРОБНОЕ СЛОВЕСНОЕ ОПИСАНИЕ БИЗНЕС-ПРОЦЕССА (с новой страницы)
    # ==========================================
    add_gost_heading(doc, '3 Подробное словесное описание бизнес-процесса', level=1, new_page=True)

    p_bp_intro = doc.add_paragraph()
    format_gost_paragraph(p_bp_intro, space_after=6)
    r = p_bp_intro.add_run(
        'Моделируемый бизнес-процесс «Продажа товаров в продуктовом магазине» реализуется в очном формате '
        'непосредственного взаимодействия покупателя с персоналом и инфраструктурой магазина. '
        'Процесс состоит из следующих последовательных этапов:'
    )
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)

    steps = [
        ('3.1 Вход и выбор товаров в торговом зале. ', 
         'Покупатель входит в магазин «Продукты», берет покупательскую корзину и направляется в торговый зал. '
         'В торговом зале покупатель осматривает представленные на витринах и стеллажах продукты питания, '
         'а также изучает информацию о цене, размещенную на бумажных ценниках. Выбрав необходимые продовольственные товары, '
         'покупатель помещает их в корзину и направляется в зону кассового узла.'),
        
        ('3.2 Выкладка товаров на кассовую ленту. ', 
         'Прибыв к расчетной зоне, покупатель выкладывает отобранные продукты питания из корзины на транспортерную ленту '
         'кассового стола перед кассиром-продавцом.'),
        
        ('3.3 Считывание и идентификация штрихкодов. ', 
         'Кассир берет поочередно каждую единицу товара и подносит ее штрихкодом к окну стационарного или ручного сканера. '
         'Оптический сканер считывает графический штриховой код с упаковки товара, преобразует его в цифровой код и передает по кабельному интерфейсу в POS-терминал.'),
        
        ('3.4 Запрос сведений из товароучетной базы данных. ', 
         'POS-терминал автоматически отправляет электронный сетевой запрос на сервер товароучетной системы (1С:Предприятие). '
         'Система обрабатывает запрос, находит товар в номенклатуре и возвращает обратно актуальную розничную цену, наименование и ставку НДС. '
         'Строка товара мгновенно отображается на дисплее кассира и на внешнем мониторе покупателя.'),
        
        ('3.5 Согласование суммы к оплате и формы расчета. ', 
         'Кассир устно приветствует клиента, сообщает итоговую сумму к оплате, уточняет потребность в фирменном упаковочном пакете, '
         'а также спрашивает о желаемой форме расчета (безналичный платеж банковской картой или наличные деньги). '
         'Покупатель устно озвучивает выбранный способ оплаты.'),
        
        ('3.6 Авторизация и проведение платежа. ', 
         'При безналичном расчете покупатель прикладывает банковскую карту (либо мобильное устройство с модулем бесконтактной оплаты NFC) '
         'к банковскому терминалу (пин-паду). Банковский терминал шифрует данные и передает электронный запрос на авторизацию в процессинговый центр '
         'банка-эквайера. Банк проверяет платежеспособность, производит списание средств со счета покупателя и возвращает терминалу код одобрения транзакции. '
         'Банковский терминал распечатывает бумажный слип-чек и передает статус успешной оплаты в POS-терминал. '
         'При наличном расчете покупатель передает кассиру бумажные банкноты и монеты, кассир вносит полученную сумму в кассу и выдает покупателю сдачу наличными.'),
        
        ('3.7 Фискализация и печать кассового чека. ', 
         'После фиксации оплаты POS-терминал подает управляющую команду на встроенный фискальный регистратор контрольно-кассовой машины (ККМ). '
         'Регистратор формирует электронную фискальную запись и распечатывает фискальный кассовый чек. '
         'Кассир отрывает кассовый чек и передает его в руки покупателю вместе со слип-чеком.'),
        
        ('3.8 Актуализация остатков на складе и завершение процесса. ', 
         'POS-терминал направляет электронный пакет данных о проданных позициях в товароучетную систему (1С:Предприятие) для списания остатков со склада торгового зала. '
         'Кассир складывает приобретенные товары в пакет и передает упакованный товар покупателю. '
         'Покупатель забирает продукты, кассовые чеки и покидает пределы магазина. Процесс полностью завершен.')
    ]

    for title, text in steps:
        p_step = doc.add_paragraph()
        format_gost_paragraph(p_step, space_after=6)
        r = p_step.add_run(title)
        r.bold = True
        r.font.name = 'Times New Roman'
        r.font.size = Pt(14)
        r2 = p_step.add_run(text)
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(14)

    # ==========================================
    # РАЗДЕЛ 4: РЕЗУЛЬТАТЫ ВЫПОЛНЕНИЯ РАБОТЫ (с новой страницы)
    # ==========================================
    add_gost_heading(doc, '4 Результаты выполнения работы', level=1, new_page=True)

    # 4.1 Субъекты и объекты
    add_gost_heading(doc, '4.1 Субъекты и объекты предметной области', level=2, new_page=False)

    p_struct_intro = doc.add_paragraph()
    format_gost_paragraph(p_struct_intro, space_after=6)
    r = p_struct_intro.add_run(
        'В соответствии с методическими требованиями все элементы исследуемой предметной области разделены '
        'на субъекты (люди, одушевленные участники) и объекты (технические средства, материальные предметы, информационные системы). '
        'Кроме того, произведена организационная декомпозиция на три внутренних подразделения предприятия «Магазин "Продукты"» и внешнюю среду:'
    )
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)

    struct_items = [
        ('1. Организационная единица «Магазин "Продукты"»:', True),
        ('а) Подразделение «Торговый зал»:', False),
        ('• Покупатель (клиент магазина) — субъект процесса, инициирующий покупку;', False),
        ('• Витрина / Полка с продуктами — материальный объект, содержащий продовольственные товары и ценники.', False),
        ('б) Подразделение «Кассовый узел (Зона расчета)»:', False),
        ('• Кассир-продавец (оператор кассы) — субъект, осуществляющий расчетно-кассовое обслуживание;', False),
        ('• Сканер штрихкодов — оптический объект для считывания штриховых кодов;', False),
        ('• POS-терминал / ККМ — кассовый компьютер с монитором кассира и встроенным фискальным регистратором;', False),
        ('• Банковский терминал (пин-пад / ридер) — специализированное устройство приема безналичных платежей.', False),
        ('в) Подразделение «Бэк-офис и ИТ-инфраструктура (Серверная)»:', False),
        ('• Товароучетная система (сервер базы данных «1С:Предприятие») — программно-аппаратный объект учета цен и остатков;', False),
        ('• Администратор / Товаровед магазина — субъект, осуществляющий контроль товарооборота и формирование отчетности.', False),
        ('2. Внешняя среда:', True),
        ('• Процессинговый центр банка-эквайера — внешняя финансовая информационная система авторизации платежей.', False)
    ]
    for text, is_bold in struct_items:
        p_item = doc.add_paragraph()
        format_gost_paragraph(p_item, space_after=3)
        r = p_item.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(14)
        if is_bold:
            r.bold = True

    # 4.2 Таблица взаимодействия
    add_gost_heading(doc, '4.2 Информационное и материальное взаимодействие', level=2, new_page=False)

    p_tbl_ref = doc.add_paragraph()
    format_gost_paragraph(p_tbl_ref, space_after=6)
    r = p_tbl_ref.add_run(
        'Информационное и материальное взаимодействие между субъектами и объектами предметной области представлено в таблице 1. '
        'В соответствии с требованиями к оформлению в графе «Форма взаимодействия» полностью исключены отглагольные существительные, '
        'а электронное взаимодействие физических лиц организовано строго через технические устройства-посредники.'
    )
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)

    # Подпись таблицы по ГОСТ 7.32 (сверху, без точки)
    p_tbl_caption = doc.add_paragraph()
    format_gost_paragraph(p_tbl_caption, space_before=10, space_after=4, align=WD_ALIGN_PARAGRAPH.LEFT, first_line_indent=0)
    r = p_tbl_caption.add_run('Таблица 1 — Информационное и материальное взаимодействие в предметной области')
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)
    r.bold = True

    table_data = [
        ('Витрина магазина', 'Покупатель', 'Товар (продукты питания)', 'материальный'),
        ('Витрина магазина', 'Покупатель', 'Ценник (информация о стоимости)', 'бумажный'),
        ('Покупатель', 'Кассир-продавец', 'Товар на кассовой ленте', 'материальный'),
        ('Покупатель', 'Кассир-продавец', 'Вопрос о товаре / скидке', 'устный'),
        ('Кассир-продавец', 'Покупатель', 'Сумма к оплате / ответ', 'устный'),
        ('Товар (упаковка)', 'Сканер штрихкодов', 'Штрихкод на упаковке', 'электронный'),
        ('Сканер штрихкодов', 'POS-терминал', 'Цифровой код товара', 'электронный'),
        ('POS-терминал', 'Товароучетная система (1С)', 'Запрос цены и наличия', 'электронный'),
        ('Товароучетная система (1С)', 'POS-терминал', 'Сведения о товаре (цена, наименование)', 'электронный'),
        ('Покупатель', 'POS-терминал', 'Банковская карта (NFC) / наличные средства', 'материальный'),
        ('POS-терминал', 'Банковский терминал', 'Команда на оплату (сумма)', 'электронный'),
        ('Банковский терминал', 'Процессинговый центр банка', 'Запрос на авторизацию', 'электронный'),
        ('Процессинговый центр банка', 'Банковский терминал', 'Код подтверждения (одобрение транзакции)', 'электронный'),
        ('Банковский терминал', 'POS-терминал', 'Статус оплаты (успех)', 'электронный'),
        ('Банковский терминал', 'Покупатель', 'Слип-чек терминала', 'бумажный'),
        ('POS-терминал', 'Кассир-продавец', 'Кассовый чек (печать)', 'бумажный'),
        ('Кассир-продавец', 'Покупатель', 'Кассовый чек (фискальный)', 'бумажный'),
        ('Кассир-продавец', 'Покупатель', 'Сдача (наличные средства)', 'материальный'),
        ('Кассир-продавец', 'Покупатель', 'Упакованный товар в фирменном пакете', 'материальный'),
        ('POS-терминал', 'Товароучетная система (1С)', 'Данные о списании проданного товара', 'электронный'),
        ('Товароучетная система (1С)', 'Администратор / Товаровед', 'Отчет о продажах и остатках', 'бумажный')
    ]

    table = doc.add_table(rows=1, cols=4)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table)

    hdr_cells = table.rows[0].cells
    hdr_titles = ['От кого', 'Кому', 'Форма информационного / материального взаимодействия', 'Тип взаимодействия']
    for i, title in enumerate(hdr_titles):
        hdr_cells[i].text = title
        set_cell_background(hdr_cells[i], 'D9E2EC')
        set_cell_margins(hdr_cells[i], top=100, bottom=100, left=120, right=120)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:
            run.font.name = 'Times New Roman'
            run.font.size = Pt(11)
            run.font.bold = True

    for row_idx, data in enumerate(table_data):
        row = table.add_row()
        cells = row.cells
        bg_color = 'F8FAFC' if row_idx % 2 == 1 else 'FFFFFF'
        for col_idx, text in enumerate(data):
            cells[col_idx].text = text
            set_cell_background(cells[col_idx], bg_color)
            set_cell_margins(cells[col_idx], top=70, bottom=70, left=100, right=100)
            p = cells[col_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if col_idx in [0, 1, 3] else WD_ALIGN_PARAGRAPH.LEFT
            for run in p.runs:
                run.font.name = 'Times New Roman'
                run.font.size = Pt(10.5)

    # ==========================================
    # ПОДРАЗДЕЛ 4.3: МНЕМОСХЕМА (АЛЬБОМНЫЙ ЛИСТ ДЛЯ ИДЕАЛЬНОЙ ЧИТАЕМОСТИ)
    # ==========================================
    sec_landscape = doc.add_section(WD_SECTION_START.NEW_PAGE)
    sec_landscape.orientation = WD_ORIENT.LANDSCAPE
    sec_landscape.page_width = Inches(297 / 25.4)
    sec_landscape.page_height = Inches(210 / 25.4)
    sec_landscape.top_margin = Inches(18 / 25.4)
    sec_landscape.bottom_margin = Inches(18 / 25.4)
    sec_landscape.left_margin = Inches(25 / 25.4)
    sec_landscape.right_margin = Inches(15 / 25.4)

    # Заголовок подраздела 4.3
    add_gost_heading(doc, '4.3 Мнемосхема бизнес-процесса', level=2, new_page=False)

    p_diag_ref = doc.add_paragraph()
    format_gost_paragraph(p_diag_ref, space_after=6)
    r = p_diag_ref.add_run('Графическая мнемосхема бизнес-процесса «Продажа товаров в продуктовом магазине» представлена на рисунке 1.')
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)

    # Вставка изображения на всю ширину альбомной страницы (9.7 дюйма = ~24.6 см)
    if os.path.exists('mnemoscheme_store.png'):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(4)
        p_img.paragraph_format.space_after = Pt(6)
        p_img.paragraph_format.first_line_indent = Inches(0)
        run_img = p_img.add_run()
        run_img.add_picture('mnemoscheme_store.png', width=Inches(9.7))
        
        # Подпись рисунка строго по ГОСТ 7.32 (по центру, без точки, длинное тире)
        p_caption = doc.add_paragraph()
        p_caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_caption.paragraph_format.space_before = Pt(4)
        p_caption.paragraph_format.space_after = Pt(8)
        p_caption.paragraph_format.first_line_indent = Inches(0)
        r = p_caption.add_run('Рисунок 1 — Мнемосхема бизнес-процесса «Продажа товаров в продуктовом магазине»')
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        r.font.bold = True

    # ==========================================
    # РАЗДЕЛ 5: ВЫВОДЫ (Возврат к книжной ориентации, с новой страницы)
    # ==========================================
    sec_concl = doc.add_section(WD_SECTION_START.NEW_PAGE)
    sec_concl.orientation = WD_ORIENT.PORTRAIT
    sec_concl.page_width = Inches(210 / 25.4)
    sec_concl.page_height = Inches(297 / 25.4)
    sec_concl.top_margin = Inches(20 / 25.4)
    sec_concl.bottom_margin = Inches(20 / 25.4)
    sec_concl.left_margin = Inches(30 / 25.4)
    sec_concl.right_margin = Inches(15 / 25.4)

    add_gost_heading(doc, '5 Выводы', level=1, new_page=False)

    concl_p1 = (
        'В ходе выполнения лабораторной работы № 1 были сформированы и закреплены практические навыки системного описания, '
        'структурной декомпозиции и построения мнемосхемы предметной области для сложного бизнес-процесса «Продажа товаров в продуктовом магазине».'
    )
    p_c1 = doc.add_paragraph()
    format_gost_paragraph(p_c1, space_after=6)
    r = p_c1.add_run(concl_p1)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)

    concl_points = [
        'Определена организационная структура предприятия (магазин «Продукты»), включающая три внутренних подразделения («Торговый зал», «Кассовый узел», «Бэк-офис и ИТ-инфраструктура») и внешнюю сущность (процессинговый центр банка-эквайера).',
        'Выполнена четкая классификация информационных и материальных связей по четырем типам: материальный (товары, деньги, банковские карты), бумажный (кассовые и слип-чеки, ценники, отчетность), устный (речевой диалог покупателя и кассира) и электронный (сетевые запросы, цифровые коды, сигналы подтверждения).',
        'Полностью соблюдены регламентные требования кафедры АСУ УУНиТ: в формулировках форм взаимодействия отсутствуют отглагольные существительные, электронный обмен между физическими лицами происходит исключительно через аппаратные посредники (POS-терминал, сканер штрихкодов, пин-пад, сервер 1С), а бизнес-процесс смоделирован в очном формате непосредственного обслуживания покупателя в торговом зале.',
        'Построенная мнемосхема визуализирует полный жизненный цикл операции купли-продажи и обеспечивает полную преемственность данных для последующего функционального моделирования в нотации IDEF0 в рамках лабораторной работы № 2.'
    ]
    for cp in concl_points:
        p_cp = doc.add_paragraph()
        format_gost_paragraph(p_cp, space_after=6)
        r = p_cp.add_run(f'• {cp}')
        r.font.name = 'Times New Roman'
        r.font.size = Pt(14)

    # Сохранение с защитой от блокировки открытыми файлами в Word
    save_targets = [
        'Отчет_ЛР1_ТБМ_ГОСТ.docx',
        'ЛР1_ПИ209бзу_1_Ардаширов_Байгускаров_Баянов.docx',
        'ЛР1_ПИ208бзу_1_Ардаширов_Байгускаров_Баянов.docx',
        os.path.join('МАТЕРИАЛЫ_ДЛЯ_СДАЧИ_ТБМ', '1_Лабораторная_работа_1_Мнемосхема', 'Отчет_ЛР1_ТБМ_ГОСТ.docx'),
        os.path.join('МАТЕРИАЛЫ_ДЛЯ_СДАЧИ_ТБМ', '1_Лабораторная_работа_1_Мнемосхема', 'ЛР1_ПИ209бзу_1_Ардаширов_Байгускаров_Баянов.docx'),
        os.path.join('МАТЕРИАЛЫ_ДЛЯ_СДАЧИ_ТБМ', '1_Лабораторная_работа_1_Мнемосхема', 'ЛР1_ПИ208бзу_1_Ардаширов_Байгускаров_Баянов.docx')
    ]
    for target in save_targets:
        os.makedirs(os.path.dirname(os.path.abspath(target)), exist_ok=True)
        try:
            doc.save(target)
            print(f'GOST report saved: {target}')
        except PermissionError:
            print(f'Warning: {target} is currently locked by Word.')

if __name__ == '__main__':
    build_gost_report()
