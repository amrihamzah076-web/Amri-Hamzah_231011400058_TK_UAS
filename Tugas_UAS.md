# Tugas Proyek Akhir (UAS) : Representasi Tahapan Kompilasi

**NAMA:** Amri Hamzah
**NIM:** 231011400058
**KELAS:** 06 TPLE 002
**Mata Kuliah:** Teknik Kompilasi

---

## 1. Pilihan Konstruksi
Konstruksi sintaksis yang dipilih untuk diimplementasikan adalah **Perulangan (Looping: While)**.
Bentuk umum perulangan ini mengevaluasi sebuah kondisi di awal; jika kondisi bernilai `True` (benar), maka blok pernyataan (statement) di dalamnya akan dieksekusi terus-menerus hingga kondisi bernilai `False`.

---

## 2. Pattern (Pola Sintaks)
Pola tata bahasa didefinisikan menggunakan pendekatan *Backus-Naur Form* (BNF) sederhana:

```**bnf**
<while_stmt> ::= "while" "(" <condition> ")" "{" <statements> "}"
<condition>  ::= <identifier> <operator> <value>
<operator>   ::= "<" | ">" | "==" | "!=" | "<=" | ">="
<statements> ::= <identifier> "=" <expression> ";"
<expression> ::= <identifier> | <value> | <identifier> <arithmetic_op> <value>
<img width="499" height="519" alt="WhatsApp Image 2024-10-26 at 14 12 02" src="https://github.com/user-attachments/assets/c5b912c1-eb69-4254-a45c-ee97505a9234" />
```

---

## 3. Implementasi Program
Berikut adalah simulasi compiler pipeline menggunakan bahasa pemrograman Python. Program ini memodelkan keempat tahapan secara terstruktur: memecah token, membentuk Abstract Syntax Tree (AST) sederhana, memvalidasi semantik melalui symbol table tiruan, dan merakitnya menjadi bentuk TAC.

**Pyhton**

````
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
    compiler.compile()`
````

---

## 4. Penjelasan & Dokumentasi Tahapan
Program yang telah dibuat mensimulasikan keempat tahapan penting kompilasi untuk konstruksi `while` loop. Berikut rincian cara kerja dari tiap tahapan:

Analisis Leksikal (Scanner)
Fungsi: `lexical_analysis()`

Deskripsi: Program membaca string mentah (source code). Menggunakan Regular Expression (regex), program memisahkan simbol-simbol khusus seperti tanda kurung `()`, kurung kurawal {}, operator `<`, `=`, `+`, dan tanda `;` dengan menambahkan spasi. String tersebut kemudian dipecah menggunakan `.split()` menjadi array berisi sekumpulan unit terkecil yang disebut Token.

Input: `while ( x < 10 ) { x = x + 1 ; }`

Output (Tokens): `['while', '(', 'x', '<', '10', ')', '{', 'x', '=', 'x', '+', '1', ';', '}']`

Analisis Sintaksis (Parser)
Fungsi: `syntax_analysis()`

Deskripsi: Menggunakan sekumpulan Token dari tahap leksikal, program memastikan urutan token sesuai dengan aturan bahasa (pola BNF). Program mencari indeks dari tanda kurung () untuk mengekstrak Kondisi, serta mencari indeks kurung kurawal {} untuk mengekstrak Statement (Body). Jika strukturnya benar, program menghasilkan Abstract Syntax Tree (AST) sederhana berbasis tipe data Dictionary di Python.

Output (AST): `{'type': 'WhileLoop', 'condition': ['x', '<', '10'], 'body': ['x', '=', 'x', '+', '1', ';']}`

Analisis Semantik (Semantic Analyzer)
Fungsi: `semantic_analysis()`

Deskripsi: Program memeriksa "makna" di balik kode. Pada simulasi ini, program mengecek apakah Identifier (nama variabel) yang ada di dalam blok kondisi (`x`) telah dideklarasikan sebelumnya. Hal ini dilakukan dengan mencocokkan variabel terhadap Symbol Table (tabel `self.symbol_table` pada inisialisasi kelas). Jika variabel belum ada di tabel, proses kompilasi akan mengeluarkan error (`NameError`).

Generasi Kode Antara (Intermediate Code / TAC Generator)
Fungsi: `generate_tac()`

Deskripsi: AST yang sudah tervalidasi kemudian dipetakan ke dalam bentuk Three-Address Code. Karena ini adalah perulangan `while`, program membangkitkan dua buah label: label awalan (`L1`) dan label akhiran (`L2`). Logika yang dihasilkan adalah:

Tandai titik awal perulangan (`L1:`).

Evaluasi kondisi. Jika salah (ifFalse), maka lompat (goto) ke luar perulangan (`L2`).

Jika benar, jalankan body di dalamnya.

Setelah body dieksekusi, paksa program kembali melompat ke titik awal (`goto L1`) untuk mengevaluasi ulang kondisi.

Output (TAC):
`L1:
ifFalse x < 10 goto L2
    x = x + 1;
    goto L1
L2:`
