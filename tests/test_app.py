import ast
import pytest
import os
import re

def extract_ast_from_file(filename):
    """Extrai a árvore sintática do arquivo Python"""
    if not os.path.exists(filename):
        pytest.skip(f"Arquivo {filename} não encontrado")
    
    with open(filename, "r", encoding="utf-8") as file:
        return ast.parse(file.read(), filename=filename)

def find_function_calls(tree, function_name):
    """Encontra chamadas de função específicas na árvore sintática"""
    calls = []
    for node in ast.walk(tree):
        # Caso tradicional: chamadas de função como func()
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr == function_name:
                calls.append(node)
            
            # Procura por padrões como st.sidebar.widget()
            if function_name == 'sidebar' and isinstance(node.func.value, ast.Attribute):
                if hasattr(node.func.value, 'attr') and node.func.value.attr == 'sidebar':
                    calls.append(node)
    return calls

def find_imports(tree, module_name):
    """Verifica se um módulo específico foi importado"""
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for name in node.names:
                if name.name == module_name:
                    return True
        elif isinstance(node, ast.ImportFrom):
            if node.module == module_name:
                return True
    return False

def test_streamlit_import():
    """Verifica se o streamlit foi importado"""
    tree = extract_ast_from_file("main.py")
    assert find_imports(tree, "streamlit"), "O módulo streamlit deve ser importado"

def test_pandas_import():
    """Verifica se o pandas foi importado"""
    tree = extract_ast_from_file("main.py")
    assert find_imports(tree, "pandas"), "O módulo pandas deve ser importado"

def test_dashboard_title():
    """Verifica se o título do dashboard foi definido e segue o formato especificado"""
    tree = extract_ast_from_file("main.py")
    title_calls = find_function_calls(tree, "title")
    
    assert title_calls, "Deve existir uma chamada à função st.title()"
    # Verifica o formato do título em alguma das chamadas
    title_format_found = False
    for call in title_calls:
        if call.args:
            # Verifica se é uma string literal (usando ast.Constant em vez de ast.Str que está depreciado)
            if isinstance(call.args[0], ast.Constant):
                title_text = call.args[0].value
                if "Dashboard Final:" in title_text and "<Título do seu Projeto>" not in title_text:
                    title_format_found = True
    
    assert title_format_found, "O título deve seguir o formato 'Dashboard Final: <Título específico>'"

def test_csv_loading():
    """Verifica se o código carrega um arquivo CSV de dados/output.csv"""
    tree = extract_ast_from_file("main.py")
    
    # Procura chamadas ao pandas como pd.read_csv
    read_csv_calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr == "read_csv":
                read_csv_calls.append(node)
    
    assert read_csv_calls, "Deve existir uma chamada à função pd.read_csv()"
    # Verifica se alguma das chamadas carrega dados/output.csv
    output_csv_found = False
    for call in read_csv_calls:
        if call.args:
            # Usando ast.Constant em vez de ast.Str (que está depreciado)
            if isinstance(call.args[0], ast.Constant) and "dados/output.csv" in call.args[0].value:
                output_csv_found = True
    
    assert output_csv_found, "Deve carregar o arquivo 'dados/output.csv'"

def test_sidebar_filters():
    """Verifica se existem pelo menos 3 filtros na sidebar"""
    tree = extract_ast_from_file("main.py")
    
    # Procura chamadas à sidebar
    sidebar_calls = find_function_calls(tree, "sidebar")
    assert sidebar_calls, "Deve existir pelo menos uma chamada à st.sidebar"
    
    # Lista de funções de widgets do streamlit
    widget_functions = ["text_input", "checkbox", "radio", "selectbox", "multiselect", "slider",
                       "select_slider", "number_input", "text_area", "date_input", "time_input",
                       "file_uploader", "color_picker", "button"]
    
    # Conta os widgets encontrados
    widget_count = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            # Verifica padrões como st.sidebar.widget()
            if (hasattr(node.func, 'value') and 
                isinstance(node.func.value, ast.Attribute) and
                hasattr(node.func.value, 'value') and 
                isinstance(node.func.value.value, ast.Name) and
                node.func.value.value.id == 'st' and
                node.func.value.attr == 'sidebar' and
                node.func.attr in widget_functions):
                widget_count += 1
            # Verificar se é uma chamada a um método do sidebar
            elif hasattr(node.func, 'value') and isinstance(node.func.value, ast.Attribute):
                if node.func.value.attr == 'sidebar' and node.func.attr in widget_functions:
                    widget_count += 1
            # Ou se é uma chamada direta a um widget após uma referência à sidebar
            elif node.func.attr in widget_functions:
                for sidebar in sidebar_calls:
                    # Posição aproximada no código - impreciso, mas dá uma ideia
                    if hasattr(sidebar, 'lineno') and hasattr(node, 'lineno') and sidebar.lineno < node.lineno:
                        widget_count += 1
                        break
    
    assert widget_count >= 3, "Deve haver pelo menos 3 widgets de filtro na sidebar"

def test_data_table():
    """Verifica se existe uma tabela de dados"""
    tree = extract_ast_from_file("main.py")
    
    # Funções que podem exibir tabelas no streamlit
    table_functions = ["dataframe", "table", "write"]
    
    # Conta as tabelas encontradas
    table_found = False
    for function in table_functions:
        calls = find_function_calls(tree, function)
        if calls:
            table_found = True
            break
    
    assert table_found, "Deve existir uma tabela de dados (st.dataframe, st.table ou st.write com DataFrame)"

def test_charts():
    """Verifica se existem pelo menos dois gráficos"""
    tree = extract_ast_from_file("main.py")
    
    # Funções de gráficos do streamlit
    chart_functions = ["line_chart", "area_chart", "bar_chart", "pyplot", "altair_chart", 
                      "vega_lite_chart", "plotly_chart", "bokeh_chart", "pydeck_chart"]
    
    # Conta os gráficos encontrados
    chart_count = 0
    for function in chart_functions:
        calls = find_function_calls(tree, function)
        chart_count += len(calls)
    
    assert chart_count >= 2, "Deve haver pelo menos 2 gráficos no dashboard"

def test_markdown_or_write():
    """Verifica se existem explicações ou descrições usando markdown ou write"""
    tree = extract_ast_from_file("main.py")
    
    # Funções para texto explicativo
    text_functions = ["markdown", "write", "header", "subheader", "text"]
    
    # Verifica se pelo menos uma dessas funções é chamada
    text_found = False
    for function in text_functions:
        calls = find_function_calls(tree, function)
        if calls:
            text_found = True
            break
    
    assert text_found, "Deve existir pelo menos um texto explicativo (st.markdown, st.write, etc.)"
