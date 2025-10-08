import os
import sys
import re
from pathlib import Path

class Menu():
    def __init__(self):
        self.opcion = 0
        self.salir = False
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.doc_path = os.path.join(self.base_dir, "documentacion.md")
        # Cargar el documento al inicializar
        self.lines = self.read_lines(Path(self.doc_path))
        self.paras = self.all_paragraphs(self.lines)

    def limpiar_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    ''' HELPER FUNCTIONS
    '''
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
        """Find section whose title contains title_search (case-insensitive).
        Returns section text (lines) or empty list if not found."""
        headings = self.parse_headings(lines)
        for idx, level, title in headings:
            if title_search.lower() in title.lower():
                start = idx + 1
                # find next heading with level <= current level
                end = len(lines)
                for idx2, level2, _ in headings:
                    if idx2 > idx and level2 <= level:
                        end = idx2
                        break
                return lines[start:end]
        return []

    def section_paragraphs(self, lines):
        """Return dict title->paragraphs for each top-level heading (all headings accepted)."""
        headings = self.parse_headings(lines)
        sections = {}
        for idx, level, title in headings:
            start = idx + 1
            end = len(lines)
            for idx2, level2, _ in headings:
                if idx2 > idx and level2 <= level:
                    end = idx2
                    break
            content_lines = [ln for ln in lines[start:end] if not re.match(r'^(#{1,6})\s*', ln)]
            # split content into paragraphs
            paras = []
            buf = []
            for ln in content_lines:
                if ln.strip() == "":
                    if buf:
                        paras.append("\n".join(buf).strip())
                        buf = []
                else:
                    buf.append(ln)
            if buf:
                paras.append("\n".join(buf).strip())
            sections[title] = paras
        return sections

    def show_text(self, text):
        self.limpiar_terminal()
        print("\n" + text + "\n")
        input("Presione Enter para volver al menú...")
        self.limpiar_terminal()


    ''' MENU MODULES
    '''

    def mostrar(self):
        self.limpiar_terminal()
        print("\n--- Bienvenido a la documentación del proyecto 01: Tienda Aurelion ---")
        print("Para empezar, seleccione el número correspondiente a la información que desea consultar:")
        print("1. Información general")
        print("2. Dataset")
        print("3. Información y pasos del programa interactivo")    
        print("4. Pseudocódigo y diagrama")
        print("5. Sugerencias de Copilot")
        print("6. Código de Python")
        print("7. Salir")

    def general(self):
        self.limpiar_terminal()
        if len(self.paras) < 1:
            print("No se encontraron párrafos en el documento.")
            input("Presione Enter para continuar...")
            return
        start, end = 0, min(3, len(self.paras))
        self.show_text("\n\n".join(self.paras[start:end]))

    def dataset(self):
        while True:
            self.limpiar_terminal()
            print("\nSubmenú Opción 2")
            print("a) Ver párrafos 4 y 5")
            print("b) Ver sección 'Dataset de referencia' excluyendo párrafos 4 y 5")
            print("r) Volver")
            choice = input("Elija a/b/r: ").strip().lower()
            if choice == "a":
                self.limpiar_terminal()
                # párrafos 4 y 5 (indices 3 y 4)
                start_idx = 3
                out = []
                for i in range(start_idx, start_idx + 2):
                    if i < len(self.paras):
                        out.append(self.paras[i])
                if out:
                    self.show_text("\n\n".join(out))
                else:
                    print("No hay suficientes párrafos para mostrar 4 y 5.")
                    input("Presione Enter para continuar...")
            elif choice == "b":
                self.limpiar_terminal()
                sec_lines = self.get_section(self.lines, "Dataset de referencia")
                if not sec_lines:
                    print("No se encontró la sección 'Dataset de referencia'.")
                    input("Presione Enter para continuar...")
                    continue
                # obtener párrafos de la sección
                sec_pars = []
                buf = []
                for ln in sec_lines:
                    if ln.strip() == "":
                        if buf:
                            sec_pars.append("\n".join(buf).strip())
                            buf = []
                    else:
                        buf.append(ln)
                if buf:
                    sec_pars.append("\n".join(buf).strip())
                # excluir 'párrafos 4 y 5' del documento global si aparecen en la sección:
                exclude = set()
                if len(self.paras) > 3:
                    exclude.add(self.paras[3])
                if len(self.paras) > 4:
                    exclude.add(self.paras[4])
                filtered = [p for p in sec_pars if p not in exclude]
                if filtered:
                    self.show_text("\n\n".join(filtered))
                else:
                    print("La sección quedó vacía tras excluir los párrafos solicitados.")
                    input("Presione Enter para continuar...")
            elif choice == "r":
                self.limpiar_terminal()
                return
            else:
                print("Opción inválida. Intente nuevamente.")
                input("Presione Enter para continuar...")

    def pasos_programa(self):
        self.limpiar_terminal()
        # Extraer sección "Pasos" o "Pasos: descomposición de problemas"
        sec_lines = self.get_section(self.lines, "Pasos")
        if not sec_lines:
            print("No se encontró la sección de 'Pasos'.")
            input("Presione Enter para continuar...")
            return
        # mostrar párrafos 1 a 3 de esa sección (si existen)
        paras = []
        buf = []
        for ln in sec_lines:
            if ln.strip() == "":
                if buf:
                    paras.append("\n".join(buf).strip())
                    buf = []
            else:
                buf.append(ln)
        if buf:
            paras.append("\n".join(buf).strip())
        if not paras:
            print("La sección de 'Pasos' no contiene párrafos detectables.")
            input("Presione Enter para continuar...")
            return
        self.show_text("\n\n".join(paras[:3]))

    def pseudocodigo_diagrama(self):
        self.limpiar_terminal()
        sec_lines = self.get_section(self.lines, "Pseudocódigo")
        if not sec_lines:
            sec_lines = self.get_section(self.lines, "Pseudocodigo")
        if not sec_lines:
            print("No se encontró la sección de 'Pseudocódigo y diagrama de flujo'.")
            input("Presione Enter para continuar...")
            return
        paras = []
        buf = []
        for ln in sec_lines:
            if ln.strip() == "":
                if buf:
                    paras.append("\n".join(buf).strip())
                    buf = []
            else:
                buf.append(ln)
        if buf:
            paras.append("\n".join(buf).strip())
        self.show_text("\n\n".join(paras[:3]))

    def sugerencias_copilot(self):
        self.limpiar_terminal()
        sec_lines = self.get_section(self.lines, "Sugerencias Copilot")
        if not sec_lines:
            print("No se encontró la sección 'Sugerencias Copilot'.")
            input("Presione Enter para continuar...")
            return
        paras = []
        buf = []
        for ln in sec_lines:
            if ln.strip() == "":
                if buf:
                    paras.append("\n".join(buf).strip())
                    buf = []
            else:
                buf.append(ln)
        if buf:
            paras.append("\n".join(buf).strip())
        self.show_text("\n\n".join(paras[:3]))

    def codigo_python(self):
        self.limpiar_terminal()
        # Mostrar la sección completa "Programa Python" o "Código" si existe
        sec_lines = self.get_section(self.lines, "Programa Python")
        if not sec_lines:
            sec_lines = self.get_section(self.lines, "Código")
        if not sec_lines:
            print("No se encontró la sección 'Programa Python' ni 'Código'.")
            input("Presione Enter para continuar...")
            return
        self.show_text("\n".join(sec_lines).strip())

    def seleccionar(self):
        # main loop
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
                    self.codigo_python()
                elif self.opcion == 7:
                    self.limpiar_terminal()
                    print("Saliendo del programa...")
                    self.salir = True
                else:
                    self.limpiar_terminal()
                    print("Opción no válida. Intente de nuevo.")
                    input("Presione Enter para continuar...")
            except ValueError:
                self.limpiar_terminal()
                print("Entrada no válida. Por favor, ingrese un número.")
                input("Presione Enter para continuar...")

if __name__ == "__main__":
    menu = Menu()
    menu.seleccionar()