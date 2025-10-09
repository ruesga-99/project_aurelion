import os
import re
from pathlib import Path
import unicodedata

class Menu():
    def __init__(self):
        self.opcion = 0
        self.salir = False
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.doc_path = os.path.join(self.base_dir, "documentacion.md")
        self.self_path = os.path.abspath(__file__)

        if not os.path.exists(self.doc_path):
            print("Error: No se encontró el archivo 'documentacion.md'.")
            exit(1)

        self.lines = self.read_lines(Path(self.doc_path))
        self.paras = self.all_paragraphs(self.lines)

    ''' HELPER FUNCTIONS
    '''

    def limpiar_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def read_lines(self, path):
        return path.read_text(encoding="utf-8").splitlines()

    def parse_headings(self, lines):
        """Return list of (line_no, level, title)."""
        headings = []
        for i, ln in enumerate(lines):
            m = re.match(r'^(#{1,6})\s*(.+)$', ln)
            if m:
                level = len(m.group(1))
                title = m.group(2).strip()
                headings.append((i, level, title))
        return headings
    
    def all_paragraphs(self, lines):
        """Return list of paragraphs across the whole document (headings excluded)."""
        paras = []
        buf = []
        for ln in lines:
            if re.match(r'^(#{1,6})\s*', ln):
                continue
            if ln.strip() == "":
                if buf:
                    paras.append("\n".join(buf).strip())
                    buf = []
            else:
                buf.append(ln)
        if buf:
            paras.append("\n".join(buf).strip())
        return paras

    def get_section(self, lines, title_search):
        """Find section whose title contains title_search (case-insensitive)."""
        headings = self.parse_headings(lines)
        for idx, level, title in headings:
            if title_search.lower() in title.lower():
                start = idx + 1
                end = len(lines)
                for idx2, level2, _ in headings:
                    if idx2 > idx and level2 <= level:
                        end = idx2
                        break
                return lines[start:end]
        return []

    def extract_code_block(self, lines):
        """Extrae el bloque de código contenido entre ``` ... ```"""
        inside_code = False
        code_lines = []
        for ln in lines:
            if ln.strip().startswith("```"):
                inside_code = not inside_code
                continue
            if inside_code:
                code_lines.append(ln)
        return "\n".join(code_lines).strip()

    def show_text(self, text):
        self.limpiar_terminal()
        print("\n" + text + "\n")
        input("Presione Enter para regresar al menú...")

    ''' MENU MODULES
    '''

    def mostrar(self):
        self.limpiar_terminal()
        print("¡Bienvenido a la documentación del proyecto 01: Tienda Aurelion!")
        print("\nSeleccione la opción deseada:")
        print("1. Información general")
        print("2. Dataset de referencia")
        print("\nPuedes consultar también sobre el trabajo detrás de este programa interactivo:")
        print("3. Información y pasos del programa")    
        print("4. Pseudocódigo y diagrama")
        print("5. Sugerencias de Copilot")
        print("\n6. Salir")

    def general(self):
        """
        Muestra la sección 'Información general' completa desde el Markdown.
        """
        sec_lines = self.get_section(self.lines, "Información general")
        if not sec_lines:
            self.show_text("No se encontró la sección 'Información general' en el documento.")
            return
        text = "\n".join(sec_lines).strip()
        self.show_text(text)

    def dataset(self):
        while True:
            self.limpiar_terminal()
            print("\nSubmenú de Dataset:")
            print("a) Resumen")
            print("b) Detalle")
            print("Presione Enter para regresar al menú principal.")
            choice = input("Elija a/b\n").strip().lower()

            if choice == "a":
                start_idx = 3
                out = []
                for i in range(start_idx, start_idx + 2):
                    if i < len(self.paras):
                        out.append(self.paras[i])
                if out:
                    self.show_text("\n\n".join(out))

            elif choice == "b":
                # Obtener la sección completa con formato
                sec_lines = self.get_section(self.lines, "Dataset de referencia")
                if not sec_lines:
                    self.show_text("No se encontró la sección 'Dataset de referencia'.")
                    continue

                # Identificar los párrafos 4 y 5 para excluirlos
                exclude = set()
                if len(self.paras) > 3:
                    exclude.add(self.paras[3])
                if len(self.paras) > 4:
                    exclude.add(self.paras[4])

                # Filtrar líneas que contienen esos párrafos
                filtered_lines = []
                current_para = []
                for ln in sec_lines:
                    if ln.strip() == "":
                        if current_para:
                            text = "\n".join(current_para).strip()
                            if text not in exclude:
                                filtered_lines.extend(current_para)
                                filtered_lines.append("")  # mantener saltos
                            current_para = []
                    elif re.match(r'^(#{3,3})\s', ln):  # Mantener ### títulos nivel 3
                        filtered_lines.append(ln)
                    else:
                        current_para.append(ln)

                if current_para:
                    text = "\n".join(current_para).strip()
                    if text not in exclude:
                        filtered_lines.extend(current_para)

                # Mostrar con formato original
                if filtered_lines:
                    self.show_text("\n".join(filtered_lines))
                else:
                    self.show_text("No hay contenido para mostrar tras la exclusión.")

            elif choice == "":
                return

    def pasos_programa(self):
        sec_lines = self.get_section(self.lines, "Pasos")
        if not sec_lines:
            return
        text = "\n".join(sec_lines).strip()
        if text:
            self.show_text(text)

    def pseudocodigo_diagrama(self):
        """
        Extrae e imprime las subsecciones de nivel 3 relacionadas con
        'Pseudocódigo' y 'Diagrama' (incluyendo sus propias líneas de
        encabezado) desde el documento.
        """
        headings = self.parse_headings(self.lines)
        if not headings:
            self.show_text("No se encontraron encabezados en el documento.")
            return

        # Normalizar para comparar sin tildes
        def _norm(s):
            s2 = unicodedata.normalize('NFD', s)
            s2 = ''.join(c for c in s2 if unicodedata.category(c) != 'Mn')
            return s2.lower()

        terms = ["pseudocodigo", "diagrama"]
        sections = []

        for idx, level, title in headings:
            # Buscamos subtítulos de nivel 3 que contengan los términos
            if level != 3:
                continue
            low_title = _norm(title)
            if any(t in low_title for t in terms):
                # Incluir la línea de encabezado (start = idx)
                start = idx
                end = len(self.lines)
                for idx2, level2, _ in headings:
                    if idx2 > idx and level2 <= level:
                        end = idx2
                        break
                section_lines = self.lines[start:end]
                sections.append("\n".join(section_lines).strip())

        if sections:
            # Mostrar las secciones encontradas, manteniendo títulos y formato
            out = "\n\n".join(sections)
            self.show_text(out)
        else:
            self.show_text("No se encontraron secciones de 'Pseudocódigo' o 'Diagrama' en el documento.")

    def sugerencias_copilot(self):
        # Buscamos la sección completa incluyendo su encabezado
        headings = self.parse_headings(self.lines)
        target_idx = None
        for idx, level, title in headings:
            if "sugerencias copilot" in title.lower():
                target_idx = idx
                target_level = level
                break

        if target_idx is None:
            self.show_text("No se encontró la sección 'Sugerencias Copilot'.")
            return

        start = target_idx
        end = len(self.lines)
        for idx2, level2, _ in headings:
            if idx2 > start and level2 <= target_level:
                end = idx2
                break

        # Normalizar función interna para comparaciones sin tildes
        def _norm(s):
            s2 = unicodedata.normalize('NFD', s)
            s2 = ''.join(c for c in s2 if unicodedata.category(c) != 'Mn')
            return s2.lower()

        # Recolectar subsecciones nivel 2 y 3 dentro del rango [start, end)
        sections = []
        # Build a list of headings within the doc for quick lookup
        for idx, level, title in headings:
            if idx < start or idx >= end:
                continue
            if level in (2, 3):
                # compute subsection end
                sub_start = idx
                sub_end = end
                for idx2, level2, _ in headings:
                    if idx2 > idx and idx2 < end and level2 <= level:
                        sub_end = idx2
                        break
                section_lines = self.lines[sub_start:sub_end]
                sections.append("\n".join(section_lines).strip())

        # If no level 2/3 headings found, fallback to show whole section (including header)
        if not sections:
            sec = self.lines[start:end]
            out = "\n".join(sec).strip()
            self.show_text(out if out else "No hay contenido en 'Sugerencias Copilot'.")
            return

        out = "\n\n".join(sections)
        self.show_text(out)

    def seleccionar(self):
        while not self.salir:
            self.mostrar()
            try:
                self.opcion = int(input("Seleccione una opción: ").strip())
                if self.opcion == 1:
                    self.general()
                elif self.opcion == 2:
                    self.dataset()
                elif self.opcion == 3:
                    self.pasos_programa()
                elif self.opcion == 4:
                    self.pseudocodigo_diagrama()
                elif self.opcion == 5:
                    self.sugerencias_copilot()
                elif self.opcion == 6:
                    self.limpiar_terminal()
                    print("Saliendo del programa...")
                    self.salir = True
                else:
                    input("Opción no válida. Presione Enter para continuar...")
            except ValueError:
                input("Entrada no válida. Presione Enter para continuar...")

if __name__ == "__main__":
    menu = Menu()
    menu.seleccionar()
