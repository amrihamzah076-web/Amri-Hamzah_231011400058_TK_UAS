import re

class WhileLoopCompiler:
    def __init__(self, source_code):
        self.source_code = source_code
        self.label_counter = 1
        # Simulasi Symbol Table (tabel variabel yang sudah dideklarasikan)
        self.symbol_table = {"x": "int", "y": "int", "batas": "int"}

    def new_label(self):
        """Membuat label unik untuk keperluan jump di TAC"""
        lbl = f"L{self.label_counter}"
        self.label_counter += 1
        return lbl

    def lexical_analysis(self):
        """Tahap 1: Memecah input source code menjadi sekumpulan token"""
        # Menambahkan spasi di sekitar simbol khusus agar mudah di-split
        code = re.sub(r'([(){}=<>;+*/-])', r' \1 ', self.source_code)
        tokens = code.split()
        return tokens

    def syntax_analysis(self, tokens):
        """Tahap 2: Membentuk Abstract Syntax Tree (AST) berbasis Dictionary"""
        if 'while' not in tokens:
            raise SyntaxError("Struktur 'while' loop tidak ditemukan atau tidak valid.")
        
        try:
            # Mengekstrak blok kondisi
            cond_start = tokens.index('(') + 1
            cond_end = tokens.index(')')
            condition = tokens[cond_start:cond_end]

            # Mengekstrak blok body (statements)
            body_start = tokens.index('{') + 1
            body_end = tokens.index('}')
            body = tokens[body_start:body_end]
            
            # Membangun AST node
            ast = {
                "type": "WhileLoop",
                "condition": condition,
                "body": body
            }
            return ast
        except ValueError:
            raise SyntaxError("Kurung buka/tutup tidak lengkap pada sintaks 'while'.")

    def semantic_analysis(self, ast):
        """Tahap 3: Mengecek validasi dasar (Variabel terdeklarasi)"""
        # Mengambil identifier pertama dari kondisi (contoh: 'x' dari 'x < 10')
        condition = ast["condition"]
        identifier = condition[0] 
        
        if identifier not in self.symbol_table:
            raise NameError(f"Error Semantik: Variabel '{identifier}' belum dideklarasikan.")
        
        return True # Semantik lolos validasi

    def generate_tac(self, ast):
        """Tahap 4: Menghasilkan Three-Address Code (TAC) dari AST"""
        cond_str = " ".join(ast["condition"])
        # Membersihkan spasi sebelum titik koma untuk estetika output
        body_str = " ".join(ast["body"]).replace(" ;", ";") 
        
        label_start = self.new_label()
        label_end = self.new_label()

        tac = []
        tac.append(f"{label_start}:")
        tac.append(f"ifFalse {cond_str} goto {label_end}")
        tac.append(f"    {body_str}")
        tac.append(f"    goto {label_start}")
        tac.append(f"{label_end}:")
        
        return "\n".join(tac)

    def compile(self):
        """Menjalankan seluruh pipeline kompilasi"""
        print("=== INPUT SOURCE CODE ===")
        print(self.source_code, "\n")

        print("--- 1. Hasil Analisis Leksikal (Tokens) ---")
        tokens = self.lexical_analysis()
        print(tokens, "\n")

        print("--- 2. Hasil Analisis Sintaksis (AST) ---")
        ast = self.syntax_analysis(tokens)
        print(ast, "\n")

        print("--- 3. Hasil Analisis Semantik ---")
        self.semantic_analysis(ast)
        print("[OK] Validasi semantik sukses: Variabel ditemukan di Symbol Table.\n")

        print("--- 4. Generasi Three-Address Code (TAC) ---")
        tac = self.generate_tac(ast)
        print(tac)


# --- Pengujian Program (Main) ---
if __name__ == "__main__":
    # Source code yang ingin di-compile
    source = "while ( x < 10 ) { x = x + 1 ; }"
    
    # Inisialisasi dan jalankan kompilasi
    compiler = WhileLoopCompiler(source)
    compiler.compile()